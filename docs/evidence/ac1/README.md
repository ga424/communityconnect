# AC-1 execution evidence — November 4, 2026

Gustavo approved packet v1, including contract tests and the CI transition. The exact authorization is in [the prompt record](../../../prompts/2026-11-04-ac1-approval.txt). The historical packet at `8ea0e80759ae06dc80cf5bf4bfa5666313074378` is the pre-test undo point; PR #3 contains that packet and is preserved as an ancestor of this implementation branch. No merge was performed.

## Reproducible result

Run `docker compose run --build --rm test`, then `python scripts/verify_ac1_baseline.py`. Pytest exits **1** because the details endpoint remains deferred. The phase verifier exits **0** only for this exact result:

| Group | Actual outcome |
| --- | --- |
| New contract tests | 72 passed |
| Existing harness | 4 passed |
| Existing S-1 AC-1, AC-2, AC-3, AC-5 | 4 passed |
| Existing S-1 AC-4, AC-6 | 2 assertion failures from the unchanged 501 details stub |
| S-6 AC-18–AC-22 | 5 unchanged, AC-labelled skips |
| Collection/setup/runtime errors | 0 |

The tests were committed **before application edits** at `2b73ab0d5f21fb63e9b7c1406446c3cf7043682d`. Their real [red summary](red-summary.json) and [JUnit](red-junit.xml) show all 72 new cases failing semantically against the stubs, alongside the 6 existing S-1 failures. The [local result](local-summary.json) and [JUnit](local-junit.xml) record the implemented phase. Existing tests, design, migrations, controls, settings and clock match [14 protected hashes](protected-baseline.json).

`python scripts/verify_ac1_baseline.py --self-test` accepted a valid report and rejected 11 defect types, including missing tests, setup/collection errors, unexpected failures and extra skips. [Results](gate-self-test.json) are separate from the actual application run. [The fixed manifest](expected-tests.json) was frozen in the red-test commit; the gate does not regenerate expectations from passing output.

Liquibase update, repeat update, rollback and reapply all succeeded: [migration output](migration-output.txt). AISE structural validation passed with the previously documented historical EV-REPO-ROOT missing-claim warning. The sensitive-data guard, Compose validation and `git diff --check` passed. These are bounded prototype checks, not a full security assessment.

## Review focus

| File | Implementation and review evidence |
| --- | --- |
| app/requests.py | Caller then resident membership, then strict Pydantic shape, description and category validation. Raw JSON parsing is deferred until authorization. Exact error envelopes; public-only DTO with UTC timestamps. POST offloads synchronous DB work to a worker thread. Details route is unchanged. |
| app/models.py | All input values are SQL parameters. One transaction covers membership checks and one insert; membership row is held with FOR SHARE. The unit comes from membership. List filters by both community and submitting user and sorts date/ID descending. Existing local DB guard is retained. |
| tests/test_s1_contract.py | Frozen tests cover rejection without writes, precedence, malformed/out-of-range IDs, nonresident roles, strict bodies, Unicode/length/trim boundaries, category case, same-unit isolation and deterministic order. |
| scripts/verify_ac1_baseline.py | Exact full IDs and frozen file hashes; rejects changed/missing/extra outcomes and failures other than the two specific 501 assertions. |
| .github/workflows/scaffold-baseline.yml | AC-1 phase gate; original read-only permissions, pinned actions, migration rehearsal, scan, real pytest exit, uploads and cleanup retained. |

Codex inspected the diff, SQL parameters, transaction boundaries, error paths, logs and protected-file hashes. No application logging of request bodies, headers or credentials was introduced. This is AI self-review; Kundan/Sandeep/Gustavo peer acceptance has not been invented.

## Remaining work

Human implementation review is pending. AC-2/3/5 pass because their guards are prerequisites for a safe first write; their individual review tasks remain open. AC-4/6 and all S-6 behavior are not implemented. Full-story design/gap review, course provenance reconciliation and final all-S-1-green fresh-clone verification remain pending. No provider integration, migration, dependency change, merge or deployment is included. The known Starlette TestClient deprecation warning remains for a separately scoped dependency review.

The exact recording/result SHAs and eventual CI/PR links are reconciled in AISE ledgers, Jira and append-only `refs/notes/ai-provenance`. Remote CI evidence is only recorded after an actual run.
