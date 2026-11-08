# COMC-16 manager announcements — readiness packet

Revised mapping: **S-5, AC16/17**, evidence trace E-4/E-13. Legacy S-8/AC20/21 below the Jira history is not the current milestone numbering. This ticket remains a future product capability; no announcement endpoint, worker or email delivery exists.

## Confirmed product decisions

Gustavo confirmed on November8 that board approval is required **for each target community**, and **one designated board approver** can grant it. These are human product decisions, not new interview evidence. The existence and identity of a designation must be verified by the eventual authorization model; a generic board role alone must not silently make every board member a designated approver.

The revised AC16 precondition now means every delivered community has satisfied that approval rule. AC17 still requires that an unrelated community receive neither feed content nor email. The source requirement is preserved; no original E/A/Q log is silently rewritten. Q2's broad approval question is answered by the user; the implementation mechanics below remain open.

## Required contract before code

1. Manager authorization must be checked separately from board approval for each community. COMC-10 provides the proposed assignment/context dependency; its contract/implementation is not yet accepted or delivered.
2. Specify who designates/removes the approver and how assignment changes take effect. The current single-membership schema does not yet represent designated approval authority. Propose a schema/migration and recovery plan in the later design; do not add it implicitly.
3. Approval must reference an exact notice revision and community. Proposed invariant: edits invalidate prior approvals for the changed revision. This is a technical proposal requiring contract acceptance, not an already implemented fact.
4. **Confirmed by Gustavo:** publish only to approved communities and show the remainder as pending. Return per-community approved/published/pending state so the manager can see what was delivered. No feed/email effect occurs for a pending target. Define retry/failure states separately; approval does not guarantee delivery success.
5. Define retry/deduplication and recipient snapshot semantics. Proposed delivery key includes notice revision, community, resident and channel; repeated worker runs must not create duplicate feed/email effects. External email remains captured/synthetic until separately authorized.
6. Keep board-authored publication (COMC-15) and manager multi-community publication distinct. Review existing COMC-15→16 dependency and add the direct COMC-10→16 assignment dependency without deleting history.

## Test-plan cases to derive after decisions

| Scenario | Observable condition |
| --- | --- |
| Approved manager notice for two authorized communities | One feed entry and one captured email per intended resident under the approved recipient policy |
| Missing approval in one target | No delivery to that target; approved targets publish; unapproved targets remain visibly pending |
| Caller is not designated approver | Approval refused even if caller has a general board role |
| Designated approver for A tries approving B | Refused; no B authorization inferred |
| Manager not assigned to approved target | Publication refused for that target despite its board approval |
| Text/revision changed after approval | Stale approval cannot authorize changed content |
| Assignment/approval removed before publication | Re-evaluate authority; no stale cached authorization |
| Repeated publish/worker retry | No duplicate user-visible effects for the approved delivery identity |
| Unrelated community / AC17 | Neither feed entry nor captured email |
| Persistence/delivery failure | Defined atomicity/retry outcome, no unauthorized partial effect |

## Stop and next artifact

Kundan reviews product meaning, Sandeep reviews authorization/transaction tests, Gustavo coordinates decisions. Produce a bounded design/migration/test-first packet after the remaining designation-authority and delivery-contract decisions; do not implement announcement delivery, real email or approval-schema changes under this readiness record. No current traceability row is marked as an existing test.
