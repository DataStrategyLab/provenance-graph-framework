# Provenance Graph Framework
## Lean v0.1 PRD and Cross-Agent Execution Plan (Claude Code primary, Codex reviewer)

**Version:** v0.3 (tightened from v0.2)
**Date:** July 6, 2026
**Owner:** Data Strategy Lab LLC
**Repo:** https://github.com/DataStrategyLab (public, open source; repo published first)
**Primary build agent:** Claude Code
**Secondary review agent:** OpenAI Codex
**Primary design principle:** Language-agnostic core, thin Python tooling, cross-agent portability through AGENTS.md

---

## 0. What this version changed and why

This is a tightening pass, not a rewrite. The prior draft was a v0.1 spec carrying a v3.0 body. The structure is kept. The changes:

1. **Cut v0.1 to what is actually buildable and load-bearing.** Evals, CI beyond a basic lane, and the legal and GovCon packs move out of v0.1 into "Next." The prior draft listed Promptfoo, Inspect, CI, and three ICP packs as v0.1 goals in section 5.1 while section 6 said defer evals. That contradiction is resolved in favor of a genuinely minimal v0.1: schemas, thin CLI, one association example, hooks, one ICP's instructions, human approval gate.
2. **Resequenced build order.** One real artifact is built end-to-end against a loose, unfrozen schema before the node and edge model is locked. The prior order (two weeks of schema authoring before the first real example) is the event-sourcing trap: you learn the model is wrong only when you build the second example, and by then you have golden fixtures and schema versions to migrate.
3. **Stated the provenance-integrity stance plainly.** v0.1 provides cooperative-honesty provenance (it documents good-faith work), not tamper-evidence (it cannot prove nothing was fabricated). The event log is plaintext JSONL, hook-appended, and bypassable. This is said out loud in sections 1, 3, and the security section so a legal or GovCon reviewer is never misled. Tamper-evidence (hash-chained log, signed approvals) is named as a v1.0+ option gated on a buyer who needs it.
4. **Reframed Codex from "independent reviewer" to "second-opinion and DX layer."** Two frontier models reviewing each other is correlated review: they share failure modes. Codex is useful, but it is not an independent safety control and is removed from the threat-model control list. The real controls are the human, the deterministic CLI, and CI.
5. **Scoped the accessibility claim down.** Automated accessibility preflight catches a minority of WCAG issues. The release package's accessibility note is explicitly labeled "automated checks only, human audit still required," so it never implies a conformance claim the tool cannot back.
6. **Named the graph as infrastructure, not the product.** The human-readable release packet is the deliverable. The machine-readable graph export is supporting infrastructure. The framework must be useful to a buyer who never opens nodes.json.
7. **Fixed Claude Code and Codex specifics against current (July 2026) docs.** Details in sections 13, 14, and 19: the secret-scanning hook must be PreToolUse not PostToolUse (PostToolUse cannot undo a write), commands and skills have merged into one /slash-command system, disable-model-invocation has a live invocation bug to design around, and Codex reads AGENTS.md natively but does not share the .claude/ skills directory.

Two things deliberately not done, per owner direction: no demand-validation section (go-to-market handled separately), and no expansion of the v1.0 through v3.0 material (compressed to a single forward-pointer in section 5).

---

## 1. Executive decision

Build the Provenance Graph Framework as a repo-native, language-agnostic framework for governed AI-assisted work products. It is not another agent runtime. Its value is that every material claim, source, assumption, contradiction, draft span, review decision, approval, and release package for a governed artifact stays inspectable from intake through delivery.

The unit sold is the human-readable release packet: a defensible memo, brief, or proposal section with its sources, its open questions, its reviewer sign-off, and a record of what changed before release. The provenance graph is the infrastructure that makes that packet trustworthy and reproducible. It is not the thing the buyer opens first.

Be precise about what v0.1 proves. It provides cooperative-honesty provenance: a faithful record of good-faith work by people and agents who are cooperating with the process. It is not tamper-evident. The event log is a plaintext file that a determined actor can edit, and the hooks that append to it can be bypassed by writing the file directly or running an agent without the hooks loaded. That is the honest and correct scope for a v0.1 open-source starter kit. Tamper-evidence is a later option, not a v0.1 promise.

The framework uses:

1. AGENTS.md as the canonical shared instruction source (Claude Code and Codex both read it, the latter natively).
2. CLAUDE.md as a thin Claude Code shim that imports AGENTS.md.
3. JSON Schema, Markdown, YAML, JSONL, and SKILL.md as the portable core.
4. Thin Python 3.12 scripts as the reference implementation.
5. Claude Code as the primary implementation environment.
6. Codex as a second-opinion, security-scan, and developer-experience reviewer (not an independent safety control).
7. No server, no database, no proprietary runtime lock-in for v0.1.

Design rule that governs everything below: enforcement lives in tools (hooks, CLI checks, CI), guidance lives in prose (AGENTS.md, instructions). If a rule must hold, it is a hook or a CLI check, never a sentence in a markdown file.

---

## 2. Product positioning

**Name:** Provenance Graph Framework. Short name: PGF.

**One-line positioning:** an open-source framework for making high-stakes AI-assisted work products traceable from evidence intake to human-approved release.

**Category:** evidence-first governance layer for agentic AI work products.

**What it is (v0.1):** a repo template, a schema library, a thin Python CLI, a small set of workflow specs, portable instruction files and skills, and one worked example. A public-sector-friendly operating model for reviewable AI outputs.

**What it is not:** a replacement for Claude Code, Codex, LangGraph, the OpenAI Agents SDK, Promptfoo, Inspect, or MCP. Not a hosted product in v0.1. Not a graph database. Not a legal-advice engine. Not a procurement-compliance guarantee. Not a tamper-evident audit system in v0.1. Not an autonomous publishing system. Not a no-review output generator.

---

## 3. Problem statement

AI-assisted deliverables in public-sector, GovCon, association, and law-firm settings are judged by defensibility, not only speed. A draft is not enough. Teams need to answer: which evidence supports this claim; which source was used and when it was retrieved; which claims are uncertain, contradictory, stale, or unsupported; which reviewer approved the final version; which accessibility, confidentiality, CUI, disclosure, or legal-ethics checks were applied; what changed between reviewed and released versions; and whether a client, board, contracting officer, supervising attorney, or procurement reviewer could reconstruct the work.

Today those answers live in scattered chat transcripts, human memory, footnotes, email threads, doc comments, or inaccessible tool logs.

PGF makes provenance a first-class data model. Every governed artifact gets an append-only event log. That log materializes into a queryable graph and a human-readable release package.

Scope of the guarantee, stated plainly: PGF v0.1 documents that work was done a certain way by cooperating participants. It does not prove that the log was not altered afterward. It raises the floor on defensibility and reproducibility. It is not a chain-of-custody or tamper-proof system. A buyer who needs the second thing needs the v1.0+ tamper-evidence option (section 22), not v0.1.

---

## 4. Primary ICPs and use cases

All ICPs share the same core (governed artifact, event log, claim graph, evidence graph, review events, approval record, release package). What changes is the artifact class and the review threshold, expressed in instruction files, not in the graph model.

**Public sector and government-adjacent:** policy briefs, public-comment drafts, program-guidance summaries, AI-governance memos. Value: evidence traceability, accessibility-by-design, audit-ready packaging, clear human sign-off.

**GovCon:** capture briefs, proposal sections, compliance narratives, past-performance summaries, customer and competitive research. Value: CUI-aware handling patterns, source-hierarchy discipline, review and approval records, contradiction handling, NIST and Section 508 documentation.

**Associations:** board briefs, member advisories, standards summaries, legislative updates. Value: board defensibility, member trust, citation fidelity, plain-language review, source freshness. (This is the v0.1 canonical example.)

**Law firms and legal teams:** internal research memos, chronologies, diligence summaries, matter research packets. Value: human supervision, no fabricated authority, confidentiality-aware workflows, source-to-proposition traceability, reviewer lineage.

**AI platform and developer teams:** internal AI-governance playbooks, reviewable AI-assisted design, agent-workflow release gates. Value: cross-agent portability, better PR-review evidence, governance baked into repo workflows.

---

## 5. Goals

### 5.1 v0.1 goals (the only ones this document plans in detail)

1. Ship a forkable repo template. Target: a fresh clone runs the canonical example in one sitting. (The "under 30 minutes" figure from the prior draft is a target to test in Phase 6, not an asserted fact.)
2. Make AGENTS.md the canonical shared instruction source; CLAUDE.md a thin import shim.
3. Encode a portable provenance model in JSON Schema, frozen only after the canonical example is built.
4. Implement a thin Python CLI: init, validate, event append, materialize, check, review-packet, export.
5. Store provenance as append-only JSONL events; materialize deterministic nodes.json, edges.json, state.json.
6. Ship one canonical end-to-end example: association board brief, including one contradiction and one accepted override.
7. Ship association instructions and templates (one ICP). Legal and GovCon instructions are Next, not v0.1.
8. Enforce a human approval gate via Claude Code hooks and a CLI release gate.
9. Ship unit tests, schema-validation tests, and golden fixtures for the canonical example.
10. Ship a basic CI lane (lint, tests, `pgf check` on the example). Evals and multi-lane CI are Next.
11. Publish contributor-friendly quickstart and one example walkthrough.

Explicitly not in v0.1: Promptfoo evals, Inspect evals, the legal and GovCon example packs, MCP integration, runtime adapters beyond Claude Code and a Codex review path, any server, any database, tamper-evidence.

### 5.2 Beyond v0.1 (forward-pointer only, not planned here)

Next (v1.0 candidate): the legal and GovCon instruction packs; Promptfoo and Inspect eval lanes; schema-versioning discipline as a public API; a documented security model; OSS launch assets. Later (v2.0+): optional SQLite or DuckDB materialized index for larger graphs; richer query; tamper-evidence (hash-chained log, signed approvals) if a buyer needs it; optional MCP trust-boundary layer; typed Python package migration if PGF becomes load-bearing internal DSL infrastructure rather than primarily a public artifact. These are directions, not commitments, and are deliberately left unplanned.

---

## 6. Non-goals for v0.1

Do not build: a hosted SaaS app, a graph-database requirement, a FastAPI service, a web dashboard, an MCP server, a plugin marketplace, a multi-tenant permission system, a legal-research product, a compliance-certification product, a workflow runtime that competes with LangGraph, or a general-purpose agent framework. The first version is small, inspectable, easy to fork, and easy to understand.

---

## 7. Design principles

**AGENTS.md is canonical.** It is the source of truth for agent-facing repo instructions. Claude Code imports it through CLAUDE.md; Codex reads it natively; other agents can consume it. Keep it under 200 lines; the 2026 research on context files (efficiency gains from a small file, correctness losses from a bloated one, and the catalogued "smells" of context bloat and conflicting instructions) all point the same way: small, stable root, scoped detail elsewhere.

**Runtime shims stay thin.** CLAUDE.md imports AGENTS.md and adds only Claude-specific notes. .claude/settings.json configures hooks and permissions. .claude/skills/ holds Claude-first procedures. Codex review prompts live in prompts/codex/. Adapters stay optional until schemas stabilize.

**Provenance is a data model, not a log dump, but the graph is infrastructure not the product.** Every material claim maps to a claim node, evidence and source nodes, review events, approval or escalation state, and release status. The buyer consumes the release packet; the graph makes it trustworthy.

**Keep the core language-agnostic.** The durable contract is JSON Schema, YAML workflows, Markdown instructions, SKILL.md packages, JSONL events, JSON graph exports. Python is only the reference implementation. Rationale for the open-source posture: fork friction near zero, and the framework reads as a neutral standard rather than a vendor side-project.

**Borrow LangGraph patterns, do not depend on LangGraph.** Adopt explicit state, graph-shaped workflows, checkpoints, human-in-the-loop pauses, clear node and edge semantics, and separation of orchestration from policy. Do not require LangGraph in v0.1; it is an optional adapter later.

**Enforcement belongs in tools, not prose.** Instruction files guide. Hooks, CLI checks, tests, and CI enforce.

**Human approval is mandatory.** No client-facing artifact is releasable without a human approval event.

**Cooperative-honesty, not tamper-evidence, in v0.1.** Say so in the docs. Do not let "audit trail" imply "tamper-proof."

**Public-sector adjacent by default.** Every workflow assumes accessibility, auditability, confidentiality, source trust, and sign-off lineage matter. Automated accessibility checks are a preflight, not a conformance claim.

---

## 8. Repository architecture (v0.1)

Trimmed to what v0.1 ships. Files marked (Next) are placeholders documented in ROADMAP.md, not built now.

```text
provenance-graph-framework/
  AGENTS.md
  CLAUDE.md
  README.md
  LICENSE
  NOTICE
  CONTRIBUTING.md
  SECURITY.md
  ROADMAP.md
  pyproject.toml
  Makefile

  cli/
    pgf/
      __init__.py
      __main__.py
      commands/
        init.py
        validate.py
        event.py
        materialize.py
        check.py
        review_packet.py
        export.py
      core/
        schemas.py
        events.py
        materializer.py
        gates.py
        ids.py
        paths.py
        errors.py
      tests/

  schemas/
    v0/
      graph-event.schema.json
      artifact.schema.json
      claim.schema.json
      source.schema.json
      evidence.schema.json
      edge.schema.json
      review.schema.json
      approval.schema.json
      release.schema.json

  provenance/
    graph-model.md
    event-taxonomy.md
    confidence-scale.md
    source-hierarchy.md
    materiality-policy.md
    release-state-machine.md

  workflows/
    intake-to-claim-graph.yaml
    verify-and-escalate.yaml
    approve-and-package.yaml

  instructions/
    artifact.association-board-brief.md
    review.materiality.md
    review.accessibility-and-disclosure.md
    # (Next) artifact.legal-research-memo.md
    # (Next) artifact.govcon-capture-brief.md
    # (Next) review.confidentiality-and-cui.md

  templates/
    intake.md
    evidence-plan.md
    claim-register.md
    contradiction-packet.md
    review-packet.md
    approval-record.md
    release-package-index.md
    accessibility-note.md
    disclosure-note.md

  .claude/
    settings.json
    agents/
      researcher.md
      drafter.md
      verifier.md
      approver.md
    skills/
      evidence-plan/SKILL.md
      claim-normalization/SKILL.md
      contradiction-resolution/SKILL.md
      produce-review-packet/SKILL.md
      generate-approval-summary/SKILL.md
    hooks/
      append-event.py
      validate-record.py
      block-release.py
      no-secret-leak.py

  prompts/
    codex/
      pr-review.md
      security-review.md
      architecture-challenge.md

  examples/
    association-board-brief/
      intake.md
      draft.md
      events.jsonl
      expected/
        nodes.json
        edges.json
        state.json
        release-package/

  docs/
    quickstart.md
    claude-code-setup.md
    codex-setup.md
    architecture.md
    schema-reference.md
    security-model.md
    faq.md

  .github/
    workflows/
      ci.yml
    ISSUE_TEMPLATE/
    PULL_REQUEST_TEMPLATE.md
```

Note the deferred directories from the prior draft (evals/, adapters/, the multi-lane .github workflows, the second and third example packs) are intentionally absent. They are named in ROADMAP.md.

---

## 9. File responsibility rules

### 9.1 AGENTS.md
Canonical shared agent contract. Contains: project purpose, runtime-neutral principles, build and test commands, coding and schema standards, review requirements, security rules, human-approval rule, source and evidence hierarchy, the no-fabrication and no-hidden-source-substitution rules, and the explicit cooperative-honesty scope statement. Does not contain: long artifact procedures, long legal or GovCon policy, Claude-specific hook config, Codex-specific prompts, or detailed examples. Keep under 200 lines.

### 9.2 CLAUDE.md
Short. Imports AGENTS.md with `@AGENTS.md`. Adds only Claude Code operating notes (plan mode before schema and hook changes, where the skills live, that release-readiness is decided by pgf check plus hooks plus CI plus a human approval event, and do not duplicate AGENTS.md).

### 9.3 instructions/
Scoped policy and artifact procedures. Each file: artifact class, audience, required evidence tier, required review roles, required disclosure and accessibility checks, required release artifacts, escalation triggers, example failure modes. v0.1 ships the association file plus the two review files; legal and GovCon are Next.

### 9.4 .claude/skills/
Commands and skills have merged in current Claude Code: files in .claude/commands/ and .claude/skills/ both create /slash-commands, and skills are the recommended path. So v0.1 puts everything in skills/ and does not maintain a separate prompts/ tree for Claude (Codex prompts stay under prompts/codex/ because Codex does not read .claude/).

For the release-critical procedures (produce-review-packet, generate-approval-summary), you want manual-only invocation so the model never fires them on its own. The intended control is `disable-model-invocation: true`. Caveat to design around: there is a current Claude Code bug (anthropics/claude-code#26251) where that field can also block manual /slash invocation. Until it is fixed, the safe pattern is to set `user-invocable: true` explicitly and test that the slash command runs; do not rely on `disable-model-invocation` alone, and back the real gate with the hook and CLI check, not the skill's invocation setting.

Skill frontmatter used in v0.1: name, description (front-load the trigger case; the description budget is roughly 1% of the context window and long lists get truncated), allowed-tools (read-only for research and verification skills: Read, Grep, Glob). Keep each SKILL.md under 500 lines with reference material in adjacent files.

### 9.5 .claude/agents/
Four subagents in v0.1: Researcher, Drafter, Verifier, Approver. The prior draft's Security Reviewer and DX Reviewer move to Codex prompts (they are review roles, not build roles, and correlated-model review should not masquerade as an in-repo control). Research and review subagents are read-only where possible. Subagents cannot show interactive permission prompts, so a tool call that would need approval is treated as denied inside a subagent; give them read-only tools and let the parent session handle writes and approvals.

### 9.6 schemas/
Public contract. Each schema: $id, schema_version, required fields, explicit enums for lifecycle states, additionalProperties:false unless an extension point is intentional, and tested examples. Freeze only after the canonical example is built (see build order, section 20). Schema $id convention: DSL does not own a vanity domain, and the framework publishes to GitHub first, so $id points at raw content in the DSL org, which resolves to the actual file: `https://raw.githubusercontent.com/DataStrategyLab/provenance-graph-framework/main/schemas/v0/<name>.schema.json`. Pin the branch (`main`) rather than a moving ref so $ref between schemas stays stable. If rename-proof identifiers are later wanted, switch to a tagged-release path (`.../refs/tags/v0.1.0/...`) or GitHub Pages at `datastrategylab.github.io`. Not needed for v0.1.

### 9.7 events.jsonl
System of record for an artifact, within the cooperative-honesty scope. Append-only, one JSON object per line, monotonic seq, UTC timestamp, actor ID, artifact ID, event type, payload, optional tool and review metadata. Plaintext and editable; not tamper-evident in v0.1.

---

## 10. Core data model

### 10.1 Governed artifact (required fields)
```json
{
  "id": "artifact:association-board-brief:001",
  "schema_version": "0.1.0",
  "artifact_type": "association_board_brief",
  "title": "Example Board Brief",
  "audience": "association_board",
  "classification": "public|internal|confidential|cui_possible",
  "status": "intake|drafting|verification|review|approved|released|archived",
  "created_at": "2026-07-02T00:00:00Z",
  "owner": "human:owner-id"
}
```

### 10.2 Node types (v0.1)
artifact, claim, source, evidence, question, assumption, constraint, draft_span, review, approval, release. (The prior draft's recommended v1 node types such as risk, control, cui_boundary, reviewer_override, benchmark_result are Next, added only when the legal and GovCon packs need them. Do not lock them into v0.1 schemas.)

### 10.3 Edge types (v0.1)
supports, contradicts, derived_from, reviewed_by, overrides, released_as. (v1 candidates such as maps_to_control, maps_to_requirement, evaluated_by are Next.)

### 10.4 Event types (v0.1)
```text
artifact.created / artifact.updated
source.added / source.updated
evidence.added
claim.added / claim.updated
edge.added / edge.removed
question.added / assumption.added / constraint.added
draft_span.added
review.requested / review.recorded
contradiction.detected
override.proposed / override.accepted
approval.requested / approval.recorded
release.check_requested / release.check_passed / release.check_failed
release.exported
```

### 10.5 Claim node schema (sketch)
```json
{
  "$id": "https://raw.githubusercontent.com/DataStrategyLab/provenance-graph-framework/main/schemas/v0/claim.schema.json",
  "type": "object",
  "required": ["id","schema_version","artifact_id","text","claim_type","materiality","confidence_band","status"],
  "properties": {
    "id": { "type": "string" },
    "schema_version": { "type": "string" },
    "artifact_id": { "type": "string" },
    "text": { "type": "string", "minLength": 1 },
    "claim_type": { "type": "string", "enum": ["factual","legal","policy","technical","market","financial","procedural","recommendation"] },
    "materiality": { "type": "string", "enum": ["low","medium","high","critical"] },
    "confidence_band": { "type": "string", "enum": ["low","medium","high","verified"] },
    "status": { "type": "string", "enum": ["open","supported","contradicted","needs_review","approved","rejected"] },
    "source_refs": { "type": "array", "items": { "type": "string" } },
    "requires_human_review": { "type": "boolean" },
    "notes": { "type": "string" }
  },
  "additionalProperties": false
}
```

The honest hard problem, flagged not solved: claim granularity. Turning prose into claim nodes at the right resolution (not one node for "the memo is correct," not 300 nodes nobody maintains) is the single thing that decides whether the graph is real or decorative. The claim-normalization skill owns this, and it is the highest-risk part of the whole framework. v0.1 does not solve it; it ships a first-cut heuristic in the skill, tests it against the canonical example, and treats improving it as the primary post-v0.1 research question. Do not let the schema's tidiness disguise that this is unsolved.

### 10.6 Graph event schema (sketch)
```json
{
  "$id": "https://raw.githubusercontent.com/DataStrategyLab/provenance-graph-framework/main/schemas/v0/graph-event.schema.json",
  "type": "object",
  "required": ["schema_version","event_id","artifact_id","seq","ts","actor","event_type","payload"],
  "properties": {
    "schema_version": { "type": "string" },
    "event_id": { "type": "string" },
    "artifact_id": { "type": "string" },
    "seq": { "type": "integer", "minimum": 1 },
    "ts": { "type": "string", "format": "date-time" },
    "actor": { "type": "string" },
    "event_type": { "type": "string" },
    "payload": { "type": "object" },
    "tool": {
      "type": "object",
      "properties": {
        "runtime": { "type": "string", "enum": ["human","claude_code","codex","ci","other"] },
        "session_id": { "type": "string" },
        "tool_name": { "type": "string" }
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

---

## 11. State machine

```text
intake -> evidence_planning -> claim_graph -> drafting -> verification
      -> contradiction_resolution -> human_review -> approved -> packaged -> released -> archived
```

Release is blocked unless: every high or critical materiality claim has supporting evidence; every contradiction has a disposition; every required review role is satisfied; required accessibility and disclosure checks are complete (as automated preflight, with the human-audit caveat carried into the note); no required evidence is stale beyond the artifact policy; no unresolved confidentiality or CUI issue; a human approval event exists; `pgf check` passes; CI passes.

---

## 12. Core workflows (v0.1: three, not five)

The prior draft's evidence-to-draft and post-release-feedback workflows are folded in or deferred. Three workflows carry v0.1.

### 12.1 Intake to claim graph
Inputs: artifact type, audience, context, deadline, classification, release channel, known sources, research questions, required reviewer roles.
Outputs: intake.md, evidence-plan.md, initial events.jsonl, source and claim candidates, open questions and assumptions.
Claude Code: read AGENTS.md, load the association instruction file, invoke the evidence-plan skill, create the starter event log, run `pgf validate`, run `pgf materialize`.

### 12.2 Verification and escalation
Inputs: draft, claim graph, source graph, review policy.
Outputs: review events, contradiction packet, escalation list, updated state.
Verifier questions: (1) supported by authoritative evidence? (2) contradictory, outdated, or incomplete evidence? (3) wording within the allowed confidence band? (4) any accessibility, confidentiality, legal, CUI, or disclosure risk? The Drafter produces the draft with every material statement mapped to a claim node and no fabricated citations; that drafting step lives inside this loop's front half rather than as its own ceremony.

### 12.3 Approval to release package
Inputs: verified draft, review packet, approval record, release template.
Outputs and package layout:
```text
release-package/
  artifact.md
  provenance-index.md
  review-summary.md
  approval-record.json
  graph/
    events.jsonl
    nodes.json
    edges.json
    state.json
  assurance/
    accessibility-note.md      # automated checks only; human audit still required
    disclosure-note.md
    source-quality-summary.md
```
The human-readable trio (artifact.md, provenance-index.md, review-summary.md) is the deliverable. The graph/ directory is supporting evidence for anyone who wants to reconstruct the work.

---

## 13. Claude Code operating model

### 13.1 Role
Claude Code is the implementation driver: scaffolding, Python CLI, JSON Schemas, skills, subagents, hooks, the example, tests, local checks, docs, and fixing review findings.

### 13.2 Subagents (four)
**Researcher:** gather and organize evidence; read and research tools only; return source candidates with trust tier; record uncertainty; do not draft finals or write release state.
**Drafter:** produce drafts from graph-backed claims; every material statement maps to a claim; cautious language where evidence is incomplete; no invented citations; do not release.
**Verifier:** review every material claim; read-only where possible; emit pass, warn, fail, or escalate; surface contradictions and stale evidence; flag accessibility, confidentiality, legal, CUI, disclosure concerns.
**Approver:** prepare an approval summary for a human; never approve as the human; summarize residual risk and changes since the last reviewed version; require an explicit human approval event.

### 13.3 Hooks (the enforcement layer, corrected)
Hooks enforce what instructions cannot. Corrections from the prior draft, verified against current hook docs:

- PostToolUse fires after the tool already ran and cannot undo it. So a secret-scan wired to PostToolUse cannot prevent a leak. `no-secret-leak.py` must be **PreToolUse** on Write and Edit (and Read for sensitive paths), exiting 2 to block. This is the single most important correction.
- Exit code 2 is the blocking signal (exit 1 blocks nothing). PreToolUse exit 2 stops the tool; a Stop hook exit 2 forces Claude to keep working.
- Subagent Stop hooks auto-convert to SubagentStop, so a naive Stop matcher on "*" behaves differently inside subagents. Scope it deliberately.
- The team-shared, committed gates go in .claude/settings.json; personal overrides go in .claude/settings.local.json (gitignored) so a teammate cannot silently disable a production gate.

Required v0.1 hooks:
1. `append-event.py` (PostToolUse, matcher Write|Edit): append a provenance event when an artifact or record file changes. PostToolUse is correct here because appending after the write is exactly the intent.
2. `validate-record.py` (PostToolUse, matcher Write|Edit): validate changed JSON or YAML records via the CLI and surface errors back to Claude.
3. `no-secret-leak.py` (PreToolUse, matcher Write|Edit|Read): block writes or reads that would expose secrets or real client data. Must be PreToolUse to actually block.
4. `block-release.py` (PreToolUse, matcher Bash): inspect tool_input.command; if it is `pgf export` and the release gate fails (bands unmet, contradiction undisposed, or no human approval event), exit 2 with the reason.

Sample .claude/settings.json:
```json
{
  "permissions": { "defaultMode": "plan" },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Write|Edit|Read",
        "hooks": [ { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/no-secret-leak.py\"", "timeout": 10 } ] },
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/block-release.py\"", "timeout": 10 } ] }
    ],
    "PostToolUse": [
      { "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/append-event.py\"", "timeout": 15 },
          { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-record.py\"", "timeout": 15 }
        ] }
    ]
  }
}
```
Honest limit of hooks as a control: they enforce the process only when the process runs through Claude Code with these settings loaded. Running the CLI directly, or another agent, bypasses them. That is why the release gate is also a CLI check (`pgf check` / `pgf export`) and a CI check, not only a hook. Three enforcement points, not one.

---

## 14. Codex operating model (second opinion, not independent control)

### 14.1 Role, honestly scoped
Codex is a useful second reader: PR review, security scanning (Codex ships an application-security scanning capability), performance review, docs review, architecture challenge, test-coverage review, cross-agent portability review. It runs checks in an isolated environment and cites terminal evidence.

What Codex is not: an independent safety control. Two frontier models share failure modes; if Claude Code rationalizes an overclaim or misses an injection, Codex may do the same. Codex review reduces self-review bias and catches real bugs, which is worth having, but it is not counted among the framework's controls. The controls are the human, the deterministic CLI, and CI.

### 14.2 Cross-agent reality (verified)
Codex reads AGENTS.md natively (global ~/.codex, then repo root, then nested), so the "one canonical AGENTS.md, both agents read it" claim holds for instructions. But: Codex reads skills from .codex/skills or .agents/skills, not .claude/skills, and Codex deprecated custom prompts in favor of skills. So skills are not automatically shared across the two tools. v0.1 keeps skills Claude-first under .claude/, and keeps Codex's contribution to review prompts under prompts/codex/ plus the shared AGENTS.md. Do not claim skill portability across Claude Code and Codex that the directory conventions do not deliver.

### 14.3 Codex prompts (v0.1: three)
PR review, security review, architecture challenge. Each: use AGENTS.md as the canonical source; reproduce the relevant checks (`pgf check examples/association-board-brief`, `pytest`, `ruff check .`); return findings by severity, exact commands run, terminal evidence, and the smallest recommended patch per accepted finding. Human approval remains required; Codex is not a release approver.

---

## 15. CLI requirements

### 15.1 Commands (v0.1: seven; benchmark deferred)
```bash
pgf init <artifact-dir> --type association-board-brief
pgf validate <path> --schema <schema-id>
pgf event append <artifact-dir> --event <event.json>
pgf materialize <artifact-dir>
pgf check <artifact-dir>
pgf review-packet <artifact-dir>
pgf export <artifact-dir>
```

### 15.2 Exit codes
0 success; 1 validation or readiness failure; 2 release-blocking failure; 3 configuration error; 4 unsupported schema version; 5 unsafe operation blocked.

### 15.3 Determinism (harder than "sort the keys")
Materialization must be byte-identical across two runs on the same log AND across machines. That means: sort nodes by stable ID and edges by stable tuple; fix JSON formatting (separators, key order, ensure_ascii, trailing newline); pin float and timestamp formatting; normalize line endings (LF) and write in UTF-8; and never inject a fresh UUID or wall-clock time into materialized output. Cross-machine determinism is a named acceptance test (section 26), not an assumption.

---

## 16. Evaluation strategy (deferred, pointer only)

Evals are Next, not v0.1. When added: Promptfoo for declarative, CI-friendly checks (unsupported-claim detection, citation fidelity, contradiction surfacing, prompt injection, accessibility preflight, abstention) and Inspect for richer agentic and tool-use evaluations. v0.1 ships tests and golden fixtures (section 26), which are the deterministic backbone; the eval lanes layer on top later. This keeps v0.1 free of a model-graded, API-key-dependent test dependency.

---

## 17. CI (v0.1: one fast lane)

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python -m pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest
      - run: python -m pgf check examples/association-board-brief
      - run: python -m pgf materialize examples/association-board-brief
      - run: git diff --exit-code examples/association-board-brief/expected
```
The final two steps are the determinism gate: materialize, then fail if the committed golden output changed. Multi-lane CI (schema lane, eval lane, nightly) is Next.

---

## 18. Setup for Claude Code users (condensed)

Prereqs: Git, Python 3.12, pip or uv, Claude Code authenticated, repo access.
```bash
git clone <repo-url> provenance-graph-framework
cd provenance-graph-framework
python3.12 -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pgf check examples/association-board-brief
python -m pgf materialize examples/association-board-brief
python -m pgf export examples/association-board-brief
pytest
```
Confirm CLAUDE.md contains `@AGENTS.md`, launch `claude`, and verify Claude states that AGENTS.md is canonical, no release without human approval, and pgf check plus hooks enforce readiness. Per-task discipline: plan mode first, smallest correct change, local tests, `pgf check` on affected examples, PR, optional Codex second read, resolve accepted findings, request human review.

---

## 19. Setup for Codex users (condensed)

Prereqs: Codex access, repo connected, root AGENTS.md committed. Codex builds its instruction chain per run from ~/.codex then repo root then nested dirs. Ensure AGENTS.md lists the build and check commands (Codex will run listed programmatic checks before finishing). First review prompt: review this branch as a second reader (not the sole approver), use AGENTS.md as canonical, run `pytest` / `ruff check .` / `pgf check examples/association-board-brief` / `pgf materialize ...`, and return blocking issues, non-blocking improvements, commands run, and terminal evidence. Do not use Codex as the only reviewer for release; human approval is required.

---

## 20. Phased execution roadmap (resequenced)

The key change from the prior draft: build one real artifact against a loose schema before freezing the model. Durations assume a two-person team at partial allocation and are ceilings, not commitments.

**Phase 0: scope lock (a few days).** Repo skeleton, AGENTS.md, CLAUDE.md, README, pyproject, directory structure, LICENSE (Apache-2.0 for code). Human approves the v0.1 scope in section 5.1. Exit: no server or DB in v0.1; AGENTS.md under 200 lines.

**Phase 1: loose schema plus one real artifact, together (about 2 weeks).** Draft the node and edge model as loose JSON Schema (additionalProperties tolerant at first). In the same phase, hand-build the association board brief's event log and run it through validate and materialize. Discover the model's real shape by using it. HUMAN-REVIEW CHECKPOINT: lock the node and edge model only at the end of this phase, once one real artifact has exercised it. This is the resequence that avoids fixture-and-version churn.

**Phase 2: thin CLI (about 2 to 3 weeks).** Implement validate, event append, materialize (deterministic), check, review-packet, export. Golden fixtures for the canonical example: valid log, log missing supporting evidence, log missing approval, log with contradiction and accepted override. Expected nodes.json, edges.json, state.json, release package. Exit: two-command proof works (check + export), invalid fixtures fail predictably, cross-run and cross-machine materialization is byte-identical.

**Phase 3: Claude Code enforcement (about 1 to 2 weeks).** settings.json, the four hooks (with the PreToolUse secret-scan and release-gate corrections), the four subagents, the five skills. HUMAN-REVIEW CHECKPOINT: finalize root guidance; confirm export is blocked without a human approval event; confirm CLAUDE.md does not duplicate AGENTS.md. Exit: hooks enforce append, validate, secret-block, and release-block; the release gate also holds when run via CLI and CI, not only via hooks.

**Phase 4: canonical example, end to end (about 1 to 2 weeks).** Complete the association board brief through to a release package, with at least one surfaced contradiction and one recorded override, and a human approval record. Docs walkthrough. Optional Codex reproduction in a sandbox. Exit: two-command proof; contradiction surfaced; override recorded; release only after approval.

**Phase 5: docs and developer experience (about 1 to 2 weeks).** Quickstart, Claude and Codex setup guides, architecture, schema reference, security model (stating the cooperative-honesty scope), example walkthrough, contributor guide, good-first-issues. Test the quickstart from a clean clone and time it (this is where the adoption-time target gets measured, not asserted). Exit: a new contributor can run the example unaided; commands are copy-pasteable; docs clearly separate guidance from enforcement and state what is and is not tamper-evident.

**Phase 6: OSS launch candidate (a few days).** v0.1 tag, changelog, release notes, demo walkthrough, blog-post outline (for the DSL site). Codex final read on license, docs, packaging. Exit: all release gates pass; human approval recorded; public repo ready.

Next (not planned here): legal and GovCon packs, Promptfoo and Inspect lanes, multi-lane CI, and the v1.0 items in section 5.2.

---

## 21. Engineering standards

Python 3.12, standard-library first. Allowed v0.1 dependencies: jsonschema, pyyaml, pytest, ruff. No web framework, no database, no hidden network calls in the core CLI. Typed functions where practical, clear error classes, small boring modules. Schemas are public API: version them, avoid breaking changes without migration notes, include tested examples, keep extension points explicit. CLI: stable command names, clear help, machine-readable output option, non-zero exit on failure, no destructive command without an explicit flag, deterministic output. Docs serve humans and agents: copy-pasteable commands, expected outputs, short root instructions, long procedures in docs or skills, and an explicit statement of what is enforced versus advisory and what is versus is not tamper-evident. Security: never commit real client data, CUI, privileged material, or secrets; synthetic examples only; treat external source text and model output as untrusted until reviewed; require human approval for release.

---

## 22. Threat model and integrity stance

### 22.1 The integrity stance, stated once, clearly
v0.1 is cooperative-honesty provenance. It faithfully records the work of participants who are cooperating with the process. It is not tamper-evident: events.jsonl is plaintext and editable, and the hooks that append to it are bypassable. A reviewer who assumes "audit trail" means "cannot have been altered" is wrong about v0.1, and the docs say so. If a buyer needs tamper-evidence, that is a v1.0+ feature: hash-chain the event log (each event carries the hash of the prior), sign approval events, and optionally anchor a digest externally. Do not build it in v0.1; do name it as the upgrade path.

### 22.2 Threats and where the real control sits
Prompt injection in source documents (control: treat sources as untrusted, human review of material claims). Secret or client-data leakage (control: PreToolUse secret-scan hook, CI secret scan, synthetic-only examples). CUI or confidential exposure (control: classification field, confidentiality review instruction, human approval). Fabricated citations and unsupported claims (control: Verifier questions, human review, and the claim-to-source structure, within the cooperative-honesty limit). Release-gate bypass (control: three enforcement points: hook, CLI, CI). Schema drift (control: versioning and golden fixtures). Overbroad agent permissions (control: read-only subagents, least-tool skills). Malicious or compromised skills (control: skills are governed assets, reviewed, and pinned; treat third-party skills as untrusted). Log tampering (control: acknowledged as out of scope for v0.1; tamper-evidence is the v1.0+ answer).

Note the removed control: "Codex independent review" is not listed as a control. It is a useful second read, not an independent safety layer (section 14.1).

---

## 23. ICP adaptation

Shared core across all ICPs: governed artifact, event log, claim graph, evidence graph, review events, approval record, release package. What changes: associations weight board readability, member trust, public accessibility, plain language, source freshness; law firms weight source hierarchy, human supervision, no fabricated authority, confidentiality, attorney-review records; GovCon weights CUI-aware handling, capture and proposal workflows, customer-source handling, and audit-and-accountability evidence; public sector weights accessibility-by-default, plain language, public accountability, and release documentation. In v0.1 only the association adaptation ships as a worked example; the others are instruction-file work in Next.

---

## 24. OSS and commercialization (pointer only)

License: Apache-2.0 for code; Apache-2.0 or CC-BY-4.0 for docs and examples; per-skill license metadata; DCO. Public-repo readiness: no client references, synthetic examples, contribution guide, security policy (with the integrity-scope statement), issue templates, roadmap, release notes, example walkthrough. Commercialization is handled separately by DSL and is deliberately not expanded here; the open-source repo and the DSL launch post are the credibility and lead-gen surface.

---

## 25. Acceptance criteria (falsifiable)

### 25.1 v0.1
1. A fresh clone installs and runs the canonical example.
2. `python -m pgf check examples/association-board-brief` passes.
3. `python -m pgf export examples/association-board-brief` emits a complete release package.
4. Removing a required supporting-evidence event makes `pgf check` fail and name the offending claim.
5. Removing the human approval event makes export fail (via CLI and via the hook).
6. The same event log materializes to byte-identical nodes.json, edges.json, and state.json across two runs.
7. The same event log materializes to byte-identical output on a second machine or a clean CI runner (cross-machine determinism).
8. The canonical example includes at least one surfaced contradiction and one recorded override.
9. The release package's human-readable trio (artifact, provenance index, review summary) is complete and readable without opening the graph/ directory.
10. The accessibility note in the release package states that only automated checks ran and human audit is still required.
11. AGENTS.md is canonical and under 200 lines; CLAUDE.md imports it and does not duplicate it.
12. The docs state the cooperative-honesty scope: the log is not tamper-evident in v0.1.
13. The fast CI lane passes, including the determinism diff gate.
14. No real client data, CUI, or secrets exist anywhere in the repo.
15. The secret-scan hook is PreToolUse and blocks a planted test secret before the write.

---

## 26. Ready-to-paste AGENTS.md starter

```markdown
# AGENTS.md

## Project purpose
Provenance Graph Framework (PGF) is a language-agnostic, repo-native framework for governed AI-assisted work products. It makes claims, sources, evidence, reviews, approvals, and release state traceable from intake through release.

## Integrity scope (read this first)
PGF v0.1 provides cooperative-honesty provenance: a faithful record of good-faith work. It is NOT tamper-evident. The event log is plaintext and editable, and hooks are bypassable. Do not describe PGF output as tamper-proof or as a chain of custody. Tamper-evidence is a future option, not a v0.1 promise.

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

## Build and test commands
Set up:
`python3.12 -m venv .venv && source .venv/bin/activate && python -m pip install -e ".[dev]"`
Run checks:
`ruff check .` then `pytest` then `python -m pgf check examples/association-board-brief` then `python -m pgf materialize examples/association-board-brief`

## Architecture rules
- JSON Schema, Markdown, YAML, SKILL.md, and JSONL are the durable core. Python is the thin reference implementation.
- No server, database, or hosted dependency in v0.1.
- Do not make Claude Code, Codex, LangGraph, the OpenAI Agents SDK, MCP, Promptfoo, or Inspect required for the core CLI. Adapters are optional.

## Coding standards
Python 3.12, standard library first, minimal dependencies, deterministic output ordering, tests for every command, actionable error messages, stable public interfaces once documented.

## Review standards
Run the relevant checks before finishing any task; if checks cannot run, say exactly why. Claude Code implements and self-reviews first. Codex provides an independent second read on meaningful branches (a second opinion, not a release approver). Human review is required before release.

## Public-sector and regulated-output standards
Include accessibility and disclosure checks where relevant, and label accessibility output as automated-only (human audit still required). Treat legal and GovCon examples as educational, not advice or certification. Mark unresolved uncertainty clearly. Keep source retrieval and review metadata. Prefer synthetic examples.
```

---

## 27. Ready-to-paste CLAUDE.md starter

```markdown
# Provenance Graph Framework

@AGENTS.md

## Claude Code operating notes
Use plan mode before changing schemas, hooks, release gates, or example packs.
Use the project skills in `.claude/skills/` for repeatable procedures. Use subagents for research, drafting, verification, and approval-summary preparation.
Do not duplicate AGENTS.md here. AGENTS.md is canonical.
Do not mark any artifact as release-ready. Release readiness is determined by `pgf check`, release hooks, CI, and a human approval event.
Provenance in this repo is cooperative-honesty, not tamper-evident. Do not describe outputs as tamper-proof.
```

---

## 28. First-week build plan (resequenced)

Day 1: create repo; add AGENTS.md, CLAUDE.md, README skeleton, pyproject, LICENSE, directory structure.
Day 2: draft the loose graph model, event taxonomy, confidence scale, source hierarchy (tolerant schemas, not yet frozen).
Day 3: hand-build the association example's intake and a first slice of events.jsonl; run validate and materialize against the loose schema; note where the model is wrong.
Day 4: implement `pgf validate`, `pgf event append`, and a minimal deterministic `pgf materialize`; add valid and invalid fixtures.
Day 5: extend the association example; run local checks; if useful, send the branch to Codex for a second read; convert accepted findings into issues. Freeze the node and edge model only after the example has exercised it.

---

## 29. Source notes for maintainers

Tightened from the v0.2 draft. Cross-agent pattern: AGENTS.md canonical, CLAUDE.md a thin shim, Claude Code hooks as local deterministic enforcement (with the PreToolUse secret-scan and release-gate corrections), Codex as a second-opinion and security-scan reader (not an independent control), LangGraph as architecture inspiration only, Promptfoo and Inspect deferred to Next. NIST AI RMF, NIST SP 800-171, Section 508 or WCAG (2.0 procurement baseline versus 2.2 recommendation, both mapped in the accessibility instruction), and ABA Formal Opinion 512 are context for the ICPs, not compliance claims. MCP is a later trust-boundary option, not a v0.1 dependency. Integrity stance is cooperative-honesty, not tamper-evidence, and the docs say so. Next step: use this document as the initial Claude Code project brief, build the skeleton, and establish Codex as a second reader on meaningful branches.
```
