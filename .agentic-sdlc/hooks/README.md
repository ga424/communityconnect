# AISE Hooks

This directory contains hook support copied during `/agentic-sdlc:init`.

Use `claude-settings.example.json` as a starting point for project or managed Claude Code settings. The example is not active until copied into `.claude/settings.json`, merged into user settings, or distributed through managed policy.

Default posture:

- Block high-risk sensitive data before file writes and command execution.
- Deny risky permission requests with a structured `PermissionRequest` hook decision when Claude Code is about to ask for broader access.
- Audit after write operations.
- Use subagent lifecycle hooks to validate delegated work boundaries and completion evidence.
- Require project validation before task completion.
- Keep production regulated data out of model context unless explicitly approved by the data owner.
- Keep copied hook scripts local to the workspace so initialized projects do not depend on the AISE package checkout path.
- Keep unreviewed national, multijurisdiction, global, or regulated jurisdictions and jurisdiction-specific restricted flows disabled until source freshness, legal/compliance approval, and runtime routing evidence exist.
- Treat MCP writes, bypass permission modes, secret file reads, destructive deletion commands, and regulated data transfers as blocked unless the owning authority has approved the workflow.
