# S-1 bounded implementation plan

Status as of November 7, 2026: AC-1/AC-2 are merged (PRs #4/#6). AC-3 has CI/local runtime evidence and awaits separate human acceptance. Explicitly approved AC-4 with read-only AC-6 is implemented in [PR8](https://github.com/ga424/communityconnect/pull/8), still open; [bounded AI review](../reviews/PR-8-and-AC-5-2026-11-07.md) found no blocking code defect and reverified 120 passes / zero failures / five S-6 skips. GitHub shows an approval from abreugus; named teammate acceptance is not inferred. [AC-5 packet v1](AC-5-approval.md) is the next proposal: verification-only after integration, with no code/test/CI changes. Approval remains pending.

## How

FastAPI routes in app/requests.py use app/models.py PostgreSQL query helpers, settings in app/settings.py and app.clock.now(). Liquibase creates communities, units, app_users, memberships and maintenance_requests. Tests seed two communities, three resident users, memberships and requests; no real identity. No migration runs implicitly at API startup. All public errors follow the design envelope and validation precedence. This plan must be reviewed against docs/design/S-1.md and docs/features/S-1-acceptance.md before edits.

## Prerequisites

COMC-37: container/migration rehearsal. COMC-39 and COMC-40: both executable test baselines. COMC-33/35: reviewed S-1 design/gap dispositions. COMC-41: human approval of bounded tasks. Gustavo's AC-1, AC-2 and AC-4 approvals are recorded in prompts/; they do not complete other reviewers' work or approve AC-5. Review AC-3's no-code evidence before accepting the next packet. The draft test hooks do not settle open product questions.

## Numbered tasks

For every task: save the exact bounded prompt, record human approval, commit an undo point, make only approved changes, inspect the diff/logs and edge cases, run the targeted test and prior passing tests, commit and record actual evidence. Tests and approved design are protected.

1. **AC-1 / COMC-54:** follow [AC-1 approval packet v1](AC-1-approval.md). Implement create/self-list with existing validation and access invariants; add contract tests first and promote the CI phase explicitly. Allowed application files are app/requests.py and app/models.py; reuse settings/clock unchanged. Preserve GET-by-ID as a stub. Stop only when AC-1, required write-path/isolation checks, harness checks and the approved phase gate pass. Full test output and existing-test hashes must be recorded.
2. **AC-2 / COMC-55:** approved and merged in PR #6. The NUL/unpaired-surrogate fix, text-policy addendum, eight regression cases and exact 88-pass / 2-deferred-failure / 5-skip phase are verified. Separate full-story peer acceptance remains pending; preserve historical approval and evidence.
3. **AC-3 / COMC-56:** existing community isolation passes in CI run 42417030245 on merged main. No code change is required. Review [evidence](../evidence/ac3/README.md) for list exclusion, cross-community denial and unchanged write state; keep human acceptance separate from runtime verification.
4. **AC-4 / COMC-57:** explicitly approved [packet v1](AC-4-approval.md) implemented in PR8, including 30 frozen contracts and the approved 120/0/5 CI phase. [Actual approval](../../prompts/2026-11-07-ac4-approval.txt) supersedes historical pending wording. Final-head CI and bounded review pass; PR8 remains unmerged and individual teammate acceptance remains pending.
5. **AC-5 / COMC-58:** proposed [verification-only packet v1](AC-5-approval.md). Existing same-community self-only access already passes. After approval and PR8 integration, rerun the unchanged harness on named main, inspect seven existing isolation/owner controls, record evidence and stop for human acceptance. No application, test, design, schema or CI change; broader household/board policy remains open.
6. **AC-6 / COMC-59:** persisted-status reads are implemented by the explicitly approved AC4 overlap and pass in PR8. Test fixtures set status; no status-update endpoint exists. Keep the separate verification/acceptance record open until actual reviewer decisions are recorded.

## Not requested for this increment

No S-6 implementation, real payments, UI, authentication, roles admin, notifications, reopening, photos or deployments. Future work remains in Jira. Do not build anything dependent on OQ1/OQ2.
