# S-1 bounded implementation plan

Status as of November 7, 2026: AC-1 and explicitly approved AC-2 are implemented and merged (PRs #4/#6). AC-3 is [verified in fresh CI without a code change](../evidence/ac3/README.md), pending human review. [AC-4 packet v1](AC-4-approval.md) is the next implementation proposal; it explicitly includes the same read route's AC-6 overlap, 30 new contract cases and CI promotion. No AC-4 implementation approval is recorded. Kundan/Sandeep full-story reviews remain pending.

## How

FastAPI routes in app/requests.py use app/models.py PostgreSQL query helpers, settings in app/settings.py and app.clock.now(). Liquibase creates communities, units, app_users, memberships and maintenance_requests. Tests seed two communities, three resident users, memberships and requests; no real identity. No migration runs implicitly at API startup. All public errors follow the design envelope and validation precedence. This plan must be reviewed against docs/design/S-1.md and docs/features/S-1-acceptance.md before edits.

## Prerequisites

COMC-37: container/migration rehearsal. COMC-39 and COMC-40: both executable test baselines. COMC-33/35: reviewed S-1 design/gap dispositions. COMC-41: human approval of bounded tasks. Gustavo's AC-1 and AC-2 approvals are recorded in prompts/; they do not complete other reviewers' work or approve AC-4. Review AC-3's no-code evidence before accepting the next packet. The draft test hooks do not settle open product questions.

## Numbered tasks

For every task: save the exact bounded prompt, record human approval, commit an undo point, make only approved changes, inspect the diff/logs and edge cases, run the targeted test and prior passing tests, commit and record actual evidence. Tests and approved design are protected.

1. **AC-1 / COMC-54:** follow [AC-1 approval packet v1](AC-1-approval.md). Implement create/self-list with existing validation and access invariants; add contract tests first and promote the CI phase explicitly. Allowed application files are app/requests.py and app/models.py; reuse settings/clock unchanged. Preserve GET-by-ID as a stub. Stop only when AC-1, required write-path/isolation checks, harness checks and the approved phase gate pass. Full test output and existing-test hashes must be recorded.
2. **AC-2 / COMC-55:** approved and merged in PR #6. The NUL/unpaired-surrogate fix, text-policy addendum, eight regression cases and exact 88-pass / 2-deferred-failure / 5-skip phase are verified. Separate full-story peer acceptance remains pending; preserve historical approval and evidence.
3. **AC-3 / COMC-56:** existing community isolation passes in CI run 42417030245 on merged main. No code change is required. Review [evidence](../evidence/ac3/README.md) for list exclusion, cross-community denial and unchanged write state; keep human acceptance separate from runtime verification.
4. **AC-4 / COMC-57:** proposed [packet v1](AC-4-approval.md). Implement ID lookup with caller, membership and submitter filters only after explicit approval, including its 30 contracts and CI phase change. Authorized reads must return the persisted status, which also makes the existing AC-6 test pass. Do not preserve an artificial failure or silently broaden the packet.
5. **AC-5 / COMC-58:** verify self-only access within the same community in app/requests.py and app/models.py. Stop when test_ac5_neighbor_in_same_community_does_not_see_request passes. If already passing, record verification rather than invent a code change. Broader household/board policy remains open.
6. **AC-6 / COMC-59:** expose persisted status through lookup in app/requests.py and app/models.py. Stop when test_ac6_resident_sees_in_progress_status passes. The test fixture changes status; do not add a status-update endpoint. Run all six S-1 tests and inspect all existing edge cases.

## Not requested for this increment

No S-6 implementation, real payments, UI, authentication, roles admin, notifications, reopening, photos or deployments. Future work remains in Jira. Do not build anything dependent on OQ1/OQ2.
