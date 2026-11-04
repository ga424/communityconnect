# Verified tests-first baseline

Tested commit: `47d553957ec95bb5d6428ef34364862f37cfaf25`. Changes after this point only record evidence and normalize the traceability CSV; no application/test assertions changed.

| Check | Local fresh clone | GitHub Actions |
| --- | --- | --- |
| Liquibase update, repeat update, rollback one, reapply | Passed | Passed |
| Harness tests | 4 passed | 4 passed |
| S-1 AC-1..6 | 6 semantic failures on 501 stubs | 6 semantic failures on 501 stubs |
| S-6 AC-18..22 | 5 AC-labelled skips | 5 AC-labelled skips |
| Setup/collection errors | 0 | 0 |
| Pytest exit | 1 (expected red) | 1 (expected red) |
| Expected-red verifier | Passed | Passed |

[CI run 41775497234](https://github.com/ga424/communityconnect/actions/runs/41775497234) contains the complete remote output. Compact results and hashes: [validation.json](../evidence/bootstrap/validation.json), [local JUnit](../evidence/bootstrap/local-junit.xml), [CI JUnit](../evidence/bootstrap/ci-junit.xml).

The first local attempt could not write Docker Buildx state outside the workspace. After the user started Docker Desktop, migration execution succeeded; the build succeeded using `BUILDX_CONFIG=/tmp/communityconnect-buildx docker compose run --build --rm test`. This uses Docker’s [documented state-directory variable](https://docs.docker.com/build/building/variables/#buildx_config); no permissions or guardrails were disabled. Docker Engine reported 29.2.1.

Local collection also found all 15 tests. Python compile, pip check, Compose configuration, shell syntax and authored-source sensitive-data scan passed. The AISE structural validator passed with a warning on the initial evidence record's `summary`/missing `claim` field; later records use `claim`. This is not strict-release validation.

One Starlette warning remains: the installed TestClient deprecates httpx support. Sandeep should review the supported client migration before the next dependency update. No test failure was caused by this warning.

This is scaffold/test readiness evidence only. S-1 business behavior is still unimplemented; S-6 remains design/test-only. The S-6 fixture adapter is a proposed test-only contract and has no payment persistence implementation. Kundan/Sandeep review and AC-specific approval remain pending. A green expected-red CI job is not a completed story, QA approval, security assurance or submission finish line.
