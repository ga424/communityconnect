# Agent Measurement Stack

## Metadata

- Report ID: AGENT-MEASUREMENT-STACK-0001
- Pipeline ID: AISE-DELIVERY-0001
- Release ID: RELEASE-0001
- Owner:
- Reviewers: delivery lead, platform/SRE, security, privacy/data owner, legal/procurement where applicable
- Policy set: AISE-POLICY 0.3.4
- Source artifacts:
- Last updated:

## Decision Summary

| Plane | Selected Option | Classification | Deployment Mode | Decision | Owner | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Telemetry standard | OpenTelemetry GenAI / OpenInference / other | open-source-first / source-available / managed / disabled | local / self-hosted / managed / none | TBD | platform_or_sre |  |
| Trace and cost backend |  | open-source-first / source-available / managed / disabled | local / self-hosted / managed / none | TBD | platform_or_sre |  |
| Agent workflow orchestration |  | open-source-first / source-available / managed / disabled | local / self-hosted / managed / none | TBD | delivery_lead_or_engineering_manager |  |
| Eval gates |  | open-source-first / source-available / managed / disabled | local / CI / managed / none | TBD | qa_lead |  |
| Red-team gates |  | open-source-first / source-available / managed / disabled | local / CI / managed / none | TBD | security_or_risk_owner |  |
| Policy and security validation |  | open-source-first / enterprise-approved / disabled | local / CI / managed / none | TBD | security_or_risk_owner |  |

## Open-Source-First Candidate Assessment

| Candidate | Plane | Intended Use | License/Edition Review | Data Review | Stack Fit | Decision | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenTelemetry GenAI semantic conventions | standard | span and metric naming | TBD | TBD | TBD | adopt / reject / defer |  |
| OpenInference | standard/instrumentation | LLM, agent, tool, MCP, guardrail, evaluator spans | TBD | TBD | TBD | adopt / reject / defer |  |
| OpenLLMetry | instrumentation | provider/framework tracing | TBD | TBD | TBD | adopt / reject / defer |  |
| MLflow | observability/evals | tracing, evals, experiments, cost/latency | TBD | TBD | TBD | adopt / reject / defer |  |
| Langfuse | observability/evals | traces, prompts, datasets, metrics | TBD | TBD | TBD | adopt / reject / defer |  |
| Helicone | observability/gateway | gateway, sessions, cost/latency | TBD | TBD | TBD | adopt / reject / defer |  |
| AgentOps | observability | agent replay, cost tracking, framework integrations | TBD | TBD | TBD | adopt / reject / defer |  |
| TruLens | evals/observability | step scoring and cost/quality comparison | TBD | TBD | TBD | adopt / reject / defer |  |
| Arize Phoenix | observability/evals | traces, evals, datasets, prompt iteration | TBD | TBD | TBD | adopt / reject / defer | source-available/license posture must be reviewed |
| LangGraph | orchestration | durable workflow, human-in-loop, retries | TBD | TBD | TBD | adopt / reject / defer |  |
| Microsoft AutoGen | orchestration/evals | existing AutoGen estates only | TBD | TBD | TBD | adopt / reject / defer | maintenance-mode posture must be reviewed |
| DeepEval | evals | task completion, tool correctness, goal accuracy | TBD | TBD | TBD | adopt / reject / defer |  |
| Ragas | evals | RAG and agent metrics | TBD | TBD | TBD | adopt / reject / defer |  |
| Inspect | evals | coding, tool, sandboxed, and external-agent evals | TBD | TBD | TBD | adopt / reject / defer |  |
| promptfoo | red-team/evals | injection, leakage, excessive agency, MCP safety | TBD | TBD | TBD | adopt / reject / defer |  |

## Telemetry Contract

| Signal | Required Attributes | Content Capture | Redaction/Masking | Destination | Evidence |
| --- | --- | --- | --- | --- | --- |
| Agent run | run_id, worker, stage, workflow_mode, model/runtime | none / metadata / sampled / full | TBD | usage.jsonl / OTEL backend |  |
| LLM call | model, token counts, latency, finish reason, error | none / metadata / sampled / full | TBD | usage.jsonl / OTEL backend |  |
| Tool call | tool, arguments classification, result classification, duration, error | none / metadata / sampled / full | TBD | usage.jsonl / OTEL backend |  |
| MCP call | server, profile, tool, data class, scope, duration, error | none / metadata / sampled / full | TBD | usage.jsonl / OTEL backend |  |
| Guardrail | policy, decision, reason, blocked content class | metadata only | required | evidence.jsonl / OTEL backend |  |
| Evaluator | scorer, dataset, threshold, result, judge model where applicable | metadata / redacted examples | required | eval report / CI artifact |  |

## Eval And Red-Team Gates

| Gate | Tool | Dataset/Scenario Source | Threshold | Failure Route | CI Command | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Agent task completion | DeepEval / Inspect / other |  |  | fail build / risk / backlog |  |  |
| Tool correctness | DeepEval / Inspect / other |  |  | fail build / risk / backlog |  |  |
| RAG quality | Ragas / Phoenix / other |  |  | fail build / risk / backlog |  |  |
| Prompt injection | promptfoo / Inspect / other |  |  | fail build / security finding |  |  |
| Data leakage | promptfoo / DeepEval / other |  |  | fail build / privacy finding |  |  |
| MCP misuse | promptfoo / Inspect / other |  |  | fail build / MCP profile review |  |  |

## Usage Ledger Export

| Source | Export Method | Fields Exported | Frequency | Owner | Validation |
| --- | --- | --- | --- | --- | --- |
| Local AISE wrapper/manual record | append JSONL | run_id, worker, stage, usage, cost, outcome | per material run | delivery_lead_or_engineering_manager | JSONL parse |
| Trace backend | API/export/link | trace_id, token counts, latency, errors, tool calls | per review or CI run | platform_or_sre | stable trace link |
| CI eval artifacts | artifact/link | eval IDs, scorer, threshold, result | per CI run | qa_lead | CI status |
| Red-team artifacts | artifact/link | scenario, finding, severity, result | per CI run or release | security_or_risk_owner | CI status |

## Privacy, Security, And Retention

| Control | Expected State | Observed State | Owner | Evidence |
| --- | --- | --- | --- | --- |
| Raw regulated data capture disabled by default | yes | TBD | privacy_or_data_owner |  |
| Prompt/completion content redacted or sampled by policy | yes | TBD | privacy_or_data_owner |  |
| MCP/tool outputs bounded and scrubbed | yes | TBD | source_system_owner_or_platform_owner |  |
| Self-hosting or approved data residency recorded | yes | TBD | platform_or_sre |  |
| Retention and deletion configured | yes | TBD | platform_or_sre |  |
| SSO/RBAC/audit logging reviewed | yes | TBD | security_or_risk_owner |  |

## Rollout Plan

| Level | Target State | Current State | Gap | Owner | Due |
| --- | --- | --- | --- | --- | --- |
| 0 Template-only | templates and unknown-cost rules exist | TBD |  | delivery_lead_or_engineering_manager |  |
| 1 Local usage record | usage.jsonl records material runs | TBD |  | delivery_lead_or_engineering_manager |  |
| 2 Standards telemetry | OTEL/OpenInference spans emitted | TBD |  | platform_or_sre |  |
| 3 CI eval gates | eval and red-team gates run in CI | TBD |  | qa_lead/security_or_risk_owner |  |
| 4 Production feedback loop | traces, evals, feedback, costs, and incidents feed backlog | TBD |  | release_or_risk_authority |  |

## Findings And Exceptions

| ID | Severity | Finding | Decision Needed | Owner | Expiry |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Final Measurement Recommendation

- Recommended stack:
- Disabled or deferred tools:
- Source-available or managed exceptions:
- Regulated-data constraints:
- Required implementation work:
- Required approval before production use:
