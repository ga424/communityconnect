# CommunityConnect agent instructions

## Scope and stack
Python 3.12, FastAPI, Pydantic, PostgreSQL, Docker Compose and Liquibase SQL migrations. M1 builds only S-1 after approval. S-6 is design/test-only. Use synthetic fixtures; no live payments or production identity.

## Plan and approval
Show a bounded plan and wait for human approval before editing. State the AC ID, allowed files, protected files, data changes and stop check. Approval for one task does not approve the next. The current user request authorizes initial repository setup, draft feature packets, test baselines and check-ins; it does not constitute approval of a future S-1 implementation task. Draft preparation may proceed under that existing setup authorization. Record the actual approval in prompts/ and LEDGER.md before implementing behavior.

## Commands
The intended all-test command is `docker compose run --build --rm test`. Read README.md for prerequisites and the current expected red baseline. Never represent red feature tests as a completed story. Run the AISE structural check with `python .agentic-sdlc/hooks/validate_project.py --workspace .agentic-sdlc`.

## Protected paths and decisions
Do not change approved acceptance criteria, docs/design/, tests/, migration changesets already applied, .agentic-sdlc/config.json controls, or prior ledger records to make a failing implementation pass. Ask the named owner for a design/test correction first. Never modify .git/, add credentials, copy private interview records into this public repository, upload raw transcripts, or merge/deploy without authorization. New append-only ledger entries and newly authorized test baselines are allowed within the task scope.

## Delivery
Read the AISE state and feature packet first. Commit an undo point before each approved implementation task. Work on a feature branch. Keep one AC or coherent setup change per commit. Record exact prompts, changed paths, actual checks, commit references, specific risks and human review status. No invented approvals, SHAs, interviews or passing checks. Open questions remain unresolved. AI review is not teammate review. Preserve S-6 skipped tests with AC IDs.

## Team
Kundan: S-1 requirements/implementation; Sandeep: harness and test specification; Gustavo: provenance and integration. Independent peer review remains required. Do not assign a reviewer a completed action they have not performed.

## Branch lifecycle
The user requires post-merge branch deletion. Keep GitHub delete_branch_on_merge enabled. Before manual cleanup, fetch current refs, confirm the branch's latest head is included in main and has no open PR, then delete that exact remote head with an expected-head lease and delete merged local copies. Never delete main, an unmerged head or a branch with uncommitted work. Preserve evidence with immutable commit/PR links and start new work on a fresh branch from main. A merge is not approval for a subsequent implementation task.

## Approved later local increment — S3-AC12 v1
Gustavo approved the options-only packet, addendum,28 new tests and additive148/0/5 CI phase. His subsequent completion confirmation and COMC63/64 closures clear this bounded implementation; record those closures as Gustavo's actions, not independently authored teammate sign-offs. Follow docs/plans/S-3-AC12-approval.md and the new S3-AC12 addendum. M1's S1-only submission boundary remains. No AC11, browser UI, production identity or merge is authorized; preserve all original tests and controls.

## Approved later local increment — S3-AC11 v1
Gustavo explicitly approved S3-AC11 v1, its addendum,52 tests and additive200/0/5 CI phase. PR15/16 are integrated; COMC66/67 are Done by Gustavo with attribution preserved. Follow docs/plans/S-3-AC11-approval.md and the new approved AC11 addendum. Allow only its listed files and tests-first sequence. M1 scope remains S1-only; no UI, production identity or next-task/implementation-PR merge is authorized.
