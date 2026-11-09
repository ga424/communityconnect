# CommunityConnect

A community management portal for residents, board members, community managers and administrators. Team GKMS: Kundan Singh, Sandeep Garg and Gustavo Abreu.

## Current increment

S1 resident request creation, validation, self-listing and details are merged. S3-AC12 manager community options are merged in PR15, along with the AC11 preparation packet in PR16. The approved **S3-AC11 selected-community requests API** is also merged and available: `GET /manager/communities/{community_id}/requests` returns all residents' requests in exactly one currently assigned community, with seven public fields ordered by created_at then ID descending.

Each read checks current manager membership and holds it stable through response validation. Invalid/unknown callers receive401; invalid, absent or unassigned communities and nonmanagers receive404; an authorized empty community returns200 `[]`. Responses use no-store. Reads preserve stored data and resident access behavior. See the [approved addendum](docs/design/S-3-AC11-contract-addendum.md), [execution evidence](docs/evidence/s3-ac11/README.md) and [supplemental traceability](docs/traceability/S-3-AC11.csv).

Local verification: **200 passed,zero failures/errors,five planned S6 skips**. The52 new tests were committed first with52 real missing-route failures and148 original passes. They are unchanged in the green run. The CI phase requires the same exact205 cases and all previous integrity checks.

## Review status

Gustavo approved AC11 v1, its addendum,52 tests and CI phase. [PR17](https://github.com/ga424/communityconnect/pull/17) was merged by GitHub account abreugus at23:41:19 UTC; COMC65 is Done. [Final-head CI](https://github.com/ga424/communityconnect/actions/runs/42536348447) verified200/0/5 from downloaded artifacts, and merged main has the identical tree. Both merged feature/status branches are removed. [Integration record](docs/evidence/s3-ac11/merge-closeout.json). COMC66/67 were closed by Gustavo; independently authored teammate sign-offs were not supplied. The [implementation review](docs/reviews/S3-AC11-implementation-2026-11-08.md) records evidence and limits. Independent teammate review and full-story acceptance remain separate; no production release is authorized. Fixtures and identity header are local/test-only. Browser selection, production identity/MFA and assignment administration remain later work.

## Next proposed browser increment

[PR18 review](docs/reviews/PR-18-and-S3-browser-2026-11-08.md) found no blocking issue in the documentation closeout; its downloaded CI verifies200/0/5. PR18 remains open pending explicit merge authorization. One minor current-state CI evidence pointer is aligned in this preparation, preserving all historical ledger records.

[S3-BROWSER-1 v1](docs/plans/S-3-browser-approval.md) proposes one local read-only manager page with24 browser scenarios and6 startup guards, isolated Playwright tooling and a separate browser CI job. The existing API suite and gate stay unchanged. COMC68/69/70 are To Do for Gustavo scope, Kundan contract and Sandeep tests. No browser implementation or new executable test has started. The packet fixes error/loading/empty states, stale-response handling, local identity and review-port boundaries before approval.

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

Current expected result: **200 passes, zero failures/errors, five exact S6 skips** (205 cases, pytest exit0):120 S1/harness passes,28 AC12 passes and52 AC11 passes. S6 retains its AC18–AC22 skip reasons.

The new gate requires exactly the frozen153 previous expectations plus52 new passes, matching previous file hashes and the tests-first AC11 hash. It rejects missing/duplicate/extra cases, failures/errors, changed skips and altered manifests/files. The24 adversarial controls exercise the new gate; historical gates remain unchanged and run against their historical reports.

```bash
python scripts/verify_s3_ac11_baseline.py
python scripts/verify_s3_ac11_baseline.py --self-test
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

Production identity/MFA, UI/Playwright, provider integrations, security/dependency assurance and deployment remain later work. PostgreSQL and Python image tags need immutable release pinning and dependency/security review before release. This workflow checks migrations, AISE structure, the sensitive-data guard and the approved S-1 plus S3-AC12/AC11 contract phase; it is not a production security assessment.

Private interviews, participant identities, consent/recording files and credentials are excluded from this public repository. Team contribution signatures and final submission are not fabricated by automation.

Merged feature branches are deleted after merge; GitHub automatic branch deletion is enabled. Start each new task on a fresh branch from main. Gustavo approved [packet v1](docs/plans/AC-1-approval.md); the historical packet’s pending status is superseded by the [actual approval record](prompts/2026-11-04-ac1-approval.txt). PR #4 is merged and its branch was deleted remotely and locally. Gustavo also approved [AC-2 packet v1](docs/plans/AC-2-approval.md), including the addendum, eight tests and CI change; the [actual approval](prompts/2026-11-04-ac2-approval.txt) supersedes historical pending wording in the packet/plan. AC-2 is merged; full-story human review remains open. Gustavo approved AC-4 packet v1 with 30 tests, AC-6 status coverage and CI promotion; that actual approval is recorded above. No automatic merge, deployment or further task implementation is authorized.
