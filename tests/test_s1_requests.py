import pytest
from app import settings
from app.models import connection
from app.seed import seed_request

pytestmark = pytest.mark.s1
R1 = {"X-User-Id": "1"}
R2 = {"X-User-Id": "2"}
R3 = {"X-User-Id": "3"}


def test_ac1_resident_submits_request_shown_as_open(client):
    response = client.post("/communities/1/requests", headers=R1,
        json={"category": settings.REQUEST_CATEGORIES[0], "description": "Kitchen sink leaks"})
    assert response.status_code == 201
    created = response.json()
    assert created['description'] == 'Kitchen sink leaks'
    assert created['status'] == 'Open'
    assert created['created_at'] == '2026-01-03T12:00:00Z'
    assert created['category'] == settings.REQUEST_CATEGORIES[0]
    assert created['community_id'] == 1 and created['unit_id'] == 11
    assert isinstance(created['id'], int) and created['id'] > 0
    assert 'submitted_by' not in created
    listing = client.get('/communities/1/requests', headers=R1)
    assert listing.status_code == 200
    assert listing.json() == [created]
    with connection() as conn:
        assert conn.execute('SELECT count(*) AS n FROM maintenance_requests').fetchone()['n'] == 1


def test_ac2_blank_description_rejected_and_list_unchanged(client):
    seed_request()
    before = client.get('/communities/1/requests', headers=R1)
    assert before.status_code == 200
    for description in ['', '   ', '\t\n']:
        response = client.post('/communities/1/requests', headers=R1,
            json={'category': settings.REQUEST_CATEGORIES[0], 'description': description})
        assert response.status_code == 422
        assert response.json() == {'detail': 'Description is required'}
        after = client.get('/communities/1/requests', headers=R1)
        assert after.status_code == 200 and after.json() == before.json()
    with connection() as conn:
        assert conn.execute('SELECT count(*) AS n FROM maintenance_requests').fetchone()['n'] == 1


def test_ac3_other_community_resident_does_not_see_request(client):
    seed_request()
    response = client.get('/communities/2/requests', headers=R2)
    assert response.status_code == 200
    assert response.json() == []


def test_ac4_other_community_direct_id_returns_not_found(client):
    request_id = seed_request()
    response = client.get(f'/requests/{request_id}', headers=R2)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not found'}


def test_ac5_neighbor_in_same_community_does_not_see_request(client):
    seed_request()
    response = client.get('/communities/1/requests', headers=R3)
    assert response.status_code == 200
    assert response.json() == []


def test_ac6_resident_sees_in_progress_status(client):
    request_id = seed_request(status='In progress')
    response = client.get(f'/requests/{request_id}', headers=R1)
    assert response.status_code == 200
    assert response.json()['id'] == request_id
    assert response.json()['status'] == 'In progress'
