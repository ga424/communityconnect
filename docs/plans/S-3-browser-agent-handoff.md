# S3-BROWSER-1 multi-agent handoff — November 8, 2026

Gustavo requested multi-agent delivery only if COMC-69 and COMC-70 both accept. The fresh Jira read returned **To Do and zero comments for both**. Implementation remains unstarted; COMC-68 stays To Do. PR19 is the preparation PR, not an implementation PR. This plan does not alter the conditionally approved addendum, 30 test IDs or existing API phase.

Two read-only AI agents completed preparation: `browser_test_readiness` inspected the contract/test inventory; `browser_infra_readiness` inspected the container/CI boundaries. Neither edited files, ran tests, installed dependencies or recorded a human acceptance. The coordinator checked their cited source locations. Their findings support the named reviews rather than replace them.

## Ownership after the review condition is satisfied

| Role | Exclusive file ownership | Handoff |
| --- | --- | --- |
| QA agent | `browser_tests/*`, `scripts/seed_browser_review.py`, `scripts/verify_s3_browser_baseline.py`; supplies proposed frozen test manifests | Agree environment, seed and artifact interfaces with infrastructure; record semantic red cases against the old app; freeze tests/helpers before UI work |
| Infrastructure agent | `requirements.browser.in`, `requirements.browser.lock`, `Dockerfile.browser`, `compose.browser.yaml`, `scripts/browser_review.sh`, `scripts/run_browser_contract.sh`, `.github/workflows/browser-contract.yml` | Prove the existing API starts in an isolated runtime; use QA's verifier interface; freeze lock with test baseline |
| UI agent | `app/browser_ui.py`, `app/static/manager.html`, `manager.js`, `manager.css`; only approved router registration in `app/main.py` | Start implementation after coordinator verifies test freeze; preserve all existing API behavior |
| Coordinator | `AGENTS.md` approved exception, approved addendum copy, evidence/traceability, prompts, Jira, ledgers, integration commits and PR | Recheck actual acceptances and packet version; verify dependencies, review diffs, run required checks, publish actual results |

Use isolated agent worktrees or strictly exclusive file sets, with the coordinator controlling integration. No agent changes another owner's files or rewrites protected tests to make code pass. QA and infrastructure may prepare their approved files concurrently; UI execution depends on the frozen red baseline. Do not run database-mutating suites concurrently against one Compose project. One coordinator schedules those runs and cleanup.

## QA review points for Sandeep before freeze

These are coverage clarifications, not observed implementation defects; the UI and new tests do not exist yet. The proposed inventory remains unchanged. Sandeep should record the disposition within COMC-70.

1. `test_browser_two_tabs_independent` currently describes two isolated browser contexts ([inventory](S-3-browser-proposed-tests.json), assertion near line 168). Confirm coverage of two pages sharing one context, optionally retaining isolated-context coverage within that existing ID.
2. The addendum requires CSP and `nosniff` (line 11), while the transport case explicitly lists `no-store` (inventory line 173). Confirm explicit assertions for all required response headers in that existing case.
3. The addendum forbids stale success, failure and `finally` handlers from changing current state (line 21). Race cases describe delayed successes (inventory lines 133/138). Confirm delayed failure/cleanup assertions within those existing IDs.

These suggestions need no additional case IDs. Any material contract or test-specification correction still belongs to its named owner; no automatic packet amendment is made by an AI review.

## Infrastructure handoff checks

No blocking infrastructure contradiction was found by source inspection. Execution compatibility remains unverified.

- Override the inherited test command and artifact destination: existing `compose.yaml` lines 41–43 bind `./artifacts` and write `artifacts/pytest.xml`. Browser evidence must use a distinct directory and upload name.
- Explicitly select `browser_tests/pytest.ini` and `browser_tests/`; the existing pytest configuration selects `tests` and stays unchanged.
- Guard the disposable target before invoking the existing destructive fixture reset. `app/seed.py:8` has no internal environment check. The new wrapper must not reset the human preview database.
- Supply each API subprocess's full environment before startup; `app/settings.py:4` captures the database URL at import.
- Include new browser source paths in the new job's sensitive-data guard. Preserve the original API workflow unchanged.
- Resolve the isolated browser dependency lock against existing pins, record actual browser/image versions, and stop on incompatibility rather than upgrading protected dependencies.

## Delivery sequence

Both actual review acceptances → verify approved packet and preparation integration → clean feature branch and undo point → QA/infrastructure interface agreement → existing API health in isolated runtime → real red results → frozen tests/helpers/lock → UI implementation → separate browser 30-pass/zero-skip and API 200-pass/five-skip gates → local review evidence → implementation PR.

No new human acceptance, browser result, deployment, or permission to merge an implementation PR is inferred from this handoff.
