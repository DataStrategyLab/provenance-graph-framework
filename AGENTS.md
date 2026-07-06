# AGENTS.md

## Project purpose
Provenance Graph Framework (PGF) is a language-agnostic, repo-native framework for governed AI-assisted work products. It makes claims, sources, evidence, reviews, approvals, and release state traceable from intake through release.

## Integrity scope (read this first)
PGF v0.1 provides cooperative-honesty provenance: a faithful record of good-faith work. It is NOT tamper-evident. The event log is plaintext and editable, and hooks are bypassable. Do not describe PGF output as tamper-proof or as a chain of custody. Tamper-evidence is a future option (v1.0: release-package digests wrapped in an in-toto Statement, signed as a DSSE envelope), not a v0.1 promise. v0.1 records SHA-256 digests of exported release-package files for convenience; recorded digests in an editable log are not an integrity control.

## Canonical rule
This file is the canonical cross-agent instruction source. Claude Code imports it via CLAUDE.md. Codex reads it directly. Other agents should use it as primary project guidance.

## Non-negotiable principles
- Provenance is a data model, not a loose log. The human-readable release packet is the deliverable; the graph is supporting infrastructure.
- Every material claim is a claim node with supporting evidence, or is marked unresolved.
- Contradictions are surfaced, not hidden.
- No client-facing artifact is released without a human approval event.
- Release readiness is decided by pgf check, hooks, CI, and human approval. No agent marks anything release-ready.
- Do not fabricate citations, sources, authorities, commands, or test results.
- Do not commit secrets, real client data, CUI, privileged material, or confidential matter data. Examples are synthetic.
- Keep the core language-agnostic and runtime-neutral.
- Materialization is deterministic replay of a recorded history. Claim extraction is not deterministic. Never describe PGF output as "reproducible" beyond replay; the graph records what was decided, not what a model would decide again.
- Actor IDs use typed prefixes (human:, agent:, service:). An agent acting for a person records on_behalf_of in actor_detail.
- PGF is work-product and process provenance. It is not a content-credentials or media-marking system (C2PA, EU AI Act Article 50 marking); do not describe it as one.
- Regulatory facts live in date-stamped docs and instruction files, never in schemas or gates.

## Build and test commands
Set up:
`python3.12 -m venv .venv && source .venv/bin/activate && python -m pip install -e ".[dev]"`
Run checks (in order):
`ruff check .`
`pytest`
`python -m pgf check examples/association-board-brief`
`python -m pgf materialize examples/association-board-brief`
Validation is offline: `pgf validate` and `pgf check` must pass with networking disabled.

## Architecture rules
- JSON Schema, Markdown, YAML, SKILL.md, and JSONL are the durable core. Python is the thin reference implementation.
- No server, database, or hosted dependency in v0.1. No network calls in the core CLI, including schema $ref resolution (schemas resolve from the bundled local registry).
- Schema $id is a stable identifier (tagged-release URI form), never a fetch instruction.
- Node IDs embed their artifact ID and are globally unique. event_id is a ULID. The event log assumes a single writer per artifact in v0.1.
- Do not make Claude Code, Codex, LangGraph, the OpenAI Agents SDK, MCP, Promptfoo, or Inspect required for the core CLI. Adapters are optional.

## Coding standards
Python 3.12, standard library first, allowed deps: jsonschema, pyyaml, pytest, ruff. Deterministic output ordering, tests for every command, actionable error messages, stable public interfaces once documented. Normative language in provenance/ docs uses RFC 2119 keywords.

## Review standards
Run the relevant checks before finishing any task; if checks cannot run, say exactly why. Claude Code implements and self-reviews first. Codex provides an independent second read on meaningful branches (a second opinion, not a release approver). Human review is required before release.

## Review guidelines
- P0: fabricated citations or sources; release-gate bypasses; secrets or real client data; network calls in the core CLI; nondeterministic materializer output; schema changes without a migration note.
- P1: a new CLI command without tests; stale golden fixtures; AGENTS.md exceeding 200 lines; docs claiming tamper-evidence or reproducibility beyond replay.
- Do not comment on style unless it hides a bug; ruff owns style.

## Public-sector and regulated-output standards
Include accessibility and disclosure checks where relevant, and label accessibility output as automated-only (human audit still required). Treat legal and GovCon examples as educational, not advice or certification. Mark unresolved uncertainty clearly. Keep source retrieval and review metadata (retrieved_at is required on sources). Prefer synthetic examples. Every regulatory reference in docs carries an as-of date.
