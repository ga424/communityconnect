"""AC-2 packet v1: approved text representability and precedence regressions."""
import json

import pytest
from fastapi.testclient import TestClient

from app import clock, settings
from app.main import create_app
from app.models import connection
from app.seed import FIXED_NOW, reset_fixtures, seed_request

pytestmark = pytest.mark.s1
R1 = {"X-User-Id": "1"}


@pytest.fixture
def validation_client(monkeypatch):
    reset_fixtures()
    monkeypatch.setattr(clock, "now", lambda: FIXED_NOW)
    # Assert the HTTP contract even when the server raises (the reviewed defect).
    with TestClient(create_app(), raise_server_exceptions=False) as client:
        yield client


def snapshot():
    with connection() as conn:
        return conn.execute("SELECT * FROM maintenance_requests ORDER BY id").fetchall()


def submit(client, description, *, category=None, caller="1", community=1):
    body = {"category": settings.REQUEST_CATEGORIES[0] if category is None else category,
            "description": description}
    # JSON escapes reach the server; the client's UTF-8 encoder cannot hide the bug.
    return client.post(f"/communities/{community}/requests",
                       headers={"X-User-Id": caller, "Content-Type": "application/json"},
                       content=json.dumps(body, ensure_ascii=True).encode("ascii"))


def assert_rejected_without_change(client, description, status, detail, **kwargs):
    seed_request()
    before_rows = snapshot()
    before_list = client.get("/communities/1/requests", headers=R1)
    assert before_list.status_code == 200 and len(before_list.json()) == 1
    response = submit(client, description, **kwargs)
    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert snapshot() == before_rows
    after_list = client.get("/communities/1/requests", headers=R1)
    assert after_list.status_code == 200 and after_list.json() == before_list.json()


@pytest.mark.parametrize("description", [
    pytest.param("Kitchen\x00leak", id="nul"),
    pytest.param("Kitchen\ud800leak", id="unpaired-high"),
    pytest.param("Kitchen\udfffleak", id="unpaired-low"),
])
def test_ac2_rejects_unstorable_description(validation_client, description):
    assert_rejected_without_change(validation_client, description, 422, "Invalid request body")


def test_ac2_invalid_description_precedes_category(validation_client):
    category = "not-a-category"
    assert category not in settings.REQUEST_CATEGORIES
    assert_rejected_without_change(validation_client, "Kitchen\x00leak", 422,
                                   "Invalid request body", category=category)


def test_ac2_accepts_supplementary_unicode(validation_client):
    description = "Électricité 💧"
    response = submit(validation_client, "\u2003" + description + " \t")
    assert response.status_code == 201
    created = response.json()
    assert set(created) == {"id", "community_id", "unit_id", "category", "description", "status", "created_at"}
    assert isinstance(created["id"], int) and created["id"] > 0
    assert created["description"] == description
    assert created["category"] == settings.REQUEST_CATEGORIES[0]
    assert created["community_id"] == 1 and created["unit_id"] == 11
    assert created["status"] == "Open" and created["created_at"] == "2026-01-03T12:00:00Z"
    rows = snapshot()
    assert len(rows) == 1 and rows[0]["description"] == description
    assert rows[0]["submitted_by"] == 1 and rows[0]["id"] == created["id"]
    listing = validation_client.get("/communities/1/requests", headers=R1)
    assert listing.status_code == 200 and listing.json() == [created]


def test_ac2_identity_precedes_unstorable_description(validation_client):
    assert_rejected_without_change(validation_client, "Kitchen\x00leak", 401,
                                   "Unknown user", caller="999")


def test_ac2_membership_precedes_unstorable_description(validation_client):
    assert_rejected_without_change(validation_client, "Kitchen\x00leak", 404,
                                   "Not found", community=2)


def test_ac2_length_precedes_unstorable_description(validation_client):
    assert_rejected_without_change(validation_client, "x" * settings.MAX_DESCRIPTION_CHARS + "\x00",
                                   422, "Description is too long")
