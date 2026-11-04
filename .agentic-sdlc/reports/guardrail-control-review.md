# Guardrail Control Review

## Review Summary

- Review ID:
- Release ID:
- Scope:
- Guardrail profile:
- Reviewer:
- Review date:
- Verdict: GO | CONDITIONAL_GO | NO_GO | REJECT | NOT_RUN
- Evidence IDs:

## Guardrail Profile

| Domain | Trigger | Guardrail IDs | Required controls | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| Authority | TBD | TBD | TBD | TBD | pending |
| Scope | TBD | TBD | TBD | TBD | pending |
| Specification | TBD | TBD | TBD | TBD | pending |
| Engineering | TBD | TBD | TBD | TBD | pending |
| Security and privacy | TBD | TBD | TBD | TBD | pending |
| Operational | TBD | TBD | TBD | TBD | pending |
| Agent workflow | TBD | TBD | TBD | TBD | pending |
| Evidence | TBD | TBD | TBD | TBD | pending |

## Guardrail Decision Table

| Guardrail ID | Trigger | Expected state | Evidence required | Enforcement mode | Enforcement point | Failure impact | Owner | Exception path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | preventive/detective/corrective/advisory | TBD | TBD | TBD | TBD |

## Enforcement Point Map

| Enforcement point | Controls covered | Tool or process | Blocking? | Evidence IDs | Owner |
| --- | --- | --- | --- | --- | --- |
| Stage gate | TBD | TBD | yes/no | TBD | TBD |
| Validator | TBD | TBD | yes/no | TBD | TBD |
| Hook | TBD | TBD | yes/no | TBD | TBD |
| CI/CD gate | TBD | TBD | yes/no | TBD | TBD |
| Scanner | TBD | TBD | yes/no | TBD | TBD |
| Runtime monitor | TBD | TBD | yes/no | TBD | TBD |
| Independent review | TBD | TBD | yes/no | TBD | TBD |
| Adapter or MCP profile | TBD | TBD | yes/no | TBD | TBD |

## Blocking Guardrail Results

| Control or guardrail | Result | Evidence basis | Affected artifacts | Owner | Remediation or exception | Release impact |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | PASS/WARN/FAIL/REJECT/NOT_APPLICABLE | deterministic/structural/heuristic | TBD | TBD | TBD | TBD |

## Bypass And Exception Review

| Exception ID | Guardrail/control | Scope | Rationale | Compensating control | Approver | Expires | Revalidation trigger | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | proposed/approved/rejected/expired |

## Runtime Guardrails

| Runtime signal | Linked guardrail/control | Data safety review | Criticality | Destination | Runbook | Owner | Evidence IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | critical_page/urgent_business_hours/fyi_ticket/audit_only/suppressed | TBD | TBD | TBD | TBD |

## Developer And Agent Non-Conformance

| Finding ID | Source | Location | Observed behavior | Expected behavior | Severity | Route | Owner | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | developer/agent/imported_artifact/mcp/dependency | TBD | TBD | TBD | TBD | fix_now/backlog/exception/risk_acceptance | TBD | TBD |

## Metrics

| Metric | Target | Observed | Result | Evidence IDs |
| --- | --- | --- | --- | --- |
| guardrail_coverage_rate | TBD | TBD | TBD | TBD |
| blocking_guardrail_failure_age | TBD | TBD | TBD | TBD |
| guardrail_exception_expiry_compliance | TBD | TBD | TBD | TBD |
| guardrail_false_positive_rate | TBD | TBD | TBD | TBD |
| runtime_guardrail_signal_health | TBD | TBD | TBD | TBD |

## Release Recommendation

Summarize whether guardrails are enforceable, whether bypasses are authorized and current, whether runtime controls are proven, and which conditions must be met before release.
