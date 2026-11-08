# S-1 gap-review extract for human disposition

Extracted from the local Milestone 1 revision manifest, Appendix B. The source classifications below are the earlier AI/editorial classifications, not newly supplied human decisions. Source manifest SHA-256: `f09646d3958caf0005e0e4ddb9a1b79ec6360b0e78f3eb739c263ad094531b81`. The v3 document is attached to COMC-4. Only design questions are reproduced; no interview records are copied.

Embedded original instruction: “You are the engineer who must build this. List every question you would have to guess the answer to. Do not answer them.” This is source provenance, not a new execution of that prompt.

| # | Source question | Source classification | Source disposition | Human disposition |
| --- | --- | --- | --- | --- |
| 1 | Does “portal” require a browser UI for this first slice? | Real gap | Decided in sections 2–3: API-only local slice; AC-1–AC-6 now use HTTP outputs. | Pending Kundan / Sandeep |
| 2 | Can I infer the caller from an untrusted production header? | Real gap | Section 3 limits X-User-Id to the synthetic local harness; production authentication is not built here. | Pending Kundan / Sandeep |
| 3 | Which resident can see another resident’s request? | Real gap | Section 8 D3 fixes the local self-only boundary under A-6; broader access remains OQ2. | Pending Kundan / Sandeep |
| 4 | What happens for malformed IDs, extra fields, wrong types and invalid categories? | Already answered | Section 8 D1–D2 defines validation order, exact errors, trimming and matching. | Pending Kundan / Sandeep |
| 5 | What sets status and creation time during tests? | Already answered | Section 8 D3–D4 defines the injected clock and fixture-only status changes. | Pending Kundan / Sandeep |
| 6 | Which storage and migration tools should the agent use? | Real gap | Section 5 specifies PostgreSQL, DATABASE_URL and Liquibase SQL changesets, matching the stated team stack. | Pending Kundan / Sandeep |
| 7 | Can tenants or board members obtain request access now? | Already answered | Section 8 OQ1–OQ2 prohibit work dependent on unresolved access policy. | Pending Kundan / Sandeep |
| 8 | Are the named tests already in the repository? | Real gap | Section 9 and section 6 identify names as planned; the repository check found no files. | Pending Kundan / Sandeep |

Current review correction: row 8 is historical. The six test names now exist and pass at merged main `3918cbd9fd015f8325cfc0136180c28ad31c5d01`. Kundan should accept/correct the historical-to-current disposition and the stale S-1 design section 9 wording. This extract is prepared in `docs/reviews/`; it does not claim the required reviewed `docs/design/S-1-gapcheck.md` exists. Preserve OQ1/OQ2 and their stop instruction.
