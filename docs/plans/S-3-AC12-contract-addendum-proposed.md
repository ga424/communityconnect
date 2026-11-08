# S3-AC12 contract addendum — proposed v1

**Gustavo scope approved on November 8, 2026; Kundan contract and Sandeep specification reviews remain pending.** This document proposes two clarifications for the options-only increment. It does not modify the protected S-3 contract. After the required reviews accept these rules, copy them into a new `docs/design/S-3-AC12-contract-addendum.md`, preserving the original design. [Packet](S-3-AC12-approval.md); [Jira COMC-62](https://gkms.atlassian.net/browse/COMC-62).

## A1 — Manager authority is independent of a unit link

Section 5 of `docs/design/S-3-context.md` says “manager unit is null.” The actual membership check in `db/changelog/001_s1_local_schema.sql` only requires residents to have a unit. A manager with a valid non-null unit is allowed by the schema.

For `GET /manager/communities`, assignment means the caller's membership has `role='manager'` for that community. Ignore `unit_id` when selecting options. Both null and valid non-null unit values are accepted. No migration, fixture constraint weakening, resident authorization widening or unit-based grant is permitted. Normal manager fixtures may remain null; the additional regression case covers both values.

## A2 — Read timing and AC boundary

Obtain options with a single joined membership/community SELECT, scoped by caller and manager role, ordered by community ID. Use parameter binding, the existing dedicated database connection, and an uncached response. Identity existence and options selection occur in the same database transaction; current committed assignments at the options statement's snapshot determine the result. A change committed before the next read must be reflected; an in-flight read can reflect its earlier snapshot.

There is no promise of instant revocation of an already returned options list. Listing an option is not a grant to read its requests. S-3 section 8 D3's stable authorization through request-row validation applies to the later AC-11 selected-request endpoint; that endpoint must recheck current authority independently. This packet neither implements nor resolves AC-11 locking/concurrent-response tests.

## A3 — Local API result and limits

Use `X-User-Id: str | None` and the unchanged `app.requests._database_id` rules: ASCII positive PostgreSQL INTEGER, no leading zero/sign/whitespace, at most ten characters and at most 2147483647. Missing, malformed, out-of-range or nonexistent caller returns `401 {"detail":"Unknown user"}`. The internal helper is reused without refactoring it in this bounded increment.

Known callers receive `200` with only their current manager options. Zero assignments, including resident/board/admin-only memberships, return `[]`. Exact option shape is `{"id": positive_integer, "name": string_length_1_to_100}`; sort by ID ascending. No request, unit, role or user fields. Database and validation failures are not converted to empty arrays or authorization denials. GET performs no writes.

This supports AC-12's selector data contract only. Browser interaction, identity, assignment administration, pagination and real-volume latency remain future work; do not report full AC-12 UI or S-3 completion from API tests.

## Review dispositions

Gustavo scope: Approved conditional on recorded reviews; see `prompts/2026-11-08-s3-ac12-scope-approval.txt`. Kundan contract: Pending (COMC-63). Sandeep specification: Pending (COMC-64). These are proposed design choices, not interview claims or fabricated teammate approvals.
