# AISE source and execution boundary

Verified against the upstream default branch on November 7, 2026: AISE **0.3.4**, commit [`84816af9975b4e2aaac5219a40603be38dc1bd70`](https://github.com/abreugus/aise/commit/84816af9975b4e2aaac5219a40603be38dc1bd70), is the latest merged source. No GitHub release or tag is published. The GitHub connector returned 404; authenticated GitHub CLI queries and a fresh clone succeeded. The existing pin already matches, so no framework code/schema migration was necessary. This supersedes the initial setup's local-only source verification.

Gustavo explicitly chose to keep the latest merged version. Unmerged AISE PRs #1/#2, including the 0.4.0 LangGraph preview, are not adopted. [Source and file-hash evidence](../evidence/aise-refresh/latest-merged.json) confirms the bundled validator, sensitive-data guard and license are byte-identical to upstream. [Exact request and decision](../../prompts/2026-11-07-aise-next-feature.txt). Recheck upstream before a future upgrade; this is a dated observation, not a permanent latest-version claim.

The bundled workspace validator and sensitive-data guard are copied unchanged. Third-party licensing is in THIRD_PARTY_NOTICES/AISE-LICENSE.txt. Claude hook examples are examples; their presence does not mean hooks are installed in Codex. We invoke deterministic checks explicitly.

This run uses sequential Codex execution, not delegated agents. Read init/orchestrate/scaffold/test/implement skill contracts from the pinned framework. Canonical .agentic-sdlc state and ledgers control readiness. No stage is marked complete based merely on drafted files. No controls were disabled. Strict-release validation is expected to remain blocked.

Public repository data: synthetic fixtures, abstract requirements and E/A/Q IDs. Private interview notes, identities and consent artifacts stay in the restricted course/Jira package. Launch scope is local-only; no jurisdiction, real payment, external identity or production deployment is enabled. Cost/token measurements are unavailable; no productivity or savings claim is made.
