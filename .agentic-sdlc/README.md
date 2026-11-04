# .agentic-sdlc Workspace

This directory stores durable state for an AISE-governed delivery run.

## Contents

- `config.json`: local policy, stage, assurance, maturity, MCP, and authority configuration.
- `state/pipeline-state.json`: current release state, stage progress, maturity status, approvals, blockers, and evidence IDs.
- `artifacts/`: human-readable lifecycle artifacts from charter through independent review.
- `ledgers/`: append-only JSONL records for intent, evidence, decisions, risks, usage, code-change traceability, cost, and efficacy.
- `reports/`: generated reports such as traceability, TestGuard, SRA, evidence audit, guardrail control, requirements elicitation, specification assurance, threat models, vulnerability risk assessment, red/blue/purple validation, executive security risk, standards governance, agent measurement, cost/efficacy, and maturity readiness reviews.
- `feedback/`: structured downstream-to-upstream defect reports.
- `hooks/`: optional Claude Code hook examples and the sensitive-data guard script.

## Rules

- Model responses are not the system of record. Artifacts and ledgers are.
- Do not mark a stage complete without evidence IDs.
- Do not treat a policy, standard, scanner, hook, review, or runtime signal as a guardrail unless it has an owner, trigger, enforcement point, failure impact, evidence path, and exception route.
- Do not treat evidence IDs as proof unless they resolve to evidence ledger records with acceptable evidence states during strict release validation.
- Do not treat stale, contradicted, superseded, expired, or out-of-scope evidence as release proof.
- Do not treat Markdown or HTML reports as the source of truth unless they reconcile to canonical records or carry an explicit pilot exception.
- Do not reduce workflow rigor without a recorded risk route decision and the required authority.
- Keep workflow affinity explicit: each stage should connect to external anchors, selected skills or agents, controls, evidence, validators, guardrails, human authority, metrics, and feedback.
- Do not accept residual risk without scoped human authority, rationale, expiry, and revalidation conditions.
- Do not bypass, weaken, disable, or downgrade a blocking guardrail without owner, scope, rationale, compensating control, approving authority, expiry, revalidation trigger, and release impact in `reports/guardrail-control-review.md`.
- Do not silently redefine upstream intent. Write feedback and stop when a stage contract is invalid.
- Do not put real regulated data in prompts, tests, examples, reports, model context, logs, or MCP outputs unless the data owner explicitly approves the purpose and scope.
- Do not enable write-capable MCP tools without explicit scope and authority.
- Do not enable a national, multijurisdiction, global, or regulated launch jurisdiction, biometric flow, protected-population flow, sector-specific workflow, data-transfer path, or consequential automated decision until the jurisdiction overlay is reviewed and current.
- Do not use write-capable parallel agents unless their file scopes are disjoint, one owner controls shared files, worktree isolation is used, and completion evidence is recorded.
- Do not use co-work sessions, agent teams, or dynamic workflows without a lead, task or phase plan, loop limits, stop conditions, and independent review.
- Do not hand off work between agents or stages without a handoff packet when the handoff affects requirements, design, tests, source code, data handling, release posture, or regulated access.
- Do not enable source-system adapters or write-capable MCP profiles without owner, purpose, data class, least-privilege scope, prompt-injection treatment, audit route, and kill-switch evidence.
- Do not change workspace, ledger, contract, event, or report schemas without a migration record, compatibility result, validation command, and rollback or exception.
- Do not start material implementation without a standards applicability matrix for application development, global data management, architecture, UX design, records management, security risk, resilience, TDD/QA, and production readiness.
- Do not let agents convert prompts, AI summaries, synthetic users, unresolved ambiguity, or conflicting stakeholder evidence into P0/P1 requirements without source evidence, requirement quality review, scenario coverage, decision authority, and `reports/requirements-elicitation-review.md`.
- Do not treat missing local standards as approval; unknown applicability requires owner review, exception/waiver handling, and release-impact evidence in `reports/standards-governance-review.md`.
- Do not start material implementation when P0/P1 or material behavior lacks preconditions, postconditions, invariant coverage, executable tests, or approved exceptions in `reports/specification-assurance-review.md`.
- Do not treat material source, config, script, database, job, infrastructure, or runtime changes as traceable unless `ledgers/code-changes.jsonl` links changed paths to requirements, specification contracts, tests, evidence, decisions, risks, and commit or pull request references.
- Do not release when runtime postconditions, reconciliation, alerts, audit records, or persistent invariant validation cannot be proven or risk-routed.
- Do not release security-significant changes without Security First Development gates, threat model, vulnerability risk assessment, preventive/detective control evidence, and residual-risk authority in `reports/security-first-review.md`.
- Do not treat red-team findings as closed unless blue-team detection and purple-team validation are proven or a scoped risk decision explains why they are not applicable.
- Do not accept material residual cyber risk without CISO/CRO authority, and do not accept material financial cyber exposure without CFO visibility.
- Do not claim measured agent productivity, quality, safety, cost, or workflow acceleration without an open-source-first `reports/agent-measurement-stack.md` decision, telemetry contract, eval/red-team gate evidence, redaction rules, and usage-ledger export path.
- Do not claim cost savings, agent effectiveness, first-pass quality, or delivery acceleration without `ledgers/usage.jsonl` records, trace links or explicit unknowns, reviewer disposition, and a final `reports/agent-cost-efficacy.md` rollup.
- Do not release user-facing P0 workflows without product outcome metrics, accessibility acceptance criteria, runtime observability, and deterministic run/verify evidence or an approved exception.
