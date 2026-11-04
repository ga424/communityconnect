# Tests-first baseline

Status: draft; remote run pending. Local Docker engine unavailable. Local test collection and syntax checks will be recorded with the commit; no application result is inferred from collection.

Expected scaffold run: 4 harness tests pass, 6 S-1 acceptance tests fail on explicit 501 stubs, and 5 S-6 tests skip with AC IDs. All expected results are derived from the design and ACs. S-6 fixture adapter is a proposed test-only interface, not implemented payment behavior. Sandeep must review it before a later payment build.

Harness checks validate Liquibase application, synthetic membership data and schema relationships. Cross-community and same-community access tests exist from the first feature baseline (AC-3/4/5). They cannot pass until authorization behavior is implemented.

A successful expected-red CI job is evidence of test readiness only. It is not a release check, human QA approval, production security validation or completed M1 story.
