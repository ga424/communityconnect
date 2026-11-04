# Testing Assurance Review

## Identity and authority

- Status: Draft — not release evidence
- Release / commit / artifact digest:
- Specification baseline / risk tier:
- Test owner / independent QA reviewer / release authority:
- Guardrail decision and required CI check references:

## Applicability and requirements matrix

Review every family in the framework's `references/testing-assurance.md`. Required, not applicable, and exception are distinct decisions. Record a reviewed rationale for each exclusion; never count excluded work as tested.

| Component / changed paths | Requirement / spec / invariant IDs | Test family | Risk / selection rationale | Required or N/A | Test IDs / command | Tier / budget | Owner / reviewer |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Coverage and acceptance thresholds

| Scope | Line / branch / requirement coverage numerator and denominator | Critical paths | Baseline / target | Exclusions and approval | Result / evidence IDs |
| --- | --- | --- | --- | --- | --- |

## Generated testing campaigns

| Family: property / stateful / fuzz / differential / metamorphic | Oracle / model / property | Generator or corpus digest | Tool/version / settings / seed | Examples or executions / rejects / duration | Limits and isolation | Minimized reproducer / replay command | Defect / regression / evidence IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Mutation review

| Scope / operators / sampling | Baseline evidence | Killed / survived / no coverage / timeout / errors / ignored | Score formula / denominator / raw score | Survivor or exclusion reason | Independent reviewer | Fix / regression / exception / evidence |
| --- | --- | --- | --- | --- | --- | --- |

## Nonfunctional and operational results

| Requirement | Load / stress / spike / soak / recovery / security / accessibility scenario | Environment and data limits | Metric / target / actual | Result | Report hash / evidence IDs |
| --- | --- | --- | --- | --- | --- |

## Execution completeness and reproducibility

| Suite / CI job | Release identity / environment fingerprint | Command / versions / timestamp | Collected / passed / failed / skipped | Shards expected / completed | Retry history / quarantine | Raw report / ledger evidence | Gate result |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Gaps and exceptions

| Gap / defect | Impacted requirement / component | Blocking status | Compensating test or control | Authority / decision ID | Expiry | Remediation owner / due date |
| --- | --- | --- | --- | --- | --- | --- |

## Cost and efficacy

| Campaign | Budget / actual duration | Compute and agent cost / usage ledger IDs | Unique actionable defects | Escaped defects / follow-up | Stable-scope comparison / action |
| --- | --- | --- | --- | --- | --- |

## Release recommendation

- Ready criteria satisfied, including independent oracles and safe fixtures:
- Done criteria satisfied, including regression preservation and survivor triage:
- Required checks configured and failure-to-block behavior verified:
- Enforcement still dependent on manual review:
- Residual risk and unresolved contradictory or stale evidence:
- TestGuard recommendation / QA decision / release authority / date:

Missing, skipped, zero-test, incomplete or failed required runs are not passes. Report percentages only with their scope and denominator; do not claim defect-free software.
