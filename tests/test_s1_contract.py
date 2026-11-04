"""AC-1 packet v1: existing S-1 preconditions and invariants, tests first."""
import pytest

from app import settings
from app.models import connection
from app.seed import seed_request

pytestmark = pytest.mark.s1
R1 = {"X-User-Id": "1"}
PUBLIC_FIELDS = {
    "id", "community_id", "unit_id", "category", "description", "status", "created_at"
}


def payload(description="Kitchen sink leaks"):
    return {"category": settings.REQUEST_CATEGORIES[0], "description": description}


def snapshot():
    with connection() as conn:
        return conn.execute("SELECT * FROM maintenance_requests ORDER BY id").fetchall()


def reject(client, method, path, status, detail, **kwargs):
    before = snapshot()
    response = client.request(method, path, **kwargs)
    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert snapshot() == before, "A rejected request changed persisted requests"


@pytest.mark.parametrize("method", ["POST", "GET"])
@pytest.mark.parametrize("caller", [
    pytest.param(None, id="missing"), pytest.param("", id="empty"),
    pytest.param("0", id="zero"), pytest.param("-1", id="negative"),
    pytest.param("01", id="leading-zero"), pytest.param("+1", id="plus"),
    pytest.param("1.0", id="decimal"), pytest.param("abc", id="text"),
    pytest.param("1 ", id="space"), pytest.param("999", id="unknown"),
    pytest.param("9" * 100, id="outside-db-range"),
])
def test_ac1_contract_rejects_invalid_identity(client, method, caller):
    seed_request()
    reject(client, method, "/communities/1/requests", 401, "Unknown user",
           headers={} if caller is None else {"X-User-Id": caller}, json=payload())


@pytest.mark.parametrize("method", ["POST", "GET"])
def test_ac1_contract_identity_precedes_path_and_body(client, method):
    reject(client, method, "/communities/not-an-id/requests", 401, "Unknown user",
           content="{")


@pytest.mark.parametrize("method", ["POST", "GET"])
@pytest.mark.parametrize("community", [
    pytest.param("0", id="zero"), pytest.param("-1", id="negative"),
    pytest.param("01", id="leading-zero"), pytest.param("abc", id="text"),
    pytest.param("١", id="unicode-digits"),
    pytest.param("1.0", id="decimal"), pytest.param("999", id="unknown"),
    pytest.param("9" * 100, id="outside-db-range"),
    pytest.param("2", id="other-community"),
])
def test_ac1_contract_rejects_unavailable_community(client, method, community):
    seed_request()
    reject(client, method, f"/communities/{community}/requests", 404, "Not found",
           headers=R1, json=payload())


def test_ac1_contract_access_precedes_body(client):
    reject(client, "POST", "/communities/2/requests", 404, "Not found",
           headers=R1, content="{")


@pytest.mark.parametrize("method", ["POST", "GET"])
@pytest.mark.parametrize("role", ["board_member", "manager", "admin"])
def test_ac1_contract_rejects_nonresident(client, method, role):
    seed_request()
    with connection() as conn:
        conn.execute("UPDATE memberships SET role=%s WHERE user_id=1", (role,))
    reject(client, method, "/communities/1/requests", 404, "Not found",
           headers=R1, json=payload())


@pytest.mark.parametrize("body", [
    pytest.param("{", id="malformed-json"),
    pytest.param("null", id="null"), pytest.param("[]", id="array"),
    pytest.param('"text"', id="string"), pytest.param("true", id="boolean"),
    pytest.param("{}", id="missing-fields"),
    pytest.param('{"category":"Plumbing"}', id="missing-description"),
    pytest.param('{"description":"leak"}', id="missing-category"),
    pytest.param('{"category":1,"description":"leak"}', id="category-type"),
    pytest.param('{"category":"Plumbing","description":true}', id="description-type"),
    pytest.param('{"category":"Plumbing","description":"leak","unit_id":21}', id="extra-unit"),
    pytest.param('{"category":"Plumbing","description":"leak","submitted_by":2}', id="extra-caller"),
    pytest.param('{"category":"Plumbing","description":"leak","status":"Resolved"}', id="extra-status"),
])
def test_ac1_contract_rejects_invalid_body(client, body):
    seed_request()
    reject(client, "POST", "/communities/1/requests", 422, "Invalid request body",
           headers={**R1, "Content-Type": "application/json"}, content=body)


@pytest.mark.parametrize("description", [
    pytest.param("", id="empty"), pytest.param(" \t\n", id="ascii-whitespace"),
    pytest.param("\u2003", id="unicode-whitespace"),
])
def test_ac1_contract_description_precedes_category(client, description):
    seed_request()
    reject(client, "POST", "/communities/1/requests", 422, "Description is required",
           headers=R1, json={"category": "not-a-category", "description": description})


def test_ac1_contract_rejects_description_over_limit_before_category(client):
    seed_request()
    reject(client, "POST", "/communities/1/requests", 422, "Description is too long",
           headers=R1, json={"category": "not-a-category",
                            "description": "x" * (settings.MAX_DESCRIPTION_CHARS + 1)})


@pytest.mark.parametrize("category", ["plumbing", "Plumbing ", "not-a-category"])
def test_ac1_contract_category_matches_exactly(client, category):
    assert category not in settings.REQUEST_CATEGORIES, "Use a nonmatching category fixture"
    seed_request()
    reject(client, "POST", "/communities/1/requests", 422, "Unknown category",
           headers=R1, json={"category": category, "description": "leak"})


def test_ac1_contract_trims_unicode_description_at_limit(client):
    description = "é" * settings.MAX_DESCRIPTION_CHARS
    response = client.post("/communities/1/requests", headers=R1,
                           json=payload("\u2003" + description + " \t"))
    assert response.status_code == 201
    result = response.json()
    assert set(result) == PUBLIC_FIELDS
    assert result["description"] == description
    assert result["category"] == settings.REQUEST_CATEGORIES[0]
    assert result["community_id"] == 1 and result["unit_id"] == 11
    assert result["created_at"] == "2026-01-03T12:00:00Z"
    assert result["status"] == "Open"
    rows = snapshot()
    assert len(rows) == 1 and rows[0]["description"] == description
    assert rows[0]["submitted_by"] == 1 and rows[0]["id"] == result["id"]


def test_ac1_contract_lists_tied_timestamps_by_id_descending(client):
    created = []
    for description in ["First request", "Second request"]:
        response = client.post("/communities/1/requests", headers=R1, json=payload(description))
        assert response.status_code == 201
        created.append(response.json())
    assert created[0]["created_at"] == created[1]["created_at"]
    assert created[0]["id"] < created[1]["id"]
    listing = client.get("/communities/1/requests", headers=R1)
    assert listing.status_code == 200 and listing.json() == list(reversed(created))
    assert len(snapshot()) == 2


def test_ac1_contract_lists_only_submitter_even_for_same_unit(client):
    with connection() as conn:
        conn.execute("UPDATE memberships SET unit_id=11 WHERE user_id=3")
    response = client.post("/communities/1/requests", headers=R1, json=payload())
    assert response.status_code == 201
    for caller, community in [("3", 1), ("2", 2)]:
        listing = client.get(f"/communities/{community}/requests", headers={"X-User-Id": caller})
        assert listing.status_code == 200 and listing.json() == []
    assert client.get("/communities/1/requests", headers=R1).json() == [response.json()]
