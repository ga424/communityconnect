# CommunityConnect

A community management portal for residents, board members, community managers and administrators. Team GKMS: Kundan Singh, Sandeep Garg and Gustavo Abreu.

## Current increment

This branch prepares Milestone 1 through the AISE lifecycle. **No business feature is implemented yet.** S-1 maintenance requests is the first build target. S-6 simulated scheduled dues is design/test-only. All fixtures are synthetic; no real payments or production authentication are enabled.

See [feature order and owners](docs/features/README.md), [S-1 plan](docs/plans/S-1-plan.md), [S-1 design](docs/design/S-1.md), [S-6 design](docs/design/S-6.md) and [31-AC traceability](docs/traceability.csv). Designs, plans and tests still need team review. [Jira COMC](https://gkms.atlassian.net/jira/software/projects/COMC/boards/34/backlog) tracks that review separately from drafted artifacts.

## Install and run every test

Prerequisites: Git and a running Docker Engine with Docker Compose v2. No local Python/PostgreSQL/Java installation is needed for the container path.

```bash
git clone https://github.com/ga424/communityconnect.git
cd communityconnect
git checkout feature/COMC-38-m1-aise-bootstrap
docker compose run --build --rm test
```

The last line is the **one command for all tests**: it starts disposable PostgreSQL, applies Liquibase migrations, builds the Python 3.12 test image and runs pytest. Test fixture credentials in Compose are public, local-only examples; no database port is published. Tests clear only the dedicated `cc_test` database. Do not point this scaffold at shared data.

Current expected result: **4 harness passes, 6 S-1 failures, 5 S-6 skips**. S-1 calls intentionally return 501 until bounded implementation is approved; S-6 skip reasons name AC-18 through AC-22. A collection/setup failure is not an acceptable red baseline. See [baseline evidence](docs/aise/test-baseline.md) for actual execution results. The CI baseline gate validates these counts; its success is not feature completion. Replace that gate with S-1-green expectations only through reviewed baseline promotion, not to hide failing tests.

```bash
# Collect test names; starts the same database/migration prerequisites.
docker compose run --build --rm test python -m pytest --collect-only -q
# Rehearse update, repeat update, rollback and reapply on disposable cc_test.
bash scripts/migration_rehearsal.sh
# Remove this project's disposable test services when finished.
docker compose down --volumes --remove-orphans
```

`artifacts/` holds test output and JUnit results and is not committed. CI uploads its real results. The authoring machine lacks a Docker engine; local fresh-clone execution remains a Sandeep review task even if remote CI passes.

## Work by feature with AISE

1. Read [AGENTS.md](AGENTS.md), the feature packet and `.agentic-sdlc/state/pipeline-state.json`.
2. Show a bounded AC plan, allowed/protected files and stop condition; record human approval before implementation.
3. Commit an undo point. Implement that task, preserve approved tests, inspect diff/logs/edge cases, and run tests.
4. Record actual prompts, checks, review decisions and SHAs in [LEDGER.md](LEDGER.md) and AISE ledgers. Open a feature PR and link its Jira task. Do not merge or deploy implicitly.

The [pinned AISE source](docs/aise/FRAMEWORK.md) includes its deterministic validator and sensitive-data guard. Run `python .agentic-sdlc/hooks/validate_project.py --workspace .agentic-sdlc` for structural checks. Passing that check does not approve a lifecycle stage. No automatic production deploy exists.

## Boundaries and remaining work

- Kundan: approve S-1 design/plan, then implement COMC-54 through COMC-59 with independent review.
- Sandeep: review fixtures/migration recovery, both test specifications and fresh-clone execution.
- Gustavo: maintain provenance/traceability and coordinate integration and peer review.

Production identity/MFA, UI/Playwright, provider integrations, security/dependency assurance and deployment remain later work. PostgreSQL and Python image tags need immutable release pinning and dependency/security review before release. This initial workflow only checks scaffold integrity and the expected red baseline.

Private interviews, participant identities, consent/recording files and credentials are excluded from this public repository. Team contribution signatures and final submission are not fabricated by automation.
