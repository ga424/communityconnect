"""S3-AC12 v1: current manager options, synthetic fixtures, unchanged S1 access."""
import pytest

from app import settings
from app.models import connection
from app.seed import seed_request

ELM = [{"id": 3, "name": "Elm Court"}]
MOUNTAIN = {"id": 1, "name": "Mountain Ridge"}
PINE = {"id": 2, "name": "Pine Hollow"}


@pytest.fixture
def manager_client(client):
    # The existing client fixture resets the database before these additions.
    with connection() as conn:
        conn.execute("INSERT INTO communities VALUES (3, 'Elm Court')")
        conn.execute("INSERT INTO units VALUES (31, 3, 'A')")
        conn.execute("INSERT INTO app_users VALUES (101), (102), (103), (104), (105)")
        # Deliberately reverse insertion order; response order must be by ID.
        conn.execute("""INSERT INTO memberships VALUES
            (101,2,'manager',NULL), (101,1,'manager',NULL),
            (102,3,'manager',NULL)""")
    seed_request()
    return client


def snapshot():
    with connection() as conn:
        return {
            table: conn.execute(f"SELECT * FROM {table} ORDER BY {order}").fetchall()
            for table, order in (
                ("app_users", "id"), ("communities", "id"), ("units", "id"),
                ("memberships", "user_id, community_id"), ("maintenance_requests", "id"),
            )
        }


def options(client, caller="102"):
    before = snapshot()
    # Raw bytes allow the non-ASCII digit to reach ASGI without client encoding failure.
    headers = {} if caller is None else {b"X-User-Id": caller.encode("latin-1")}
    response = client.get("/manager/communities", headers=headers)
    assert snapshot() == before, "Options read changed application tables"
    return response


def assert_options(client, caller, expected):
    response = options(client, caller)
    assert response.status_code == 200
    assert response.json() == expected


def test_ac12_manager_lists_only_assigned_communities(manager_client):
    assert_options(manager_client, "102", ELM)


def test_ac12_options_multiple_assignments_sorted(manager_client):
    assert_options(manager_client, "101", [MOUNTAIN, PINE])


def test_ac12_known_user_without_assignments(manager_client):
    assert_options(manager_client, "103", [])


@pytest.mark.parametrize("role", ["resident", "board_member", "admin"])
def test_ac12_nonmanager_roles_have_no_options(manager_client, role):
    with connection() as conn:
        conn.execute("INSERT INTO memberships VALUES (104,3,%s,%s)",
                     (role, 31 if role == "resident" else None))
    assert_options(manager_client, "104", [])


@pytest.mark.parametrize("caller", [
    pytest.param(None, id="missing"), pytest.param("", id="empty"),
    pytest.param("0", id="zero"), pytest.param("-1", id="negative"),
    pytest.param("0102", id="leading-zero"), pytest.param("+102", id="plus"),
    pytest.param("102.0", id="decimal"), pytest.param("manager", id="text"),
    pytest.param(" 102", id="space"), pytest.param("\u00b2", id="unicode-digits"),
    pytest.param("9999", id="unknown"),
    pytest.param("2147483648", id="outside-db-range"),
    pytest.param("9" * 50, id="overlong"),
])
def test_ac12_reject_invalid_caller(manager_client, caller):
    response = options(manager_client, caller)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unknown user"}


def test_ac12_mixed_roles_offer_only_manager_assignments(manager_client):
    with connection() as conn:
        conn.execute("""INSERT INTO memberships VALUES
            (105,1,'manager',NULL), (105,2,'resident',21)""")
    assert_options(manager_client, "105", [MOUNTAIN])
    assert_options(manager_client, "102", ELM)
    assert_options(manager_client, "105", [MOUNTAIN])


def test_ac12_deleted_assignment_disappears(manager_client):
    assert_options(manager_client, "102", ELM)
    with connection() as conn:
        conn.execute("DELETE FROM memberships WHERE user_id=102 AND community_id=3")
    assert_options(manager_client, "102", [])


@pytest.mark.parametrize("role", ["resident", "board_member", "admin"])
def test_ac12_role_change_removes_option(manager_client, role):
    assert_options(manager_client, "102", ELM)
    with connection() as conn:
        conn.execute("UPDATE memberships SET role=%s, unit_id=%s WHERE user_id=102 AND community_id=3",
                     (role, 31 if role == "resident" else None))
    assert_options(manager_client, "102", [])


def test_ac12_added_assignment_appears_without_restart(manager_client):
    assert_options(manager_client, "103", [])
    with connection() as conn:
        conn.execute("INSERT INTO memberships VALUES (103,3,'manager',NULL)")
    assert_options(manager_client, "103", ELM)


def test_ac12_reads_leave_database_unchanged(manager_client):
    before = snapshot()
    assert_options(manager_client, "102", ELM)
    assert_options(manager_client, "103", [])
    denied = options(manager_client, "9999")
    assert denied.status_code == 401
    assert denied.json() == {"detail": "Unknown user"}
    assert snapshot() == before


def test_ac12_manager_does_not_gain_resident_access(manager_client):
    assert_options(manager_client, "101", [MOUNTAIN, PINE])
    before = snapshot()
    for route in ("/communities/1/requests", "/requests/1"):
        denied = manager_client.get(route, headers={"X-User-Id": "101"})
        assert denied.status_code == 404
        assert denied.json() == {"detail": "Not found"}
    expected = {"id": 1, "community_id": 1, "unit_id": 11,
                "category": settings.REQUEST_CATEGORIES[0], "description": "Kitchen sink leaks",
                "status": "Open", "created_at": "2026-01-03T12:00:00Z"}
    resident_list = manager_client.get("/communities/1/requests", headers={"X-User-Id": "1"})
    assert resident_list.status_code == 200
    assert resident_list.json() == [expected]
    resident_detail = manager_client.get("/requests/1", headers={"X-User-Id": "1"})
    assert resident_detail.status_code == 200
    assert resident_detail.json() == expected
    assert snapshot() == before


def test_ac12_manager_unit_link_does_not_change_authority(manager_client):
    with connection() as conn:
        conn.execute("UPDATE memberships SET unit_id=31 WHERE user_id=102 AND community_id=3")
    assert_options(manager_client, "102", ELM)
    with connection() as conn:
        conn.execute("UPDATE memberships SET unit_id=NULL WHERE user_id=102 AND community_id=3")
    assert_options(manager_client, "102", ELM)
