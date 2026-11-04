# Workflow Affinity Review

## Metadata

- Report ID: WORKFLOW-AFFINITY-REVIEW-0001
- Pipeline ID: AISE-DELIVERY-0001
- Release ID: RELEASE-0001
- Reviewer:
- Policy set: AISE-POLICY 0.3.4
- Source artifacts:
- Last updated:

## Affinity Matrix

| Stage | Skill or Agent | External Anchor | Controls | Evidence IDs | Validator or Hook | Feedback Target | Authority | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00-charter |  |  |  |  |  | feedback/ |  | TBD |
| 01-requirements |  |  |  |  |  | feedback/ |  | TBD |
| 02-design |  |  |  |  |  | feedback/ |  | TBD |
| 03-scaffold |  |  |  |  |  | feedback/ |  | TBD |
| 04-test |  |  |  |  |  | feedback/ |  | TBD |
| 05-implementation |  |  |  |  |  | feedback/ |  | TBD |
| 06-deployment |  |  |  |  |  | feedback/ |  | TBD |
| 07-review |  |  |  |  |  | feedback/ |  | TBD |

## Evidence Resolution

| Evidence ID | Ledger Record Found | Evidence State | Source Ref | Hash or Immutable Ref | Result |
| --- | --- | --- | --- | --- | --- |
|  | TBD | UNKNOWN |  |  | TBD |

## Validation Ladder

| Layer | Required | Evidence | Result |
| --- | --- | --- | --- |
| repository_validation | yes |  | TBD |
| workspace_validation | yes |  | TBD |
| json_yaml_parse | yes |  | TBD |
| stage_state_validation | yes |  | TBD |
| evidence_id_resolution | yes |  | TBD |
| sensitive_data_scan | yes |  | TBD |
| specification_assurance_review | yes | `.agentic-sdlc/reports/specification-assurance-review.md` | TBD |
| precondition_postcondition_review | yes | specification contract records, precondition records, postcondition records, and executable tests | TBD |
| invariant_review | when stateful, regulated, authorization-sensitive, funding, payment, event, job, scheduler, database, or migration behavior applies | invariant records, invariant tests, and runtime or persistent validation | TBD |
| code_change_traceability_review | yes | `.agentic-sdlc/ledgers/code-changes.jsonl` | TBD |
| standards_governance_review | yes | `.agentic-sdlc/reports/standards-governance-review.md` | TBD |
| security_first_review | yes | `.agentic-sdlc/reports/security-first-review.md` | TBD |
| threat_model_review | when security-significant change or regulated data applies | `.agentic-sdlc/reports/threat-model.md` | TBD |
| vulnerability_risk_assessment_review | yes | `.agentic-sdlc/reports/vulnerability-risk-assessment.md` | TBD |
| red_blue_purple_team_review | when material security risk applies | `.agentic-sdlc/reports/red-blue-purple-team-review.md` | TBD |
| executive_security_risk_review | when material residual risk or financial exposure remains | `.agentic-sdlc/reports/executive-security-risk-review.md` | TBD |
| qa_gate_review | yes | requirements-to-test matrix, TDD/QA evidence, and TestGuard | TBD |
| production_readiness_review | yes | artifact, CI/CD, scans, runtime, observability, support, and release authority evidence | TBD |
| agent_measurement_stack_review | yes | `.agentic-sdlc/reports/agent-measurement-stack.md` | TBD |
| agent_eval_gate_review | when agent evals are triggered | eval artifacts, thresholds, and failure routes | TBD |
| agent_redteam_gate_review | when agent red-team gates are triggered | red-team artifacts, security findings, and failure routes | TBD |
| runtime_verification | if deployment complete |  | TBD |
| risk_gate | yes |  | TBD |
| workflow_contract_review | yes |  | TBD |
| cost_and_efficacy_validation | yes | `.agentic-sdlc/ledgers/usage.jsonl`, `.agentic-sdlc/reports/agent-cost-efficacy.md` | TBD |

## Guardrail Exceptions

| Exception | Control | Scope | Authority | Expiry | Revalidation Condition | Result |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | TBD |
