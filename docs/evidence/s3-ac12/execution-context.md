# Bounded S3-AC12 execution context

Source PR14 head ba7740354bcc25b2fbcc72e736c15e3c2d128d91 is descended from freshly fetched main de7e609. The isolated feature branch was created from main and fast-forwarded to that preparation history locally; no GitHub PR was merged. AISE remains pinned0.3.4. One sequential agent, no subagents.

Stack: existing Python3.12/FastAPI/Pydantic/psycopg/PostgreSQL17/Liquibase4.33; existing Docker/Compose and GitHub Actions pins unchanged. Reuse app.requests._database_id and models.connection/user_exists; add router in a new module and register only in main. No production URL or identity; APP_ENV=test and cc_test guard stay intact. No logging of synthetic headers needed; no new background jobs or scheduling. No dependencies/schema changes.

Tests: new file only,28 frozen proposed IDs and local synthetic fixtures after shared reset. All125 old expectations and old hashes preserved. Actual red before implementation; actual full green after. CI new additive verifier preserves historical gates and runs migrations, source/structural guards and full suite. Runtime target148 passes,5 exact skips,0 failures/errors. Existing advisories and production/security/performance/accessibility assurance remain outside this increment; no production claim.

Local Docker29.9.2 is accessible with granted socket/network permissions. Use only project cc-s3-ac12-20261108 and a task-specific Buildx configuration under /private/tmp. Preserve all five unrelated Hadoop containers and existing preview files. Remove only this project's containers/volumes when finished. Protected snapshots and previous ledger prefixes are mandatory. Publication opens an implementation PR; merge remains a separate human decision.
