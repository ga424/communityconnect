"""Proposed test-only fixture adapter; review with Sandeep before S-6 build.

A future implementation must use PostgreSQL and a separately committed processor
key store; an in-memory counter cannot satisfy restart evidence. These stubs keep
the deferred tests collectable without pretending payment behavior exists.
"""
class PaymentHarness:
    def __getattr__(self, name):
        raise NotImplementedError(f"Deferred S-6 test fixture adapter: {name}")
