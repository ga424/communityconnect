"""Fixture values are test choices, not community policy decisions."""
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")
REQUEST_CATEGORIES = tuple(os.environ.get("REQUEST_CATEGORIES", "Plumbing,Electrical").split(","))
MAX_DESCRIPTION_CHARS = int(os.environ.get("MAX_DESCRIPTION_CHARS", "1000"))
DUES_AMOUNT_CENTS = int(os.environ.get("DUES_AMOUNT_CENTS", "12345"))
RETRY_DELAY_DAYS = int(os.environ.get("RETRY_DELAY_DAYS", "2"))
MAX_PAYMENT_ATTEMPTS = int(os.environ.get("MAX_PAYMENT_ATTEMPTS", "2"))
