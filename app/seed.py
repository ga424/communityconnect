"""Synthetic local fixtures only. Never an HTTP endpoint."""
from datetime import datetime, timezone
from app.models import connection

FIXED_NOW = datetime(2026, 1, 3, 12, 0, 0, tzinfo=timezone.utc)


def reset_fixtures():
    with connection() as conn:
        conn.execute("TRUNCATE maintenance_requests, memberships, app_users, units, communities RESTART IDENTITY CASCADE")
        conn.execute("INSERT INTO communities VALUES (1, 'Mountain Ridge'), (2, 'Pine Hollow')")
        conn.execute("INSERT INTO units VALUES (11, 1, 'A'), (12, 1, 'B'), (21, 2, 'A')")
        conn.execute("INSERT INTO app_users VALUES (1), (2), (3)")
        conn.execute("INSERT INTO memberships VALUES (1,1,'resident',11), (2,2,'resident',21), (3,1,'resident',12)")


def seed_request(status='Open'):
    from app.settings import REQUEST_CATEGORIES
    with connection() as conn:
        row = conn.execute("""INSERT INTO maintenance_requests
            (community_id,unit_id,submitted_by,category,description,status,created_at)
            VALUES (1,11,1,%s,'Kitchen sink leaks',%s,%s) RETURNING id""",
            (REQUEST_CATEGORIES[0], status, FIXED_NOW)).fetchone()
        return row['id']
