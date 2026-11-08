# S3-AC12 execution evidence

The options API is implemented and locally verified on the feature branch. Actual result:148 passed,0 failures/errors,5 exact S6 skips, pytest exit0. [Summary](local-summary.json) freezes runtime source hashes, JUnit hash, image identity and cleanup. CI and final commit evidence are recorded in the implementation PR and Git provenance notes after publication.

## Approval and provenance

Gustavo's original scope approval covers packet v1, addendum,28 tests and CI phase. He later reported both review tickets completed; Jira shows COMC63/64 closures by him. [Actual attribution](owner-completion-confirmation.json) and [exact prompts](../../../prompts/2026-11-08-s3-ac12-execution-confirmation.txt) preserve this distinction. Independent Kundan/Sandeep-authored acceptance was not supplied. No merge/production release is inferred. Main de7e609 was fetched; the new branch includes unmerged PR14's preparation ancestry, without merging any GitHub PR.

## Tests-first chain

Undo point6c514dd precedes tests-first commit5b5a1d6. [Frozen baseline](tests-first.json):153 exact IDs,120 passes,28 semantic404 failures for the absent route,0 errors and5 unchanged skips, exit1. Test-file SHA256 remains b9455f1fa62b2ec439956be42dc972d31e8e5fae52117980c770d615bb70ca3d after implementation. All28 proposed IDs match; the original125 expectation records are unchanged.

Readable red logs/JUnit had trailing whitespace from Docker/pytest, caught by diff checking. Those presentation copies were normalized; original byte-for-byte versions are retained in gzip archives and [hash mapping](red-evidence-normalization.json). Case attributes and failure messages were compared before/after. No executable test changed and no prior ledger was rewritten.

## Checks

- [Local JUnit](local-junit.xml), [output](local-output.txt), [actual exit](local-exit-code.txt).
- [Migration output](migration-output.txt): update, repeat, rollback one, reapply; exit0.
- [New gate controls](gate-self-test.json): valid control accepted and24 defective reports/manifests/files rejected. Original AC1/AC2/S1 historical-report gates and self-tests pass.
- Frozen protected paths and all prior ledger prefixes preserved; compile/source/structural/whitespace checks complete before publication. Six historical structural warnings remain documented. One new review-record stage omission is retained and corrected with an append-only complete record; the structural validator still reports its original warning.
- Only the dedicated cc-s3-ac12-20261108 project was removed. All five previously running Hadoop containers remain. Preview files untouched.

Known limit: test identity is spoofable and local-only; no AC11 endpoint, browser selector, production identity, real money or full S3 acceptance. Current dependency/runtime advisory work remains separate; the existing Starlette/httpx warning is disclosed. No new broad SCA/security/performance/accessibility assurance is claimed.
