# 07 Independent Review

## Metadata

- Artifact ID: REVIEW-0001
- Pipeline ID: AISE-DELIVERY-0001
- Release ID: RELEASE-0001
- Input artifacts: all prior lifecycle artifacts, ledgers, CI/CD, deployment, runtime, TestGuard, and SRA evidence
- Status: Draft
- Reviewer:
- Model:
- Skill version:
- Policy set: AISE-POLICY 0.3.4
- Repository:
- Branch:
- Commit:
- Last updated:

## Executive Verdict

| Dimension | Status | Evidence |
| --- | --- | --- |
| Delivery status | TBD |  |
| Production readiness | TBD |  |
| Evidence integrity | TBD |  |
| Residual risk | TBD |  |
| Risk acceptance | TBD |  |
| Jurisdiction regulatory readiness | TBD |  |
| Engineering maturity readiness | TBD |  |
| Technical delivery baseline readiness | TBD |  |
| Standards governance readiness | TBD | `.agentic-sdlc/reports/standards-governance-review.md` |
| Specification assurance readiness | TBD | `.agentic-sdlc/reports/specification-assurance-review.md` |
| Code change traceability readiness | TBD | `.agentic-sdlc/ledgers/code-changes.jsonl` |
| Security First Development readiness | TBD | `.agentic-sdlc/reports/security-first-review.md` |
| Agent measurement stack readiness | TBD | `.agentic-sdlc/reports/agent-measurement-stack.md` |
| Agent cost and workflow efficacy | TBD | `.agentic-sdlc/reports/agent-cost-efficacy.md` |
| Recommendation | GO / CONDITIONAL_GO / NO_GO / REJECT |  |

## Traceability Review

| Requirement | Design | Scaffold | Test | Implementation | Code Change Ledger | Deployment | Runtime Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 |  |  |  |  | CODE-CHG-0001 |  |  | TBD |

## Code Change Traceability Review

| Ledger ID | Changed Paths | Requirement/Spec/Test Links | Evidence/Decision/Risk Links | Validation Commands | Commit/PR | Finding |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | TBD |

## External Anchor Review

| Material Claim | Generated Artifact Source | External Anchor | Evidence State | Conflict Found | Owner | Result |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | UNKNOWN | TBD |  | TBD |

## Evidence ID Integrity Review

| Stage | Evidence IDs Declared | Ledger Records Found | Acceptable Evidence State | Stable Source Ref | Result |
| --- | --- | --- | --- | --- | --- |
| 00-charter |  |  | TBD |  | TBD |
| 01-requirements |  |  | TBD |  | TBD |
| 02-design |  |  | TBD |  | TBD |
| 03-scaffold |  |  | TBD |  | TBD |
| 04-test |  |  | TBD |  | TBD |
| 05-implementation |  |  | TBD |  | TBD |
| 06-deployment |  |  | RUNTIME_VERIFIED required when complete |  | TBD |
| 07-review |  |  | TBD |  | TBD |

## P0 Coverage Review

| P0 Requirement | Acceptance Criteria | Tests | Runtime Evidence | Finding |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Cross-Stage Inconsistencies

| Finding | Expected | Observed | Evidence | Severity | Owner |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Security, Compliance, Data, and Resilience

Summarize control results and evidence gaps.

## Standards Governance Review

| Domain | Applicability | Binding Authority | Evidence Completeness | Exceptions/Waivers | Release Impact |
| --- | --- | --- | --- | --- | --- |
| Application development standards | TBD |  | TBD |  | TBD |
| Global data management standards | TBD |  | TBD |  | TBD |
| Architecture standards | TBD |  | TBD |  | TBD |
| UX design standards | TBD |  | TBD |  | TBD |
| Records management standards | TBD |  | TBD |  | TBD |
| Security risk standards | TBD |  | TBD |  | TBD |
| Security First Development | TBD |  | TBD |  | TBD |
| Resilience standards | TBD |  | TBD |  | TBD |
| TDD/QA standards | TBD |  | TBD |  | TBD |
| Production readiness standards | TBD |  | TBD |  | TBD |

## Privacy and Regulatory Readiness

| Domain | Applicability | Evidence Completeness | Findings | Release Impact |
| --- | --- | --- | --- | --- |
| General privacy and PII | TBD | TBD |  | TBD |
| Sector-regulated records | TBD | TBD |  | TBD |
| Child, minor, or protected-population data | TBD | TBD |  | TBD |
| Health, safety, disability, or highly sensitive data | TBD | TBD |  | TBD |
| Financial, benefit, entitlement, or eligibility data | TBD | TBD |  | TBD |
| Payment/PCI data | TBD | TBD |  | TBD |
| Biometric, location, employment, or automated-decision obligations | TBD | TBD |  | TBD |
| Jurisdiction regulatory overlays | TBD | TBD |  | TBD |

## Security First Development Review

| Area | Evidence | Result | Residual Risk | Authority |
| --- | --- | --- | --- | --- |
| Security-first SDLC gates | `.agentic-sdlc/reports/security-first-review.md` | TBD |  | ciso_or_security_owner |
| Threat model | `.agentic-sdlc/reports/threat-model.md` | TBD |  | security_architect_or_security_owner |
| Vulnerability risk assessment | `.agentic-sdlc/reports/vulnerability-risk-assessment.md` | TBD |  | security_or_risk_owner |
| Red/blue/purple validation | `.agentic-sdlc/reports/red-blue-purple-team-review.md` | TBD |  | security_operations_or_red_team_owner |
| Executive security risk review | `.agentic-sdlc/reports/executive-security-risk-review.md` | TBD |  | ciso_cro_cfo_or_release_authority |
| CISO/CRO/CFO material-risk decision | decision ledger or risk acceptance | TBD |  | release_or_risk_authority |

## Specification Assurance Review

| Area | Evidence | Result | Gap | Owner |
| --- | --- | --- | --- | --- |
| Specification contracts | `.agentic-sdlc/reports/specification-assurance-review.md` | TBD |  | product_owner_or_ba |
| Preconditions | precondition records and tests | TBD |  | qa_lead_or_product_owner |
| Postconditions | postcondition records, tests, and runtime signals | TBD |  | qa_lead_or_product_owner |
| Invariants | invariant records, tests, and persistent validation | TBD |  | architect_or_technical_owner |
| Exceptions | approved N/A or risk-route decisions with expiry and revalidation | TBD |  | release_or_risk_authority |

## Jurisdiction Regulatory Readiness

| Jurisdiction/Region Group | Trigger Basis | Domains | Source Freshness | Owner Approval | Runtime Controls | Findings | Release Impact |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | current_check_required_before_launch | Pending |  |  | TBD |

| Default-Deny Check | Observed State | Evidence | Finding |
| --- | --- | --- | --- |
| Unreviewed jurisdictions are disabled | TBD |  |  |
| Sector-specific regulated workflows have reviewed domain rules | TBD |  |  |
| Biometric capture, liveness, retention, and deletion are reviewed before enablement | TBD |  |  |
| Protected-population geolocation, profiling, targeted ads, sale/share, and messaging are reviewed before enablement | TBD |  |  |
| Automated eligibility, entitlement, funding, fraud, prioritization, or access decisions are reviewed before enablement | TBD |  |  |
| Breach-notification routing covers affected person jurisdictions | TBD |  |  |

## Runtime Reality

Capture what was observed from the running system and whether it matches the stage artifacts. The running system is the truth for production-readiness review.

## Engineering Maturity Review

| Lane | Status | Evidence | Finding | Owner |
| --- | --- | --- | --- | --- |
| Product discovery | TBD |  |  | product_owner_or_research_owner |
| API contract governance | TBD |  |  | service_owner_or_architect |
| Data migration safety | TBD |  |  | data_owner_or_database_owner |
| Observability and SLOs | TBD |  |  | platform_or_sre |
| Supply-chain provenance | TBD |  |  | security_or_risk_owner |
| Accessibility and UX quality | TBD |  |  | accessibility_or_product_owner |
| Developer experience | TBD |  |  | technical_owner |
| Technical delivery baseline | TBD |  |  | delivery_lead_or_engineering_manager |
| Codebase context management | TBD |  |  | technical_owner |
| Approved stack governance | TBD |  |  | architect_or_technical_owner |
| Test coverage management | TBD |  |  | qa_lead |
| Performance and reliability testing | TBD |  |  | qa_lead_or_sre |
| Component CI/CD automation | TBD |  |  | platform_or_sre |
| Configuration and key management | TBD |  |  | security_or_platform_owner |
| Observability alert quality | TBD |  |  | platform_or_sre |
| Agent measurement stack | TBD | `.agentic-sdlc/reports/agent-measurement-stack.md` |  | delivery_lead_or_engineering_manager |
| Code change traceability management | TBD | `.agentic-sdlc/ledgers/code-changes.jsonl` |  | technical_owner_or_lead_developer |
| Standards governance management | TBD | `.agentic-sdlc/reports/standards-governance-review.md` |  | governance_risk_or_architecture_owner |
| Security First Development management | TBD | `.agentic-sdlc/reports/security-first-review.md` |  | ciso_or_security_owner |
| Threat model management | TBD | `.agentic-sdlc/reports/threat-model.md` |  | security_architect_or_security_owner |
| Vulnerability risk assessment management | TBD | `.agentic-sdlc/reports/vulnerability-risk-assessment.md` |  | security_or_risk_owner |
| Red/blue/purple validation management | TBD | `.agentic-sdlc/reports/red-blue-purple-team-review.md` |  | security_operations_or_red_team_owner |
| Executive security risk governance | TBD | `.agentic-sdlc/reports/executive-security-risk-review.md` |  | ciso_cro_cfo_or_release_authority |
| Application development standard management | TBD |  |  | engineering_standards_owner |
| Global data management standard management | TBD |  |  | data_governance_owner |
| Architecture standard management | TBD |  |  | architecture_owner |
| UX design standard management | TBD |  |  | design_system_or_product_design_owner |
| Records management standard management | TBD |  |  | records_management_or_legal_owner |
| Security risk standard management | TBD |  |  | security_or_risk_owner |
| Resilience standard management | TBD |  |  | sre_or_business_continuity_owner |
| TDD and QA management | TBD |  |  | qa_lead_or_quality_owner |
| Production readiness management | TBD |  |  | release_or_sre_owner |
| Skill execution governance | TBD |  |  | delivery_lead_or_engineering_manager |
| Agent workflow management | TBD |  |  | delivery_lead_or_engineering_manager |
| MCP governance | TBD |  |  | source_system_owner_or_platform_owner |

## Technical Delivery Review

| Area | Expected Evidence | Observed Evidence | Release Impact |
| --- | --- | --- | --- |
| Definition of Ready | readiness evidence was complete before implementation or blockers were handled |  | TBD |
| Definition of Done | done evidence exists for requirements, tests, CI/CD, runtime, controls, and operations |  | TBD |
| Requirements matrix | P0/P1 requirements map to design, code, tests, CI/CD, runtime, privacy, and owner state |  | TBD |
| Approved stack conformance | implementation follows approved/invested stack and architecture style or has exception |  | TBD |
| Codebase context packet | current codebase and cross-codebase impact were reviewed before implementation |  | TBD |
| Contract-first development | API, event, schema, database, job, binary, script, and file contracts are covered where applicable |  | TBD |
| Test coverage | unit, integration, contract, E2E, security, privacy, accessibility, performance, regression |  | TBD |
| Static analysis | SAST/static code analysis, type/lint, dependency, secret, IaC, and container scans |  | TBD |
| Component CI/CD | services, database, jobs, workers, events, binaries, scripts, containers, IaC, docs/artifacts |  | TBD |
| Configuration and keys | config store, environment rules, secret store, key/cert owners, rotation, runtime validation |  | TBD |
| Observability and alerting | APM, traces, logs, metrics, audit events, dashboards, alert criticality, runbooks |  | TBD |
| Agent measurement | open-source-first stack decision, telemetry contract, eval/red-team gates, usage export, redaction, retention, and exceptions |  | TBD |
| Preventive/detective controls | controls have owners, evidence sources, escalation routes, monitoring, and revalidation cadence |  | TBD |
| Persistent validation | synthetic checks, canaries, drift/freshness checks, SLO burn, post-release validation |  | TBD |

## Technical Debt, Lifecycle, SCA, and Runtime Risk Review

| Area | Expected | Observed | Release Impact | Owner |
| --- | --- | --- | --- | --- |
| Technical debt | fix-now debt remediated; material backlog debt has owner, severity, expiry |  | TBD | technical_owner |
| Anti-patterns | known anti-patterns and architecture drift are not expanded without exception |  | TBD | architect_or_technical_owner |
| Outdated/EOL technologies | unsupported versions have upgrade, migration, exception, or block decision |  | TBD | technical_owner |
| Divest technologies | no new or expanded use unless exception is approved |  | TBD | architect_or_technical_owner |
| Unused imports/dependencies | unused imports, code, and dependencies removed or justified |  | TBD | technical_owner |
| SCA/cyber risk | critical, high, reachable, exposed, secret, malware, license, IaC, and container findings triaged |  | TBD | security_or_risk_owner |
| Material vulnerabilities/exposures | exposed or exploitable risks remediated or accepted by correct authority |  | TBD | security_or_risk_owner |
| Service risk assessment | tier, blast radius, dependencies, operations, privacy, security, compliance, residual risk reviewed |  | TBD | release_or_risk_authority |
| Long-running jobs | idempotency, timeouts, cancellation, retries/backoff, DLQ, queue lag/job age alerts, runbooks proven |  | TBD | platform_or_sre |

## Agent Cost And Workflow Efficacy

| Area | Expected Evidence | Observed Evidence | Release Impact |
| --- | --- | --- | --- |
| Measurement prerequisites | `.agentic-sdlc/reports/agent-measurement-stack.md` records selected standards, backend, eval/red-team gates, redaction, retention, and exceptions |  | TBD |
| Usage ledger | material skill and agent runs have records in `.agentic-sdlc/ledgers/usage.jsonl` |  | TBD |
| Per-run cost inputs | tokens, elapsed time, tools, MCP calls, CI/runtime usage, human review, and rework are actual, estimated, or explicitly unknown |  | TBD |
| Cost source and confidence | estimates cite method, source, currency where applicable, confidence, and unknowns |  | TBD |
| Accepted output disposition | outputs are accepted, revised, rejected, duplicate, superseded, or pending with reviewer evidence |  | TBD |
| Workflow efficacy | first-pass completion, evidence completeness, defects found/prevented, policy adherence, and reviewer disposition are summarized |  | TBD |
| Parallelism/co-work efficiency | lead-time benefit is weighed against coordination, merge, duplicate work, and rework cost |  | TBD |
| Improvement actions | expensive, ineffective, noisy, or under-instrumented workflows have owners and next actions |  | TBD |

## Agent and MCP Review

| Workflow | Agents Used | MCP Profiles | Write Scope | Permission Denials | Evidence Output | Result |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | TBD |

## Skill Execution Review

| Skill | Stage | Contract Present | References Loaded | Checks Run | Output Artifact | Stop or Handoff | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | TBD |  |  |  |  | TBD |

## Parallel and Co-Work Review

| Plan | Mode | Lead | Workstreams | Disjoint Scope Proven | Shared File Owner | Merge Evidence | Independent Reviewer | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | TBD |  |  |  | TBD |

## Coordination Loop Review

| Loop | Trigger | Owner | Max Iterations or Stop Condition | Evidence Written | Stop Reason | Release Impact |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | TBD |

## Validation Ladder Review

| Validation Layer | Command or Evidence | Result | Finding |
| --- | --- | --- | --- |
| Repository package validation | `./scripts/validate-package.sh .` | TBD |  |
| Workspace validation | `python3 scripts/validate_project.py --workspace .agentic-sdlc` | TBD |  |
| Strict release validation | `python3 scripts/validate_project.py --workspace .agentic-sdlc --strict-release` | TBD |  |
| JSON/YAML parsing |  | TBD |  |
| Sensitive-data scan | `python3 scripts/guard_sensitive_data.py .agentic-sdlc/artifacts .agentic-sdlc/ledgers .agentic-sdlc/reports` | TBD |  |
| Runtime verification |  | TBD |  |
| Workflow contract review | `.agentic-sdlc/reports/agent-workflow-review.md` | TBD |  |
| Technical delivery review | `.agentic-sdlc/reports/technical-delivery-review.md` | TBD |  |
| Standards governance review | `.agentic-sdlc/reports/standards-governance-review.md` | TBD |  |
| Specification assurance review | `.agentic-sdlc/reports/specification-assurance-review.md` | TBD |  |
| Code change traceability review | `.agentic-sdlc/ledgers/code-changes.jsonl` | TBD |  |
| Security First Development review | `.agentic-sdlc/reports/security-first-review.md` | TBD |  |
| Threat model review | `.agentic-sdlc/reports/threat-model.md` | TBD |  |
| Vulnerability risk assessment review | `.agentic-sdlc/reports/vulnerability-risk-assessment.md` | TBD |  |
| Red/blue/purple team review | `.agentic-sdlc/reports/red-blue-purple-team-review.md` | TBD |  |
| Executive security risk review | `.agentic-sdlc/reports/executive-security-risk-review.md` | TBD |  |
| QA gate review | requirements-to-test matrix, TDD/QA evidence, and TestGuard | TBD |  |
| Production readiness review | artifact, CI/CD, scans, runtime, observability, support, and release authority evidence | TBD |  |
| Cost and efficacy review | `.agentic-sdlc/reports/agent-cost-efficacy.md` | TBD |  |
| Agent measurement stack review | `.agentic-sdlc/reports/agent-measurement-stack.md` | TBD |  |
| Agent eval gate review | eval artifacts, thresholds, and failure routes | TBD |  |
| Agent red-team gate review | red-team artifacts, security findings, and failure routes | TBD |  |

## Open-Source-First Agent Measurement Stack Review

| Area | Expected Evidence | Observed Evidence | Release Impact |
| --- | --- | --- | --- |
| Stack decision | standards/open-source options considered before source-available, managed, or proprietary tooling |  | TBD |
| Telemetry contract | OpenTelemetry GenAI, OpenInference, or approved mapping covers agents, skills, tools, MCP, evals, guardrails, cost, latency, and errors |  | TBD |
| Backend and deployment mode | local/self-hosted preferred; managed or source-available use has license/privacy/security/platform approval |  | TBD |
| Data protection | prompt/completion/tool/MCP capture, redaction, retention, deletion, RBAC, and audit logging are defined |  | TBD |
| Eval gates | DeepEval, Ragas, Inspect, TruLens, MLflow, Phoenix, Langfuse, or approved equivalent has dataset, scorer, threshold, artifact, and owner |  | TBD |
| Red-team gates | promptfoo, Inspect, DeepEval, or approved equivalent tests prompt injection, leakage, MCP misuse, unauthorized action, and excessive agency |  | TBD |
| Usage export | measurement results link to `.agentic-sdlc/ledgers/usage.jsonl`, `evidence.jsonl`, and final cost/efficacy report |  | TBD |

## Findings

| ID | Severity | Registry ID | Title | Evidence | Remediation | Verification | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Risk Acceptance

List proposed, required, approved, expired, and rejected risk acceptances.

## Knowledge Update Proposals

List proposed updates to systems, integrations, patterns, decisions, or policies. Do not mark proposed knowledge as accepted without human review.

## Gate Checks

| Gate | Result | Evidence |
| --- | --- | --- |
| Evidence completeness sufficient for assessment | TBD |  |
| No blocker findings remain | TBD |  |
| Required P0 coverage is complete | TBD |  |
| Deployment/runtime evidence supports release | TBD |  |
| Completed-stage evidence IDs resolve to ledger records with acceptable states | TBD |  |
| Material residual risk has authorized acceptance | TBD |  |
| Material claims were checked against external anchors | TBD |  |
| Privacy and regulatory readiness has owner approval or valid risk decision | TBD |  |
| Jurisdiction regulatory readiness has current source evidence, owner approval, and runtime launch controls | TBD |  |
| Engineering maturity lanes have evidence, owners, and accepted gaps | TBD |  |
| Agent workflow and MCP access stayed within approved boundaries | TBD |  |
| Skill execution contracts, handoff packets, parallel plans, and loop records are complete | TBD |  |
| Validation ladder results are complete and available for release authority | TBD |  |
| Definition of Done is satisfied for technical delivery or exceptions are scoped, approved, and time-bound | TBD |  |
| Standards governance applicability, binding authority, standards-derived controls/tests, exceptions, records, resilience, TDD/QA, and production readiness are complete | TBD |  |
| Specification contracts, preconditions, postconditions, invariants, tests, runtime validation, and exceptions are complete | TBD |  |
| Security First Development gates, threat model, vulnerability risk assessment, red/blue/purple validation, executive risk review, and residual-risk decisions are complete | TBD |  |
| Requirements matrix, approved stack, test coverage, performance, CI/CD, container/runtime, config/key, observability, alerting, and persistent validation evidence are complete | TBD |  |
| Technical debt, outdated/divest technologies, anti-patterns, unused dependencies, SCA/cyber risk, service risk, and long-running job risks are remediated, accepted, or tracked with owners | TBD |  |
| Agent measurement stack decision, telemetry contract, eval gates, red-team gates, usage export, and data controls are complete or explicitly excepted by the right authority | TBD |  |
| Agent cost and workflow efficacy report is complete, with unknown costs explained and improvement actions owned | TBD |  |

## Evidence Envelope

```yaml
attestation:
  stage: 07-review
  input_artifacts:
    - CHARTER-0001
    - REQUIREMENTS-0001
    - DESIGN-0001
    - SCAFFOLD-0001
    - TEST-0001
    - IMPLEMENTATION-0001
    - DEPLOYMENT-0001
  output_artifacts:
    - REVIEW-0001
  evidence_ids: []
  policy_set: AISE-POLICY 0.3.4
  approvals: []
```

## Human Release Decision

- Approver:
- Role:
- Authority:
- Decision:
- Conditions:
- Date:
