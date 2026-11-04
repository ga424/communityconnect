# Codebase context and skill contract

Entry: empty public ga424/communityconnect repository; M1 v3; COMC issues. Approved technology direction: Python/FastAPI/Pydantic/PostgreSQL/Docker/Liquibase. No inherited application code, CI, migrations, jobs or production infrastructure.

Selected skills: pinned AISE init and orchestrate; scaffold and test contracts used for draft setup. Inputs are the approved proposal scope and still-reviewable M1 designs. Output is a draft branch with canonical workspace, drafts, stubs and red baseline, not a completed stage. Checks: workspace validator, sensitive-data scan, syntax, Compose validation, expected red baseline in CI if available. Stop: any mismatch with ACs, unsafe data, failed environment setup, or a feature implementation requiring the next human approval.

Component boundaries: API, PostgreSQL test schema, Liquibase runner and pytest. No web UI, provider adapter or long-running scheduler is enabled. Accessibility, production telemetry/SLO, SCA, SBOM, full security review and deployment controls remain future gates; structural success does not satisfy them. No risk waiver is made.

Team review: Kundan validates S-1 contract/plan, Sandeep validates migrations/test fixtures and S-6 tests, Gustavo reviews integration/provenance. AI inspection is recorded separately. No measurable cost/efficacy data is available.
