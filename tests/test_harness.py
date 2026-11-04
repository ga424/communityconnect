import psycopg
import pytest
from app.models import connection

pytestmark = pytest.mark.harness


def test_health_identifies_nonproduction_scaffold(client):
    assert client.get("/health").json() == {"status": "scaffold", "production_eligible": False}


def test_liquibase_applied_schema_and_seeded_synthetic_memberships(client):
    with connection() as conn:
        assert conn.execute("SELECT count(*) AS n FROM databasechangelog WHERE id='001-s1-local-schema'").fetchone()['n'] == 1
        assert conn.execute("SELECT count(*) AS n FROM memberships").fetchone()['n'] == 3


def test_schema_rejects_resident_unit_in_another_community(client):
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        with connection() as conn:
            conn.execute("UPDATE memberships SET unit_id=21 WHERE user_id=1")


def test_schema_rejects_resident_without_unit(client):
    with pytest.raises(psycopg.errors.CheckViolation):
        with connection() as conn:
            conn.execute("UPDATE memberships SET unit_id=NULL WHERE user_id=1")
