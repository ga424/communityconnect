# AC-1 / COMC-54 — approval packet v1

**Status: awaiting Gustavo's explicit approval.** Prepared November 4, 2026 from merged PR #2 (main checkpoint dafd2ca71b89fd2d2a8fc0fdae6d8209f93dee12). No implementation authorization is recorded. This packet refines task 1 of S-1-plan.md; it does not approve tasks 2–6 or settle open questions.

## Observable outcome

Given seeded resident R1 has a unit in Mountain Ridge and an allowed category, when R1 posts "Kitchen sink leaks", return 201 with that description, Open status, the injected UTC time and a positive generated ID. R1's own community list contains the new request. Insert exactly one row; omit submitted_by from responses.

## How and allowed files

| Path | Authorized change only after approval |
| --- | --- |
| app/requests.py | Implement POST /communities/{community_id}/requests and GET /communities/{community_id}/requests, caller/access/input validation and public response formatting. Keep GET /requests/{request_id} as its existing 501 stub. |
| app/models.py | Parameterized PostgreSQL helpers to resolve users/resident memberships, insert one request transactionally and list only the caller's submissions in the selected community. Retain local database guard. |
| tests/test_s1_contract.py (new) | Tests-first checks for the already specified S-1 validation order, no-write rejection, trimmed/boundary descriptions, isolation and deterministic list ordering. Preserve existing tests byte-for-byte. |
| scripts/verify_ac1_baseline.py (new) | Verify the approved incremental result by full test IDs; reject setup errors, unexpected failures, missing tests and new skips. Preserve the old red-baseline verifier as historical evidence. |
| .github/workflows/scaffold-baseline.yml | Select/name the AC-1 phase gate and preserve test exit/output artifacts, migration checks, secret scan and read-only permissions. |
| README.md; docs/evidence/ac1/; prompts/; LEDGER.md; AISE ledgers/state/artifact for this task | Record current command/results, exact prompt and actual approval, undo/result SHAs, evidence and unresolved risks. Append ledger history. |

Reuse app/settings.py and app/clock.py unchanged. Do not modify existing tests, docs/design/, acceptance criteria, db/changelog/, AGENTS.md or AISE policy controls. Do not add migrations, new dependencies or provider endpoints. If an allowed scope is insufficient, stop and report the concrete conflict.

## Required behavior at first write

1. Resolve caller first from the synthetic header; missing, malformed or unknown caller → 401 {"detail":"Unknown user"}. Use the design's positive-decimal ID format. Validate path and resident membership next; malformed/unauthorized community or non-resident → 404 {"detail":"Not found"}. Do not read/return other residents' records.
2. Only then parse the JSON object containing exactly category and description as strings. Invalid JSON/shape/types/extras → 422 {"detail":"Invalid request body"}. No DB write occurs on rejection.
3. Apply Python str.strip() and len(). Empty → Description is required; above MAX_DESCRIPTION_CHARS → Description is too long; non-exact category outside REQUEST_CATEGORIES → Unknown category. Use those existing named settings, not new policy values. Validation order remains description before category.
4. Derive user, community and unit from the resolved membership. Supply Open and app.clock.now() in UTC, never client fields. Commit one row on success and return the documented fields with YYYY-MM-DDTHH:MM:SSZ formatting.
5. Scope list queries by community_id and submitted_by, after verifying resident membership. Sort created_at descending then id descending. No details endpoint, manager update, tenant policy or wider household access.

Validation/access rules are binding preconditions of AC-1. Implementing them may also satisfy AC-2/3/5. Do not deliberately leave invalid writes or leaks so those tasks stay red; their later tasks can be verification-only with their own recorded review.

## Execution sequence

1. Record Gustavo's actual approval text and the exact scope/version approved. Verify the current main/PR head and a clean worktree. Create a new feature branch from current main; record its starting commit as the undo point before edits.
2. Add only the new contract tests derived from the existing design. Run them against the current stubs, preserve semantic red output and commit that test specification/undo point before changing app code. Do not alter existing expected values.
3. Implement the two allowed routes and helpers. Review transaction boundaries, SQL parameters, visibility filters, validation precedence and logs. Run targeted tests and the full suite.
4. Switch CI to the approved incremental gate, preserving all assertions and the original red evidence. Verify the gate rejects a missing required test, setup error, unexpected failure or extra skip. Record evidence of that gate validation.
5. Publish the feature PR with exact results and per-file review notes; update COMC-54 and AISE records. Stop at review readiness; no automatic merge, next AC or deployment. Delete the feature branch only after its latest head is merged.

## Test and stop conditions

- All four existing harness tests, AC-1, AC-2, AC-3, AC-5 and every new contract test must pass. This covers the first write path's no-write-on-invalid-input and self-only access invariants, not merely the happy path.
- AC-4 and AC-6 remain their existing semantic failures on the unchanged 501 details stub. Treat unexpected outcomes as a scope/test issue to review; do not weaken tests.
- All five S-6 tests retain their exact AC-labelled skip reasons; no other skip/error is allowed. Check exact required test IDs, not just totals. Base suite result should be 8 passes, 2 expected failures, 5 skips, plus the new passing contract cases; pytest exit is still 1 until the remaining details route is implemented.
- Contract test cases: missing/invalid/unknown identity; identity precedence over bad path/body; wrong-community/non-resident access; malformed JSON, nonobject/extra/missing/mistyped fields; whitespace-only and over-limit descriptions; trimmed description at the configured limit; category case mismatch; rejected-write row/list unchanged; two requests at equal clock time sorted by descending ID; response omission of submitted_by.
- Preserve and inspect the full run output/JUnit, API errors and DB counts. Compare existing test-file hashes to the pre-task baseline. All application checks remain local/synthetic; no production-readiness claim.

## Approval meaning and remaining work

Approval means Gustavo accepts this bounded AC-1 scope, its proposed new contract tests and CI phase change. It does not sign for Kundan/Sandeep, close their full S-1 gap/design/test reviews, approve AC-4 or S-6, or mark the complete story done. Named team responsibilities remain in Jira. Those broader review tasks and final fresh-clone all-S-1-green verification remain required before submission.

Suggested response: **Approve AC-1 packet v1, including its contract tests and CI phase change.** Any narrower approval must state the excluded portion; implementation cannot proceed with an unresolved write-path guard or incompatible CI gate.
