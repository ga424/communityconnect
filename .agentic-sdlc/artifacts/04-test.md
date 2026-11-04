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
