# AC-5 packet v1 — verify self-only request visibility

**Decision requested: approve verification and acceptance preparation for COMC-58. No application change, new test, migration or CI phase change is proposed. Execution approval is pending.**

Lead: Kundan. Test reviewer: Sandeep. Scope and provenance reviewer: Gustavo. This packet follows the [PR8 review](../reviews/PR-8-and-AC-5-2026-11-07.md). It does not approve PR8's merge or establish full-story human acceptance.

## Starting point and purpose

AC-5's existing test already passes at PR8 head `354960fb81b55c2081dc3c5264a225be48930cd8`. Create/self-list behavior was delivered in AC-1; AC-4 adds owner-scoped detail retrieval with AC-6 status coverage. The current suite has 125 cases: **120 pass, zero failures/errors, five unchanged S-6 skips**, pytest exit 0. [Reviewed CI evidence](../evidence/pr8-review/summary.json) records that result. This historical result is not a claim that the proposed task has been executed.

The task will verify the integrated result at a named merged commit and give the team a concise acceptance record. It must not manufacture a code change for behavior that is already correct. PR8 is currently open, and PR7's preparation commits are ancestors. Before execution, verify PR8's intended implementation is present on current main; if it is not, report that integration dependency and stop before claiming merged-main verification. Do not merge without authorization.

## Contract and scope

Preserve S-1 AC-5 verbatim:

> Given R3 is another resident in Mountain Ridge, When R3 lists its requests, Then R1’s request is absent.

Trace: E-12 and assumption A-6; design rules R1/R2 and decision D3. This verifies the provisional submitter-only rule already used by the prototype. It does not settle OQ2 (household or board access), OQ1 (tenant eligibility), or production identity. X-User-Id remains a synthetic harness selector.

## Bounded steps after approval

1. Record the exact approval, current main SHA, PR8 integration proof and protected source hashes. Start a fresh branch from that verified main commit; commit the evidence-only undo checkpoint before execution.
2. Run the unchanged Docker harness against its dedicated disposable database. Use a unique Compose project name and a writable temporary Buildx directory when needed. Never affect unrelated containers or shared databases.
3. Inspect these existing controls in the full JUnit report; do not add duplicate tests:

| Existing test | Observable evidence |
| --- | --- |
| `test_ac5_neighbor_in_same_community_does_not_see_request` | Same-community neighbor's list excludes the owner's request |
| `test_ac1_contract_lists_only_submitter_even_for_same_unit` | Same-unit neighbor sees nothing; the owner still sees their own request |
| `test_ac4_details_reject_other_submitter[same-community]` | Same-community guessed ID returns exact 404 with no stored-row change |
| `test_ac4_details_reject_other_submitter[same-unit]` | Same-unit guessed ID returns exact 404 with no stored-row change |
| `test_ac4_other_community_direct_id_returns_not_found` | Cross-community guessed ID remains denied |
| `test_ac1_resident_submits_request_shown_as_open` | Owner create/list positive control remains functional |
| `test_ac6_resident_sees_in_progress_status` | Owner can retrieve persisted status |

The first, fifth, sixth and seventh tests are in `tests/test_s1_requests.py`; the same-unit list contract is in `tests/test_s1_contract.py`; the two detail-denial cases are in `tests/test_s1_details.py`. Also report all six original S-1 acceptance outcomes separately from full-story acceptance.

4. Require real all-test exit 0 and the unchanged exact 120/0/5 S-1 gate. Run the existing gate self-test and existing migration rehearsal; inspect logs and hashes. Report failures honestly and stop for a separately scoped correction if any behavior, test, design, dependency or CI change is needed.
5. Save source SHA, commands, JUnit/checksums, migration output, results and limitations under `docs/evidence/ac5/`; append exact prompts and ledger records; update Jira without inventing teammate decisions. Remove only this run's disposable resources.
6. Open an evidence-only PR and stop for the named reviewers. After an authorized merge, verify ancestry/no open PR and delete the exact merged remote/local branch as required by AGENTS.md.

## Allowed and protected paths

Allowed: new `docs/evidence/ac5/` records, exact `prompts/` records, append-only `LEDGER.md` and `.agentic-sdlc/ledgers/*.jsonl`; current status in `docs/plans/S-1-plan.md`, README and AISE state/review/test artifacts. Ignore disposable runtime artifacts. Preserve historical evidence and prior ledger bytes.

Protected: all application code, tests/helpers, accepted contracts and design, SQL/Liquibase migrations, seed/settings/clock, dependencies, Docker/Compose, workflows, all gate scripts/manifests, AGENTS.md, AISE configuration/hooks and private interview records. No data migration, runtime configuration or package change. Fixture writes are limited to the existing disposable test harness.

## Stop check and review record

The task is ready for review only when all 125 cases match the unchanged phase, all seven selected controls and all six original S-1 acceptance cases pass, source/test/control hashes match, migration rehearsal passes, evidence links resolve and cleanup is recorded. A green run is runtime evidence, not human signoff.

| Reviewer | Decision to record | Current state |
| --- | --- | --- |
| Kundan | AC-5 behavior matches the provisional self-only requirement | Pending |
| Sandeep | Test scope, positive/negative controls, exact gate and migration evidence are sound | Pending |
| Gustavo | Actual approval, source SHA, AI-use provenance and Jira/ledger links are accurate | Pending |

COMC-58 remains open until its acceptance evidence is recorded. Full S-1 peer review, course submission checks and remaining story decisions are separate. No S-6 implementation, UI, payment, authentication/MFA, status-update endpoint or deployment is authorized. AISE stays pinned to merged version 0.3.4.

Proposed approval wording: “Approved. Proceed with AC-5 packet v1 as verification-only after PR8 is integrated, preserving code, tests and CI. Keep Jira and the AISE ledger updated and open an evidence PR for review.”
