# Bootstrap guardrail map

| Control | Owner | Trigger/enforcement | Evidence/failure action |
| --- | --- | --- | --- |
| Synthetic public data only | Gustavo | Pre-commit/CI sensitive-data scan and review | Guard scan; stop for real records or secrets |
| No silent feature implementation | Kundan | AGENTS.md and per-task plan approval | Jira/ledger; keep 501 stubs until approval |
| Preserve test baseline | Sandeep | Expected-red verifier + protected tests | CI JUnit; reject unexpected failure or changed expectations |
| Disposable data only | Sandeep | APP_ENV=test + cc_test connection guard; no published DB port | Harness/schema checks; stop on wrong config |
| No production eligibility | Gustavo | Health marker; no deploy workflow; AISE pending release state | No release approval or bypass granted |

Initial setup authorized by the recorded user request. Source system write scope: this GitHub repository/PR and COMC Jira delivery records only. No unreviewed personal-data source access or production changes. Hooks are examples; deterministic scans are invoked explicitly. No exception/bypass is authorized. Future failures return to the named owner; only that human can approve a scoped correction. Runtime security monitoring and production controls remain pending.
