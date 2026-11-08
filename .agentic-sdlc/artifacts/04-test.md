# Current AC11 execution checkpoint — November 8, 2026

Approved AC11 v1 is locally implemented:200 passes,zero failures/errors,five exact S6 skips.52 tests frozen before code at359f9e6a8a8633d95ac5fbc22d8746a5f9f529d6; prior153 expectations/test hashes preserved. Real lock/fault cases and24 gate controls pass. New router plus main registration only; no schema/dependency/resident changes. See docs/evidence/s3-ac11/README.md and docs/reviews/S3-AC11-implementation-2026-11-08.md. PR15/16 merged; prior branches cleaned. PR17 is open; implementation CI42536188957 verifies200/0/5 at 026a6c3bdc972a7cf26d6d56ffd336a30097e767. Human result review and implementation-PR merge remain pending. Final publication-head CI is linked in the PR/Jira/Git note. Older checkpoints below are historical, not current authority.

# Current AC11 tests-first checkpoint

Approved52 cases now executable and frozen:148 passed,52 missing-route failures,zero errors,5 existing skips;205 collected. Exact inventory verified; original153 strict gate and116 protected hashes pass. See docs/evidence/s3-ac11/tests-first.json. No application code changed yet. Current approved scope supersedes historical pending checkpoints below.

# Review-ticket status recheck — November 8, 2026

**Status recheck, November 8, 2026:** COMC-66 and COMC-67 are now Done, closed by Gustavo at 18:11:58 and 18:12:01 Eastern. Neither ticket has a review comment or attachment; no independent reviewer authorship is claimed. PR15 remains open. Separate approval of this AC11 packet and authorization to merge/integrate PR15 have not yet been recorded. The 52-case plan and executable files are unchanged. Earlier planning language below retains its original checkpoint; this update supersedes ticket-status wording only. [Evidence](../../docs/evidence/pr15-review/review-recheck-20261108.json).

---

# Current test state — PR15 review and AC11 proposal

EV-PR15-REVIEW-20261108 reverified148 passes, zero failures/errors and five exact skips at8f993ab from CI42529654327. [Proposed AC11 inventory](../../docs/plans/S-3-AC11-proposed-tests.json) defines52 future cases with R1–R4, exact error/field/state and real concurrency coverage. Target200/0/5 is not a result; no new executable tests or CI edits. COMC67 Sandeep specification approval is pending. Broader production/performance/security/accessibility tests remain excluded and unclaimed.

---

# Current scope — AC5 verification result, November 8, 2026

Gustavo explicitly approved PR8 merge/branch cleanup and AC5 packet v1 verification-only (EV-AC5-APPROVAL-20261108). PR8 is merged into fc208ec; PR7/PR8 branches are removed remotely/locally after checks (EV-PR8-MERGE-CLEANUP-20261108). Evidence-only checkpoint e615d78 preserves approved packet/ledger history and executable source identical to merged main.

EV-AC5-LOCAL-20261108: unchanged full suite120 passed / zero failures/errors / five exact S6 skips, real exit0; seven selected controls and all six original S1 cases pass. All107 protected hashes,24 gate defect controls, migration update/repeat/rollback/reapply and structural/source/whitespace checks pass. Dedicated test resources removed; running localhost preview and all previously running containers preserved. No application, test, design, migration, dependency or CI change. [Full evidence](../../docs/evidence/ac5/README.md).

PR10 CI EV-AC5-CI-42450409215 passed at77fe12f and its downloaded JUnit independently passed the unchanged120/0/5 gate with exit0. Bounded verification is ready for human result review. Kundan behavior, Sandeep QA/migrations and Gustavo provenance remain pending; prior merge/execution approvals are acknowledged and do not invent result acceptance. Separate AC3/full-story/course and broader production assurance remain pending; no next task or deployment authorized. Known historical warnings are retained. Earlier status text below is historical and superseded for this scope.

---

# Tests-first draft

Six S-1 tests assert AC-1..6 against HTTP outputs and synthetic PostgreSQL state. Five S-6 assertions cover AC-18..22 and are explicitly skipped; payments remain unbuilt. Four harness tests validate health, applied migration, membership relationship and resident-unit constraint.

EV-CI-41775497234: 4 passed / 6 failed / 5 skipped, zero setup/collection errors. The six failures are semantic 501 stub responses. Current S-1 assertions cover positive creation/status (R1), invalid description (R2), cross-community/direct-ID/same-community boundaries (R3/R4). Full design-edge-case coverage is pending; no comprehensive QA approval or security claim.

Sandeep must review the executable specification and proposed S-6 fixture API. Approve the test baseline before implementation. Tests must not be changed to make implementation green without the design/test defect process. Production behavior is unimplemented.

## Approved AC-1 contract-test baseline
Gustavo approved packet v1 and its contract-test/CI scope; EV-AC1-APPROVAL records the actual reply. tests/test_s1_contract.py adds 72 cases for existing design preconditions, validation order, no-write rejection, authorization, boundaries and ordering. EV-AC1-RED records their semantic red run before implementation. Existing tests are frozen in docs/evidence/ac1/protected-baseline.json; exact test IDs/outcomes and all test hashes for the approved incremental phase are in expected-tests.json. Full-story peer review remains pending.

## AC-1 local implementation result

Test-first commit `2b73ab0d5f21fb63e9b7c1406446c3cf7043682d` precedes implementation `15edff908305ffe51c7b7f7615bc22f87b4ef053`. All 72 contract cases now pass, with four harness passes and existing AC-1/2/3/5 passes; AC-4/6 remain 501 failures and five S-6 AC-labelled skips remain. Zero errors. Frozen manifest checks exact IDs and test-file hashes. Gate self-test rejects 11 defect types. See docs/evidence/ac1/local-summary.json and EV-AC1-LOCAL. Full-story QA and Sandeep peer review remain pending.

## AC-2 approved tests-first specification

Gustavo approved AC2 packet v1 including the representability policy, eight regression cases and the CI phase change (EV-AC2-APPROVAL). New tests/test_s1_validation.py collects eight cases; tests and all original 87 expectations are frozen in docs/evidence/ac2/expected-tests.json before application edits. Full red execution is pending at this checkpoint; do not infer its outcome or peer QA acceptance from collection. Original tests/designs/models/schema/controls are protected.

AC2 red execution completed before application edits: 84 passed, 6 failed, 5 skipped, zero errors. Four new cases fail semantically (three 500s and one wrong error precedence); four new controls pass. This resolves the earlier pending-execution checkpoint without claiming every new test was red. Evidence: EV-AC2-RED. New test hashes and all original expectations are frozen in docs/evidence/ac2/.

AC2 implemented result at `130af5d22bda7a98c4cff79e78904add49778b35`: all eight new cases pass, with full 88/2/5 phase and zero errors. Original test files/hashes and expectations preserved. Stage4 hash equals the implementation-time test hash. This supersedes the red checkpoint only for current outcomes; red evidence remains intact. Human QA acceptance is still pending.


## AC4 execution — November 7, 2026

AC4 approval EV-AC4-APPROVAL explicitly covers 30 new contracts and AC6 status. Test-first commit fb8db8046e3458a14d4c9edf04f019d3fcf7332e: 88 pass/32 semantic 501 failures/5 skips, zero errors (EV-AC4-RED). All original 95 outcomes unchanged. Frozen tests/manifest then passed locally at 120/0/5 (EV-AC4-LOCAL). 24 gate rejection controls and historical compatibility pass. Human test review pending; no original tests changed.
