# AC-2 execution evidence — November 4, 2026

Gustavo approved packet v1, its text-policy addendum, eight regression cases and CI change. [Exact approval](../../../prompts/2026-11-04-ac2-approval.txt); [binding addendum](../../design/S-1-AC2-validation-addendum.md). Approved packet commit `73842903bc1f1388324c0c3e5766cec5d7fa833d` is the pre-test undo point. PR5 was still open when work started; its approved history is preserved in the feature branch. No merge to main was performed by this task.

## Test-first evidence

Test/addendum baseline `661a205dbfb4860d14194e54d75b46edec54cdca` was committed **before application edits**. [Actual red result](red-summary.json): **84 passed, 6 failed, 5 skipped**, zero errors, 95 cases. Three new cases reproduced HTTP 500 instead of 422 and one reproduced the wrong error precedence. Four new controls already passed; they were not artificially made red. The two existing AC4/6 failures remained deferred. [Red JUnit](red-junit.xml).

## Implemented result

Run `docker compose run --build --rm test`, then `python scripts/verify_ac2_baseline.py`:

| Group | Actual local result |
| --- | --- |
| Eight AC2 regression cases | 8 passed |
| Original AC1 contract cases | 72 passed |
| Harness | 4 passed |
| Original AC1/2/3/5 cases | 4 passed |
| AC4/6 details route | 2 unchanged 501 assertion failures |
| S6 AC18–22 | 5 exact skips |
| Collection/setup/runtime errors | 0 |

Total **88 passed, 2 deferred failures, 5 skipped**, pytest exit **1**, phase-gate exit **0**. [Local summary](local-summary.json) and [JUnit](local-junit.xml) preserve actual outcomes. F1 is remediated in the local implementation: NUL and unpaired-surrogate description text is rejected before insertion; the tests prove seeded rows/lists remain unchanged. Valid accented/emoji text is preserved. Human implementation review remains pending.

The application diff is only the four-line representability guard after blank/length checks and before category validation. No broad DB exception handler or sanitization was added. Caller/access rules, model helpers and transaction boundaries are unchanged. The details stub is unchanged. All [40 protected file hashes](protected-baseline.json) and the new test-file hash match the committed baseline.

## CI gate and migration proof

The fixed [95-case manifest](expected-tests.json) preserves all original 87 expectations and hashes and adds only the eight named passing cases. The AC1 verifier exposes only a reusable phase-count parameter, retaining its 80/2/5 default and CLI behavior. The new AC2 wrapper fixes 88/2/5, validates the protected AC1 manifest hash, checks the exact extension and verifies each test outcome/hash.

[Gate self-test](gate-self-test.json) accepted valid controls and rejected 11 shared defects plus seven AC2 extension/manifest defects, including missing original/new tests, errors, unexpected failures/skips and modified expectations/hashes. [Historical AC1 compatibility self-test](ac1-compatibility-self-test.json) and `python scripts/verify_ac1_baseline.py --junit docs/evidence/ac1/local-junit.xml` passed. The old gate is intentionally for its old report; the new gate checks the full current suite.

Liquibase update, repeat update, rollback and reapply succeeded with unchanged migrations: [output](migration-output.txt). AISE structural validation, the source-sensitive-data guard, Compose validation and whitespace checks passed. Existing historical ledger and TestClient warnings remain documented; no broad dependency/security assessment is claimed. Workflow read-only permissions, pinned actions, artifact capture, real pytest exit and cleanup are retained. Remote CI is recorded only after an actual run.

## Review boundary

Codex reviewed text-policy placement, Unicode range checks, no-write assertions, source/test hashes, manifest preservation and verifier negative controls. This is AI self-review, not teammate acceptance. Kundan reviews implementation; Sandeep reviews tests/gates; Gustavo reviews provenance/integration. Original designs, tests, AC1 evidence, models, dependencies, schema and controls are unchanged. No next task, merge, deployment, production identity or payments are authorized.

Exact implementation/delivery SHAs and eventual CI/PR links are reconciled through AISE ledgers, Jira and append-only `refs/notes/ai-provenance`. Full S1 and final all-S1-green verification remain pending.
