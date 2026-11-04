# S-1 bounded implementation plan

Status: draft; Kundan and Sandeep review pending. Setup is authorized; no AC implementation approval is recorded.

## How

FastAPI routes in app/requests.py use app/models.py PostgreSQL query helpers, settings in app/settings.py and app.clock.now(). Liquibase creates communities, units, app_users, memberships and maintenance_requests. Tests seed two communities, three resident users, memberships and requests; no real identity. No migration runs implicitly at API startup. All public errors follow the design envelope and validation precedence. This plan must be reviewed against docs/design/S-1.md and docs/features/S-1-acceptance.md before edits.

## Prerequisites

COMC-37: container/migration rehearsal. COMC-39 and COMC-40: both executable test baselines. COMC-33/35: reviewed S-1 design/gap dispositions. COMC-41: human approval of this plan. The draft test hooks do not settle open product questions.

## Numbered tasks

For every task: save the exact bounded prompt, record human approval, commit an undo point, make only approved changes, inspect the diff/logs and edge cases, run the targeted test and prior passing tests, commit and record actual evidence. Tests and approved design are protected.

1. **AC-1 / COMC-54:** implement create and self-list for a valid resident. Files: app/requests.py, app/models.py, app/settings.py, app/clock.py. Never expose another user's rows while adding the list. Stop when test_ac1_resident_submits_request_shown_as_open passes. Check exactly one Open row, trimmed description and injected UTC time.
2. **AC-2 / COMC-55:** implement validation order/body/description rules in app/requests.py (models.py only if needed for no-write behavior). Stop when test_ac2_blank_description_rejected_and_list_unchanged passes. Check whitespace, oversize, wrong types, extra fields, malformed JSON and unchanged storage. Do not change tests to match framework defaults.
3. **AC-3 / COMC-56:** verify/enforce community isolation in app/requests.py and app/models.py. Stop when test_ac3_other_community_resident_does_not_see_request passes. Check no cross-community response or write. If AC-1 already satisfies it, record no-code verification; do not introduce an insecure intermediate state.
4. **AC-4 / COMC-57:** implement ID lookup with caller, membership and submitter filters. Files: app/requests.py, app/models.py. Stop when test_ac4_other_community_direct_id_returns_not_found passes. Check unknown, unauthorized and malformed ID all use the specified 404 envelope.
5. **AC-5 / COMC-58:** verify self-only access within the same community in app/requests.py and app/models.py. Stop when test_ac5_neighbor_in_same_community_does_not_see_request passes. If already passing, record verification rather than invent a code change. Broader household/board policy remains open.
6. **AC-6 / COMC-59:** expose persisted status through lookup in app/requests.py and app/models.py. Stop when test_ac6_resident_sees_in_progress_status passes. The test fixture changes status; do not add a status-update endpoint. Run all six S-1 tests and inspect all existing edge cases.

## Not requested for this increment

No S-6 implementation, real payments, UI, authentication, roles admin, notifications, reopening, photos or deployments. Future work remains in Jira. Do not build anything dependent on OQ1/OQ2.
