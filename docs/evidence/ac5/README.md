# AC-5 verification-only evidence — November 8, 2026

**Approved verification passed: 120 tests passed, zero failures/errors, five unchanged S-6 skips; real pytest exit 0.** No application, test, design, migration, dependency, container, workflow or gate change was required. Human result acceptance is pending.

## Source, approval and integration

Gustavo's [actual approval](../../../prompts/2026-11-08-ac5-approval.txt) authorizes PR8 merge/branch deletion and AC5 packet v1 verification-only. The [bounded execution record](../../../prompts/2026-11-08-ac5-execution.txt) preserves allowed/protected files and the stop check.

- Integrated main: `fc208ec4a093cdd81c6e87158e7a93561822226c`, the authorized merge of [PR8](https://github.com/ga424/communityconnect/pull/8).
- Reviewed PR8 implementation head: `354960fb81b55c2081dc3c5264a225be48930cd8`.
- Verification/undo checkpoint: `e615d78717c29e1f7d84c031940edf60eab46a53`, committed before tests. Its executable/test/design/feature/workflow/control bytes are identical to integrated main and the reviewed PR8 head.
- Approved packet/prior documentation history: `244026ec788d26688ab5a4fe1c6fa50f2e8203b9`, preserved by a local documentation-only merge into a fresh branch from main. PR9 remains open; this task did not merge it on GitHub.
- AISE remains pinned to merged 0.3.4. Existing requirement wording, provisional self-only assumption A-6 and OQ1/OQ2 are unchanged.

## Actual results

[Machine summary](local-summary.json) · [JUnit](local-junit.xml) · [pytest output](test-output.txt) · [real exit code](pytest-exit-code.txt) · [gate controls](gate-self-test.json) · [protected hashes](protected-baseline.json).

| Check | Result |
| --- | --- |
| Complete unchanged suite | 125 cases: 120 pass, 0 failures/errors, 5 exact S-6 skips, exit0 |
| All six original S-1 acceptance cases | Pass; original tests remain unchanged |
| Selected isolation/owner controls below | All seven pass |
| Exact S-1 phase gate | Pass without phase or manifest changes |
| Gate self-test | Valid control accepted; 13 report and 11 manifest defects rejected |
| Protected integrity | All 107 frozen hashes match; executable source matches merged main |
| Liquibase rehearsal | Update, repeat update, rollback one changeset, reapply all pass |
| Other checks | Compose config, AISE structure, source guard, prior ledger prefix and whitespace checks pass |
| Cleanup | Dedicated verification project removed; all pre-existing containers and preview health preserved |

## Evidence-PR CI

[PR10](https://github.com/ga424/communityconnect/pull/10) was subsequently merged by the GitHub account abreugus into b41387f1c63c0b469b2c17026095c47d43932011; the assistant did not invoke that merge. PR9 was also marked merged through ancestor integration. Its exact merged head722f1ba passed run42450702977; the downloaded [merged-head JUnit](merged-head-ci-junit.xml) again passed120/0/5 with exit0. [Post-publication evidence](post-publication.json) records the platform events and cleanup. A small append-only audit addendum is on a separate follow-up branch because it was in flight when PR10 merged. The prior result-head check follows. [Run42450409215](https://github.com/ga424/communityconnect/actions/runs/42450409215) passed at result commit `77fe12f8266dba5c63fc5a1b499589e139ddc716`. Its downloaded [JUnit](ci-junit.xml) independently passed the unchanged exact gate:120 passes, zero failures/errors, five exact S6 skips and real exit0. [CI summary](ci-summary.json) records checksum and successful steps, including migrations and cleanup. Later recording-head CI is captured in append-only Git provenance notes. No human result acceptance or merge is inferred.

## AC-5 and related controls

The existing primary AC-5 criterion remains: Given R3 is another resident in Mountain Ridge, When R3 lists its requests, Then R1's request is absent. This is a verification of the current provisional rule, not a decision about future household/board/tenant access.

| Existing case | Actual result |
| --- | --- |
| `test_ac5_neighbor_in_same_community_does_not_see_request` | Pass: neighbor list excludes owner's request |
| `test_ac1_contract_lists_only_submitter_even_for_same_unit` | Pass: same-unit neighbor sees nothing; owner still sees own request |
| `test_ac4_details_reject_other_submitter[same-community]` | Pass: exact404, no request-row change |
| `test_ac4_details_reject_other_submitter[same-unit]` | Pass: exact404, no request-row change |
| `test_ac4_other_community_direct_id_returns_not_found` | Pass: cross-community guessed ID denied |
| `test_ac1_resident_submits_request_shown_as_open` | Pass: owner create/list positive control |
| `test_ac6_resident_sees_in_progress_status` | Pass: owner reads persisted status |

Full node IDs and individual outcomes for these seven controls and all six original S-1 cases are recorded in local-summary.json. No duplicate test was added.

## Reproduction and resource boundaries

From this repository checkout, with Docker Desktop running:

```bash
export COMPOSE_PROJECT_NAME=cc-ac5-20261108
export BUILDX_CONFIG=/tmp/communityconnect-ac5-buildx
bash scripts/migration_rehearsal.sh
docker compose run --build --rm test
python3 scripts/verify_s1_baseline.py --junit artifacts/pytest.xml
python3 scripts/verify_s1_baseline.py --self-test
docker compose down --volumes --remove-orphans
```

Use an unused project name if that name is already active. Only disposable cc_test fixtures are allowed. [Migration output](migration-output.txt) and [cleanup output](cleanup-output.txt) preserve the actual run. The initial non-login shell lacked Docker on PATH and stopped before starting containers; retry used the normal configured login shell, with no repository configuration change. This is an environment preflight retry, not a failing feature test.

The user review project `cc-review-preview` and unrelated containers remained running. http://127.0.0.1:8765/health still returned200 after cleanup. The preview uses the same implementation bytes as merged main; its UI remains a separate local review wrapper.

## Merge and branch cleanup

[Merge/cleanup proof](merge-and-cleanup.json) records the exact expected PR8 head, merged main SHA and fresh ancestry/no-open-PR/clean-tree checks. GitHub automatically deleted `feature/COMC-57-ac4`; its local branch was deleted. GitHub also marked ancestor PR7 merged and deleted `chore/aise-refresh-ac3`; its clean local copy was removed. Worktrees were detached at immutable heads and preserved. PR9 and the evidence branch were later merged and cleaned up as recorded in post-publication.json. An in-flight audit correction temporarily recreated the evidence branch after automatic deletion; it was renamed to docs/COMC-58-audit-followup, preserving the unmerged commit without retaining the merged branch name. Automatic post-merge deletion stays enabled.

## Review and limits

| Owner | Required result review | State |
| --- | --- | --- |
| Kundan | AC5 behavior and provisional self-only requirement | Pending |
| Sandeep | Positive/negative controls, exact gate, migration and hash evidence | Pending |
| Gustavo | Exact approval, integrated source, AI-use and Jira/ledger traceability | Pending |

Gustavo's merge and execution authorizations are recorded; the table concerns review of the newly produced evidence. Sequential AI verification is not independent teammate signoff. COMC-58 stays In Progress until actual acceptance is recorded. Separate AC3/full-story/course reviews remain visible. No subsequent task is proposed or authorized here.

Known warnings remain: Starlette TestClient/httpx deprecation and historical EV-REPO-ROOT missing claim. The supplemental CHANGE-AC5-RESULT-SHA record omitted paths; its complete superseding record restores explicit traceability without rewriting history. The validator still warns about the retained original record. Existing CI Action/runner migration advisories remain separate maintenance work. No dependency/control change was made. S-6 remains unbuilt; no status-update endpoint, real identity/MFA, payments, shared hosting or production deployment. Broader security, performance, accessibility, resilience, supply-chain and regulatory assurance remain outside this prototype verification. Evidence-PR CI above is verified; final recording-head SHAs/checksums are recorded through append-only provenance notes and Jira.
