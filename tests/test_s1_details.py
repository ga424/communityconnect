"""AC-4 packet v1: request ownership, resident scope and AC-6 stored status."""
import pytest
from fastapi.testclient import TestClient

from app import clock, settings
from app.main import create_app
from app.models import connection
from app.seed import FIXED_NOW, reset_fixtures, seed_request

pytestmark = pytest.mark.s1
R1 = {"X-User-Id": "1"}


@pytest.fixture
def details_client(monkeypatch):
    reset_fixtures()
    monkeypatch.setattr(clock, "now", lambda: FIXED_NOW)
    with TestClient(create_app(), raise_server_exceptions=False) as client:
        yield client


def snapshot():
    with connection() as conn:
        return conn.execute("SELECT * FROM maintenance_requests ORDER BY id").fetchall()


def read_without_write(client, request_id, headers):
    before = snapshot()
    response = client.get(f"/requests/{request_id}", headers=headers)
    assert snapshot() == before, "Reading details changed persisted requests"
    return response


def reject(client, request_id, status, detail, *, headers=R1):
    response = read_without_write(client, request_id, headers)
    assert response.status_code == status
    assert response.json() == {"detail": detail}


def expected_record(request_id, *, community=1, unit=11, description="Kitchen sink leaks", status="Open"):
    # Exact public contract from known fixtures, independent of response serialization.
    return {"id": request_id, "community_id": community, "unit_id": unit,
            "category": settings.REQUEST_CATEGORIES[0], "description": description,
            "status": status, "created_at": "2026-01-03T12:00:00Z"}


@pytest.mark.parametrize("caller", [
    pytest.param(None, id="missing"), pytest.param("", id="empty"),
    pytest.param("0", id="zero"), pytest.param("-1", id="negative"),
    pytest.param("01", id="leading-zero"), pytest.param("+1", id="plus"),
    pytest.param("1.0", id="decimal"), pytest.param("abc", id="text"),
    pytest.param("1 ", id="space"), pytest.param("999", id="unknown"),
    pytest.param("9" * 100, id="outside-db-range"),
])
def test_ac4_details_reject_invalid_caller(details_client, caller):
    request_id = seed_request()
    reject(details_client, request_id, 401, "Unknown user",
           headers={} if caller is None else {"X-User-Id": caller})


@pytest.mark.parametrize("request_id", [
    pytest.param("0", id="zero"), pytest.param("-1", id="negative"),
    pytest.param("01", id="leading-zero"), pytest.param("abc", id="text"),
    pytest.param("١", id="unicode-digits"), pytest.param("1.0", id="decimal"),
    pytest.param("999", id="unknown"), pytest.param("9" * 100, id="outside-db-range"),
])
def test_ac4_details_reject_unavailable_id(details_client, request_id):
    seed_request()
    reject(details_client, request_id, 404, "Not found")


def test_ac4_details_identity_precedes_path(details_client):
    seed_request()
    reject(details_client, "not-an-id", 401, "Unknown user", headers={"X-User-Id": "999"})


@pytest.mark.parametrize("role", ["board_member", "manager", "admin"])
def test_ac4_details_reject_nonresident_owner(details_client, role):
    request_id = seed_request()
    with connection() as conn:
        conn.execute("UPDATE memberships SET role=%s WHERE user_id=1 AND community_id=1", (role,))
    reject(details_client, request_id, 404, "Not found")


def test_ac4_details_membership_elsewhere_does_not_authorize(details_client):
    request_id = seed_request()
    with connection() as conn:
        conn.execute("UPDATE memberships SET role='board_member' WHERE user_id=1 AND community_id=1")
        conn.execute("INSERT INTO memberships VALUES (1,2,'resident',21)")
    reject(details_client, request_id, 404, "Not found")


def test_ac4_details_owner_in_two_communities(details_client):
    first_id = seed_request()
    with connection() as conn:
        conn.execute("INSERT INTO memberships VALUES (1,2,'resident',21)")
        second_id = conn.execute(
            """INSERT INTO maintenance_requests
               (community_id, unit_id, submitted_by, category, description, status, created_at)
               VALUES (2,21,1,%s,'Second community request','Resolved',%s) RETURNING id""",
            (settings.REQUEST_CATEGORIES[0], FIXED_NOW),
        ).fetchone()["id"]
    expected = [expected_record(first_id), expected_record(
        second_id, community=2, unit=21, description="Second community request", status="Resolved",
    )]
    for record in expected:
        response = read_without_write(details_client, record["id"], R1)
        assert response.status_code == 200
        assert response.json() == record


@pytest.mark.parametrize("same_unit", [pytest.param(False, id="same-community"),
                                      pytest.param(True, id="same-unit")])
def test_ac4_details_reject_other_submitter(details_client, same_unit):
    request_id = seed_request()
    if same_unit:
        with connection() as conn:
            conn.execute("UPDATE memberships SET unit_id=11 WHERE user_id=3 AND community_id=1")
    reject(details_client, request_id, 404, "Not found", headers={"X-User-Id": "3"})


@pytest.mark.parametrize("status", [pytest.param("Open", id="open"),
                                   pytest.param("In progress", id="in-progress"),
                                   pytest.param("Resolved", id="resolved")])
def test_ac4_details_returns_persisted_status(details_client, status):
    request_id = seed_request(status=status)
    response = read_without_write(details_client, request_id, R1)
    assert response.status_code == 200
    assert response.json() == expected_record(request_id, status=status)
