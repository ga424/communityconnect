# S3-AC11 implementation review — November 8, 2026

The selected-community manager API passes all52 approved cases. Full local phase:200 passes,zero failures/errors,five unchanged S6 skips. No blocking finding in this bounded AI code review. Human result/merge review and any independently authored teammate sign-off remain separate.

## Behavior and code inspection

The new router parses identity before the raw community path on matched routes, uses the unchanged database-ID parser and response model, and issues parameterized SQL. Its membership query locks the exact user/community/manager row independently of request rows; unit_id is irrelevant and empty communities still require authorization. It reads only the selected community, projects exactly seven fields, orders by timestamp then ID descending, and validates all rows inside the connection context. There are no writes, remembered selection, broad exception handlers, resident changes, migrations or new dependencies. app/main.py has only the router import/registration.

A committed removal/role change denies the next read. An already-authorized read can finish before revocation commits. No lock is promised during HTTP delivery. Existing DB foreign keys tie manager assignments to actual communities. An absent path segment remains an unmatched framework route, outside matched-route error precedence.

## Evidence and integrity

Tests-first359f9e6a8a8633d95ac5fbc22d8746a5f9f529d6 predates all application changes. The real red run had52 failures and148 passes,zero errors,five skips. The unchanged52 cases now pass, including actual concurrent delete/non-key update blocking, transaction cleanup on validation failure, connection-failure recovery, no writes and resident regression controls. Literal fixture expectations are independent of the serializer. Test-local bounded waits and PostgreSQL lock observations are used; no production hooks or sleep-only lock oracle.

The additive gate freezes the old AC12 manifest, recursively validates previous manifests, preserves all153 expectations and test hashes, and requires52 exact new passes. Actual pytest exit0 is mandatory. The24 adversarial controls and all previous gate controls pass.116 protected files and prior ledger prefixes match. Source guard/structure/whitespace checks pass with seven pre-existing structural warnings. Migration update/repeat/rollback/reapply passed and dedicated test services were removed. Five unrelated Hadoop containers remain. Remote CI is pending publication.

## Remaining boundaries and owners

- Gustavo: review the implementation PR result; merge is not authorized by the task scope approval.
- Kundan/Sandeep: independently authored review remains unverified; Jira closures by Gustavo are recorded accurately. Full-story/course reviews remain open.
- Sandeep (before a browser or release increment): review existing TestClient deprecation, dependency/image pinning and SCA. No dependency upgrade in this scope; revalidate when that increment is proposed.
- Gustavo/team (before expanding volume or deploying): bound list volume/pagination and request/DB timeout/SLO decisions. Current unpaginated read matches the approved small synthetic fixture contract; no performance target was approved or measured.
- Browser switching/Playwright, production identity/MFA, assignment administration and S3 full-story acceptance remain undelivered. S6 remains intentionally unbuilt; M1's S1-only submission scope is unchanged.

Approved Python/FastAPI/Pydantic/PostgreSQL stack and codebase patterns are retained. No regulated records, real payments, production data or new jurisdiction is introduced. Local R1–R4 contract coverage is verified; production assurance, accessibility, coverage percentages and load performance are not claimed.

Tracked nonblocking risks: existing TestClient deprecation (P3, Sandeep, review before the next test/dependency increment); unpaginated volume and missing production timeouts/SLOs (P2 for future deployment, Gustavo/team, resolve before shared or production use). Revalidate these boundaries when a new scope is proposed.
