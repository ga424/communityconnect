"""Database boundary; Liquibase owns schema creation."""
from contextlib import contextmanager
from urllib.parse import urlparse
import os
from datetime import datetime
import psycopg
from psycopg.rows import dict_row
from app import settings


@contextmanager
def connection():
    # This scaffold can only connect to its dedicated disposable test database.
    if os.environ.get("APP_ENV") != "test" or urlparse(settings.DATABASE_URL).path != "/cc_test":
        raise RuntimeError("Scaffold requires APP_ENV=test and the cc_test database")
    with psycopg.connect(settings.DATABASE_URL, row_factory=dict_row) as conn:
        yield conn


def user_exists(conn, user_id: int) -> bool:
    return conn.execute("SELECT 1 FROM app_users WHERE id = %s", (user_id,)).fetchone() is not None


def resident_unit(conn, user_id: int, community_id: int) -> int | None:
    # Hold membership stable through authorization and the following read/write.
    row = conn.execute(
        """SELECT unit_id FROM memberships
           WHERE user_id = %s AND community_id = %s AND role = 'resident'
           FOR SHARE""",
        (user_id, community_id),
    ).fetchone()
    return row["unit_id"] if row else None


def insert_request(conn, *, user_id: int, community_id: int, unit_id: int,
                   category: str, description: str, created_at: datetime) -> dict:
    return conn.execute(
        """INSERT INTO maintenance_requests
           (community_id, unit_id, submitted_by, category, description, status, created_at)
           VALUES (%s, %s, %s, %s, %s, 'Open', %s)
           RETURNING id, community_id, unit_id, category, description, status, created_at""",
        (community_id, unit_id, user_id, category, description, created_at),
    ).fetchone()


def own_requests(conn, *, user_id: int, community_id: int) -> list[dict]:
    return conn.execute(
        """SELECT id, community_id, unit_id, category, description, status, created_at
           FROM maintenance_requests
           WHERE community_id = %s AND submitted_by = %s
           ORDER BY created_at DESC, id DESC""",
        (community_id, user_id),
    ).fetchall()


def own_request(conn, *, user_id: int, request_id: int) -> dict | None:
    # Scope row and resident membership together; keep that membership stable
    # through response validation. A membership elsewhere grants no access.
    return conn.execute(
        """SELECT r.id, r.community_id, r.unit_id, r.category, r.description,
                  r.status, r.created_at
           FROM maintenance_requests AS r
           JOIN memberships AS m
             ON m.user_id = r.submitted_by AND m.community_id = r.community_id
           WHERE r.id = %s AND r.submitted_by = %s AND m.role = 'resident'
           FOR SHARE OF m""",
        (request_id, user_id),
    ).fetchone()
