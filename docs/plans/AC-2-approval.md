# AC-2 / COMC-55 — approval packet v1

**Status: proposed; awaiting Gustavo's explicit approval.** Prepared from merged PR #4, main checkpoint `3708f9dd02abb43feffa54ebfa4df47aa58bbb74`. No AC-2 application changes, acceptance tests or CI promotion have been executed. The diagnostic probe used in review is not a new acceptance baseline.

## Why this is the next task

The six-task S-1 plan puts AC-2 next. Its original blank/whitespace-description test already passes through AC-1's required guards. Review found one additional validation defect: a nonempty description containing NUL or an unpaired Unicode surrogate reaches the database adapter and returns HTTP 500. Three diagnostic inputs reproduced this; no row was inserted. See [PR4 review](../reviews/PR-4-and-AC-2-2026-11-04.md) and [observed results](../evidence/pr4-review/validation-probe.json).

**Proposed outcome:** preserve AC-2's existing blank-description behavior and reject unsupported description text with a controlled 422 before any insert. This packet explicitly proposes the missing text-policy decision, eight regression cases and the corresponding CI phase. It does not silently amend the protected design or authorize the next S-1 task.

## Contract decision included in this approval

After caller, path/membership and JSON/body-shape checks, keep description processing in this order:

1. Apply Python `str.strip()`; empty → 422 `{"detail":"Description is required"}`.
2. Apply `len()`; above `MAX_DESCRIPTION_CHARS` → 422 `{"detail":"Description is too long"}`.
3. **New clarification:** a nonempty, in-limit description must contain Unicode scalar values and exclude U+0000, so it is representable in PostgreSQL text. NUL or an unpaired surrogate → 422 `{"detail":"Invalid request body"}`. Reject; do not strip, replace, escape into stored text or silently truncate these characters.
4. Preserve exact, case-sensitive category validation → 422 `{"detail":"Unknown category"}`.

This means an unsupported description precedes an unknown category, while an oversized description still returns the existing length error first. Categories continue to use the existing exact allow-list; no new category policy is introduced. Valid accented text and supplementary Unicode characters such as emoji remain supported. Every rejection leaves persisted requests and the resident's list unchanged.

This clarification will be captured in a **new** `docs/design/S-1-AC2-validation-addendum.md` only after approval; the original design text stays unchanged. Do not catch all database exceptions or translate connection/schema failures into input errors. Validate the described text condition before the insert; preserve rollback behavior for other failures.

## Allowed files after approval

| Path | Bounded change |
| --- | --- |
| app/requests.py | Add only the description-text guard at the proposed validation position. Preserve identity, access, other body/description/category behavior, response fields and the details stub. |
| tests/test_s1_validation.py (new) | Add the eight cases below first; preserve every existing test byte-for-byte. |
| docs/design/S-1-AC2-validation-addendum.md (new) | Record the explicit approved text-policy clarification and its precedence, without rewriting the original S-1/S-6 designs. |
| scripts/verify_ac1_baseline.py | Only expose phase counts as an explicit parameter to reusable verification/self-test functions, defaulting to the current 80/2/5 behavior. The existing AC-1 CLI, fixed manifest and historical-report validation must remain equivalent. |
| scripts/verify_ac2_baseline.py (new) | Select the fixed AC-2 manifest/counts and reuse the exact-ID/hash verifier. Require the original 87 expectations to remain identical; accept only eight explicitly named new passing cases. |
| .github/workflows/scaffold-baseline.yml | Name/select the AC-2 phase; preserve read-only permissions, pinned actions, migration rehearsal, source guard, pytest exit capture, artifact upload and cleanup. |
| docs/evidence/ac2/; README.md; prompts/; LEDGER.md; relevant AISE ledgers/state/artifacts | Save actual approval, tests-first undo/result SHAs, manifests, hashes, outputs, review and open risks. Append ledger history. |

**Protected:** all current `tests/` files; original `docs/design/S-1.md` and `S-6.md`; acceptance criteria; AC-1 evidence/manifest; `app/models.py`, settings/clock and all other app files; migrations/schema; dependencies; AGENTS.md; AISE controls. No data migration, dependency addition, production authentication, provider work or new endpoint is allowed. If the listed scope is insufficient, stop with the concrete conflict.

## Eight new contract cases

| Proposed test / case | Required observable result |
| --- | --- |
| test_ac2_rejects_unstorable_description[nul] | 422 Invalid request body; no write/list change |
| test_ac2_rejects_unstorable_description[unpaired-high] | 422 Invalid request body; no write/list change |
| test_ac2_rejects_unstorable_description[unpaired-low] | 422 Invalid request body; no write/list change |
| test_ac2_invalid_description_precedes_category | Unsupported description plus unknown category → 422 Invalid request body; no write |
| test_ac2_accepts_supplementary_unicode | Valid emoji/accented description with outer whitespace → 201, correctly trimmed/stored/publicly returned, exactly one row |
| test_ac2_identity_precedes_unstorable_description | Invalid caller plus unsupported description → 401 Unknown user; no write |
| test_ac2_membership_precedes_unstorable_description | Unauthorized community plus unsupported description → 404 Not found; no write |
| test_ac2_length_precedes_unstorable_description | Description over the configured limit containing NUL → 422 Description is too long; no write |

Send unsupported Unicode as JSON escapes so failures originate in the server rather than the HTTP client's encoder. Tests must assert the response without concealing unexpected exceptions; use a TestClient configured to expose HTTP 500 as a response for these negative cases. Preserve seeded baseline rows when checking unchanged storage/list output.

## Execution sequence and stop checks

1. Record the actual approval, exact packet version and any exclusions. Fetch current main, verify a clean checkout and create a fresh feature branch. Record the current main SHA as undo point; refresh this packet if the scope-relevant source changed.
2. Add the approved design addendum and only the new eight-case test file. Execute against current behavior; record actual failing cases and passing guards. Commit this test specification **before** application edits. Do not manufacture eight failing tests when some controls already pass.
3. Add the small text guard. Preserve existing expected values and all 87 current test outcomes. Inspect the diff, caller/membership precedence, database rollback, logs and Unicode behavior.
4. Create the frozen AC-2 manifest from the committed test specification: original 87 IDs/outcomes/hashes unchanged, eight new passing IDs and their file hash. Promote CI explicitly. Verify the old AC-1 gate still accepts its original report; verify the new gate rejects missing old/new tests, duplicates, setup/collection errors, unexpected failures, added/changed skips and test-hash mismatches.
5. Run the full container suite and migration checks. **Expected approved phase: 88 passed, 2 deferred AC-4/AC-6 failures, 5 unchanged S-6 skips = 95 cases; pytest exit remains 1.** No new error, missing test, skip or other failure is permitted. Capture actual outputs and compare protected hashes.
6. Update COMC-55 and AISE with exact evidence, open the implementation PR and stop for human review. Delete its branch only after the latest head is merged and no open PR remains.

## Approval boundary

Approval means Gustavo accepts this AC-2 scope, the explicit unsupported-description policy/precedence, eight new tests and CI promotion. Kundan remains implementation lead; Sandeep reviews tests/gate evidence; Gustavo reviews provenance/integration. It does not sign for teammates, close full-story design/gap reviews, authorize AC-3/4/5/6, merge/deploy, or mark S-1 complete. AC-4/6 remain deferred; S-6 remains unbuilt.

Suggested approval: **Approve AC-2 packet v1, including the text-policy addendum, eight regression cases and CI phase change.** This sentence is proposed approval wording, not a recorded decision.
