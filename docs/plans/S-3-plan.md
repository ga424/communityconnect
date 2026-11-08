# S-3 sequence and review gates

The original design/test-plan deliverable is merged in PR13. [COMC-10](https://gkms.atlassian.net/browse/COMC-10) remains In Progress; neither route nor browser selector is implemented. Revised source uses S3/AC11/AC12, superseding COMC-10's legacy identifiers for this slice.

| Order | Bounded work | Status and dependency |
| --- | --- | --- |
| 1 | Review S3 contract and tests; decide AC12 addendum | Packet prepared; Kundan contract, Sandeep test and Gustavo scope decisions pending |
| 2 | [COMC-62 / S3-AC12 v1](S-3-AC12-approval.md): community options API | To Do awaiting approval;28 proposed cases; current CI remains120/0/5 |
| 3 | AC11 selected-community request reads | Not authorized; separate packet must settle transaction-stable membership, denial precedence, fields/status/order and concurrency tests |
| 4 | Browser selector and selected-request view | Not authorized; separate UI/Playwright packet after API contracts, with actual user-facing AC11/12 evidence |
| 5 | S3 result acceptance | Named team review of API and UI evidence; no completion from API-only results |

This ordering limits review size; AC12 does not itself grant request access. AC11 must independently recheck authorization. No sprint dates or capacity estimates were invented. M1 remains the existing S1 implementation submission boundary; later product increments use supplemental traceability. COMC16's dependency on community authorization is not satisfied by a plan or an options list alone.
