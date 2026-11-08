# CommunityConnect

A community management portal for residents, board members, community managers and administrators. Team GKMS: Kundan Singh, Sandeep Garg and Gustavo Abreu.

## Current increment

This branch prepares Milestone 1 through the AISE lifecycle. **AC-1 creation/self-listing and AC-2 validation are merged. The approved AC-4 request-details implementation, including AC-6 persisted status, is ready for review.** Residents can retrieve only their own requests in a community where they hold resident membership. Unknown callers receive 401; missing, malformed and unauthorized request IDs share the same 404 envelope. [Actual approval](prompts/2026-11-07-ac4-approval.txt) supersedes historical pending wording in the [packet](docs/plans/AC-4-approval.md). [Execution evidence](docs/evidence/ac4/README.md) records test-first red/green checks. All current S-1 acceptance tests pass; human full-story acceptance remains pending. S-6 is design/test-only. Fixtures are synthetic; no real payments or production authentication are enabled.

See [feature order and owners](docs/features/README.md), [S-1 plan](docs/plans/S-1-plan.md), [S-1 design](docs/design/S-1.md), [S-6 design](docs/design/S-6.md) and [31-AC traceability](docs/traceability.csv). Designs, plans and tests still need team review. [Jira COMC](https://gkms.atlassian.net/jira/software/projects/COMC/boards/34/backlog) tracks that review separately from drafted artifacts.

## Latest review and next decision

[PR8 bounded review](docs/reviews/PR-8-and-AC-5-2026-11-07.md) reverified final-head CI (120/0/5) and found no blocking code defect. PR8 remains open; GitHub records an approval from abreugus, while named teammate acceptance remains pending. The next proposed task is [AC-5 packet v1](docs/plans/AC-5-approval.md): verification-only after integration, preserving all code, tests and CI. No AC5 execution approval is recorded. Automatic branch deletion is enabled; unmerged branches are retained.

## Install and run every test

Prerequisites: Git and a running Docker Engine with Docker Compose v2. No local Python/PostgreSQL/Java installation is needed for the container path.

```bash
git clone https://github.com/ga424/communityconnect.git
cd communityconnect
docker compose run --build --rm test
```

The last line is the **one command for all tests**: it starts disposable PostgreSQL, applies Liquibase migrations, builds the Python 3.12 test image and runs pytest. Test fixture credentials in Compose are public, local-only examples; no database port is published. Tests clear only the dedicated `cc_test` database. Do not point this scaffold at shared data.

Current expected result: **120 passes, zero failures, five S-6 skips** (125 cases, pytest exit 0). The passes comprise 30 AC-4 details contracts, 8 AC-2 regressions, 72 AC-1 contracts, 4 harness cases and all six original S-1 acceptance tests. S-6 retains its exact AC-18 through AC-22 skip reasons.

The approved S-1 gate preserves all 95 prior test IDs and hashes, promotes only the original AC4/AC6 outcomes, and requires the 30 approved additions. It rejects missing/duplicate/extra cases, any failures/errors, changed skips and modified test hashes. Passing is evidence for review of the local prototype; it does not establish production readiness or teammate acceptance. Historical [AC1](docs/evidence/ac1/README.md) and [AC2](docs/evidence/ac2/README.md) manifests/verifiers remain unchanged.

```bash
python scripts/verify_s1_baseline.py
python scripts/verify_s1_baseline.py --self-test
# Backward compatibility of historical phases:
python scripts/verify_ac1_baseline.py --junit docs/evidence/ac1/local-junit.xml
python scripts/verify_ac2_baseline.py --junit docs/evidence/ac2/local-junit.xml
```

```bash
# Collect test names; starts the same database/migration prerequisites.
docker compose run --build --rm test python -m pytest --collect-only -q
# Rehearse update, repeat update, rollback and reapply on disposable cc_test.
bash scripts/migration_rehearsal.sh
# Remove this project's disposable test services when finished.
docker compose down --volumes --remove-orphans
```

`artifacts/` holds test output and JUnit results and is not committed. CI uploads its real results. Docker Desktop was started during this session. Historical bootstrap runs are documented separately; the current S-1 run must match the phase above. Sandeep’s human review remains pending. If a sandbox cannot write Buildx state under the home directory, set `BUILDX_CONFIG` to a writable temporary directory; the test command is otherwise unchanged.

## Work by feature with AISE

1. Read [AGENTS.md](AGENTS.md), the feature packet and `.agentic-sdlc/state/pipeline-state.json`.
2. Show a bounded AC plan, allowed/protected files and stop condition; record human approval before implementation.
3. Commit an undo point. Implement that task, preserve approved tests, inspect diff/logs/edge cases, and run tests.
4. Record actual prompts, checks, review decisions and SHAs in [LEDGER.md](LEDGER.md) and AISE ledgers. Open a feature PR and link its Jira task. Do not merge or deploy implicitly.

The [pinned AISE source](docs/aise/FRAMEWORK.md) includes its deterministic validator and sensitive-data guard. Run `python .agentic-sdlc/hooks/validate_project.py --workspace .agentic-sdlc` for structural checks. Passing that check does not approve a lifecycle stage. No automatic production deploy exists.

## Boundaries and remaining work

- Kundan: review AC-4 implementation and remaining S-1 design/gap work; COMC-56/58 retain separate verification/acceptance and COMC-59 tracks the approved AC-6 read-only overlap.
- Sandeep: review fixtures/migration recovery, both test specifications and fresh-clone execution.
- Gustavo: maintain provenance/traceability and coordinate integration and peer review.

Production identity/MFA, UI/Playwright, provider integrations, security/dependency assurance and deployment remain later work. PostgreSQL and Python image tags need immutable release pinning and dependency/security review before release. This workflow checks migrations, AISE structure, the sensitive-data guard and the approved S-1 contract phase; it is not a production security assessment.

Private interviews, participant identities, consent/recording files and credentials are excluded from this public repository. Team contribution signatures and final submission are not fabricated by automation.

Merged feature branches are deleted after merge; GitHub automatic branch deletion is enabled. Start each new task on a fresh branch from main. Gustavo approved [packet v1](docs/plans/AC-1-approval.md); the historical packet’s pending status is superseded by the [actual approval record](prompts/2026-11-04-ac1-approval.txt). PR #4 is merged and its branch was deleted remotely and locally. Gustavo also approved [AC-2 packet v1](docs/plans/AC-2-approval.md), including the addendum, eight tests and CI change; the [actual approval](prompts/2026-11-04-ac2-approval.txt) supersedes historical pending wording in the packet/plan. AC-2 is merged; full-story human review remains open. Gustavo approved AC-4 packet v1 with 30 tests, AC-6 status coverage and CI promotion; that actual approval is recorded above. No automatic merge, deployment or further task implementation is authorized.
