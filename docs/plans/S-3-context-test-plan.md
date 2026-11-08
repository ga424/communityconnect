# S-3 context test plan — design only

Draft for Sandeep's review, with Kundan reviewing business meaning. No executable cases or CI edits are made. Current phase remains120 passing cases plus5 exact S6 skips. Current traceability remains `Not yet written` for AC11/12. Exact executable counts and file-level edits belong in a later approved implementation packet.

## Fixture and observation contract

Use only the existing disposable `cc_test` harness. Create M1 with manager assignments in Mountain Ridge and Pine Hollow, M2 with only Elm Court, plus resident/board/admin users with no manager role. Include another user who is manager in A and resident in B. Seed distinct requests in each community, equal creation times for ordering, all three existing statuses, and a community with no requests. The setup must restore a known state per case, without changing or weakening current shared fixtures.

Assert HTTP status, exact response shape/content and database state invariants. Check no authorization/error response reveals IDs/names/request details for an unassigned community. Capture before/after state for read/denial cases. Do not mock the authorization query in contract tests.

| ID | Proposed test name / coverage | Observable expected result |
| --- | --- | --- |
| AC12 / T01 | test_ac12_manager_lists_only_assigned_communities | M2 receives only Elm Court; exact id/name shape |
| AC11 / T02 | test_ac11_manager_reads_only_selected_community | M1 selecting Pine Hollow receives only its requests |
| T03 | test_context_switch_does_not_reuse_previous_selection | A→B→A yields corresponding rows without remembered context |
| T04 | test_manager_context_is_independent_between_callers | Interleaved M1/M2 calls remain assignment-scoped |
| T05 | test_manager_unknown_identity_precedes_path | Missing/invalid/nonexistent callers return exact401 before invalid path handling |
| T06 | test_manager_route_rejects_other_roles | Resident/board/admin roles without manager assignment never authorize selected request reads |
| T07 | test_manager_unavailable_community_is_indistinguishable | Missing, malformed, out-of-range or unassigned selected community returns identical404 |
| T08 | test_manager_empty_options_and_empty_community | Known no-assignment caller gets empty options; authorized empty community gets empty requests |
| T09 | test_manager_revocation_denies_subsequent_read | After committed removal/role change, next selected read is404 and options omit the community |
| T10 | test_manager_assignment_elsewhere_does_not_authorize | Manager in A/resident in B has no manager-wide B read; resident routes stay self-only |
| T11 | test_manager_public_fields_order_status_and_no_writes | Seven allowed fields, UTC timestamps, stable two-key ordering, stored statuses and unchanged records |
| T12 | existing S1/S6 suite | Preserve all120 current passes,5 exact skips and original IDs/hashes |

Malformed-ID and caller cases must reuse the current syntax/range/error precedence, including leading zero, plus sign, whitespace, non-ASCII digit and overflow. Enumerate actual parameter IDs only after reviewers settle the contract; do not claim this table is exactly12 pytest cases.

## Required future tests-first execution

1. Obtain Kundan contract and Sandeep test-plan decisions. Resolve every material gap or explicitly defer the dependent scope. Explicitly authorize implementation beyond M1's S1-only boundary.
2. Prepare a bounded packet naming exact new test files, fixtures, case IDs, frozen original hashes, app files, proposed CI phase and undo/stop checks. Avoid combining UI, admin assignment or status writes.
3. Record approval, commit the undo point and add approved contract tests first. Run against missing behavior and record actual red outcomes; an API that is not implemented may return404 rather than a planned stub status. Never manufacture the expected failure count.
4. Implement only the approved manager-read scope; preserve resident routes and existing contracts. Run new cases, full suite, migration checks as applicable and unchanged-gate compatibility; capture actual exit codes/results.
5. Open the feature PR with exact diff/evidence/Jira links. No merge, deployment or review completion inferred from test results.

## Human review record

Kundan contract: Pending. Sandeep test specification: Pending. Gustavo integration/scope: request authorizes current design deliverable only; future implementation packet pending. No reviewer signatures filled by Codex.
