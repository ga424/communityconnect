# Ledgers

The ledger files in this directory are append-only JSONL records.

- `intent.jsonl`: business outcomes, journeys, capabilities, requirements, and acceptance criteria.
- `evidence.jsonl`: machine, human, runtime, and source-of-record evidence.
- `decisions.jsonl`: architecture, policy, test, deployment, and risk decisions.
- `risks.jsonl`: findings, risks, waivers, and risk acceptances.
- `usage.jsonl`: skill, agent, tool, MCP, CI, runtime, human-review, cost, and efficacy records.
- `code-changes.jsonl`: code and file changes produced through AISE, linked to requirements, specification contracts, tests, evidence, decisions, risks, commits, branches, and pull requests.

Each non-empty line must be valid JSON. Prefer stable IDs, timestamps, source references, evidence state, confidence, owner, and related artifact IDs.

Code-change records should use `record_type: "code_change"` and include:

- `id`, `created_at`, `stage`, `agent`, `skill`, `change_type`, `change_materiality`, `paths`, `summary`, and `evidence_state`.
- Trace links such as `requirement_ids`, `acceptance_criterion_ids`, `specification_contract_ids`, `precondition_ids`, `postcondition_ids`, `invariant_ids`, `test_ids`, `evidence_ids`, `decision_ids`, and `risk_ids`.
- Delivery links such as `validation_commands`, `commit`, `branch`, and `pull_request`.

For material implementation work, do not leave `code-changes.jsonl` as a narrative-only audit trail. It should be specific enough for Stage 7, TestGuard, reviewers, and release approvers to trace each changed path back to approved specification and verification evidence.

## Append-only corrections
A record with `supersedes` replaces the interpretation of the named earlier record for human review while preserving its history. These correction links are not currently resolved automatically by the bundled structural validator; consumers must follow the chain and must not count superseded rows as additional completed work. A machine_verified code-change record proves the stated content/check scope only, not that linked ACs passed. Runtime evidence names its own tested commit.
