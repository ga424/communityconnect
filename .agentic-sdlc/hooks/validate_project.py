#!/usr/bin/env python3
"""Validate an initialized .agentic-sdlc workspace."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


COMPLETE_STATUSES = {"complete", "completed", "approved", "done", "verified"}
ACCEPTED_RISK_STATUSES = {"accepted", "approved", "closed", "resolved", "waived"}
ACCEPTABLE_EVIDENCE_STATES = {
    "human_confirmed",
    "machine_verified",
    "runtime_verified",
    "human-confirmed",
    "machine-verified",
    "runtime-verified",
}
SATISFIED_MATURITY_STATUSES = COMPLETE_STATUSES | {
    "not_applicable",
    "not-applicable",
    "n/a",
    "na",
    "approved_exception",
    "exception_approved",
    "disabled_no_mcp",
}
PLACEHOLDER_SOURCE_VALUES = {"", "n/a", "na", "none", "unknown", "tbd", "placeholder"}
STAGE_INDEXES = {
    "00-charter": 0,
    "01-requirements": 1,
    "02-design": 2,
    "03-scaffold": 3,
    "04-test": 4,
    "05-implementation": 5,
    "06-deployment": 6,
    "07-review": 7,
}
NON_RELEASE_EVIDENCE_STATES = {"stale", "contradicted", "superseded", "proposed"}
FRESHNESS_DATE_FIELDS = (
    "expires_at",
    "freshness_expires_at",
    "freshness_expiry",
    "valid_until",
)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL in {path}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"JSONL record must be an object in {path}:{line_number}")
        records.append(value)
    return records


def normalized_status(value: Any) -> str:
    return str(value or "").strip().lower()


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and any(str(item).strip() for item in value)


def normalized_token(value: Any) -> str:
    return normalized_status(value).replace("-", "_")


def evidence_state(record: dict[str, Any]) -> str:
    return normalized_status(record.get("evidence_state") or record.get("verification_status"))


def evidence_has_stable_source(record: dict[str, Any]) -> bool:
    for field in ("source_ref", "source", "source_system", "retrieval_method", "hash"):
        value = normalized_status(record.get(field))
        if value not in PLACEHOLDER_SOURCE_VALUES:
            return True
    return False


def non_placeholder(value: Any) -> bool:
    if value in (None, "", False):
        return False
    if isinstance(value, (list, dict, tuple, set)) and not value:
        return False
    return normalized_status(value) not in PLACEHOLDER_SOURCE_VALUES


def parse_temporal_date(value: Any) -> date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text).date()
    except ValueError:
        try:
            return date.fromisoformat(value.strip()[:10])
        except ValueError:
            return None


def evidence_freshness_failures(record: dict[str, Any], today: date | None = None) -> list[str]:
    failures: list[str] = []
    state = normalized_token(evidence_state(record))
    if state in NON_RELEASE_EVIDENCE_STATES:
        failures.append(f"state is {state}")
    if record.get("stale") is True:
        failures.append("marked stale")
    if record.get("contradicted") is True:
        failures.append("marked contradicted")
    if record.get("superseded") is True:
        failures.append("marked superseded")
    if non_placeholder(record.get("contradicted_by")):
        failures.append("has contradicted_by")
    if non_placeholder(record.get("superseded_by")):
        failures.append("has superseded_by")
    current = today or datetime.now(timezone.utc).date()
    for field in FRESHNESS_DATE_FIELDS:
        value = record.get(field)
        if value in (None, ""):
            continue
        parsed = parse_temporal_date(value)
        if parsed is None:
            failures.append(f"has invalid {field}")
        elif parsed < current:
            failures.append(f"{field} expired")
    return failures


def stage_index(stage_name: Any) -> int | None:
    text = str(stage_name or "").strip()
    if text in STAGE_INDEXES:
        return STAGE_INDEXES[text]
    if len(text) >= 2 and text[:2].isdigit():
        return int(text[:2])
    return None


def evidence_stage_matches(record: dict[str, Any], stage_name: str) -> bool:
    record_stage = record.get("stage")
    expected_index = stage_index(stage_name)
    if record_stage == stage_name:
        return True
    if isinstance(record_stage, int) and expected_index is not None:
        return record_stage == expected_index
    if isinstance(record_stage, str):
        normalized_record = normalized_status(record_stage)
        if normalized_record == normalized_status(stage_name):
            return True
        if expected_index is not None and normalized_record.startswith(f"{expected_index:02d}"):
            return True
    return False


def validate_workspace(workspace: Path, strict_release: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in (
        "README.md",
        "config.json",
        "state/pipeline-state.json",
        "artifacts",
        "ledgers",
        "reports",
        "feedback",
        "hooks",
        "hooks/README.md",
        "hooks/claude-settings.example.json",
        "hooks/guard_sensitive_data.py",
        "hooks/validate_project.py",
    ):
        if not (workspace / relative).exists():
            errors.append(f"missing workspace path: {relative}")

    for relative in (
        "reports/agent-workflow-review.md",
        "reports/agent-measurement-stack.md",
        "reports/agent-cost-efficacy.md",
        "reports/codebase-context.md",
        "reports/guardrail-control-review.md",
        "reports/requirements-elicitation-review.md",
        "reports/standards-governance-review.md",
        "reports/specification-assurance-review.md",
        "reports/security-first-review.md",
        "reports/threat-model.md",
        "reports/vulnerability-risk-assessment.md",
        "reports/red-blue-purple-team-review.md",
        "reports/executive-security-risk-review.md",
        "reports/workflow-affinity-review.md",
        "reports/technical-delivery-review.md",
    ):
        if not (workspace / relative).exists():
            message = f"missing workflow report template: {relative}"
            errors.append(message) if strict_release else warnings.append(message)

    if errors:
        return errors, warnings

    try:
        config = read_json(workspace / "config.json")
        pipeline_state = read_json(workspace / "state" / "pipeline-state.json")
    except ValueError as exc:
        return [str(exc)], warnings

    if config.get("workspace") != ".agentic-sdlc":
        errors.append("config workspace must be .agentic-sdlc")
    state_policy = config.get("state_regulatory", {})
    if not state_policy:
        warnings.append("config missing state_regulatory defaults")
    maturity_policy = config.get("engineering_maturity", {})
    if not maturity_policy:
        warnings.append("config missing engineering_maturity defaults")
    target_architecture_policy = config.get("target_architecture", {})
    if not target_architecture_policy:
        warnings.append("config missing target_architecture defaults")
    guardrail_layer_policy = config.get("guardrail_layer", {})
    if not guardrail_layer_policy:
        warnings.append("config missing guardrail_layer defaults")
    standards_governance_policy = config.get("standards_governance", {})
    if not standards_governance_policy:
        warnings.append("config missing standards_governance defaults")
    specification_assurance_policy = config.get("specification_assurance", {})
    if not specification_assurance_policy:
        warnings.append("config missing specification_assurance defaults")
    requirements_elicitation_policy = config.get("requirements_elicitation", {})
    if not requirements_elicitation_policy:
        warnings.append("config missing requirements_elicitation defaults")
    security_first_policy = config.get("security_first_development", {})
    if not security_first_policy:
        warnings.append("config missing security_first_development defaults")

    stages = pipeline_state.get("pipeline", {}).get("stage_status")
    if not isinstance(stages, list) or not stages:
        errors.append("pipeline.stage_status must be a non-empty list")
        return errors, warnings

    last_stage_index = -1
    seen_stage_indexes: set[int] = set()
    for stage in stages:
        if not isinstance(stage, dict):
            errors.append("stage_status entries must be objects")
            continue
        stage_name = stage.get("stage", "UNKNOWN")
        current_stage_index = stage_index(stage_name)
        if current_stage_index is None:
            errors.append(f"stage {stage_name} has unknown stage index")
        else:
            if current_stage_index in seen_stage_indexes:
                errors.append(f"duplicate stage index {current_stage_index:02d} for stage {stage_name}")
            seen_stage_indexes.add(current_stage_index)
            if current_stage_index < last_stage_index:
                errors.append(f"stage {stage_name} is out of lifecycle order")
            last_stage_index = current_stage_index
        artifact = stage.get("artifact")
        if artifact and not (workspace / artifact).is_file():
            errors.append(f"missing artifact for stage {stage_name}: {artifact}")

        status = normalized_status(stage.get("status"))
        evidence_ids = stage.get("evidence_ids", [])
        if status in COMPLETE_STATUSES and not evidence_ids:
            errors.append(f"stage {stage_name} is complete without evidence_ids")

        approval = stage.get("approval", {})
        if status in COMPLETE_STATUSES and not isinstance(approval, dict):
            errors.append(f"stage {stage_name} approval must be an object")
        elif status in COMPLETE_STATUSES and strict_release:
            if normalized_status(approval.get("status")) not in COMPLETE_STATUSES:
                errors.append(f"stage {stage_name} is complete without approved authority")

    ledger_dir = workspace / "ledgers"
    ledgers: dict[str, list[dict[str, Any]]] = {}
    for ledger in (
        "intent.jsonl",
        "evidence.jsonl",
        "decisions.jsonl",
        "risks.jsonl",
        "usage.jsonl",
        "code-changes.jsonl",
    ):
        path = ledger_dir / ledger
        if not path.exists():
            message = f"missing ledger: ledgers/{ledger}"
            required_before_strict = ledger not in {"usage.jsonl", "code-changes.jsonl"}
            errors.append(message) if strict_release or required_before_strict else warnings.append(message)
            continue
        try:
            ledgers[ledger] = read_jsonl(path)
        except ValueError as exc:
            errors.append(str(exc))

    seen_ledger_ids: dict[str, str] = {}
    for ledger_name, records in ledgers.items():
        for record in records:
            record_id = str(record.get("id", "")).strip()
            if not record_id:
                message = f"{ledger_name} record missing id: {record}"
                errors.append(message) if strict_release else warnings.append(message)
                continue
            if record_id in seen_ledger_ids:
                errors.append(
                    f"duplicate ledger id {record_id} in {ledger_name}; first seen in {seen_ledger_ids[record_id]}"
                )
            else:
                seen_ledger_ids[record_id] = ledger_name

    for record in ledgers.get("code-changes.jsonl", []):
        record_id = str(record.get("id", "UNKNOWN"))
        missing_fields = [
            field
            for field in ("id", "record_type", "created_at", "stage", "change_type", "paths", "summary")
            if not record.get(field)
        ]
        if missing_fields:
            message = f"code change record {record_id} missing {', '.join(missing_fields)}"
            errors.append(message) if strict_release else warnings.append(message)
        if record.get("record_type") and record.get("record_type") != "code_change":
            message = f"code change record {record_id} must use record_type code_change"
            errors.append(message) if strict_release else warnings.append(message)
        if record.get("paths") and not non_empty_list(record.get("paths")):
            message = f"code change record {record_id} paths must be a non-empty list"
            errors.append(message) if strict_release else warnings.append(message)
        trace_fields = (
            "requirement_ids",
            "acceptance_criterion_ids",
            "specification_contract_ids",
            "test_ids",
            "evidence_ids",
            "decision_ids",
            "risk_ids",
        )
        has_trace_link = any(non_empty_list(record.get(field)) for field in trace_fields)
        materiality = normalized_status(record.get("change_materiality"))
        if strict_release and materiality not in {"low", "non_material", "not_applicable", "not-applicable", "na"}:
            if not has_trace_link:
                errors.append(
                    f"material code change record {record_id} has no requirement, specification, test, evidence, decision, or risk trace link"
                )
            if not non_empty_list(record.get("validation_commands")):
                errors.append(f"material code change record {record_id} has no validation_commands")
            if not record.get("commit") and not record.get("pull_request"):
                errors.append(f"material code change record {record_id} has no commit or pull_request reference")

    evidence_by_id = {
        str(record.get("id")): record
        for record in ledgers.get("evidence.jsonl", [])
        if str(record.get("id", "")).strip()
    }
    for record in ledgers.get("code-changes.jsonl", []):
        record_id = str(record.get("id", "UNKNOWN"))
        for evidence_id in record.get("evidence_ids", []):
            evidence_id_text = str(evidence_id)
            if evidence_id_text and evidence_id_text not in evidence_by_id:
                message = f"code change record {record_id} references missing evidence ledger record {evidence_id_text}"
                errors.append(message) if strict_release else warnings.append(message)
    for record in ledgers.get("evidence.jsonl", []):
        missing_fields = [field for field in ("id", "claim") if not record.get(field)]
        if missing_fields:
            message = f"evidence record missing {', '.join(missing_fields)}: {record}"
            errors.append(message) if strict_release else warnings.append(message)
        if strict_release:
            record_id = str(record.get("id", "UNKNOWN"))
            if normalized_token(evidence_state(record)) not in ACCEPTABLE_EVIDENCE_STATES:
                errors.append(f"evidence record {record_id} has non-verifying evidence state")
            freshness_failures = evidence_freshness_failures(record)
            if freshness_failures:
                errors.append(
                    f"evidence record {record_id} is not current release proof: {', '.join(freshness_failures)}"
                )
            if not evidence_has_stable_source(record):
                errors.append(f"evidence record {record_id} has no stable source reference")

    open_blockers = []
    for record in ledgers.get("risks.jsonl", []):
        severity = normalized_status(record.get("severity"))
        status = normalized_status(record.get("status"))
        if severity == "blocker" and status not in ACCEPTED_RISK_STATUSES:
            open_blockers.append(record.get("id", "UNKNOWN"))

    if open_blockers:
        message = f"open blocker risks: {', '.join(open_blockers)}"
        if strict_release:
            errors.append(message)
        else:
            warnings.append(message)

    if strict_release:
        pipeline = pipeline_state.get("pipeline", {})
        if pipeline.get("blockers"):
            errors.append("pipeline blockers must be empty for strict release")
        service = pipeline.get("service", {})
        launch_scope = normalized_status(service.get("launch_scope"))
        jurisdiction_overlay_status = normalized_status(
            service.get("jurisdiction_overlay_status", service.get("state_overlay_status"))
        )
        jurisdiction_launch_scopes = {"national", "multistate", "multijurisdiction", "global"}
        if launch_scope in jurisdiction_launch_scopes and jurisdiction_overlay_status not in COMPLETE_STATUSES:
            errors.append("national, multijurisdiction, or global launch requires completed jurisdiction overlay review")
        if launch_scope in jurisdiction_launch_scopes and not service.get("operating_jurisdictions"):
            errors.append("national, multijurisdiction, or global launch requires operating_jurisdictions")
        for stage in stages:
            if not isinstance(stage, dict):
                continue
            stage_name = str(stage.get("stage", "UNKNOWN"))
            if normalized_status(stage.get("status")) not in COMPLETE_STATUSES:
                continue
            stage_evidence_ids = stage.get("evidence_ids", [])
            if not isinstance(stage_evidence_ids, list):
                errors.append(f"stage {stage_name} evidence_ids must be a list")
                continue
            verified_records = []
            for evidence_id in stage_evidence_ids:
                evidence_id_text = str(evidence_id)
                record = evidence_by_id.get(evidence_id_text)
                if not record:
                    errors.append(f"stage {stage_name} references missing evidence ledger record {evidence_id_text}")
                    continue
                if normalized_token(evidence_state(record)) in ACCEPTABLE_EVIDENCE_STATES:
                    verified_records.append(record)
                else:
                    errors.append(
                        f"stage {stage_name} evidence {evidence_id_text} lacks human, machine, or runtime verification"
                    )
                freshness_failures = evidence_freshness_failures(record)
                if freshness_failures:
                    errors.append(
                        f"stage {stage_name} evidence {evidence_id_text} is not current release proof: "
                        + ", ".join(freshness_failures)
                    )
                if not evidence_has_stable_source(record):
                    errors.append(f"stage {stage_name} evidence {evidence_id_text} has no stable source reference")
            if not verified_records:
                errors.append(f"stage {stage_name} has no human/machine/runtime verified evidence record")
        deployment_stage = next(
            (
                stage
                for stage in stages
                if isinstance(stage, dict)
                and stage_index(stage.get("stage")) == 6
                and normalized_status(stage.get("status")) in COMPLETE_STATUSES
            ),
            None,
        )
        if deployment_stage:
            deployment_records = []
            for evidence_id in deployment_stage.get("evidence_ids", []) or []:
                record = evidence_by_id.get(str(evidence_id))
                if record:
                    deployment_records.append(record)
            runtime_verified = any(
                normalized_token(evidence_state(record)) == "runtime_verified"
                and evidence_stage_matches(record, str(deployment_stage.get("stage", "06-deployment")))
                for record in deployment_records
            )
            if not runtime_verified:
                errors.append("completed deployment lacks runtime-verified evidence record")
        for assurance_name, assurance_status in pipeline.get("assurance_status", {}).items():
            if normalized_status(assurance_status) not in COMPLETE_STATUSES:
                errors.append(f"assurance {assurance_name} is not complete")
        maturity_status = pipeline.get("engineering_maturity_status", {})
        enabled_lanes = maturity_policy.get("enabled_lanes", []) if isinstance(maturity_policy, dict) else []
        for lane in enabled_lanes:
            status = normalized_status(maturity_status.get(lane))
            if status not in SATISFIED_MATURITY_STATUSES:
                errors.append(f"engineering maturity lane {lane} is not complete or approved not applicable")
        agent_team_status = normalized_status(maturity_status.get("agent_team_mode"))
        if agent_team_status not in SATISFIED_MATURITY_STATUSES and agent_team_status != "disabled_until_parallel_bounded_plan":
            errors.append("agent team mode must be complete, approved not applicable, or disabled until a bounded plan exists")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an .agentic-sdlc workspace.")
    parser.add_argument("--workspace", default=".agentic-sdlc", help="Workspace path")
    parser.add_argument("--strict-release", action="store_true", help="Apply release-completion checks")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    errors, warnings = validate_workspace(workspace, args.strict_release)

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("Project validation: FAIL", file=sys.stderr)
        return 1

    print("Project validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
