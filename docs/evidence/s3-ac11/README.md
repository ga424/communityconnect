# AC11 execution evidence

Gustavo approved S3-AC11 v1, its addendum,52 tests and additive200/0/5 CI phase. PR15/16 were already merged; reviewer tickets66/67 were closed by Gustavo, with no independently authored reviewer disposition.

- Undo: `85547272a0661c1eaadb4bded9cdc50e620603fd`.
- Tests-first: `359f9e6a8a8633d95ac5fbc22d8746a5f9f529d6`; SHA256 `ca65fe6833b940901e51025b6f6a93b1550ecdbe8faba17199d2e8e3eaf55d38`.
- Red:148 passed,52 semantic missing-route failures,zero errors,5 original skips;205 collected; real exit1. Exact52 IDs matched the approved inventory.
- Green:200 passed,zero failures/errors,5 original skips; real exit0. All52 new cases pass without changing the frozen test file.
- New gate accepts the valid control and rejects24 report/manifest/disk defects; all historical gates and self-tests pass unchanged.
- Migration update/repeat/rollback/reapply passed; dedicated services removed; five unrelated Hadoop containers preserved.
- 116 protected path hashes and7 prior ledger prefixes match.

The concurrency cases delegate real validation and observe real PostgreSQL blocking during the final row for both deletion and non-key role change. They release/join workers, verify the first read and confirm denial after commit. Fault cases verify500, lock release and recovery. These establish the bounded transaction behavior, not a network-delivery revocation promise.

[Local summary](local-summary.json), [red evidence](tests-first.json), [approved addendum](../../design/S-3-AC11-contract-addendum.md), [review](../../reviews/S3-AC11-implementation-2026-11-08.md). Final commit/CI evidence will be linked in the publication record and Git provenance notes. Current test warning is the existing Starlette/httpx deprecation; seven historical AISE record warnings remain. No performance/SCA/production-security assurance is claimed.

## Publication

[PR17](https://github.com/ga424/communityconnect/pull/17) is open against main. Implementation commit `026a6c3bdc972a7cf26d6d56ffd336a30097e767` passed [CI42536188957](https://github.com/ga424/communityconnect/actions/runs/42536188957):200 passes,zero failures/errors,five exact S6 skips,real exit0;24 gate controls and migration/cleanup steps verified from downloaded artifacts. [CI summary](ci-summary.json). This metadata publication will trigger its own CI; the final head and run are recorded in the PR/Jira and append-only Git notes under refs/notes/ai-provenance, avoiding a self-referential commit. Result acceptance and merge remain pending.
