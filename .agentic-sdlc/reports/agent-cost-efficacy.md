# Agent Cost And Efficacy

## Metadata

- Report ID: AGENT-COST-EFFICACY-0001
- Pipeline ID: AISE-DELIVERY-0001
- Release ID: RELEASE-0001
- Reviewer:
- Policy set: AISE-POLICY 0.3.4
- Source artifacts:
- Usage ledger: `.agentic-sdlc/ledgers/usage.jsonl`
- Measurement stack report: `.agentic-sdlc/reports/agent-measurement-stack.md`
- Last updated:

## Agent And Skill Run Register

| Run ID | Worker | Type | Stage/Lane | Purpose | Inputs | Outputs | Evidence IDs | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-0001 |  | skill / agent / subagent / background_task / co_work / dynamic_phase / batch_verification |  |  |  |  |  | pending |

## Per-Run Cost Inputs

| Run ID | Model/Runtime | Reasoning Effort | Elapsed Time | Input Tokens | Output Tokens | Tool Calls | MCP Calls | CI Minutes | Human Review Minutes | Cost Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-0001 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | 0 | 0 | UNKNOWN | UNKNOWN | unavailable | unknown |

## Measurement Stack Inputs

| Area | Source | Selected Tooling | Evidence | Unknowns |
| --- | --- | --- | --- | --- |
| Telemetry standard | `.agentic-sdlc/reports/agent-measurement-stack.md` | OpenTelemetry/OpenInference/OpenLLMetry/TBD |  |  |
| Trace/eval backend | `.agentic-sdlc/reports/agent-measurement-stack.md` | MLflow/Langfuse/Helicone/AgentOps/TruLens/Phoenix/TBD |  |  |
| Eval gates | test and CI artifacts | DeepEval/Ragas/Inspect/TruLens/MLflow/Phoenix/Langfuse/TBD |  |  |
| Red-team gates | security test artifacts | promptfoo/Inspect/DeepEval/TBD |  |  |
| Data controls | privacy/security/license approvals | redaction, retention, deletion, RBAC, audit logging |  |  |

## Cost Summary

| Scope | Model Cost | Tool/API Cost | CI/Runtime Cost | Human Effort | Total Estimate | Actual/Estimated/Unknown | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Total release | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 0 Charter | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 1 Requirements | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 2 Design | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 3 Scaffold | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 4 Test | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 5 Implementation | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 6 Deployment | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |
| Stage 7 Review | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |  |

## Efficacy Summary

| Dimension | Expected | Observed | Evidence | Result |
| --- | --- | --- | --- | --- |
| Accepted outputs | approved artifacts or changes match requested scope |  |  | TBD |
| Evidence completeness | material claims have evidence IDs and source refs |  |  | TBD |
| First-pass quality | downstream stages did not need preventable rework |  |  | TBD |
| Requirement quality | acceptance criteria and requirements matrix were usable by design/test agents |  |  | TBD |
| Test and coverage quality | tests mapped to requirements, changed code, critical paths, and risk |  |  | TBD |
| Risk discovery | technical debt, lifecycle, SCA/cyber, service, and job risks were routed |  |  | TBD |
| Policy adherence | guardrails, hooks, MCP boundaries, and human authority were respected |  |  | TBD |
| Measurement integrity | trace capture, usage export, eval gates, red-team gates, and redaction controls support the claims |  | `.agentic-sdlc/reports/agent-measurement-stack.md` | TBD |
| Runtime confidence | deployment, observability, alerting, and persistent validation improved release confidence |  |  | TBD |

## Worker Efficacy

| Worker | Useful Outputs | Confirmed Findings | Unsupported Claims | Rework Required | Defects Found or Prevented | Reviewer Disposition | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | accepted / revised / rejected / duplicate / pending | TBD |

## Parallel And Co-Work Efficiency

| Workflow | Workers | Intended Lead-Time Benefit | Coordination Cost | Merge/Rework Cost | Defects Introduced or Prevented | Net Assessment |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | TBD |

## Cost Unknowns And Instrumentation Gaps

| Unknown | Reason | Impact | Instrumentation Needed | Owner |
| --- | --- | --- | --- | --- |
| Token or model cost | runtime did not expose value / not recorded / not applicable |  | usage export, billing integration, or manual estimate method | delivery_lead_or_engineering_manager |
| Measurement backend | not selected / not deployed / not exportable / source-available exception unresolved |  | open-source-first stack decision and trace/eval export path | delivery_lead_or_engineering_manager |

## Improvement Actions

| Action | Trigger | Expected Benefit | Owner | Due |
| --- | --- | --- | --- | --- |
|  | high cost, low efficacy, missing usage, repeated rework, weak evidence, or noisy findings |  |  |  |

## Final Interpretation

- Total estimated cost:
- Actual cost evidence available:
- Unknown cost limitations:
- Measurement stack support:
- Most effective worker or workflow:
- Least effective worker or workflow:
- Parallelism/co-work assessment:
- Efficacy verdict: effective / partially_effective / ineffective / unmeasured
- Required changes before next release:
