# CommunityConnect provenance ledger

Only actual reviewable changes are recorded. AI inspection is not human approval. The eight-entry milestone minimum is not yet satisfied. Private interview-summary records remain in the restricted course package pending a reviewed, de-identified repository transfer.

## Entry 1
artifact: README.md; commit 746a9b2b47a5fd2f9ef4379ad92cc8d5f84f490d
tool: OpenAI Codex, GPT-6 (exact build not exposed); 2026-11-03 session
prompts: Initial feature-scoped AISE check-ins; full request at prompts/2026-11-03-initial-checkins.txt
review: Codex checked current Jira scope and M1 source; selected S-1 and excluded obsolete donor-platform scope. Human review pending.
checks: GitHub create-file returned the SHA above; git clone succeeded.
evidence: COMC-38; M1 repository baseline
risk: Feature design, test execution and teammate approval are not established by the initial README.

## Entry 2
artifact: AISE workspace, AGENTS.md and bootstrap plan; commit recorded in the subsequent check-in
 tool: OpenAI Codex, GPT-6 (exact build not exposed); 2026-11-03 session
prompts: Initial AISE setup request; prompts/2026-11-03-initial-checkins.txt
review: Codex read pinned AISE contracts, preserved all default controls, and classified this as draft setup. Kundan's peer review remains pending.
checks: AISE workspace structural validator PASS (one non-blocking claim-field warning); sensitive-data guard on authored public text PASS; git diff --check PASS.
evidence: COMC-38, INTENT-COMC-M1-INIT, EV-REPO-ROOT
risk: Structural validation does not establish stage approval, release readiness, privacy approval or functioning feature behavior.

Entry 2 commit reference: 21ff38c (full SHA is resolved by git rev-parse 21ff38c; copied into the final commit manifest).

## Entry 3
artifact: docs/design/S-1.md, docs/design/S-6.md, docs/features/, docs/plans/S-1-plan.md, docs/traceability.csv
 tool: OpenAI Codex, GPT-6 (exact build not exposed); 2026-11-03 session
prompts: Initial feature setup request; prompts/2026-11-03-initial-checkins.txt
review: Codex transferred design sections from M1 v3, preserved open questions and 31 AC rows, and split the S-1 plan into six Jira-linked tasks. No gap-check or human approval is claimed. Kundan/Sandeep review pending.
checks: Design sections extracted from the supplied revised document; AC text copied from current COMC-9/17; no participant notes copied. git diff --check recorded at commit.
evidence: COMC-33/34/41, S-1 AC-1..6, S-6 AC-18..22
risk: Draft test harness choices and feature packets require teammate review; the full platform is not specified by these two local slices.

Entry 3 commit reference: 19eb9ea (full SHA in the final commit manifest).

## Entry 4
artifact: Docker/Compose, requirements lock, FastAPI stubs, local seed/schema/migrations, harness tests and CI recipe
 tool: OpenAI Codex, GPT-6 (exact build not exposed); 2026-11-03 session
prompts: Initial setup request; prompts/2026-11-03-initial-checkins.txt
review: Codex inspected typed design boundaries, migration foreign keys, destructive fixture scope and non-production guard. Business endpoints remain 501. The sensitive-data guard flagged the long public dummy password; changed the disposable database fixture to the obvious cc_test value and rescanned without changing guard rules. Sandeep/Gustavo peer review pending.
checks: pip check PASS; Python compile PASS; Docker Compose config PASS; shell syntax PASS; sensitive-data scan PASS after synthetic fixture correction. Docker execution unavailable locally; remote baseline pending.
evidence: COMC-37; S-1 schema/fixture contract; no S-1 implementation
risk: Migration update/rollback, Linux dependency installation and fresh-clone container execution remain unverified until actual runtime evidence. Latest Starlette warns that httpx TestClient support is deprecated; migration to its supported test client remains to review.

## Entry 5
artifact: tests/test_s1_requests.py, tests/test_s6_payments.py and tests/s6_harness.py
 tool: OpenAI Codex, GPT-6 (exact build not exposed); 2026-11-03 session
prompts: Initial feature check-ins request; prompts/2026-11-03-initial-checkins.txt
review: Codex derived assertions from AC-1..6 and AC-18..22 and checked ID/name mapping. S-6 uses explicit AC skip reasons and a deferred fixture adapter contract. Cross-community tests are present before feature implementation. Sandeep's specification review remains pending.
checks: APP_ENV=test .venv/bin/python -m pytest --collect-only -q: 15 tests collected (six S-1, five S-6, four harness); compileall PASS. Collection does not execute PostgreSQL assertions; runtime red evidence pending.
evidence: COMC-39, COMC-40; S-1 AC-1..6; S-6 AC-18..22
risk: S-6 test-only fixture adapter requires review and implementation before future payment tests can execute. No real provider, auth or payment persistence is present.

## Commit references for Entries 2–5

- 21ff38c58657bb46f44e8cd703643834362a110e — chore(COMC-38): initialize pinned AISE governance workspace
- 19eb9ea1c146830b4ccb043e06d646114aa6f7fd — docs(COMC-41): add S-1 and S-6 feature packets and bounded plan
- 92634ffbc0dffb8c5087577628055f6d7c5638f1 — chore(COMC-37): add local PostgreSQL Liquibase and FastAPI scaffold
- 47d553957ec95bb5d6428ef34364862f37cfaf25 — test(COMC-39): add S-1 red tests and deferred S-6 acceptance contracts

## Entry 6
artifact: AISE stage drafts/runtime evidence, commit manifest and Jira/PR handoff; its own full commit SHA is recorded in refs/notes/ai-provenance to avoid a self-referential tracked-file hash
 tool: OpenAI Codex, GPT-6 (exact build not exposed); 2026-11-03 session
prompts: Initial feature setup request and Docker availability update; prompts/2026-11-03-initial-checkins.txt and prompts/2026-11-03-docker-available.txt
review: Codex inspected source/test/SQL boundaries, read actual CI outcomes and preserved all feature approvals as pending. Kundan/Sandeep peer review remains pending.
checks: CI run 41775497234 on 47d553957ec95bb5d6428ef34364862f37cfaf25 succeeded: migration update/repeat/rollback/reapply; 4 harness passes, 6 expected semantic failures, 5 AC skips. Local result is recorded in docs/aise/test-baseline.md after execution.
evidence: EV-CI-41775497234; COMC-37/38/39/40/41/44; draft PR #1
risk: No business functionality, complete edge-case specification, human approval, production assurance, signed contribution or completed eight-entry milestone ledger is established.

To read the recording commit's append-only provenance note: `git fetch origin refs/notes/ai-provenance:refs/notes/ai-provenance`, then `git log --show-notes=ai-provenance`. Notes name exact commit SHAs without rewriting the committed artifacts. Future review entries should also cite this recording commit in LEDGER.md.

Entry 6 completion addendum: local Docker Desktop 29.2.1 fresh-clone run at 47d553957ec95bb5d6428ef34364862f37cfaf25 matched CI (4 passed, 6 failed, 5 skipped; no setup errors). Liquibase update/repeat/rollback/reapply passed. First build attempt hit a sandbox Buildx cache-write restriction; documented BUILDX_CONFIG in /tmp resolved it without changing permissions. Full compact evidence is docs/evidence/bootstrap/validation.json. Traceability CSV normalized a source line break after :: and updated the header to Test name; all 31 rows remain, with all 11 named test functions verified to exist. No test assertions or product decisions changed.

## Entry 7
artifact: docs/reviews/PR-2-and-AC-1-2026-11-04.md, docs/plans/AC-1-approval.md, S-1 plan refinements, branch workflow and append-only AISE corrections
tool: OpenAI Codex, GPT-6 (exact build not exposed); November 4, 2026 America/New_York
prompts: PR2/S-1 approval review plus merged-branch cleanup; full user requests in prompts/2026-11-04-pr2-ac1-review.txt. Proposed future implementation prompt is prompts/AC-1-bounded-task-proposed.txt and is explicitly unexecuted.
review: Codex inspected the merged PR diff, design, tests, CI gate and ledger; identified incompatible six-red CI, happy-path-only task stop checks and overbroad provenance mappings. Prepared a bounded packet and corrected provenance by appending superseding records; preserved original history and product/test expectations. This is AI self-review, not Kundan/Sandeep or Gustavo approval.
checks: PR2 executable-source diff empty; both JUnit hashes match with 4 pass/6 fail/5 skip and zero setup errors; all 31 unique AC rows and 11 named tests resolve; CI at reviewed head succeeded. Branch was fully merged with no open PR before leased deletion; automatic deletion enabled and read back true. Existing structural validator passes with its documented historical warning. No feature tests re-executed for documentation-only changes; final branch CI will revalidate the scaffold.
evidence: PR2 head 85e817ab73f8cfad5dc9caf5b950eedbdda614c7, merge dafd2ca71b89fd2d2a8fc0fdae6d8209f93dee12; COMC-41/44/54; EV-PR2-REVIEW-20261104; EV-BRANCH-CLEANUP-20261104
risk: AC1 implementation, contract tests and CI promotion remain unapproved; full teammate review, original gap-check transfer, complete provenance and final all-S1-green verification remain pending. Supersession records require consumer interpretation; the bundled validator does not resolve them automatically.

Entry 6 exact recording SHA: 85e817ab73f8cfad5dc9caf5b950eedbdda614c7, delivered in PR #2. Entry 6's earlier draft PR #1 reference preceded the separate evidence PR and is historical. Entry 7's own SHA is recorded in its Git provenance note and linked from Jira/PR after committing.

## AC-1 approval and undo checkpoint
Gustavo explicitly approved packet v1, its contract tests and CI transition; exact text: prompts/2026-11-04-ac1-approval.txt. Current main checkpoint is dafd2ca71b89fd2d2a8fc0fdae6d8209f93dee12. A new feature branch was created there and fast-forwarded to approved review commit 8ea0e80759ae06dc80cf5bf4bfa5666313074378 (PR #3 is still open). That commit is the pre-test undo point. No merge to main was performed. Existing tests/design/migrations/policies/settings/clock hashes are preserved in docs/evidence/ac1/protected-baseline.json. A separate red test commit will be made before application edits.

## Entry 8
artifact: tests/test_s1_contract.py; docs/evidence/ac1/red-junit.xml, red-summary.json, expected-tests.json, protected-baseline.json; actual approval record
tool: OpenAI Codex, GPT-6 (exact build not exposed); November 4, 2026 America/New_York
prompts: Explicit AC-1 approval in prompts/2026-11-04-ac1-approval.txt; approved bounded execution recorded in prompts/2026-11-04-ac1-execution.txt and referenced packet v1.
review: Codex derived 72 contract cases from existing design rules and the approved packet; inspected exact denial envelopes, unchanged persistence, validation order, self-only access and ordering. Preserved all existing tests and migrations. Human approval is for the packet's scope; no teammate execution/review is invented.
checks: 72 new cases collect. Full container test run before application edits: 78 failed (all semantic 501 assertions), 4 passed, 5 skipped, zero errors; pytest exit 1. Hashes and exact phase expectations recorded.
evidence: COMC-54; S-1 AC-1 plus binding invariants; EV-AC1-APPROVAL; EV-AC1-RED
risk: Business behavior still unimplemented at this checkpoint; the expected incremental verifier has not yet been implemented or validated. Full-story peer review and course provenance reconciliation remain pending despite reaching eight genuine entries.

## Entry 9
artifact: app/requests.py, app/models.py, scripts/verify_ac1_baseline.py, CI phase transition, README and docs/evidence/ac1/ execution evidence
tool: OpenAI Codex, GPT-6 (exact build not exposed); November 4, 2026 America/New_York
prompts: prompts/2026-11-04-ac1-approval.txt and prompts/2026-11-04-ac1-execution.txt; approved packet v1 at 8ea0e80759ae06dc80cf5bf4bfa5666313074378
review: Codex inspected caller/access/input precedence, parameterized SQL, membership lock and transaction, self-only filtering, UTC public responses, exact error/no-write behavior, unchanged details stub, logs and file hashes. AI review only; human peer acceptance remains pending.
checks: Full Docker run: 80 passed, 2 deferred 501 failures, 5 unchanged S-6 skips, zero errors; pytest exit 1. Phase verifier passed and rejected 11 defect types. Liquibase update/repeat/rollback/reapply passed. Fourteen protected hashes match. AISE structural validation passed with the documented historical warning; sensitive-data guard, Compose validation and diff whitespace checks passed.
evidence: EV-AC1-LOCAL; docs/evidence/ac1/local-summary.json; red-test undo 2b73ab0d5f21fb63e9b7c1406446c3cf7043682d; COMC-54. Implementation commit SHA is recorded by its Git provenance note and the subsequent reconciliation entry.
risk: Remote CI is pending at this checkpoint. Full S-1, all S-6 behavior, Kundan/Sandeep review and final full-story verification remain pending. Synthetic auth is local-only. No merge/deployment or next-task approval is claimed.

Entry 8 exact red-test SHA: `2b73ab0d5f21fb63e9b7c1406446c3cf7043682d`. Entry 9 exact implementation SHA: `15edff908305ffe51c7b7f7615bc22f87b4ef053`. AISE code-change records now map these commits to AC-1 and its mandatory first-write guards; no unimplemented AC-4/6 or S-6 completion is attributed. Pipeline Stage 05 is in progress for bounded AC-1 only; all broader stage approvals remain pending. This reconciliation commit changes evidence/state only; its own SHA is preserved in a Git provenance note.
