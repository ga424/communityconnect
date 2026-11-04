# Codebase Context

## Metadata

- Report ID: CODEBASE-CONTEXT-0001
- Pipeline ID: AISE-DELIVERY-0001
- Release ID: RELEASE-0001
- Agent: codebase-context-agent
- Policy set: AISE-POLICY 0.3.4
- Repository scope:
- Source artifacts:
- Last updated:

## System Map

| System/Repo | Service/Module | Type | Owner | Evidence State | Source Ref |
| --- | --- | --- | --- | --- | --- |
|  |  | service/module/library/job/binary/script/iac/docs |  | UNKNOWN |  |

## Approved Stack Evidence

| Area | Observed/Approved Value | Source | Lifecycle Status | Divest Policy Status | Owner | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Language/framework/runtime |  |  | unknown | unknown | architect_or_technical_owner |  |
| Package manager/build tool |  |  | unknown | unknown | technical_owner |  |
| Test/static/security tooling |  |  | unknown | unknown | qa_or_security_owner |  |
| Database/migration tooling |  |  | unknown | unknown | data_owner_or_database_owner |  |
| Job scheduler/worker tooling |  |  | unknown | unknown | platform_or_sre |  |
| Observability/APM/logging/tracing |  |  | unknown | unknown | platform_or_sre |  |
| Agent measurement telemetry/eval/red-team tooling |  |  | unknown | unknown | delivery_lead_or_engineering_manager | `.agentic-sdlc/reports/agent-measurement-stack.md` |
| Config/secret/key management |  |  | unknown | unknown | security_or_platform_owner |  |

## Standards Evidence

| Domain | Observed Standard Or Policy | Source | Applicability | Owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| Application development |  |  | unknown | engineering_standards_owner |  |
| Global data management |  |  | unknown | data_governance_owner |  |
| Architecture |  |  | unknown | architecture_owner |  |
| UX design |  |  | unknown | design_system_or_product_design_owner |  |
| Records management |  |  | unknown | records_management_or_legal_owner |  |
| Security risk |  |  | unknown | security_or_risk_owner |  |
| Security First Development |  |  | unknown | ciso_or_security_owner | `reports/security-first-review.md` |
| Resilience |  |  | unknown | sre_or_business_continuity_owner |  |
| TDD/QA |  |  | unknown | qa_lead_or_quality_owner |  |
| Production readiness |  |  | unknown | release_or_sre_owner |  |

## Architecture And Contract Inventory

| Boundary | Style | Contract | Producer | Consumers | Compatibility Evidence | Risk |
| --- | --- | --- | --- | --- | --- | --- |
|  | microservice/modular/event/batch/workflow/hybrid | API/event/schema/database/job/binary/script/file |  |  |  |  |

## Specification Assurance Inventory

| Requirement Or Contract | Preconditions Source | Postconditions Source | Invariant Source | Runtime Signal | Missing Evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | product_owner_ba_or_qa_lead |

## Test, CI/CD, And Quality Inventory

| Component | Existing Checks | Coverage Signals | CI/CD Pipeline | Missing Evidence |
| --- | --- | --- | --- | --- |
|  | build/lint/type/unit/integration/contract/performance/security/privacy/accessibility/regression |  |  |  |

## Runtime And Operations Inventory

| Area | Observed State | Evidence | Owner | Risk |
| --- | --- | --- | --- | --- |
| Environments and config |  |  | platform_or_sre |  |
| Secrets, keys, certificates |  |  | security_or_platform_owner |  |
| Containers and artifacts |  |  | platform_or_sre |  |
| APM, traces, logs, metrics |  |  | platform_or_sre |  |
| Agent workflow traces, evals, red-team gates, and usage export |  |  | delivery_lead_or_engineering_manager |  |
| Alerts, runbooks, incident route |  |  | platform_or_sre |  |
| Persistent validation |  |  | platform_or_sre |  |

## Debt, Lifecycle, And Cyber Risk Inventory

| Finding | Location/Asset | Category | Severity | Evidence State | Recommended Route | Owner |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | technical_debt/antipattern/outdated_version/eol_version/divest_technology/unused_import/unused_dependency/sca_cyber_risk/service_risk/long_running_job | TBD | UNKNOWN | fix_now/backlog/accepted_risk |  |

## Security First Inventory

| Area | Existing Evidence | Missing Evidence | Owner | Risk |
| --- | --- | --- | --- | --- |
| Threat model and abuse cases |  |  | security_architect_or_security_owner |  |
| Vulnerability risk assessment process |  |  | security_or_risk_owner |  |
| SAST/SCA/secrets/IaC/container/API/DAST/pentest/runtime finding sources |  |  | security_or_risk_owner |  |
| Red-team scenarios and blue-team detection |  |  | security_operations_or_red_team_owner |  |
| Purple-team validation and retest process |  |  | security_operations_or_red_team_owner |  |
| Executive residual-risk decision path |  |  | ciso_cro_cfo_or_release_authority |  |

## Cross-Codebase Impact

| Upstream/Downstream | Contract/Dependency | Impact | Owner | Evidence State | Open Question |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | UNKNOWN |  |

## Handoff Summary

| Receiving Agent/Stage | Must Know | Evidence IDs | Blocking Unknowns |
| --- | --- | --- | --- |
| design-agent |  |  |  |
| test-agent |  |  |  |
| implementation-agent |  |  |  |
| testguard-agent | specification contracts, preconditions, postconditions, invariants, exception behavior, executable tests, runtime signals, and unverified guarantees |  |  |
| security-reviewer-agent |  |  |  |
| observability-agent |  |  |  |
| deployment-agent |  |  |  |
