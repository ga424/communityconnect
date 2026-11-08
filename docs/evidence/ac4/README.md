# AC-4 execution — resident request details and AC-6 status

Gustavo explicitly approved the corrected packet v1, 30 contract tests, AC-6 status coverage and CI phase change. [Actual approval](../../../prompts/2026-11-07-ac4-approval.txt); [execution boundary](../../../prompts/2026-11-07-ac4-execution.txt). Kundan reviews implementation, Sandeep tests/gate evidence, Gustavo provenance. Scope approval is not independent teammate acceptance.

## Result

The existing GET `/requests/{request_id}` now validates the caller first, then reads only a request submitted by that caller with current resident membership in its community. It returns the existing seven public fields, including persisted status. Unknown caller: exact 401. Missing/malformed/unauthorized ID: identical 404. Reads do not change persisted requests. No status-write endpoint, schema/dependency change or new access policy.

Local Docker result: **120 passed, zero failures/errors, five unchanged S-6 skips; pytest exit 0**. All six original S-1 acceptance tests and all 30 new contracts pass. [Local summary](local-summary.json); [JUnit](local-junit.xml); [migration log](migration-output.txt). [GitHub CI run 42419977346](https://github.com/ga424/communityconnect/actions/runs/42419977346) passed at implementation commit `8df963e73801713e3eb6c9b02e7d6ce8092f14f7`, also 120/0/5 with pytest exit 0. Downloaded JUnit independently passed the exact gate. [CI summary](ci-summary.json); [CI JUnit](ci-junit.xml). [PR8](https://github.com/ga424/communityconnect/pull/8) is open for review; it was opened by ga424 and updated with the evidence after the connector reported an existing PR.

## Test-first evidence

- Pre-test undo: `62b9df05338fe44a86747197502e088fa0cf45b5`, preserving PR7's approved packet/evidence history. Fresh feature branch was created from main `c0b26c34a1514631ec0825633e25473b570feb05` and fast-forwarded to this checkpoint; PR7 remains open.
- Red test commit: `fb8db8046e3458a14d4c9edf04f019d3fcf7332e`. Exactly **88 pass / 32 fail / 5 skip**, zero errors, exit 1. All 30 new failures assert the stub's 501 instead of the contract result. The two original AC4/AC6 failures remain; original 95 outcomes independently reverified. [Red summary](red-summary.json); [red JUnit](red-junit.xml).
- [Frozen manifest](expected-tests.json) and new test file are unchanged since the red commit. [80 protected source hashes](protected-baseline.json) match. Existing tests/helpers, historical manifests/evidence/verifiers, design, migrations, dependencies and controls remain unchanged. Unrelated application definitions match by AST comparison.

## CI contract

The new `verify_s1_baseline.py` requires all 125 exact IDs, 120 passes and the five exact S-6 skips. Only the original AC4/AC6 expectations are promoted; all other original expectations/hashes remain fixed. It rejects actual red output and [24 report/manifest mutations](gate-self-test.json). Historical AC1/AC2 reports and self-tests still pass their untouched verifiers ([AC1](ac1-compatibility.json), [AC2](ac2-compatibility.json)).

CI requires actual pytest exit 0 and keeps read-only permissions, pinned Actions, migration rehearsal, artifact capture and cleanup. The new gate passes only a validated manifest into the existing shared verifier, using Counter-style counts without a zero-valued failure key. This preserves historical verifier code/defaults while enforcing zero failures for this approved phase.

## Review limits

Liquibase update/repeat/rollback/reapply, structural/source checks, Compose validation, Python parsing and whitespace checks passed. The existing TestClient deprecation and historical EV-REPO-ROOT warning remain. No new material defect was found in the bounded AI self-review. Human full-story design/test acceptance, separate AC3/AC5 task review, course provenance, production identity/security/NFR assurance and S-6 remain pending. X-User-Id is a synthetic test selector; the suite is not a production security certification.

No merge/deployment or next-task implementation is authorized. Keep open branches until merge; automatic branch deletion remains enabled. Exact recording SHAs and final CI provenance use append-only Git notes under `refs/notes/ai-provenance` to avoid self-referential evidence commits.
