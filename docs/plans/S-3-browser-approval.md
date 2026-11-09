# S3-BROWSER-1 packet v1 — local manager community view

**Scope conditionally approved by Gustavo; Kundan/Sandeep acceptances pending.** [COMC-68](https://gkms.atlassian.net/browse/COMC-68): Gustavo integration/implementation; [COMC-69](https://gkms.atlassian.net/browse/COMC-69): Kundan behavior/contract review; [COMC-70](https://gkms.atlassian.net/browse/COMC-70): Sandeep test/tooling review. All three remain To Do. See the [current approval/integration record](../reviews/S3-browser-approval-status-2026-11-08.md). The packet below preserves the proposed implementation boundary; subsequent dated decisions supersede its earlier pending-approval/PR18 status statements.

## Decision in one page

Build one read-only `/manager` page for the already merged AC12 options and AC11 request APIs. A fixed synthetic manager chooses one of their assigned communities and sees only its requests. The page must clear stale rows during selection/Refresh, ignore late responses, handle errors/empty states, render text safely and work with keyboard/mobile layouts. Provide a reproducible loopback-only preview and real Playwright evidence.

Approve the [proposed consumer addendum](S-3-browser-contract-addendum-proposed.md), [machine-readable contract](S-3-browser-contract-proposed.json), [exact30-case inventory](S-3-browser-proposed-tests.json), isolated browser tooling and new CI job **after** the two named reviews are recorded. This approval would authorize future tests-first execution only; result acceptance, merge, deployment and later features remain separate.

Current proven baseline: PR18 head `adc68b806bdf08ba6169a5edc2874fbf66b63dcd`, **200 passed,0 failures/errors,5 exact S6 skips (205 cases)**. PR18 is open and requires its own merge authorization. Integrate/rebase the preparation packet before coding, verify current main, and capture a fresh undo point. The preparation branch is stacked on PR18 only to keep review diffs distinct.

Proposed future checks are two separate required phases: unchanged API **200/0/5**, plus browser/startup **30 passes/0 failures/errors/skips**. Combined235 collected cases is bookkeeping, not a replacement gate or a result already achieved. This preparation changes no app/test/dependency/schema/workflow file.

## User outcome and trace

Source S3: “Switch between communities”; source AC11 selects Pine Hollow for M1; source AC12 offers only Elm Court to M2. E-3 motivates separation; A-2 (one login) remains an assumption because this packet uses a synthetic local identity. Original M1 traceability and S1-only submission scope stay unchanged; a supplemental browser trace will explicitly distinguish automated API/browser proof from real walkthrough/full-story acceptance.

```gherkin
Scenario: AC11 — selected community only
  Given M1 manages Mountain Ridge and Pine Hollow
  And each community has an Open request
  When M1 chooses Pine Hollow in the browser
  Then the heading is Pine Hollow and only its request is shown
  And Mountain Ridge rows are absent immediately when selection changes

Scenario: AC12 — assigned options only
  Given M2 manages only Elm Court
  When M2 opens the community selector
  Then Elm Court is the only community option

Scenario: Late responses cannot restore an earlier community
  Given a real Mountain Ridge response is still in flight
  When M1 selects Pine Hollow and its response completes
  And the earlier response arrives later
  Then only Pine Hollow remains visible

Scenario: A fresh read observes committed revocation
  Given M1 previously viewed Mountain Ridge
  And that assignment is removed and committed
  When M1 refreshes or reads it again
  Then its rows are cleared and access is refused or the option disappears
```

## Layout and state choices to approve

A single page contains title, synthetic-review banner, Community select, Refresh, status/error area, selected-community heading and read-only request table. No automatic selection, identity picker, remembered context, detail navigation, edit/status controls or pagination. The addendum fixes initial/loading/empty/error, stale-response, revocation and restoration behavior. Proposed10-second fetch timeout and manual recovery are explicit new UI decisions, not interview statements or backend SLOs.

## Tooling and local test topology

Retain Python3.12/FastAPI/Pydantic/PostgreSQL and AISE0.3.4. Plain HTML/CSS/JavaScript requires no Node build chain or front-end framework. Propose Python Playwright1.64.1 with pyee14.0.0 and greenlet3.5.6 in a **separate** browser-only lock; existing dependency pins remain constraints. Use the async Playwright library through asyncio.run in ordinary pytest functions, without a new pytest plugin. This supports Event-gated response delays without blocking the browser dispatcher. No versions are installed or claimed compatible by this preparation; resolving a conflict with protected pins is a stop, not permission to upgrade them.

New Dockerfile.browser uses Python3.12, existing requirements.lock plus the separate browser lock and `python -m playwright install --with-deps chromium`. Record actual package versions, browser build and image digest before the red baseline; freeze helper/test/fixture hashes before UI code. A new compose.browser.yaml reuses the existing DB/migration/test definitions through extends; preserve the original Compose/Docker files. Browser job has its own disposable project/database and no published DB port; use bounded shared-memory sizing, no privileged host permissions. Test browser and Uvicorn run within the disposable test container on loopback. Per-test fixtures start/stop servers and browsers, seed via guarded setup and restore known data; no parallel DB-mutating tests.

For human review, an explicit review profile launches the same app on host127.0.0.1:8766 using M1 by default in the launcher (server requires explicit identity env); choose M2/103 through launcher arguments, not in-page controls. Explicit seeding occurs once at setup; restart never resets data automatically. Separate project/port from the existing8765 wrapper. Refuse collision rather than stopping someone else's containers or reusing their DB. Provide start/stop commands and record any missing Docker prerequisite honestly.

[Official library usage](https://playwright.dev/python/docs/library), [browser installation](https://playwright.dev/python/docs/browsers), [Docker guidance](https://playwright.dev/python/docs/docker) and [network/route.fetch guidance](https://playwright.dev/python/docs/network) were checked November8,2026. [PyPI1.64.1 metadata](https://pypi.org/pypi/playwright/1.64.1/json) lists pyee>=13,<15 and greenlet>=3.1.1,<4. Isolated package/image compatibility and vulnerability review remain implementation checks, not established facts from these docs.

## Exact approved-file boundary if accepted

| File(s) | Allowed future change |
| --- | --- |
| app/browser_ui.py; app/static/manager.html, manager.js, manager.css (new) | Serve guarded page/session/allowlisted assets and implement specified read-only UI |
| app/main.py | Import/register new browser router only when explicitly enabled; preserve current APP_ENV guard, routers and health |
| browser_tests/conftest.py, pytest.ini, test_manager_browser.py, test_boot_guards.py (new) |24 browser cases plus6 guards, isolated fixtures/process cleanup, no existing shared-fixture edits |
| scripts/seed_browser_review.py; scripts/browser_review.sh (new) | Guarded synthetic setup and explicit loopback start/stop; no application startup reset |
| requirements.browser.in / requirements.browser.lock; Dockerfile.browser; compose.browser.yaml (new) | Isolated pinned browser dependencies/runtime; existing dependency and container files untouched |
| scripts/run_browser_contract.sh; scripts/verify_s3_browser_baseline.py (new) | Dedicated runner, real exit0, exact30-case/hash gate and20 negative controls |
| .github/workflows/browser-contract.yml (new) | Separate required browser job, timeout/artifact/always-cleanup; original workflow unchanged |
| docs/design/S-3-browser-contract-addendum.md (new after approval) | Copy only the approved addendum; original design files untouched |
| docs/evidence/s3-browser/, docs/traceability/S-3-browser.csv (new) | Actual red/green/CI/screenshots/browser-version/walkthrough evidence |
| AGENTS.md | Append only the exact approved local browser exception |
| README, S3 plan/packet/reviews, prompts, AISE ledgers/state/artifacts | Accurate status and append-only provenance |

Protected: every current test/fixture/manifest/verifier; all existing manager/resident/model/seed/settings/clock/payment code except the named main registration; existing designs/traceability/schema/migrations; original Docker/Compose/dependencies/pytest config/CI workflow; AISE framework/config/hooks and prior ledger bytes. No copied interview records or participant names in fixtures. Stop if this file boundary is insufficient.

## Tests-first and CI execution, after approval

1. Confirm PR18/preparation integration and exact approved addendum/30 IDs; record Gustavo scope and actual Kundan/Sandeep dispositions without invented authorship. Capture clean main/undo and protected hashes.
2. Add only approved new tooling, fixture runner and30 tests first. The old app must launch and /health respond. Missing /manager is a real404 assertion failure, not an import/startup error. Guard cases may already pass; record the actual red count and unexpected passes. No placeholders/skips/xfails or retry-to-green.
3. Freeze new tests, fixtures/seed helper and lock at a real commit. Implement the new page/router with only allowed main registration. Preserve all old tests/pins and immutable contract meaning.
4. Separate browser CI job runs30 exact cases in Chromium with real exit0 and no skips/errors/failures. It pins the current AC11 source-manifest hash, preserves all old test hashes and freezes new test/helper hashes.20 controls listed in the inventory must reject missing/extra/duplicate/failed/error/skipped evidence and changed source/manifest/file expectations. The existing API job still verifies200/0/5 and24 old gate controls unchanged. Both jobs must pass under this packet; no combined total can hide a failed suite. This is a review/acceptance requirement, not a claim that GitHub branch-protection settings have been changed.
5. Store JUnit, stdout, exit status, package/browser versions, image digest, gate controls and synthetic screenshots/traces. Failure artifacts must upload even when tests fail; cleanup must always remove only the dedicated project. Core ACs/revocation use real API/DB; faults/delays are labeled. Before/after table snapshots account explicitly for fixture mutations.
6. Run local review on the Mac after automated checks: M1 select A/B, M2 assigned-only options, empty state, keyboard/mobile. Record actual observer, time, screenshots and results; do not prefill human acceptance. Full S3/Professor Dale submission approval remains separate.
7. Open implementation PR and update Jira/AISE with exact commits/results. Reviewers decide acceptance; no automatic merge or subsequent feature.

## Stop conditions and remaining risks

Stop for dependency conflicts, inability to start a real existing API before tests, need for protected-file changes, sleep-only race evidence, fixture isolation failure, exposing non-loopback ports, real identity/payment data, or a material contract/test correction after freeze. A failed declared check is not replaced with a skip. Fix only approved implementation defects; test defects require their owner decision.

Kundan owns whether the UI wording/state choices match the source outcome; Sandeep owns deterministic harness/CI/compatibility review; Gustavo owns scope and integration. No team capacity, sprint dates, story points or review completion is invented. Existing TestClient deprecation and unpinned older image/dependency assurance remain tracked for future release; do not expand this task to production hardening. Browser engine coverage is Chromium only; no performance SLA, penetration test, full WCAG or production-security claim.

## Approvals

Gustavo: approve/revise/reject S3-BROWSER-1 v1, its addendum,30 tests, separate pinned browser tooling and new browser CI job. Kundan: COMC-69 contract decision. Sandeep: COMC-70 test/tooling decision. Until recorded, COMC-68 stays To Do. PR18 merge authorization is a separate decision; its branch is preserved while open and deleted only after verified latest-head integration. Approval of this preparation PR alone does not authorize implementation.
