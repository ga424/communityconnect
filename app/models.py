"""Database boundary; Liquibase owns schema creation."""
from contextlib import contextmanager
from urllib.parse import urlparse
import os
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
