> Integration update: PR17 merged at `cf1e457052bbbe806a3711194e426181c599165f` by abreugus; final-head CI verifies200/0/5 and both merged branches are removed. COMC65 Done. [Closeout](../evidence/s3-ac11/merge-closeout.json). Earlier pending checkpoints below are historical; no next feature approval is inferred.

> Execution update: AC11 v1 is implemented locally after actual approval. Frozen52 tests pass; full200/0/5 phase verified. See [evidence](../evidence/s3-ac11/README.md). Result review/merge remains pending. The historical preparation and approval checkpoints below retain their original wording.

# S3-AC11 packet v1 — selected-community request reads

**Approved execution update:** Gustavo answered “Approve merge and AC11 v1” to the question explicitly naming this addendum,52 tests and200/0/5 CI phase. [Exact record](../../prompts/2026-11-08-s3-ac11-approval.txt). PR15/16 are integrated; COMC66/67 are Done by Gustavo. Earlier pending statements below describe historical checkpoints. No new result/merge approval is inferred.

**Status recheck, November 8, 2026:** COMC-66 and COMC-67 are now Done, closed by Gustavo at 18:11:58 and 18:12:01 Eastern. Neither ticket has a review comment or attachment; no independent reviewer authorship is claimed. PR15 remains open. Separate approval of this AC11 packet and authorization to merge/integrate PR15 have not yet been recorded. The 52-case plan and executable files are unchanged. Earlier planning language below retains its original checkpoint; this update supersedes ticket-status wording only.

**Proposed, awaiting approval.** [COMC-65](https://gkms.atlassian.net/browse/COMC-65), parent [COMC-10](https://gkms.atlassian.net/browse/COMC-10). Gustavo owns integration/scope; Kundan reviews the contract in COMC-66; Sandeep reviews the test plan in COMC-67. No review completion or scope approval is implied by this draft or by the AC12 reviews.

## Outcome

Let a manager read requests for exactly one currently assigned community. Source AC11/E-3: M1 manages Mountain Ridge/Pine Hollow; selecting Pine Hollow shows only its request. This packet delivers the API part through `GET /manager/communities/{community_id}/requests`; a later UI increment must prove the browser outcome. M1's original S1-only submission scope is unchanged.

**Dependency:** integrate reviewed PR15 before beginning this implementation. Current review baseline is `8f993ab6fb96e837315918d0da2b344642a05c57`, with verified148 passes and five unchanged S6 skips. PR15 is currently open; the preparation branch is stacked on it solely to keep this documentation diff small. Before coding, fetch main, verify PR15's reviewed contents are integrated, capture the actual base and recheck this packet against any intervening changes.

## Contract to approve

Approve the [proposed addendum](S-3-AC11-contract-addendum-proposed.md) and [machine-readable contract](S-3-AC11-contract-proposed.json). They specify exact field/error behavior, manager role independent of a unit link, current membership locking through response validation, ordered public rows and no writes. Original design documents and approved AC12 addendum remain unchanged.

```gherkin
Scenario: AC11 reads only the selected managed community
  Given M1 manages Mountain Ridge and Pine Hollow
  And each has one Open request
  When M1 requests Pine Hollow's manager request list
  Then the exact array contains only Pine Hollow's request
  And no submitter identity or other community's request is returned

Scenario: Authorization is checked on every selection
  Given a known caller has no manager assignment to the selected community
  When that caller requests its manager request list
  Then the response is 404 with exactly {"detail":"Not found"}
  And the database is unchanged

Scenario: Committed revocation affects the next read
  Given M1 previously read an assigned community
  And M1's assignment removal has committed
  When M1 reads it again
  Then the response is 404 with no request details

Scenario: In-flight validation and revocation have a defined order
  Given an authorized read holds its manager membership stable
  When a concurrent transaction tries to remove or change that membership
  Then the mutation waits until response data validation ends
  And once that revocation commits a later read is denied
```

## Exact proposed test inventory

**52 cases** in new `tests/test_s3_selected_requests.py`; [JSON](S-3-AC11-proposed-tests.json) fixes each node ID and parameter value. Proposed future full phase: **200 passed,0 failed,0 errors,5 unchanged skips;205 total**. None of these new tests is written or run yet. The current proven phase remains148/0/5.

| Function | Cases | Required observable assertions |
| --- | ---: | --- |
| `test_ac11_manager_reads_only_selected_community` | 1 | Source AC11: A and B each have one Open request; M1 reading B returns exactly B request21. |
| `test_ac11_manager_reads_all_residents_in_selected_community` | 1 | Add a second resident request in A: manager sees both owners, and no B/C rows. |
| `test_ac11_assigned_empty_community_returns_empty_array` | 1 | M1 assigned to empty Birch4 receives200 []. |
| `test_ac11_switch_has_no_remembered_context` | 1 | M1 reads A, B, A; each exact array matches only the URL selection. |
| `test_ac11_interleaved_managers_stay_isolated` | 1 | Interleave M1(A/B) and M2(C) requests; allowed arrays exact, cross-assignment reads exact404. |
| `test_ac11_reject_invalid_caller` | 13 | Matched selected route returns exact401 Unknown user; no data. Superscript2 sent as raw Latin1 header bytes. |
| `test_ac11_unavailable_community_is_indistinguishable` | 13 | Known M1 receives exact404 Not found for every matched unavailable path; response contains no community/request details. |
| `test_ac11_identity_precedes_invalid_path` | 3 | Against path bad, callers None/9999/² each receive exact401, not404/422. |
| `test_ac11_nonmanager_cannot_read` | 3 | User104 with only the stated A role receives exact404; resident has valid unit11. |
| `test_ac11_known_unassigned_caller_denied` | 1 | Known103 without any memberships receives exact404 reading A. |
| `test_ac11_mixed_roles_do_not_grant_manager_access` | 1 | User106 managerA/residentB reads all A but is denied manager B; resident B route remains own-only. |
| `test_ac11_committed_removal_denies_later_read` | 1 | After successful options and A reads, commit deletion of M1/A membership; next request404 and next options omit A. |
| `test_ac11_committed_role_change_denies_later_read` | 3 | After successful A read commit role change; next manager read404 and option gone. Resident change uses unit11. |
| `test_ac11_new_assignment_authorizes_next_read` | 1 | Known103 denied A; commit managerA assignment; next read returns A without restart. |
| `test_ac11_unit_link_does_not_change_authority` | 1 | M1/A reads identical rows with valid unit11 and with null unit. |
| `test_ac11_public_fields_order_status_and_utc` | 1 | Exact seven-field dictionaries exclude submitted_by; include all three statuses; created_at desc then id desc including tie; non-UTC input renders UTC seconds. |
| `test_ac11_reads_preserve_application_tables` | 1 | Successful, empty and denied reads preserve exact snapshots of five application tables. |
| `test_ac11_resident_routes_remain_self_only` | 1 | Manager gains no resident list/details access; resident1 sees own A row, never resident3 row; no stored changes. |
| `test_ac11_membership_stable_through_validation` | 2 | Real concurrent delete or non-key board role update waits on API transaction during delegated row validation; first read may200, committed change makes next404. |
| `test_ac11_validation_failure_releases_transaction` | 1 | After proving route exists, inject row-validation failure: server500, not auth denial/empty list; subsequent FOR UPDATE NOWAIT succeeds, rows unchanged. |
| `test_ac11_database_failure_is_not_authorization_denial` | 1 | After proving route exists, inject connection OperationalError: server500, not401/404/200; restore fixture and successful read. |

Encode path values as URL path segments without trimming spaces or changing Unicode; send malformed headers as the exact listed raw bytes. Every ordinary read helper checks exact status/body, required no-store headers and snapshots of all five application tables. The failing-server cases assert500 rather than a fake authorization response, restore injected faults, and verify recovery. These fault injections exercise error handling only; they do not fabricate successful authorization, request rows or lock outcomes.

## Fixture and transaction-test plan

Use existing `client` reset first; additions stay in the new test file. Keep original shared fixtures and all153 existing expectations untouched. Reuse communities1/2, units11/12/21 and residents1/2/3. Add Elm3/unit31, empty Birch4/unit41, managers101 (1/2/4) and102 (3), known103 without assignments,104 for role cases,106 manager1/resident2-unit21, resident201 in3 and resident202 in2. Use valid composite foreign keys; manager101 submits no requests, so its membership can be removed safely.

Base requests11(A,resident1),21(B,resident2),31(C,resident201) are Open with fixed UTC times. Add resident3's A row and resident202's B row only where needed. The projection/order test supplies all stored statuses, two equal timestamps and an offset timestamp; expected UTC dictionaries are literal fixture-derived values, not built by the application serializer. Empty4 has an assignment but no requests. Restore all fixture changes per case through the shared reset.

Concurrency cases must first assert an ordinary route probe returns200, so the missing implementation fails semantically before any worker starts. Then delegate the real connection/validator through test-local wrappers: capture the API connection PID; seed at least two selected-community rows and hold the final expected row's real validation behind an Event; start a second real connection deleting membership or updating its non-key role to board_member. An observer must see the updater blocked by the captured API PID (for example `pg_blocking_pids`), and the updater must not have committed. Release validation, join both workers, verify the exact allowed first response, then commit/observe mutation and verify the next read404. Do not use sleeps as the sole oracle or mock the authorization query. Bounded waits and database statement/lock timeouts belong to the test connections; use `finally` to release Events, roll back/close connections and join workers. Fail rather than skip on an unobservable synchronization or leaked worker. Account for the one intentional membership mutation when comparing table snapshots; every other row remains identical.

Validation-failure case also probes200 first, then raises in a test-local wrapper after real validation has been reached. Use a TestClient configured to observe server500; after failure, a separate transaction's `FOR UPDATE NOWAIT` on that membership must succeed and snapshots stay unchanged. Connection-failure injection is separate, restored in `finally`, and followed by a valid read. No production-only test hook or new shared fixture is allowed.

## Allowed future files

| Path | Only change permitted by approval of this packet |
| --- | --- |
| `app/manager_requests.py` (new) | One router; identity/path checks via unchanged parser; parameterized membership lock/query; reuse existing response model; no blanket exception conversion |
| `app/main.py` | Import/register that router only; keep local guard, existing routers and health |
| `tests/test_s3_selected_requests.py` (new) | Exactly52 proposed cases, local fixture/instrumentation helpers; freeze actual tests-first hash before feature implementation |
| `scripts/verify_s3_ac11_baseline.py` (new) | Additive exact205-case verifier, freeze prior153 expectations/test hashes and new52 IDs/hash; adversarial self-tests |
| `.github/workflows/scaffold-baseline.yml` | Activate approved200/0/5 phase, preserve existing source/migration/artifact/cleanup controls and historical gates/self-tests |
| `docs/design/S-3-AC11-contract-addendum.md` (new) | Copy the actually approved proposal into an execution contract; do not rewrite original designs |
| `docs/evidence/s3-ac11/`, `docs/traceability/S-3-AC11.csv` (new) | Actual approval, undo point, red/green/CI/integrity evidence and supplemental API traceability |
| `AGENTS.md` | Append only the explicitly approved AC11 local-increment exception |
| `README.md`, `docs/plans/S-3-plan.md`, this packet, `docs/reviews/`, `prompts/`, `LEDGER.md`, AISE ledgers/state/stage artifacts | Accurate status and append-only provenance; no invented acceptance |

Protected: every existing test/fixture/manifest/verifier, options router, resident routes/models/serializer/parser, seed/settings/clock/payments, all existing designs, migrations, Docker/dependency inputs, M1 traceability, AISE framework/config/hooks and prior ledger bytes. Existing code does not need refactoring for this route. Stop if a protected change becomes necessary and present the correction to its owner.

## Execution and CI acceptance

1. Record Gustavo's explicit packet/addendum/52-test/CI approval plus Kundan and Sandeep's actual decisions. Prior AC12 closures do not satisfy these new reviews. Confirm PR15 integration, a clean base and unchanged assumptions.
2. Commit an undo checkpoint. Add52 cases first, collect exact IDs, run the complete suite and preserve real exit/JUnit. Some denial cases may initially return framework404; record actual failures and any unexpected passes instead of predicting52 red failures. No collection/setup errors, fabricated fail calls or new skips may stand in for missing behavior.
3. Freeze the new test file at its tests-first commit, then implement only the allowed route. Preserve the original153 expectations and every old test-file hash.
4. Add a new strict manifest and gate for exactly205 cases with200 passes, zero failures/errors and five exact S6 skips. Keep prior AC1/AC2/S1/AC12 scripts untouched and run them against their historical reports. The new verifier must recursively validate the prior AC12 manifest and old hashes; a valid control passes, and controls reject missing/extra/duplicate cases, failed/error suites, changed skip reasons, weak expectations, altered source manifests and changed/missing old/new test files. Use the same24 defect categories as the AC12 gate, adapted to the new manifest and tests, while retaining all historical gate self-tests. Keep actual pytest exit0 mandatory.
5. Run the full Docker suite, migration rehearsal, gate controls, protected-hash and append-only checks. Update Jira/AISE with actual results, open the implementation PR, and request result review. No automatic merge or subsequent feature approval.

No UI, login/MFA, invitation/assignment administration, tenant/board policy, status writes, payments, schema/dependency upgrade or production release. No sprint dates/capacity guessed. Production pagination/timeouts/SLOs remain future questions. Stop if concurrency evidence needs a flaky sleep-only test, a weakened contract or a new runtime dependency.

## Decision to record

Gustavo: approve/revise/reject **S3-AC11 packet v1, addendum,52 tests and additive CI phase**, after the named contract/test decisions and PR15 integration. Kundan: approve/revise/reject COMC-66. Sandeep: approve/revise/reject COMC-67. These are pending; planning does not create their answers. PR15 merge is a separate integration decision.
