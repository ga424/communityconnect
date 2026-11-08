# CommunityConnect

A community management portal for residents, board members, community managers and administrators. Team GKMS: Kundan Singh, Sandeep Garg and Gustavo Abreu.

## Current increment

M1's S1 resident request creation, validation, self-listing and details are merged. This branch adds the approved later-product **S3-AC12 community-options API**: `GET /manager/communities` returns only the caller's current manager assignments, sorted by community ID, with exactly id/name fields. Known callers without manager assignments receive an empty array; missing/invalid/unknown callers receive401. A valid unit link does not change manager authority. All reads preserve stored data and existing resident access behavior.

Local verification passed **148 tests, zero failures/errors and five planned S6 skips**. The28 new cases were committed before implementation; their actual red baseline had28 missing-route failures and all120 previous passes. [Execution evidence](docs/evidence/s3-ac12/README.md), [approved packet](docs/plans/S-3-AC12-approval.md), [addendum](docs/design/S-3-AC12-contract-addendum.md) and [supplemental traceability](docs/traceability/S-3-AC12.csv) describe this bounded API increment. It is not merged yet. Selected-community request reads (AC11), browser selector, production login/MFA and assignment administration remain future work.

Gustavo approved scope and confirmed the two review tickets completed; Jira attributes their closures to him. Independently authored teammate sign-offs were not supplied. Result review and merge remain separate; no production release is authorized. Fixtures are synthetic, the identity header is local/test-only, and S6 payments remain intentionally unbuilt.

## Milestone and review context

M1's original [31-AC traceability](docs/traceability.csv) remains unchanged. Gustavo accepted bounded S1 behavior (COMC42); named/full-story/course reviews, contributions and submission receipts are tracked separately in the [work queue](docs/reviews/Gustavo-work-queue-status-2026-11-08.md). Historical [S1 evidence](docs/evidence/s1-closeout/summary.json) records120 passes plus5 skips before this later increment. The [S3 sequence](docs/plans/S-3-plan.md) keeps API, browser and full-story acceptance distinct. The separate localhost review wrapper is outside the product UI and is not started by tests.

## Install and run every test

Prerequisites: Git and a running Docker Engine with Docker Compose v2. No local Python/PostgreSQL/Java installation is needed for the container path.

```bash
git clone https://github.com/ga424/communityconnect.git
cd communityconnect
docker compose run --build --rm test
```

The last line is the **one command for all tests**: it starts disposable PostgreSQL, applies Liquibase migrations, builds the Python 3.12 test image and runs pytest. Test fixture credentials in Compose are public, local-only examples; no database port is published. Tests clear only the dedicated `cc_test` database. Do not point this scaffold at shared data.

Current expected result: **148 passes, zero failures/errors, five exact S6 skips** (153 cases, pytest exit0): the original120 passing S1/harness cases plus28 AC12 contracts. S6 retains its AC18–AC22 skip reasons.

The new gate requires exactly the frozen125 original expectations plus28 new passes, matching original file hashes and the tests-first AC12 hash. It rejects missing/duplicate/extra cases, failures/errors, changed skips and altered manifests/files. The24 adversarial controls exercise the new gate; historical gates remain unchanged and run against their historical reports.

```bash
python scripts/verify_s3_ac12_baseline.py
python scripts/verify_s3_ac12_baseline.py --self-test
# Compatibility checks use historical results, not the expanded current report:
python scripts/verify_s1_baseline.py --junit docs/evidence/s1-closeout/fresh-clone-junit.xml
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

`artifacts/` holds test output and JUnit results and is not committed. CI uploads its real results. Docker Desktop was started during this session. Historical bootstrap runs are documented separately; the current full run must match the phase above. Sandeep’s human review remains pending. If a sandbox cannot write Buildx state under the home directory, set `BUILDX_CONFIG` to a writable temporary directory; the test command is otherwise unchanged.

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

Production identity/MFA, UI/Playwright, provider integrations, security/dependency assurance and deployment remain later work. PostgreSQL and Python image tags need immutable release pinning and dependency/security review before release. This workflow checks migrations, AISE structure, the sensitive-data guard and the approved S-1 plus S3-AC12 contract phase; it is not a production security assessment.

Private interviews, participant identities, consent/recording files and credentials are excluded from this public repository. Team contribution signatures and final submission are not fabricated by automation.

Merged feature branches are deleted after merge; GitHub automatic branch deletion is enabled. Start each new task on a fresh branch from main. Gustavo approved [packet v1](docs/plans/AC-1-approval.md); the historical packet’s pending status is superseded by the [actual approval record](prompts/2026-11-04-ac1-approval.txt). PR #4 is merged and its branch was deleted remotely and locally. Gustavo also approved [AC-2 packet v1](docs/plans/AC-2-approval.md), including the addendum, eight tests and CI change; the [actual approval](prompts/2026-11-04-ac2-approval.txt) supersedes historical pending wording in the packet/plan. AC-2 is merged; full-story human review remains open. Gustavo approved AC-4 packet v1 with 30 tests, AC-6 status coverage and CI promotion; that actual approval is recorded above. No automatic merge, deployment or further task implementation is authorized.
