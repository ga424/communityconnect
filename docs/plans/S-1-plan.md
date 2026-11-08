# S-1 bounded implementation plan

Status as of November 8, 2026: all six S-1 runtime criteria are merged and pass. PR11 audit follow-up is merged at `3918cbd9fd015f8325cfc0136180c28ad31c5d01`; its branch is deleted. A fresh remote clone at that exact main SHA passed 120 tests, zero failures/errors and five unchanged S-6 skips, exit 0. [Acceptance review](../reviews/S-1-acceptance-2026-11-08.md) separates delivery from pending named reviews, design/gap closeout and independent final-submission-SHA verification. Gustavo accepted bounded S1 behavior and COMC42 is closed; Kundan/Sandeep reviews remain. The [S3 packet](S-3-context-approval.md) design/test-plan deliverable has now been prepared under the later work-queue request; its contract/test review and future implementation approval remain separate. M1 implementation scope is unchanged. Historical task packets retain their original wording; actual recorded approvals supersede their pending status.

## How

FastAPI routes in app/requests.py use app/models.py PostgreSQL query helpers, settings in app/settings.py and app.clock.now(). Liquibase creates communities, units, app_users, memberships and maintenance_requests. Tests seed two communities, three resident users, memberships and requests; no real identity. No migration runs implicitly at API startup. All public errors follow the design envelope and validation precedence. This plan must be reviewed against docs/design/S-1.md and docs/features/S-1-acceptance.md before edits.

## Prerequisites

COMC-37: container/migration rehearsal. COMC-39 and COMC-40: both executable test baselines. COMC-33/35: reviewed S-1 design/gap dispositions. COMC-41: human approval of bounded tasks. Gustavo's AC-1, AC-2 and AC-4 approvals are recorded in prompts/; Gustavo separately approved AC-5 verification-only on November 8. These approvals do not complete other reviewers' work. Review AC-3's no-code evidence before accepting the next packet. The draft test hooks do not settle open product questions.

## Numbered tasks

For every task: save the exact bounded prompt, record human approval, commit an undo point, make only approved changes, inspect the diff/logs and edge cases, run the targeted test and prior passing tests, commit and record actual evidence. Tests and approved design are protected.

1. **AC-1 / COMC-54:** follow [AC-1 approval packet v1](AC-1-approval.md). Implement create/self-list with existing validation and access invariants; add contract tests first and promote the CI phase explicitly. Allowed application files are app/requests.py and app/models.py; reuse settings/clock unchanged. Preserve GET-by-ID as a stub. Stop only when AC-1, required write-path/isolation checks, harness checks and the approved phase gate pass. Full test output and existing-test hashes must be recorded.
2. **AC-2 / COMC-55:** approved and merged in PR #6. The NUL/unpaired-surrogate fix, text-policy addendum, eight regression cases and exact 88-pass / 2-deferred-failure / 5-skip phase are verified. Separate full-story peer acceptance remains pending; preserve historical approval and evidence.
3. **AC-3 / COMC-56:** existing community isolation passes in CI run 42417030245 on merged main. No code change is required. Review [evidence](../evidence/ac3/README.md) for list exclusion, cross-community denial and unchanged write state; keep human acceptance separate from runtime verification.
4. **AC-4 / COMC-57:** explicitly approved [packet v1](AC-4-approval.md) is merged through PR8 into fc208ec. The 30 frozen contracts and approved 120/0/5 phase remain intact. Gustavo authorized the merge; independent full-story peer reviews remain separate. [Merge/cleanup proof](../evidence/ac5/merge-and-cleanup.json).
5. **AC-5 / COMC-58:** [packet v1](AC-5-approval.md) explicitly approved and executed as verification-only. [Results](../evidence/ac5/README.md): all seven selected controls, six original S1 cases and complete unchanged 120/0/5 suite pass; migration rehearsal and107 hashes pass. No source/test/CI change. Disposable verification resources removed, running preview preserved. PR10 is now merged; named Kundan/Sandeep/Gustavo result acceptance remains separate. An audit-only follow-up preserves a complete superseding provenance record.
6. **AC-6 / COMC-59:** read-only persisted-status behavior is merged in PR8 and reverified by AC5 regression coverage. Fixtures set status; no status-update endpoint exists. Individual peer/full-story acceptance remains separate from merged delivery.

## Not requested for this increment

No S-6 implementation, real payments, UI, authentication, roles admin, notifications, reopening, photos or deployments. Future work remains in Jira. Do not build anything dependent on OQ1/OQ2.
