# S-3-CTX-1 packet v1 — manager community context

**Proposed; awaiting Gustavo's approval. This packet authorizes a design and test-plan deliverable only.** It does not authorize implementation, executable tests, a CI phase change, merge or deployment. It is preparation for the next product feature after S-1; M1 still builds only S-1 and keeps S-6 design/test-only.

## Outcome and source

A portfolio community manager selects an assigned community and sees that community's requests, reducing the risk of answering a resident with another community's information. This is revised **S-3**, mapped to **COMC-10**. COMC-10's older S-2 / AC-4–6 labels are historical and must not be reused as current acceptance IDs.

Source: Milestone 1 Review v3, section 4, attached to COMC-4; the local revision manifest and the November 3 story-to-Jira mapping were inspected. The selected source text and hashes are in [source excerpt](../evidence/s1-closeout/next-feature-source.json). No interview records are copied.

```gherkin
Scenario: AC-11 — select a managed community
  Given M1 manages Mountain Ridge and Pine Hollow and each has one Open request
  When M1 selects Pine Hollow
  Then the request list shows only the Pine Hollow request

Scenario: AC-12 — offer only assigned communities
  Given M2 manages only Elm Court
  When M2 opens the community selector
  Then only Elm Court is offered
```

Trace: AC-11 → E-3; AC-12 → E-3 and A-2. A-2 assumes one manager login can access every assigned community. Its production validation remains open. The eventual browser selector and real login are not delivered by this contract-design task. These ACs remain **Not yet written** in executable traceability.

## Proposed contract for review

The following are explicit proposals, not settled requirements or existing endpoints. The design task must accept, revise or reject each with a named owner and rationale; unresolved decisions block a later implementation packet.

| Decision | Proposed boundary |
| --- | --- |
| D1 Identity | Local synthetic `X-User-Id` only, within the existing test environment. No login, MFA or invitation flow. |
| D2 Assignment | Read current `memberships` rows with role `manager`. No implicit admin or board access. Assignment/revocation occurs through fixtures only in this slice. |
| D3 Context | `GET /manager/communities` returns only assigned community IDs/names, sorted by ID. `GET /manager/communities/{community_id}/requests` returns the selected community's requests. No global or persisted active-community state. |
| D4 Visibility | A manager may read requests in an assigned community through the proposed manager route. Existing resident endpoints remain self-only, including when a user also manages another community. |
| D5 Response and denial | Reuse the seven public S-1 request fields and existing deterministic ordering. Unknown caller: 401 first. Invalid/unassigned community or wrong role: identical 404 with no request details. An assigned empty community returns an empty list. Confirm the no-manager-assignment selector result explicitly; proposed result is an empty list. |
| D6 Assignment changes | Authorization is evaluated per request. A removed assignment denies subsequent reads; a context selected previously does not grant access. Define the transaction boundary and concurrent revocation semantics before implementation; do not promise immediate cancellation of in-flight reads. |

The existing user/community/membership/request schema appears sufficient for seeded read-only behavior. The design must verify that claim. No migration is authorized; if a schema change is needed, stop and prepare a separate migration proposal. No status-write, tenant access, household visibility, document access, payments or notifications are included. S-1 OQ1/OQ2 remain unresolved.

## Bounded deliverable and owners

Gustavo owns the COMC-10 packet and integration handoff. Kundan reviews requirement meaning, role/assignment semantics and capability mapping. Sandeep reviews the complete isolation test matrix and failure expectations. Codex may draft under approval; it cannot supply their decisions.

After approval, produce these new files:

- `docs/design/S-3-context.md`: typed interfaces, fields/errors, data flow, authorization and revocation rules, invariants, excluded policy questions and decision table.
- `docs/reviews/S-3-context-gapcheck.md`: every unresolved question with owner, dependency and stop instruction.
- `docs/plans/S-3-context-test-plan.md`: fixtures, exact scenario IDs/expected outputs and a proposed tests-first implementation boundary. This is a document, not executable tests.

Also allowed: exact task/approval prompts, a new numbered `LEDGER.md` entry, append-only AISE ledgers, current AISE state/reports and COMC-10 review status. Do not rewrite previous records or approved S-1 criteria.

**Protected:** all application code; all tests/fixtures; migrations; dependencies; Compose/Docker; workflows and verifiers/manifests; AISE hooks/config; existing `docs/design/` files; S-1/S-6 acceptance baselines; `docs/traceability.csv` executable-test claims. New design file above is the sole design-directory addition proposed. No runtime data changes.

## Required test-plan scenarios

These are proposed scenario groups, not tests that currently exist or a promised exact executable case count.

| Group | Given / When | Required observable result |
| --- | --- | --- |
| T01 / AC-12 | M2 manages only Elm Court; list assignments | Only Elm Court is offered; no other IDs/names |
| T02 / AC-11 | M1 manages two communities; select Pine Hollow | Only Pine Hollow requests, with allowed fields/order |
| T03 | Same manager selects Mountain Ridge next | Only Mountain Ridge requests; no retained context contamination |
| T04 | Two managers interleave community reads | Each response follows its own identity/assignment and URL |
| T05 | Missing, malformed or unknown caller with any path | Existing caller-first 401 envelope |
| T06 | Resident, board member or admin without manager assignment | No manager access inferred from role alone |
| T07 | Known manager guesses unassigned/nonexistent/malformed community | Identical 404; no request details |
| T08 | Manager has no assignments, or an assigned community is empty | Explicitly approved empty-result behavior |
| T09 | Assignment removed or role changed after previous successful read | Subsequent read denied; no cached authorization |
| T10 | Manager role exists in A, resident role exists in B | No manager access to B; resident self-only behavior preserved |
| T11 | Equal request timestamps and all stored statuses | Stable ordering and stored values; reads never change state |
| T12 | Full existing S-1/S-6 suite after future implementation | All 120 existing passes and five exact S-6 skips preserved |

Include positive, negative and boundary cases, membership-change transaction assumptions, all four roles, same/cross-community reads and unauthorized-state invariants. Enumerate the final tests only after contract decisions are settled. A future test/CI packet must specify its exact additions and retain all existing IDs and hashes.

## Sequence, checks and stop condition

1. Record this task's actual approval and an undo checkpoint before drafting the three deliverables.
2. Reconcile revised S-3 AC-11/12 against COMC-10's historical invitation/switching scope. Keep invitation and assignment administration separate.
3. Inspect the existing schema and S-1 invariants; draft the proposed contract and test-plan documents without touching protected files.
4. Record named decisions or explicit pending items. Run AISE structure, source-boundary guard, whitespace and protected-path/prefix checks. No Docker rerun is required solely for this documentation work; no new runtime result is claimed.
5. Open a design PR linked to COMC-10. Stop at human review. Prepare an implementation packet only when the contract and test specification are accepted and the team explicitly authorizes expanding beyond the current M1 implementation scope.

S-1 closeout can proceed in parallel as human review work: [acceptance review](../reviews/S-1-acceptance-2026-11-08.md). Do not infer its completion from approval of this packet. No new sprint dates, hours or velocity are assigned without team capacity.

**Approval requested:** “Approve S-3-CTX-1 packet v1 as design and test-plan documentation only.” Approval of the packet is a scope decision; it is not a recorded Kundan/Sandeep contract acceptance.
