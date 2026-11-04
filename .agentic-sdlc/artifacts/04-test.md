# Tests-first draft

Six S-1 tests assert AC-1..6 against HTTP outputs and synthetic PostgreSQL state. Five S-6 assertions cover AC-18..22 and are explicitly skipped; payments remain unbuilt. Four harness tests validate health, applied migration, membership relationship and resident-unit constraint.

EV-CI-41775497234: 4 passed / 6 failed / 5 skipped, zero setup/collection errors. The six failures are semantic 501 stub responses. Current S-1 assertions cover positive creation/status (R1), invalid description (R2), cross-community/direct-ID/same-community boundaries (R3/R4). Full design-edge-case coverage is pending; no comprehensive QA approval or security claim.

Sandeep must review the executable specification and proposed S-6 fixture API. Approve the test baseline before implementation. Tests must not be changed to make implementation green without the design/test defect process. Production behavior is unimplemented.

## Approved AC-1 contract-test baseline
Gustavo approved packet v1 and its contract-test/CI scope; EV-AC1-APPROVAL records the actual reply. tests/test_s1_contract.py adds 72 cases for existing design preconditions, validation order, no-write rejection, authorization, boundaries and ordering. EV-AC1-RED records their semantic red run before implementation. Existing tests are frozen in docs/evidence/ac1/protected-baseline.json; exact test IDs/outcomes and all test hashes for the approved incremental phase are in expected-tests.json. Full-story peer review remains pending.
