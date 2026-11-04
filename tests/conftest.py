import pytest
from fastapi.testclient import TestClient
from app import clock
from app.main import create_app
from app.seed import FIXED_NOW, reset_fixtures


@pytest.fixture
def client(monkeypatch):
    reset_fixtures()
    monkeypatch.setattr(clock, "now", lambda: FIXED_NOW)
    with TestClient(create_app()) as client:
        yield client
