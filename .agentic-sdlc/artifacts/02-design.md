# Current contract proposal — S3-AC11 v1

The AC12 options API is implemented in open PR15. [AC11 proposed addendum](../../docs/plans/S-3-AC11-contract-addendum-proposed.md) and [machine-readable contract](../../docs/plans/S-3-AC11-contract-proposed.json) specify one additive selected-community read and the transaction boundary. COMC66 Kundan acceptance and Gustavo scope approval are pending. Original contracts below remain unchanged; no new design is represented as approved.

---

# Draft feature contracts

Canonical feature packets: docs/design/S-1.md and docs/design/S-6.md, transferred from M1 Review v3 with open questions intact. Proposed S-1 data relationships are db/README.md and db/changelog/001_s1_local_schema.sql. Plan: docs/plans/S-1-plan.md.

S-1 uses a local synthetic X-User-Id selector; no production authentication. S-6 has no migration or provider integration in this increment. Its deferred fixture adapter remains a test design proposal. Kundan reviews S-1; Sandeep reviews S-6/data/tests. Gap-check disposition and human architecture approval remain pending.
