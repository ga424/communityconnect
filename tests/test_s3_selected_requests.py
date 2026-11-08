"""Approved S3-AC11 v1: selected-community reads, real DB isolation and revocation."""
from contextlib import contextmanager
from threading import Event, Thread
from time import monotonic
from urllib.parse import quote

import psycopg
import pytest
from fastapi.testclient import TestClient

from app import models
from app.main import create_app
from app.models import connection as real_connection
from app.requests import RequestResponse

TABLES = {
    "communities": "id", "units": "id", "app_users": "id",
    "memberships": "user_id, community_id", "maintenance_requests": "id",
}
INVALID_CALLERS = {
    "missing": None, "empty": "", "zero": "0", "negative": "-1",
    "leading-zero": "0101", "plus": "+101", "decimal": "101.0",
    "text": "manager", "space": " 101", "unicode-digits": "²",
    "unknown": "9999", "outside-db-range": "2147483648", "overlong": "9" * 50,
}
UNAVAILABLE = {
    "zero": "0", "negative": "-1", "leading-zero": "01", "plus": "+1",
    "decimal": "1.0", "text": "community", "space": " 1", "unicode-digits": "²",
    "outside-db-range": "2147483648", "overlong": "9" * 50,
    "nonexistent": "9999", "unassigned": "3", "max-valid-absent": "2147483647",
}


def snapshot():
    with real_connection() as conn:
        return {table: conn.execute(f"SELECT * FROM {table} ORDER BY {order}").fetchall()
                for table, order in TABLES.items()}


def execute(sql, args=()):
    with real_connection() as conn:
        conn.execute(sql, args)


def row(request_id, community=1, unit=11, status="Open", created="2026-01-01T12:00:00Z"):
    return {"id": request_id, "community_id": community, "unit_id": unit,
            "category": "Plumbing", "description": f"Synthetic request {request_id}",
            "status": status, "created_at": created}


def seed_request(request_id, community=1, unit=11, owner=1, status="Open",
                 created="2026-01-01T12:00:00Z"):
    execute("""INSERT INTO maintenance_requests
               (id, community_id, unit_id, submitted_by, category, description, status, created_at)
               VALUES (%s,%s,%s,%s,'Plumbing',%s,%s,%s)""",
            (request_id, community, unit, owner, f"Synthetic request {request_id}", status, created))


@pytest.fixture
def manager_client(client):
    # The unchanged shared client reset runs before these test-local additions.
    execute("INSERT INTO communities VALUES (3,'Elm Court'),(4,'Birch')")
    execute("INSERT INTO units VALUES (31,3,'A'),(41,4,'A')")
    execute("INSERT INTO app_users VALUES (101),(102),(103),(104),(106),(201),(202)")
    execute("""INSERT INTO memberships (user_id,community_id,role,unit_id) VALUES
               (101,1,'manager',NULL),(101,2,'manager',NULL),(101,4,'manager',NULL),
               (102,3,'manager',NULL),(106,1,'manager',NULL),(106,2,'resident',21),
               (201,3,'resident',31),(202,2,'resident',21)""")
    seed_request(11)
    seed_request(21, 2, 21, 2)
    seed_request(31, 3, 31, 201)
    return client


def headers(caller):
    return {} if caller is None else {b"X-User-Id": str(caller).encode("latin1")}


def selected(client, community=1, caller="101"):
    return client.get(f"/manager/communities/{quote(str(community), safe='')}/requests",
                      headers=headers(caller))


def assert_response(response, expected, status=200, cache=True):
    assert response.status_code == status
    assert response.json() == expected
    if cache:
        assert response.headers.get("cache-control") == "no-store"


def read(client, expected, community=1, caller="101", status=200):
    before = snapshot()
    response = selected(client, community, caller)
    assert_response(response, expected, status)
    assert snapshot() == before
    return response


def denied(client, community=1, caller="101"):
    return read(client, {"detail": "Not found"}, community, caller, 404)


def options(client, expected):
    before = snapshot()
    assert_response(client.get("/manager/communities", headers=headers("101")), expected)
    assert snapshot() == before


OPTIONS = [{"id": 1, "name": "Mountain Ridge"}, {"id": 2, "name": "Pine Hollow"},
           {"id": 4, "name": "Birch"}]


def test_ac11_manager_reads_only_selected_community(manager_client):
    read(manager_client, [row(21, 2, 21)], 2)


def test_ac11_manager_reads_all_residents_in_selected_community(manager_client):
    seed_request(12, unit=12, owner=3)
    read(manager_client, [row(12, unit=12), row(11)])


def test_ac11_assigned_empty_community_returns_empty_array(manager_client):
    read(manager_client, [], 4)


def test_ac11_switch_has_no_remembered_context(manager_client):
    for community, expected in [(1, [row(11)]), (2, [row(21, 2, 21)]), (1, [row(11)])]:
        read(manager_client, expected, community)


def test_ac11_interleaved_managers_stay_isolated(manager_client):
    read(manager_client, [row(11)])
    read(manager_client, [row(31, 3, 31)], 3, "102")
    denied(manager_client, 3)
    read(manager_client, [row(21, 2, 21)], 2)
    denied(manager_client, 1, "102")
    read(manager_client, [row(31, 3, 31)], 3, "102")


@pytest.mark.parametrize("case", INVALID_CALLERS)
def test_ac11_reject_invalid_caller(manager_client, case):
    read(manager_client, {"detail": "Unknown user"}, caller=INVALID_CALLERS[case], status=401)


@pytest.mark.parametrize("case", UNAVAILABLE)
def test_ac11_unavailable_community_is_indistinguishable(manager_client, case):
    denied(manager_client, UNAVAILABLE[case])


@pytest.mark.parametrize("case", ["missing", "unknown", "malformed"])
def test_ac11_identity_precedes_invalid_path(manager_client, case):
    caller = {"missing": None, "unknown": "9999", "malformed": "²"}[case]
    read(manager_client, {"detail": "Unknown user"}, "bad", caller, 401)


@pytest.mark.parametrize("role", ["resident", "board_member", "admin"])
def test_ac11_nonmanager_cannot_read(manager_client, role):
    execute("INSERT INTO memberships VALUES (104,1,%s,%s)",
            (role, 11 if role == "resident" else None))
    denied(manager_client, caller="104")


def test_ac11_known_unassigned_caller_denied(manager_client):
    denied(manager_client, caller="103")


def test_ac11_mixed_roles_do_not_grant_manager_access(manager_client):
    seed_request(12, unit=12, owner=3)
    seed_request(22, 2, 21, 106)
    seed_request(23, 2, 21, 202)
    read(manager_client, [row(12, unit=12), row(11)], caller="106")
    denied(manager_client, 2, "106")
    before = snapshot()
    assert_response(manager_client.get("/communities/2/requests", headers=headers("106")),
                    [row(22, 2, 21)], cache=False)
    assert snapshot() == before


def test_ac11_committed_removal_denies_later_read(manager_client):
    options(manager_client, OPTIONS)
    read(manager_client, [row(11)])
    execute("DELETE FROM memberships WHERE user_id=101 AND community_id=1")
    denied(manager_client)
    options(manager_client, OPTIONS[1:])


@pytest.mark.parametrize("role", ["resident", "board_member", "admin"])
def test_ac11_committed_role_change_denies_later_read(manager_client, role):
    read(manager_client, [row(11)])
    execute("UPDATE memberships SET role=%s, unit_id=%s WHERE user_id=101 AND community_id=1",
            (role, 11 if role == "resident" else None))
    denied(manager_client)
    options(manager_client, OPTIONS[1:])


def test_ac11_new_assignment_authorizes_next_read(manager_client):
    denied(manager_client, caller="103")
    execute("INSERT INTO memberships VALUES (103,1,'manager',NULL)")
    read(manager_client, [row(11)], caller="103")


def test_ac11_unit_link_does_not_change_authority(manager_client):
    read(manager_client, [row(11)])
    execute("UPDATE memberships SET unit_id=11 WHERE user_id=101 AND community_id=1")
    read(manager_client, [row(11)])
    execute("UPDATE memberships SET unit_id=NULL WHERE user_id=101 AND community_id=1")
    read(manager_client, [row(11)])


def test_ac11_public_fields_order_status_and_utc(manager_client):
    seed_request(12, unit=12, owner=3, status="In progress", created="2026-01-02T09:15:30-05:00")
    seed_request(13, status="Resolved", created="2026-01-02T14:15:30Z")
    read(manager_client, [row(13, status="Resolved", created="2026-01-02T14:15:30Z"),
                          row(12, unit=12, status="In progress", created="2026-01-02T14:15:30Z"),
                          row(11)])


def test_ac11_reads_preserve_application_tables(manager_client):
    before = snapshot()
    read(manager_client, [row(11)])
    read(manager_client, [], 4)
    denied(manager_client, 3)
    assert snapshot() == before


def test_ac11_resident_routes_remain_self_only(manager_client):
    seed_request(12, unit=12, owner=3)
    read(manager_client, [row(12, unit=12), row(11)])
    before = snapshot()
    for path in ["/communities/1/requests", "/requests/11"]:
        assert_response(manager_client.get(path, headers=headers("101")),
                        {"detail": "Not found"}, 404, cache=False)
    assert_response(manager_client.get("/communities/1/requests", headers=headers("1")),
                    [row(11)], cache=False)
    assert_response(manager_client.get("/requests/12", headers=headers("1")),
                    {"detail": "Not found"}, 404, cache=False)
    assert snapshot() == before


@pytest.mark.parametrize("mutation", ["delete", "role-change"])
def test_ac11_membership_stable_through_validation(manager_client, monkeypatch, mutation):
    seed_request(12, unit=12, owner=3)
    expected = [row(12, unit=12), row(11)]
    read(manager_client, expected)  # Fail semantically before workers if the route is absent.
    before = snapshot()
    validation_entered, release_validation, updater_started, committed = (Event() for _ in range(4))
    pids, results, errors = {}, {}, []
    original_validate = RequestResponse.model_validate

    @contextmanager
    def observed_connection():
        with real_connection() as conn:
            conn.execute("SET LOCAL statement_timeout='8s'")
            pids["api"] = conn.execute("SELECT pg_backend_pid() AS pid").fetchone()["pid"]
            yield conn

    def paused_validation(cls, value, *args, **kwargs):
        result = original_validate(value, *args, **kwargs)
        if value["id"] == 11:  # Final row: the lock must cover every validation.
            validation_entered.set()
            assert release_validation.wait(8), "Validation release timed out"
        return result

    def api_worker():
        try:
            results["response"] = selected(manager_client)
        except BaseException as error:
            errors.append(error)

    def update_worker():
        try:
            with real_connection() as conn:
                conn.execute("SET LOCAL statement_timeout='8s'")
                conn.execute("SET LOCAL lock_timeout='8s'")
                pids["updater"] = conn.execute("SELECT pg_backend_pid() AS pid").fetchone()["pid"]
                updater_started.set()
                sql = ("DELETE FROM memberships WHERE user_id=101 AND community_id=1" if mutation == "delete"
                       else "UPDATE memberships SET role='board_member' WHERE user_id=101 AND community_id=1")
                conn.execute(sql)
            committed.set()
        except BaseException as error:
            errors.append(error)

    reader, updater = Thread(target=api_worker), Thread(target=update_worker)
    with monkeypatch.context() as patch:
        patch.setattr(models, "connection", observed_connection)
        patch.setattr(RequestResponse, "model_validate", classmethod(paused_validation))
        reader.start()
        try:
            assert validation_entered.wait(5), "API never reached final-row validation"
            updater.start()
            assert updater_started.wait(5), "Updater never acquired its connection"
            deadline, blocked = monotonic() + 5, False
            with real_connection() as observer:
                observer.execute("SET LOCAL statement_timeout='3s'")
                while monotonic() < deadline:
                    blockers = observer.execute("SELECT pg_blocking_pids(%s) AS pids",
                                                (pids["updater"],)).fetchone()["pids"]
                    if pids["api"] in blockers:
                        blocked = True
                        break
                    if committed.wait(0.02):
                        break
            assert blocked, "PostgreSQL did not observe the updater blocked by the API transaction"
            assert not committed.is_set()
        finally:
            release_validation.set()
            reader.join(10)
            if updater.ident is not None:
                updater.join(10)
    assert not reader.is_alive() and not updater.is_alive(), "Worker leaked"
    assert not errors, errors
    assert committed.is_set()
    assert_response(results["response"], expected)
    after = snapshot()
    expected_memberships = []
    for membership in before["memberships"]:
        if membership["user_id"] == 101 and membership["community_id"] == 1:
            if mutation == "delete":
                continue
            membership = {**membership, "role": "board_member"}
        expected_memberships.append(membership)
    assert after == {**before, "memberships": expected_memberships}
    denied(manager_client)


def test_ac11_validation_failure_releases_transaction(manager_client, monkeypatch):
    read(manager_client, [row(11)])
    before = snapshot()
    original_validate = RequestResponse.model_validate
    reached = []

    def broken_validation(cls, value, *args, **kwargs):
        original_validate(value, *args, **kwargs)
        reached.append(value["id"])
        raise ValueError("Injected response validation fault")

    with monkeypatch.context() as patch:
        patch.setattr(RequestResponse, "model_validate", classmethod(broken_validation))
        with TestClient(create_app(), raise_server_exceptions=False) as fault_client:
            assert selected(fault_client).status_code == 500
    assert reached == [11]
    with real_connection() as conn:
        assert conn.execute("""SELECT role FROM memberships
                               WHERE user_id=101 AND community_id=1 FOR UPDATE NOWAIT""").fetchone() == {"role": "manager"}
    assert snapshot() == before
    read(manager_client, [row(11)])


def test_ac11_database_failure_is_not_authorization_denial(manager_client, monkeypatch):
    read(manager_client, [row(11)])
    before = snapshot()
    reached = []

    @contextmanager
    def broken_connection():
        reached.append(True)
        raise psycopg.OperationalError("Injected connection fault")
        yield  # Defines a context manager; never substitutes a connection or row.

    with monkeypatch.context() as patch:
        patch.setattr(models, "connection", broken_connection)
        with TestClient(create_app(), raise_server_exceptions=False) as fault_client:
            assert selected(fault_client).status_code == 500
    assert reached == [True]
    assert snapshot() == before
    read(manager_client, [row(11)])
