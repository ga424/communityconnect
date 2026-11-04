#!/usr/bin/env python3
"""Detect high-risk sensitive data before AISE writes, commits, or records it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


HIGH_RISK_PATTERNS = (
    ("SECRET_GITHUB_TOKEN", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("SECRET_GENERIC_ASSIGNMENT", re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}")),
    ("SECRET_DISCLOSURE_COMMAND", re.compile(r"(?i)\b(?:cat|less|more|grep|rg|awk|sed)\b.{0,120}(?:\.env|\.npmrc|\.pypirc|\.netrc|\bcredentials\b|\bsecrets?\b)")),
    ("DANGEROUS_PERMISSION_MODE", re.compile(r"(?i)\b(?:bypassPermissions|dangerously-skip-permissions)\b")),
    ("DANGEROUS_DELETION_COMMAND", re.compile(r"(?i)\brm\s+-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*\s+(?:/|~|\$HOME|\*|\.git\b|\.agentic-sdlc\b)")),
    ("DATABASE_DUMP_COMMAND", re.compile(r"(?i)\b(?:pg_dump|mysqldump|mongodump|sqlite3\s+\S+\s+\.dump)\b")),
    ("KUBERNETES_SECRET_COMMAND", re.compile(r"(?i)\bkubectl\b.{0,160}\b(?:get\s+secret|describe\s+secret|exec\b.*\b(?:env|printenv)|cp\b)\b")),
    ("REGULATED_DATA_TRANSFER_COMMAND", re.compile(r"(?i)\b(?:scp|rsync|aws\s+s3\s+(?:cp|sync)|gsutil\s+(?:cp|rsync)|az\s+storage\s+blob\s+download)\b.{0,180}\b(?:prod|production|regulated|eligibility|entitlement|financial|payment|health|education|biometric|phi|pii|hipaa|ssn)\b")),
    ("MCP_MUTATION_TOOL", re.compile(r"(?i)\"tool_name\"\s*:\s*\"mcp__[^\"\n]*(?:create|update|delete|write|transition|comment|merge|close|deploy|apply|run|trigger|restart|acknowledge|resolve)[^\"\n]*\"")),
    ("SSN", re.compile(r"\b(?!000|666|9\d\d)\d{3}[- ](?!00)\d{2}[- ](?!0000)\d{4}\b")),
    ("DOB_WITH_VALUE", re.compile(r"(?i)\b(?:date of birth|dob)\b.{0,40}\b(?:19|20)\d{2}[-/]\d{1,2}[-/]\d{1,2}\b")),
    ("BANK_ACCOUNT_CONTEXT", re.compile(r"(?i)\b(?:routing number|bank account|account number)\b.{0,80}\b\d{6,17}\b")),
    ("PHI_CONTEXT", re.compile(r"(?i)\b(?:diagnosis|medical record|medicaid|therapy note|treatment plan|protected health information|ephi|phi)\b.{0,120}\b(?:name|dob|ssn|address|account number|member id|patient id|email|phone)\b")),
    ("REGULATED_RECORD_CONTEXT", re.compile(r"(?i)\b(?:education record|health record|eligibility record|entitlement record|financial record|employment record|biometric|household income|foster care|out-of-home care)\b.{0,120}\b(?:name|dob|ssn|address|account number|member id|student id|employee id|email|phone)\b")),
)

WARN_PATTERNS = (
    ("EMAIL_ADDRESS", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("PHONE_NUMBER", re.compile(r"\b(?:\+1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")),
)

CARD_CANDIDATE = re.compile(r"\b(?:\d[ -]?){13,19}\b")

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", "build"}


@dataclass
class Finding:
    severity: str
    kind: str
    location: str
    excerpt: str


def luhn_valid(value: str) -> bool:
    digits = [int(char) for char in re.sub(r"\D", "", value)]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def excerpt(text: str, start: int, end: int) -> str:
    begin = max(0, start - 30)
    finish = min(len(text), end + 30)
    return re.sub(r"\s+", " ", text[begin:finish]).strip()


def scan_text(text: str, location: str) -> list[Finding]:
    findings: list[Finding] = []
    for kind, pattern in HIGH_RISK_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(Finding("BLOCK", kind, location, excerpt(text, match.start(), match.end())))

    for match in CARD_CANDIDATE.finditer(text):
        candidate = match.group(0)
        if luhn_valid(candidate):
            findings.append(Finding("BLOCK", "PAYMENT_CARD", location, excerpt(text, match.start(), match.end())))

    for kind, pattern in WARN_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(Finding("WARN", kind, location, excerpt(text, match.start(), match.end())))
    return findings


def iter_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and not any(part in SKIP_DIRS for part in child.parts):
                    yield child
        elif path.is_file():
            yield path


def scan_paths(paths: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(paths):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(text, str(path)))
    return findings


def hook_payload_text(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input", payload.get("input", payload))
    return json.dumps(
        {
            "hook_event_name": payload.get("hook_event_name"),
            "tool_name": payload.get("tool_name"),
            "tool_input": tool_input,
            "permission_suggestions": payload.get("permission_suggestions", []),
        },
        sort_keys=True,
    )


def permission_request_decision(findings: list[Finding]) -> dict[str, Any]:
    kinds = ", ".join(sorted({finding.kind for finding in findings}))
    return {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "deny",
                "message": (
                    "AISE sensitive-data guard denied this permission request because it matched "
                    f"blocking controls: {kinds}. Use synthetic/redacted data or obtain explicit owner approval."
                ),
                "interrupt": True,
            },
        }
    }


def print_findings(findings: list[Finding], as_json: bool = False) -> None:
    if as_json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
        return
    for finding in findings:
        print(f"{finding.severity}: {finding.kind}: {finding.location}: {finding.excerpt}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan content for high-risk regulated or secret data.")
    parser.add_argument("paths", nargs="*", help="Files or directories to scan")
    parser.add_argument("--text", help="Literal text to scan")
    parser.add_argument("--hook", action="store_true", help="Read Claude Code hook JSON from stdin")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as blocking findings")
    args = parser.parse_args()

    findings: list[Finding] = []
    hook_event_name = ""
    if args.hook:
        try:
            payload = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError as exc:
            print(f"AISE guard could not parse hook input: {exc}", file=sys.stderr)
            return 2
        hook_event_name = str(payload.get("hook_event_name", ""))
        findings = scan_text(hook_payload_text(payload), "hook-input")
    elif args.text is not None:
        findings = scan_text(args.text, "literal-text")
    else:
        paths = [Path(path).expanduser() for path in (args.paths or ["."])]
        findings = scan_paths(paths)

    blocking = [finding for finding in findings if finding.severity == "BLOCK" or args.strict]
    if args.hook and hook_event_name == "PermissionRequest" and blocking:
        print(json.dumps(permission_request_decision(blocking)))
        return 0

    if findings:
        stream = sys.stderr if blocking else sys.stdout
        if args.json:
            print(json.dumps([finding.__dict__ for finding in findings], indent=2), file=stream)
        else:
            for finding in findings:
                print(f"{finding.severity}: {finding.kind}: {finding.location}: {finding.excerpt}", file=stream)

    if blocking:
        print(
            "AISE sensitive-data guard blocked this action. Use synthetic/redacted data or obtain explicit data-owner approval.",
            file=sys.stderr,
        )
        return 2 if args.hook else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
