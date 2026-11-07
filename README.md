# CommunityConnect

A community management portal for residents, board members, community managers and administrators. Team GKMS: Kundan Singh, Sandeep Garg and Gustavo Abreu.

## Current increment

This branch prepares Milestone 1 through the AISE lifecycle. **AC-1 creation/self-listing and the AC-2 validation fix are merged.** Unsupported NUL/surrogate description text returns a controlled 422; valid Unicode and validation precedence are preserved. AC-3 cross-community list isolation was [verified without a code change](docs/evidence/ac3/README.md) on merged main. The [next proposed packet is AC-4 request details](docs/plans/AC-4-approval.md); it awaits explicit approval. The details route remains a 501 stub; S-1 is incomplete. S-6 simulated scheduled dues is design/test-only. All fixtures are synthetic; no real payments or production authentication are enabled.

See [feature order and owners](docs/features/README.md), [S-1 plan](docs/plans/S-1-plan.md), [S-1 design](docs/design/S-1.md), [S-6 design](docs/design/S-6.md) and [31-AC traceability](docs/traceability.csv). Designs, plans and tests still need team review. [Jira COMC](https://gkms.atlassian.net/jira/software/projects/COMC/boards/34/backlog) tracks that review separately from drafted artifacts.

## Install and run every test

Prerequisites: Git and a running Docker Engine with Docker Compose v2. No local Python/PostgreSQL/Java installation is needed for the container path.

```bash
git clone https://github.com/ga424/communityconnect.git
cd communityconnect
docker compose run --build --rm test
```

The last line is the **one command for all tests**: it starts disposable PostgreSQL, applies Liquibase migrations, builds the Python 3.12 test image and runs pytest. Test fixture credentials in Compose are public, local-only examples; no database port is published. Tests clear only the dedicated `cc_test` database. Do not point this scaffold at shared data.

Current expected result: **88 passes, 2 deferred S-1 failures, 5 S-6 skips** (95 cases, pytest exit 1). The passes comprise 8 AC-2 regression cases, 72 AC-1 contract cases, 4 harness cases and existing AC-1/2/3/5. AC-4 and AC-6 still fail on the unchanged details stub. S-6 retains its exact AC-18 through AC-22 skip reasons.

The approved AC-2 CI gate preserves all original 87 expectations and requires exactly eight approved new passes. It checks exact test IDs, outcomes and frozen test-file hashes; it rejects missing/duplicate tests, setup errors, unexpected failures and added/changed skips. Its success means this bounded increment is ready for review, not that S-1 is complete. Existing tests and the original [red baseline evidence](docs/aise/test-baseline.md) remain unchanged. See [AC-2 execution evidence](docs/evidence/ac2/README.md) for current results and [AC-1 evidence](docs/evidence/ac1/README.md) for the historical phase. The AC-1 verifier retains its 80/2/5 default and still validates its original report.

```bash
python scripts/verify_ac2_baseline.py
python scripts/verify_ac2_baseline.py --self-test
# Backward compatibility of the historical phase:
python scripts/verify_ac1_baseline.py --junit docs/evidence/ac1/local-junit.xml
```

```bash
# Collect test names; starts the same database/migration prerequisites.
docker compose run --build --rm test python -m pytest --collect-only -q
# Rehearse update, repeat update, rollback and reapply on disposable cc_test.
bash scripts/migration_rehearsal.sh
# Remove this project's disposable test services when finished.
docker compose down --volumes --remove-orphans
```

`artifacts/` holds test output and JUnit results and is not committed. CI uploads its real results. Docker Desktop was started during this session. Historical bootstrap runs are documented separately; the current AC-2 run must match the phase above. Sandeep’s human review remains pending. If a sandbox cannot write Buildx state under the home directory, set `BUILDX_CONFIG` to a writable temporary directory; the test command is otherwise unchanged.

## Work by feature with AISE

1. Read [AGENTS.md](AGENTS.md), the feature packet and `.agentic-sdlc/state/pipeline-state.json`.
2. Show a bounded AC plan, allowed/protected files and stop condition; record human approval before implementation.
3. Commit an undo point. Implement that task, preserve approved tests, inspect diff/logs/edge cases, and run tests.
4. Record actual prompts, checks, review decisions and SHAs in [LEDGER.md](LEDGER.md) and AISE ledgers. Open a feature PR and link its Jira task. Do not merge or deploy implicitly.

The [pinned AISE source](docs/aise/FRAMEWORK.md) includes its deterministic validator and sensitive-data guard. Run `python .agentic-sdlc/hooks/validate_project.py --workspace .agentic-sdlc` for structural checks. Passing that check does not approve a lifecycle stage. No automatic production deploy exists.

## Boundaries and remaining work

- Kundan: review the AC-2 validation implementation and remaining S-1 design/gap work; COMC-56 through COMC-59 retain separate task approval/review.
- Sandeep: review fixtures/migration recovery, both test specifications and fresh-clone execution.
- Gustavo: maintain provenance/traceability and coordinate integration and peer review.

Production identity/MFA, UI/Playwright, provider integrations, security/dependency assurance and deployment remain later work. PostgreSQL and Python image tags need immutable release pinning and dependency/security review before release. This workflow checks migrations, AISE structure, the sensitive-data guard and the approved AC-2 validation phase; it is not a production security assessment.

Private interviews, participant identities, consent/recording files and credentials are excluded from this public repository. Team contribution signatures and final submission are not fabricated by automation.

Merged feature branches are deleted after merge; GitHub automatic branch deletion is enabled. Start each new task on a fresh branch from main. Gustavo approved [packet v1](docs/plans/AC-1-approval.md); the historical packet’s pending status is superseded by the [actual approval record](prompts/2026-11-04-ac1-approval.txt). PR #4 is merged and its branch was deleted remotely and locally. Gustavo also approved [AC-2 packet v1](docs/plans/AC-2-approval.md), including the addendum, eight tests and CI change; the [actual approval](prompts/2026-11-04-ac2-approval.txt) supersedes historical pending wording in the packet/plan. AC-2 is awaiting human implementation review; no automatic merge or next-task implementation is authorized.
