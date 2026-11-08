# S3-AC12 packet v1 — manager community options

**Gustavo approved this bounded later-product scope, addendum, 28 tests and additive CI phase on November 8, 2026, conditional on Kundan and Sandeep’s reviews being recorded. Implementation has not started.** Jira [COMC-62](https://gkms.atlassian.net/browse/COMC-62), parent [COMC-10](https://gkms.atlassian.net/browse/COMC-10). Integration owner: Gustavo. Kundan contract and Sandeep test-plan decisions remain pending; record their actual dispositions before the tests-first implementation starts, as required by the existing S-3 test plan.

Review baseline: merged main `de7e609a63b1caacb7e68b7cb5d82a3335321f98`; PR13 head `ff6b0f9fd799e160079c3fb9829c0abae9395ef4`. [Review](../reviews/PR-13-and-S3-AC12-2026-11-08.md). AISE stays at the recorded merged 0.3.4 pin. PR13 merge is not AC-12 approval.

## Outcome and scope

Add only `GET /manager/communities`: a known manager can obtain the assigned communities that a later selector will offer. Preserve all S-1 behavior. This is an explicit local prototype increment beyond the M1 S-1-only implementation baseline; it does not claim Professor Dale approved an expanded M1 submission. Keep M1's original traceability CSV and submission scope unchanged; use a supplemental S-3 traceability file.

AC-11 selected-community requests, browser UI, login/MFA, assignment administration, status writes, board/tenant policy, announcements, payments, dependencies and migrations are excluded. Production remains ineligible. Tests use synthetic records in disposable `cc_test` only.

## Observable contract

Apply the [proposed addendum](S-3-AC12-contract-addendum-proposed.md) together with the original S-3 contract's options rules. Manager role and community membership determine options, regardless of a unit link. Missing/invalid/nonexistent caller gets exact401; a known caller without manager assignments gets200 `[]`; valid options contain only id/name, sorted by ID. A committed assignment/role change must affect a later uncached read. No request access is granted by the list.

```gherkin
Scenario: AC-12 offers only the manager's assigned community
  Given M2 manages only Elm Court
  When M2 requests GET /manager/communities
  Then the response is 200 with exactly Elm Court's id and name
  And no other community or fields are returned

Scenario: No manager assignment
  Given a known caller has no manager membership
  When the caller requests community options
  Then the response is 200 with an empty array

Scenario: Invalid identity
  Given the identity header is missing, malformed, out of range or unknown
  When community options are requested
  Then the response is 401 with exactly {"detail":"Unknown user"}

Scenario: Committed revocation affects later options
  Given M2 previously received Elm Court as an option
  And M2's manager assignment removal has committed
  When M2 requests options again
  Then Elm Court is omitted
```

## Exact proposed test inventory

Send the non-ASCII digit case as raw Latin-1 header bytes (superscript two, 0xB2) so the API receives it; an HTTP client encoding exception is not an authorization result. All cases go in the new `tests/test_s3_community_options.py`. The [machine-readable plan](S-3-AC12-proposed-tests.json) fixes all28 node IDs and malformed header values. It is a proposal, not an executable manifest or result. Cases assert exact HTTP/JSON output and applicable state invariants without mocking the authorization query.

| Test function | Collected cases | Required assertion |
| --- | ---: | --- |
| `test_ac12_manager_lists_only_assigned_communities` | 1 | M2 receives exactly [{id:3,name:Elm Court}]; no other fields or communities. |
| `test_ac12_options_multiple_assignments_sorted` | 1 | Insert M1 assignments out of order; IDs 1,2 appear in ascending ID order with exact names. |
| `test_ac12_known_user_without_assignments` | 1 | Known user 103 with no memberships receives 200 and []. |
| `test_ac12_nonmanager_roles_have_no_options` | 3 | A membership in each listed nonmanager role returns 200 and []. Resident fixture has unit 31. |
| `test_ac12_reject_invalid_caller` | 13 | Exact 401 with {detail:Unknown user}; no options; missing omits the header. Use the values in invalid_callers. |
| `test_ac12_mixed_roles_offer_only_manager_assignments` | 1 | Manager in A and resident in B sees only A; interleave M2 and repeat first caller to reject shared cached context. |
| `test_ac12_deleted_assignment_disappears` | 1 | Read M2 option, commit deletion, read again: []. |
| `test_ac12_role_change_removes_option` | 3 | Read M2 option, commit role change, read again: []; resident change uses unit 31. |
| `test_ac12_added_assignment_appears_without_restart` | 1 | Known empty caller first gets []; commit new manager assignment, next call includes it. |
| `test_ac12_reads_leave_database_unchanged` | 1 | After fixture setup snapshot all five application tables; perform successful, empty and denied reads; exact snapshot unchanged. |
| `test_ac12_manager_does_not_gain_resident_access` | 1 | Seed resident request; obtain manager options then require existing resident list/details denial for manager; known resident still sees own row. |
| `test_ac12_manager_unit_link_does_not_change_authority` | 1 | Set M2 manager membership to valid unit31, then null; both requests return the same Elm Court option. |

Fixtures: use the existing `client` fixture first so its reset occurs before new setup. Add Elm Court3/unit31, M1 user101 assigned to communities1/2, M2 user102 assigned only to3, known empty user103 and distinct mixed-role/nonmanager users104+. No collisions with original users1–3. Insert out of ID order for sorting. Each case resets through `client`; local fixture additions live in the new file. Resident role changes use a valid matching unit. Seed a resident-owned request before read-only/state and resident-regression checks. Do not remove a membership referenced by a maintenance request. Snapshot `app_users`, `communities`, `units`, `memberships`, `maintenance_requests` in deterministic primary-key order after setup. No real data.

## Allowed future files and limits

| Path | Only authorized change if this packet is approved |
| --- | --- |
| `app/manager_communities.py` (new) | Options router, typed CommunityOption, parameterized read query; reuse existing connection, user_exists and frozen ID parser |
| `app/main.py` | Import and register that router only; keep local/test guard, resident router and health unchanged |
| `tests/test_s3_community_options.py` (new) | Exactly28 proposed cases and local helpers/fixtures, frozen at tests-first commit |
| `scripts/verify_s3_ac12_baseline.py` (new) | Strict additive phase verifier plus adversarial self-test controls |
| `.github/workflows/scaffold-baseline.yml` | Retain migration/source checks and historical gates; activate exact153-case phase as described below |
| `docs/design/S-3-AC12-contract-addendum.md` (new) | Record the actually approved addendum without rewriting the S-3 original |
| `docs/evidence/s3-ac12/` (new) | Approval/undo hashes, frozen manifest, actual red/local/CI reports and integrity checks |
| `docs/traceability/S-3-AC12.csv` (new) | Supplemental API projection: source AC12/E3/A2, new test, API evidence and browser outcome pending |
| `AGENTS.md` | Add only the explicit approved AC12 local later-product exception; retain M1 S1-only boundary and all control rules |
| `README.md`, `docs/plans/S-3-plan.md`, this packet, `docs/reviews/` | Current approved scope, verified status, usage instructions and review results |
| `prompts/`, `LEDGER.md`, `.agentic-sdlc/ledgers/`, `.agentic-sdlc/state/pipeline-state.json`, `.agentic-sdlc/artifacts/07-review.md` | Exact human responses, append-only provenance, current state/evidence; no invented signoffs |

Protected: every existing test and shared fixture, existing feature files and designs, `app/requests.py`, `app/models.py`, `app/seed.py`, settings/clock/payments, all applied migrations, Docker/dependency inputs, existing verifier scripts/manifests, M1 `docs/traceability.csv`, AISE config/hooks/framework pin and all prior ledger bytes. Capture the execution baseline at the actual approval commit and classify only the expressly allowed modifications above. If an approved behavior needs a protected change, stop and propose the correction; do not weaken a test.

## Tests-first execution and CI phase

1. Record actual scope approval and required named review dispositions. Re-fetch main, inspect intervening changes and stop if they invalidate this packet. Create a new feature branch, record a clean undo commit and protected hashes before adding tests.
2. Add exactly the approved28 cases; collect and compare actual node IDs with the proposal. Run against unchanged missing behavior, preserving real exit code and JUnit. Record actual red results; do not invent an expected failure count or replace failures with skips. Commit and freeze new file hash before implementation.
3. Add the narrow route and router registration. Preserve existing125 expectations and test-file hashes byte for byte. New manifest is exactly those125 records plus28 new required passes, with original manifest hash and actual tests-first file hash. Proposed target: **148 passed / 0 failed / 0 errors / 5 exact S-6 skips (153 total)**. No promotions or changed old skip reasons.
4. Add the new verifier, retaining all historical scripts. Validate old S-1 evidence with the unchanged gate using `docs/evidence/s1-closeout/fresh-clone-junit.xml`; validate the new full run with the new gate. Preserve AC1/AC2 historical checks and all self-tests. The old full-report S1 gate correctly rejects new IDs, so replace only that full-run invocation with the approved new full gate. Do not filter failed cases out of a report or weaken an existing verifier.
5. New gate self-tests must accept one valid control and reject missing old/new IDs, unexpected/duplicate IDs, failures/errors at case and suite level, extra skips, changed S6 reasons or unexpected S6 passes, modified old expectations/hash inventories, altered S1 manifest hash, changed new IDs/hash, missing new hash and weakened new expectations. Check actual on-disk file hashes too. These verifier controls are separate from the28 pytest cases.
6. Run the unchanged disposable migration rehearsal and full Docker suite, capture actual exit0, strict phase and gate controls, source/structural checks, protected hashes and append-only prefixes. Preserve the user's preview and unrelated containers. No extra broad test runs without a new concern.
7. Open an implementation PR with immutable evidence and Jira updates. API success leaves full browser AC12 and S3 pending. Human result review, merge permission and production assurance remain separate. Delete the implementation branch only after its eventual merge and required ancestry/clean/open-PR checks.

## Stop check and approval record

Stop for changed source ACs, disputed addendum, differing test inventory, unexplained old test/hash change, unplanned schema/dependency/UI/security scope, identity or real-volume policy dependency, failing controls, or absent required approvals. Record gaps in Jira and AISE without claiming acceptance.

Gustavo scope approval: **Approved, conditional on recorded peer reviews**; exact response is in `prompts/2026-11-08-s3-ac12-scope-approval.txt`. Kundan contract: **Pending (COMC-63)**. Sandeep test specification: **Pending (COMC-64)**. Scope approval persists for packet v1, the addendum,28 tests,153-case CI gate and later-product scope; do not request it again unchanged. Executable work waits for the actual reviews and resolution of material findings. See [current review status](../reviews/S-3-AC12-approval-status-2026-11-08.md).
