# S-3 manager community context — draft contract

S-3-CTX-1 design deliverable under Gustavo's November8 work-queue request. **Kundan contract and Sandeep test-specification acceptance are pending.** No endpoint or executable test is implemented. Revised AC11/12 source is in `docs/evidence/s1-closeout/next-feature-source.json`; legacy COMC-10 S/AC numbers are superseded only for this slice.

## 1 Problem

A portfolio manager needs to see requests for one assigned community without mixing another community's information (E-3). A-2 assumes one login spans all assigned communities; production identity remains unvalidated by this synthetic contract.

## 2 Scope

Read assigned community options and requests for one selected community through a local API. Explicit URL selection represents context; no server-global selected-community state. Use synthetic users and preseeded assignments. The browser selector is later integration work.

## 3 Non-goals

No login/MFA, invitation/assignment administration, web UI, status writes, tenant/board visibility, documents, announcements or payments. Do not widen existing resident routes. Do not add a migration or change production authorization policy.

## 4 Interface

Both proposed GET routes accept `X-User-Id: str | None`. Parse IDs with existing positive PostgreSQL INTEGER rules. Unknown/invalid caller returns `401 {"detail":"Unknown user"}` before path lookup. Invalid, missing or unassigned selected community returns `404 {"detail":"Not found"}` with no details. All successful results are `200` JSON arrays.

| Proposed route | Typed result |
| --- | --- |
| `/manager/communities` | `list[CommunityOption]`; all current manager assignments, sorted by community ID ascending |
| `/manager/communities/{community_id}` is not proposed | No general-purpose community details endpoint |
| `/manager/communities/{community_id}/requests` | `community_id: str` raw path; `list[RequestOut]` for exactly the authorized selected community |

Known users with no manager assignments receive `[]` from the options route. A known resident/board/admin without manager assignment is not implicitly authorized for the request route. Empty authorized communities return `[]`. Database/system failures are not disguised as authorization denials.

## 5 Data

Reuse existing `app_users`, `communities`, `memberships` and `maintenance_requests`. Assignment means membership for that user/community with `role='manager'`; manager unit is null. `CommunityOption={id:int,name:str}` uses the existing positive ID and 1–100-character name constraints. `RequestOut` preserves existing S1 fields/types: id, community_id, unit_id (positive int); category and description (str); status (Open/In progress/Resolved); created_at (UTC `YYYY-MM-DDTHH:MM:SSZ`). Never return submitted_by. Synthetic fixtures use distinct existing-range integer IDs for M1/M2 and three communities; no real source records.

## 6 Rules

R1: Every returned option is a current manager assignment for the caller. R2: Every returned request belongs to the selected community and the caller has a current manager assignment there. R3: Denied reads disclose no request details and change no records. R4: Context never carries across callers or requests; the route parameter and current assignment decide each read. R5: Existing resident self-only behavior and all120 passing S1/harness cases remain unchanged.

## 7 Edge cases

Unknown caller plus invalid path; role in another community; resident/admin/board without manager assignment; no assignments; assigned community with no requests; malformed/overflow ID; revoked assignment after an earlier success; equal timestamps; two callers interleaving selections.

## 8 Draft decisions and open questions

D1: Test identity is synthetic only; role strings do not grant access outside their own community membership. D2: List all assigned options by ID ascending and selected-community requests by created_at descending then id descending, without pagination in this fixture-sized slice. D3: Read authorization and selected-community rows in one transaction, holding the manager membership stable through response validation. A revocation committed before a later read is denied; an already authorized in-flight response may complete before revocation commits. Do not promise instant cancellation. D4: No assignment or read endpoint mutates state; missing authorization and missing community share404. These are proposed local contract rules awaiting review, not observed interview rules.

OQ1: Which production identity and assignment workflow establishes or revokes the manager's authority? Do not build anything that depends on this. Stop and ask.

OQ2: What pagination limits and latency target fit real community volumes? Do not build anything that depends on this. Stop and ask.

S1 OQ1/OQ2 tenant and household/board questions remain unresolved and excluded.

## 9 Acceptance tests

AC11: M1 manages Mountain Ridge/Pine Hollow; selecting Pine Hollow returns only its request. AC12: M2 manages only Elm Court; only Elm Court is offered. Proposed names: `test_ac11_manager_reads_only_selected_community` and `test_ac12_manager_lists_only_assigned_communities`. **Not yet written.** Full candidate matrix and owner decisions: `docs/plans/S-3-context-test-plan.md`. This API contract is a step toward the source's browser outcome, not completion of the user-facing story.
