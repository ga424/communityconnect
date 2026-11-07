# AC-4 packet v1 — resident request details

**Decision requested: approve this bounded packet, including 30 new contract cases, the read-only AC-6 overlap, and promotion to 120 passes / 0 failures / 5 unchanged S-6 skips. Implementation has not started.**

Primary task: [COMC-57](https://gkms.atlassian.net/browse/COMC-57), S-1 AC-4. Lead: Kundan; test review: Sandeep; scope/provenance review: Gustavo. Prerequisite: review the [AC-3 verification](../evidence/ac3/README.md) for COMC-56. No teammate review is presumed from passing tests or a merge.

## Starting point and outcome

PRs #5/#6 are merged. Baseline main is `c0b26c34a1514631ec0825633e25473b570feb05`. AISE remains the latest merged 0.3.4 revision, `84816af9975b4e2aaac5219a40603be38dc1bd70`, as selected by Gustavo. AC-3's list isolation is implemented already; no new behavior is needed for it. GET `/requests/{request_id}` still returns 501 for everyone.

After this task, a seeded resident can fetch their own request in a community where they currently hold resident membership. The response exposes the existing public fields, including the stored status. Missing, malformed and unauthorized request IDs use the same `404 {"detail":"Not found"}` envelope; an invalid caller gets `401 {"detail":"Unknown user"}` first. Reading does not mutate stored data.

This implements the existing [S-1 design](../design/S-1.md), rules R1/R2 and decisions D1/D4, without revising its protected wording. No unresolved tenant, household or board policy is decided.

## Why AC-6 is included in the scope decision

The same details endpoint must return `RequestOut`, including its persisted status. The existing AC-6 fixture sets `In progress` directly in PostgreSQL. A correct details route will therefore make AC-6 pass as well as AC-4. Approval explicitly allows that existing test to become green; it does not add a status-update endpoint. COMC-59 remains a separately tracked verification/review task. AC-5 also remains separately tracked; its current self-list behavior must stay passing.

## Bounded implementation

1. Create a fresh feature branch from current main. Verify this packet still matches it; record exact approval, source hashes and an undo checkpoint.
2. Add only `tests/test_s1_details.py`, with exactly the 30 cases below, before application changes. Preserve all existing test bytes and both historical phase manifests. Run the full suite and commit actual pre-implementation failures. Expect 88 passes / 32 semantic failures / 5 skips against the 501 stub; investigate any different result rather than inventing red evidence.
3. In `app/requests.py`, replace only the details stub with the existing caller-first validation and public response model. In `app/models.py`, add a parameterized query that scopes the requested row to its submitter and current resident membership in that row's community. Reuse existing ID parsing, connection handling and serialization. No unscoped row may be returned. Evaluate membership and the row within the same read transaction/query; preserve create/list behavior.
4. Add a new exact-result verifier and frozen S-1 manifest. Promote CI only after implementation and verification; retain historical AC-1/AC-2 verifier behavior and manifests.
5. Run full tests, gate rejection controls, migration rehearsal and structural/source/whitespace checks. Inspect the diff and logs. Record actual SHAs, evidence and risks; open a PR. Stop for human review.

## Test contract: 30 new cases

| Cases | Count | Required observable result |
| --- | ---: | --- |
| Caller missing, empty, zero, negative, leading zero, plus sign, decimal, text, trailing space, unknown user, outside database range | 11 | Existing seeded request; exact 401; no stored-row change |
| Request ID zero, negative, leading zero, text, Unicode digits, decimal, unknown positive ID, outside database range | 8 | Valid resident caller; exact 404; no stored-row change |
| Invalid caller with malformed request ID | 1 | Caller validation wins: exact 401 |
| Submitter membership changed to board_member, manager or admin | 3 | Exact 404; no details or stored-row change |
| Submitter membership removed, or moved to the other community with a valid unit there | 2 | Old request remains stored; exact 404 in each case |
| Different submitter in the same community, then in the same unit | 2 | Exact 404; no details or stored-row change |
| Authorized owner reads stored Open, In progress and Resolved request | 3 | Exact seven-field public response, correct ID/community/unit/category/description/status/UTC timestamp; no submitted_by and no write |
| **Total** | **30** | All cases use disposable synthetic fixtures |

The existing AC-4 test supplies the cross-community guessed-ID regression. The existing AC-6 test supplies the persisted-status acceptance check. Both test files remain byte-identical. Do not create duplicate tests that merely mirror implementation internals. Every new case asserts HTTP behavior and unchanged persisted request rows; success cases compare to the known seeded record. The deleted/moved-membership fixtures change only setup state, then snapshot before the read.

## Allowed and protected paths

Allowed application edits: `app/requests.py`, `app/models.py` only. Allowed new test: `tests/test_s1_details.py` only. Allowed new gate: `scripts/verify_s1_baseline.py`; evidence/manifest under `docs/evidence/ac4/`; CI phase edit in `.github/workflows/scaffold-baseline.yml`; README, exact prompts, append-only LEDGER/AISE ledger records and current AISE state/artifacts for this task.

Protected: all pre-existing tests and test helpers; original design and acceptance criteria; historical evidence/manifests; existing verifier scripts; schema/migrations/seed/settings/clock; dependencies/Docker/Compose; AGENTS and AISE controls/hooks; private interview records. Any required change outside these bounds returns for a scoped correction. No data/schema migration or new dependency is proposed.

## CI phase and stop check

The approved phase would have **125 exact test IDs: 120 passes, zero failures, five unchanged S-6 skips**. Existing 95 IDs are retained: only the two explicitly named AC-4/AC-6 expectations change from stub failure to pass in the new manifest. All existing test-file hashes remain fixed. The 30 new IDs and their file hash are frozen at the tests-first commit.

The new gate must reject missing, duplicate or unexpected tests; setup/collection errors; any failure; extra/changed skips; changed test hashes; changes to protected manifest hashes; changes to any other original expectation; unapproved new IDs or a weakened new-case expectation. Include an accepted valid control and rejection controls for these paths. Historical AC-1/AC-2 JUnit reports must still pass their unchanged verifiers. The real all-test pytest exit must now be **0**, not the earlier intentional **1**.

Preserve read-only CI permissions, pinned Actions, migration checks, artifact capture and cleanup. No new deployment job. Stop only after the targeted contracts, complete phase gate, migration rehearsal, source/structural checks and protected-hash checks pass locally or in traceable CI. If local Docker remains unavailable, record that limitation and use actual CI test-first/implementation evidence; do not claim a local run.

## Review and exclusions

No UI, Playwright, authentication provider, MFA, payment behavior, status mutation, notifications, production rollout or new access roles. X-User-Id remains a synthetic local test selector. Passing the local prototype's S-1 suite is not production authorization assurance. Full-story design/test peer review, course provenance and deployment readiness remain pending.

Approve only after reviewing this concrete packet and the recorded AC-3 evidence. Merging the preparation PR alone is not implementation approval. A future execution must preserve the actual approval text; no approval is recorded here.
