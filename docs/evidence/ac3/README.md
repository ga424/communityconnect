# AC-3 — cross-community list verification

**Runtime verified without a code change; human review remains pending.** Checked November 7, 2026 against merged main `c0b26c34a1514631ec0825633e25473b570feb05`. [COMC-56](https://gkms.atlassian.net/browse/COMC-56) remains In Progress for Kundan/Gustavo review.

The existing AC-3 scenario seeds R1's request in Mountain Ridge, then lists Pine Hollow as R2 and requires an empty list. Fresh [GitHub Actions run 42417030245](https://github.com/ga424/communityconnect/actions/runs/42417030245) passed this test, the same-unit/other-community visibility control, and both cross-community GET/POST rejection cases. The downloaded JUnit was independently checked with the unchanged exact AC-2 verifier.

Full result: **88 passes, two expected AC-4/AC-6 failures on the 501 details stub, five unchanged S-6 skips, zero errors**. The real pytest exit is 1; the approved phase gate passes. Migration update/repeat/rollback/reapply also passed in CI. [Summary and 38 source hashes](summary.json); [JUnit](ci-junit.xml); [merge and branch evidence](merge-state.json).

Source inspection supports the result: `list_requests` resolves the caller's resident membership for the requested community before querying. `own_requests` constrains both `community_id` and `submitted_by` with parameters. Existing denied-write checks compare stored rows before and after. These controls were already delivered in AC-1; introducing another code change for AC-3 would add no required behavior.

No application, test, CI, dependency, migration, design or AISE control was changed. Docker was unavailable locally; all fresh runtime evidence here is from CI. This is an AI verification record, not a new implementation approval or teammate acceptance. It does not prove production authentication, exhaustive authorization coverage, or the unfinished details endpoint.

PRs #5/#6 are merged; the AC-2 fix is on main. Their latest heads were confirmed ancestors of main, no open PR used those heads, remote branches were already absent, and merged local branches were deleted. Automatic post-merge deletion remains enabled. Untracked duplicate files in the original checkout were preserved; this work uses a clean separate worktree.

Next proposed implementation: [AC-4 packet v1](../../plans/AC-4-approval.md), including its explicit AC-6 read-only overlap, 30 test-first contracts and a 120-pass / 0-failure / 5-skip CI phase. No implementation or new tests are approved by this verification record.
