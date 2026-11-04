"""Deferred S-6 adapter contract. No business implementation or provider calls."""
from datetime import date


class RunInterrupted(RuntimeError):
    pass


def run_due_payments(today: date) -> None:
    raise NotImplementedError("S-6 is design/test-only in M1")
