# PGF v0.1 Final Build Plan
## Claude Code + Codex execution runbook

**Status:** Final. Supersedes the review-and-execution-plan document for build purposes; the analysis and dispositions there remain the rationale record.
**Date:** July 6, 2026
**Team:** Andrew (owner, PM, human approver), Adaora (engineer, agent operator)
**Agents:** Claude Code (primary implementer), Codex (second reader, security scan, GitHub PR review)
**How to use:** Commit this file as `docs/build-plan.md` and the PRD as `docs/prd-v0_3.md` in the repo before Phase 0, so both agents can read them. Then follow the phase runbook in section 5, using the setup in section 2 and the workflow rules in section 4.

Tool facts in this document were verified against the official docs in July 2026:
Claude Code: https://code.claude.com/docs and https://docs.claude.com/en/docs/claude-code/overview
Codex: https://developers.openai.com/codex/cli , https://developers.openai.com/codex/guides/agents-md , https://developers.openai.com/codex/learn/best-practices , https://developers.openai.com/codex/integrations/github

---

## 1. Decision register (locked)

Decisions from PRD v0.3 plus the review pass, restated once so no build session relitigates them. Each carries its dissent and test in the review document; this table is the operating summary.

| # | Decision | Status |
|---|---|---|
| D1 | v0.1 is lean: schemas, thin CLI, hooks, four subagents, five skills, one association example, one fast CI lane. No server, DB, evals, MCP, legal/GovCon packs | Locked (PRD) |
| D2 | Cooperative-honesty integrity scope; not tamper-evident; say so everywhere | Locked (PRD) |
| D3 | AGENTS.md canonical and under 200 lines; CLAUDE.md is a thin `@AGENTS.md` shim (Claude Code does not read AGENTS.md natively as of July 2026; the import shim is the documented pattern) | Locked (PRD, verified) |
| D4 | Release packet is the product; graph is infrastructure | Locked (PRD) |
| D5 | Enforcement in tools (permissions, hooks, CLI, CI); guidance in prose | Locked (PRD) |
| D6 | v1.0 tamper-evidence path = in-toto Statement in a DSSE envelope, Sigstore signing; v0.1 records release-package SHA-256 digests only, described as convenience, never as integrity | Locked (review, top finding 1) |
| D7 | Schema `$id` = tag-form identifier URI; `pgf validate` resolves all schemas from a bundled local registry; zero network in the core CLI, tested with networking disabled | Locked (review, top finding 2) |
| D8 | Regulatory facts live only in date-stamped docs and instruction files, never in schemas or gates (Colorado repeal-replace, EU Omnibus deferral, and the DOJ Title II extension are the proof cases) | Locked (review, top finding 3) |
| D9 | Claim-normalization skill encodes verifiability filtering, decontextualization, confidence-gated extraction, and materiality triage, with a hand-built reference-register fixture | Locked (review, top finding 4) |
| D10 | `actor` is a typed-prefix string (`human:`, `agent:`, `service:`) with an optional `actor_detail` extension object including `on_behalf_of` | Locked (review, top finding 5) |
| D11 | Claim nodes carry required `origin` (human_authored, agent_extracted, hybrid) and optional `extraction` metadata; docs say deterministic replay, never deterministic regeneration | Locked (review) |
| D12 | Source nodes require `retrieved_at` and `access`; optional `uri`, `content_digest`, `snapshot_ref` | Locked (review) |
| D13 | Node IDs embed the artifact ID (globally unique); `event_id` is a ULID; single-writer assumption documented | Locked (review) |
| D14 | `event_type` validated by pattern in schema, by registry in the materializer | Locked (review) |
| D15 | PROV mapping table in graph-model.md; PROV-O adoption rejected; exporters (`prov-jsonld`, `otel`, `in-toto`) are Next behind a reserved `pgf export --format` flag | Locked (review) |
| D16 | Optional `trace_id` / `span_id` in the event `tool` block (W3C Trace Context); OTel as store rejected | Locked (review) |
| D17 | Skills stay in `.claude/skills/` for Claude Code; Codex prompts in `prompts/codex/`; migration to a shared `.agents/skills/` convention is a ROADMAP trigger, not a v0.1 move | Locked (review; note: Codex now documents repo-shared skills at `.agents/skills`, which strengthens the future trigger but does not change v0.1) |
| D18 | Codex is a second reader, not a control; controls are the human, the deterministic CLI, and CI | Locked (PRD) |
| D19 | Spec posture now (RFC 2119 language in `provenance/`), conformance suite at v1.0; NIST is the single standards-participation venue | Locked (review, Part C) |
| D20 | Apache-2.0; moat is vertical packs plus delivery fluency, not the core schema | Locked (PRD + review) |

---

## 2. Environment setup, step by step

Both of you do 2.1 and 2.2. One of you does 2.4 once. Codex setup (2.3) can be Andrew-only at first since Codex enters at review checkpoints, not build.

### 2.1 Prerequisites (macOS, per machine)

1. Git 2.40+, Python 3.12 (`python3.12 --version`), Node.js 18+ (`node --version`).
2. GitHub access to the `DataStrategyLab` org with permission to create `provenance-graph-framework`.
3. `uv` or `pip` available for the venv workflow in AGENTS.md.

### 2.2 Claude Code setup

1. Install: `npm install -g @anthropic-ai/claude-code` (the npm package is `@anthropic-ai/claude-code`; a native installer also exists, see https://code.claude.com/docs for current options).
2. Launch `claude` in any directory and complete authentication when prompted. Sign in with the Claude account that carries your Max subscription; Claude Code usage is included in Max plans. Note for DSL: this repo is DSL work, so use the account you have designated for DSL work under your single-account setup.
3. Verify: `claude --version`, then inside a session run `/status` to confirm auth and model.
4. Personal (not project) configuration: put individual preferences in `~/.claude/CLAUDE.md` and `~/.claude/settings.json`. Keep anything PGF-enforcing out of personal files; team enforcement lives in the repo (section 3). Rule of thumb from current guidance: user settings < project `settings.json` < project `settings.local.json` < CLI flags, with managed settings above all, so a repo cannot be silently weakened by personal files but can be personally extended.
5. Do not install any MCP servers for this project in v0.1. PGF's core has no MCP dependency by design (PRD section 5.1), and fewer tools means a cleaner permission surface.
6. After the repo exists (2.4), open it with `claude` and confirm the session reports AGENTS.md content (via the CLAUDE.md import) by asking: "What are the non-negotiable principles in this repo?" It should answer from AGENTS.md without reading files.

### 2.3 Codex setup

1. Install the CLI: `npm install -g @openai/codex` (or `brew install --cask codex` on macOS). Sign in on first run with your ChatGPT account (Pro plan includes Codex) or an API key.
2. Codex reads `AGENTS.md` natively, building its instruction chain from `~/.codex`, then repo root, then nested directories, and it is trained to run the checks listed there before finishing. This is why AGENTS.md must list the exact commands (section 3.1 does).
3. Personal Codex config lives in `~/.codex/config.toml`. Keep default approval and sandbox settings to start; loosen only for this repo once trust is established. Personal repo-local overrides go in `AGENTS.override.md` (gitignored), the Codex analog of `settings.local.json`.
4. GitHub PR review (the highest-value Codex surface for this project): set up Codex cloud, enable Code review for `DataStrategyLab/provenance-graph-framework` in Codex settings, then trigger reviews by commenting `@codex review` on a PR, or enable Automatic reviews so every PR gets one. Codex flags P0/P1 issues and follows the `## Review guidelines` section of AGENTS.md (section 3.1 includes one for exactly this reason). Docs: https://developers.openai.com/codex/integrations/github
5. Local second reads before a PR exists: inside `codex`, use the built-in review flow (`/review`) to have a separate Codex agent review uncommitted changes, or run the three PGF review prompts from `prompts/codex/` by pasting them into a fresh Codex thread. One thread per task, never one long-running thread per project.
6. Skills note: Codex reads repo-shared skills from `.agents/skills/` and personal ones from `~/.agents/skills/`. PGF does not ship Codex skills in v0.1 (D17); if a review procedure gets pasted into Codex more than three times, that is the trigger to make it an `.agents/skills` skill and update D17's ROADMAP line.

### 2.4 Repo bootstrap (once)

1. Create `DataStrategyLab/provenance-graph-framework` on GitHub (public, Apache-2.0 license template, no README autogeneration; the repo skeleton comes from Phase 0).
2. Clone, then commit the two planning inputs before any agent session:
   ```bash
   mkdir -p docs
   cp <path>/provenance_graph_framework_prd_v0_3_lean.md docs/prd-v0_3.md
   cp <path>/pgf-v0_1-final-build-plan.md docs/build-plan.md
   git add docs && git commit -m "docs: PRD v0.3 and final build plan as project inputs"
   ```
3. Add the root files from section 3 (AGENTS.md, CLAUDE.md, `.claude/settings.json`, `.gitignore` entries) by hand or via the Phase 0 prompt in section 5. Adding them by hand first is slightly better: the very first Claude Code session then starts governed.
4. Branch protection on `main`: require PRs, require the `ci` check once it exists (Phase 2), no force pushes.
5. `.gitignore` must include from day one: `.claude/settings.local.json`, `AGENTS.override.md`, `.venv/`, `__pycache__/`, `.env*`.

---

## 3. Copy-ready root files (final versions)

These merge the PRD v0.3 starters (sections 26, 27, 13.3) with every review change. Use these verbatim; they are the canonical versions.

### 3.1 AGENTS.md (final, 91 lines, budget 200)

```markdown
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
```

The `## Review guidelines` section is load-bearing twice: Codex's GitHub code review reads it from AGENTS.md and scopes its P0/P1 comments to it, and the local `prompts/codex/pr-review.md` references it so both review surfaces apply one standard.

### 3.2 CLAUDE.md (final)

```markdown
# Provenance Graph Framework

@AGENTS.md

## Claude Code operating notes
Use plan mode before changing schemas, hooks, release gates, or example packs.
Use the project skills in `.claude/skills/` for repeatable procedures. Use subagents for research, drafting, verification, and approval-summary preparation; subagents are read-only, the parent session does the writes.
Do not duplicate AGENTS.md here. AGENTS.md is canonical.
Do not mark any artifact as release-ready. Release readiness is determined by `pgf check`, release hooks, CI, and a human approval event.
Never claim a release package is tamper-evident or that claim extraction is reproducible; see AGENTS.md integrity scope.
One task per session. Run /clear between unrelated tasks. Read docs/build-plan.md for the current phase before starting phase work.

## Compact instructions
When summarizing this conversation, preserve: schema or gate changes and their rationale, the list of modified files, failing test output and its resolution. Summarize exploration briefly.
```

### 3.3 .claude/settings.json (final, committed)

Changes from the PRD sample: adds a permissions `deny` list (deny rules are evaluated first and make matched files invisible to Claude, a stronger secrets control than the hook alone; the hook remains as the second layer and covers content-based leaks the path rules cannot see), adds an `ask` gate on pushes, and keeps plan as the default mode.

```json
{
  "permissions": {
    "defaultMode": "plan",
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)"
    ],
    "ask": [
      "Bash(git push:*)"
    ]
  },
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

Hook contract (verified current): hooks receive JSON on stdin; exit 0 allows, exit 1 allows with a warning surfaced to Claude, exit 2 blocks (PreToolUse) or forces continuation (Stop). The older decision/reason JSON return style is deprecated; use exit codes. Write all four hooks against this contract.

### 3.4 Subagent files (final frontmatter pattern)

The interactive `/agents` creation wizard was removed in recent Claude Code versions; create the four files directly in `.claude/agents/`. Pattern (researcher shown; drafter, verifier, approver follow the PRD section 13.2 role text):

```markdown
---
name: researcher
description: Gathers and organizes evidence for a governed artifact. Use for source discovery and evidence planning. Returns source candidates with trust tier and recorded uncertainty. Never drafts finals or writes release state.
tools: Read, Grep, Glob, WebSearch, WebFetch
model: sonnet
---
You are the PGF Researcher... (role text from PRD 13.2, plus: record retrieved_at and access type for every source candidate; record uncertainty explicitly; you are read-only, return findings to the parent session.)
```

Rules that are current behavior, encode them in every file: subagents cannot present interactive permission prompts (an ask-matching tool call inside a subagent is treated as denied), so all four subagents get read-only tool lists (no Write, Edit, Bash for researcher/verifier/approver; drafter returns draft text to the parent rather than writing files). Stop hooks in subagent frontmatter convert to SubagentStop automatically; PGF defines no subagent-level hooks in v0.1 to keep the surface small.

### 3.5 Release-critical skills (invocation safety)

For `produce-review-packet` and `generate-approval-summary`, set both `disable-model-invocation: true` and `user-invocable: true` in frontmatter, then test that `/produce-review-packet` runs manually. Rationale unchanged from the PRD: current guidance recommends `disable-model-invocation: true` for dangerous operations so the model cannot fire them autonomously, and the PRD's caveat about invocation edge cases stands, so the real gate remains the hook plus `pgf check`, never the skill's invocation setting. Skills live at `.claude/skills/<name>/SKILL.md` (directory form); the old `.claude/commands/` path still works but skills are the current recommended system, confirming PRD 9.4.

---

## 4. Operating workflow (Claude Code best practices, July 2026)

The 2026 consensus, from Anthropic's guidance and the strongest practitioner references, reduces to four rules: constrain through systems, not prompts; treat context as a scarce resource; make the agent verify its own work against checks it can run; keep every diff human-reviewable. Applied to PGF:

### 4.1 The session loop (every task)

1. **One task, one session.** Start `claude` fresh (or `/clear`) per task. Long mixed sessions degrade output; this is the single most repeated 2026 finding for both Claude Code and Codex.
2. **Explore.** Ask Claude to read the relevant files and the current phase section of `docs/build-plan.md`. For anything large, have it delegate exploration to the researcher subagent so search results stay out of the main context.
3. **Plan.** The repo defaults to plan mode (`defaultMode: "plan"`). For schema, hook, gate, or example changes this is mandatory (CLAUDE.md says so): review the plan, edit it, approve it. For trivial tasks, exit plan mode explicitly and say why in the prompt.
4. **Implement smallest correct change.** Reference files with @ mentions, state the done condition, and name the checks that define done (they are in AGENTS.md; Claude and Codex both treat listed checks as part of finishing).
5. **Verify.** Claude runs `ruff check .`, `pytest`, and the two `pgf` commands itself before declaring done. If a check cannot run, the AGENTS.md rule requires it to say exactly why.
6. **Commit and PR.** Small branches, one concern per PR, commit messages that name the phase task (for example `phase2: pgf materialize determinism + golden fixtures`).
7. **/clear and next task.**

### 4.2 The enforcement ladder

Four layers, weakest to strongest, each catching what the previous cannot. Never move a rule down the ladder:

1. **Prose** (AGENTS.md, CLAUDE.md, skills): guidance, followed most of the time, never relied on for safety.
2. **Permissions** (`settings.json` allow/ask/deny): deny rules are evaluated first and hide matched files entirely; the secrets deny-list is the first line, not the hook.
3. **Hooks**: deterministic, cannot hallucinate; the PreToolUse secret scan catches content-based leaks that path rules cannot; the release-block hook stops `pgf export` without approval.
4. **CLI + CI**: `pgf check` and the determinism diff gate hold even when someone runs the CLI directly or uses another agent. This is why every gate exists in three places (hook, CLI, CI), per PRD 13.3.

### 4.3 Context hygiene

- AGENTS.md stays under 200 lines (CI-checkable: `test $(wc -l < AGENTS.md) -le 200`). Anything longer moves to `docs/`, `provenance/`, or a skill; skill bodies load only when invoked, so long procedures are free until used.
- CLAUDE.md carries only Claude-specific operating notes plus the compact instructions block (3.2), which controls what survives `/compact` in long sessions.
- Subagents exist to protect the parent context: research, verification sweeps, and approval-summary prep run in their own windows and return summaries. Do not add a fifth subagent unless a task demonstrably needs different tools or isolation; theatrical agent teams are a documented 2026 anti-pattern.
- If a session goes sideways, do not argue with it. `/clear`, restate the task with better context, go again. Both vendors now give this advice explicitly.

### 4.4 TDD against golden fixtures (the PGF-shaped best practice)

PGF's golden-fixture design (PRD Phase 2) matches the strongest current agent workflow: write the failing test first, commit it, then instruct the agent to implement until green without touching the tests. Concretely, for each CLI command: (1) Claude writes the fixture and the failing pytest in one session, human reviews that the fixture encodes the intended behavior, commit; (2) a fresh session implements the command with the explicit instruction "make these tests pass; do not modify anything under tests/ or examples/*/expected/"; (3) the determinism gate (materialize twice, diff) runs in the same session. Codex is trained to run tests named in AGENTS.md before finishing, so the same fixtures discipline both agents.

### 4.5 The Codex second-read loop

Codex enters at three points, in increasing formality:

1. **Pre-commit local read (optional, meaningful changes only):** in the working tree, open `codex`, run the built-in review flow against uncommitted changes, or paste `prompts/codex/pr-review.md`. One thread per review; discard the thread after.
2. **PR review (standard):** every PR to `main` gets `@codex review` (or Automatic reviews once enabled). Codex reads the diff against the repo, follows the AGENTS.md `## Review guidelines`, flags P0/P1 only, and can be asked in a follow-up comment to draft fixes. Claude Code then implements accepted findings in a fresh session; do not let Codex push fixes directly in v0.1 (single-implementer discipline keeps the provenance story clean).
3. **Phase-gate reads (three per project):** at the end of Phases 2, 4, and 6, run the three PGF prompts (`pr-review.md`, `security-review.md`, `architecture-challenge.md`) as separate Codex threads against the phase branch, each required to reproduce the AGENTS.md checks and return terminal evidence. Findings become Linear issues; accepted ones are implemented by Claude Code.

Codex findings are advisory (D18). Disagreements between the agents are resolved by a human, with the tiebreaker question: which position is backed by a check that can run?

### 4.6 Two-person parallelism

- **Split by write scope, not by phase.** Parallel agents are safe only when write scopes do not collide. The natural v0.1 split: one person owns `cli/` + `schemas/` (Adaora), the other owns `provenance/` + `instructions/` + `examples/` + docs (Andrew), with `.claude/` shared through PRs only.
- **Worktrees for parallel agent sessions on one machine:** `git worktree add ../pgf-schemas phase1-schemas` gives each Claude Code session its own checkout; Conductor (already your chosen orchestrator) manages exactly this pattern if you want the UI over raw worktrees. Either is fine; raw worktrees are the leaner default for a repo this small.
- **Linear discipline:** every accepted Codex finding, every human-checkpoint outcome, and every deferred item becomes a Linear issue tagged with its phase. The build plan is the map; Linear is the live state.

---

## 5. Phase runbook

Each phase: goal, kickoff prompt (paste into a fresh Claude Code session in the repo root), Codex checkpoint, human checkpoint, exit criteria. Durations are the PRD's ceilings. Full acceptance criteria are consolidated in section 6; phase exits reference them by number.

### Phase 0: scope lock (days)

**Goal:** governed skeleton; first session already runs under AGENTS.md, permissions, and (stub) hooks.

**Pre-work by hand (before any agent session):** section 2.4 steps, plus the four root files from section 3 committed.

**Kickoff prompt:**
> Read docs/build-plan.md sections 1 and 3, and docs/prd-v0_3.md sections 5 to 9. Plan, then create the repo skeleton exactly per PRD section 8: all directories, README skeleton with the process-provenance positioning paragraph from build-plan A0.1, LICENSE (Apache-2.0), NOTICE, CONTRIBUTING.md (include the ADR breadcrumb rule: schema changes require a decision note in provenance/), SECURITY.md stating the cooperative-honesty scope, ROADMAP.md seeded with the Next block from build-plan section 7, pyproject.toml (deps: jsonschema, pyyaml; dev: pytest, ruff), and Makefile with setup/check/test targets matching AGENTS.md. Create .claude/hooks/ with the four hook files as working stubs that read stdin JSON and exit 0, each with a TODO naming its Phase 3 contract. Do not write schemas or CLI code yet. Run ruff on the result.

**Human checkpoint:** approve v0.1 scope (PRD 5.1); verify AGENTS.md line count; verify a fresh `claude` session answers the non-negotiables question from memory of the import.
**Exit:** skeleton merged to main; branch protection on; criteria 11, 14 hold trivially.

### Phase 1: loose schema plus one real artifact (about 2 weeks)

**Goal:** node/edge model discovered by building the association example against tolerant schemas; model frozen only at phase end.

**Kickoff prompt (session 1 of several):**
> Plan mode. Read docs/prd-v0_3.md section 10 and docs/build-plan.md decisions D10 to D14. Draft the v0 schemas as tolerant JSON Schema (additionalProperties permissive for now) incorporating: actor pattern plus actor_detail with on_behalf_of (D10); claim origin enum and optional extraction block (D11); source retrieved_at and access required, uri/content_digest/snapshot_ref optional (D12); node IDs embedding artifact ID, event_id as ULID (D13); event_type validated by pattern with the registry listed in provenance/event-taxonomy.md (D14); optional trace_id/span_id strings inside the tool block (D16). Use placeholder $id values in the tagged-release URI form with v0.0.0-dev (D7). Then draft provenance/graph-model.md (with the PROV mapping table and three stated divergences, RFC 2119 keywords for normative statements), event-taxonomy.md (single-writer assumption, seq rules, ULID requirement), confidence-scale.md, source-hierarchy.md, materiality-policy.md (including who may assign and change materiality), release-state-machine.md.

**Subsequent sessions:** hand-build `examples/association-board-brief/` intake and a first `events.jsonl` slice; run it against the loose schemas by ad-hoc script (the CLI does not exist yet); log every place the model fights the example as a note in the phase branch.

**Human checkpoint (phase end, mandatory):** freeze the node and edge model. Review the fight-list; every unresolved fight either changes the model now or becomes a documented divergence.
**Exit:** frozen schemas on main; example slice validates; criterion 21 holds by construction.

### Phase 2: thin CLI (2 to 3 weeks)

**Goal:** the seven commands, deterministic materialization, golden fixtures, offline validation, digest recording, fast CI lane.

**Kickoff prompt (repeat the 4.4 TDD loop per command):**
> Plan mode. Read docs/prd-v0_3.md section 15 and build-plan D6, D7. Implement cli/pgf per the PRD architecture. Requirements beyond the PRD: (1) schemas.py registers all bundled schemas from disk into a local resolver; any $ref that would require a network fetch is a hard error, exit code 3. (2) materializer determinism exactly per PRD 15.3. (3) export computes SHA-256 digests of every packaged file into the release.exported payload, state.json, and provenance-index.md, and export verification fails naming the file on any mismatch; digests are described in --help and docs as a convenience, not integrity (D6). (4) export accepts --format with the single value release-package; unknown values exit 3 pointing at ROADMAP.md. (5) materializer warns on edge endpoints outside the current artifact and on materiality downgrades lacking a subsequent review event. Write failing tests and fixtures first; after I review and commit them, implement without modifying tests/ or expected/.

**CI (same phase):** the PRD section 17 lane, plus two steps: the network-disabled run of `pgf validate`/`pgf check` (criterion 16) and the AGENTS.md line-count check.
**Codex checkpoint:** phase-gate read #1 (all three prompts). Focus per Review guidelines: determinism, offline resolution, exit codes.
**Exit:** criteria 1 through 7, 13, 16, 17, 21.

### Phase 3: Claude Code enforcement (1 to 2 weeks)

**Goal:** four real hooks, four subagents, five skills; the gate holds via hook, CLI, and CI.

**Kickoff prompt:**
> Plan mode. Read docs/prd-v0_3.md sections 9.4, 9.5, 13, and build-plan 3.3 to 3.5 and D9. Implement the four hooks against the current hook contract (stdin JSON; exit 0 allow, 1 warn, 2 block): no-secret-leak.py (PreToolUse Write|Edit|Read; content patterns for keys, tokens, and the planted test secret), block-release.py (PreToolUse Bash; parse tool_input.command for pgf export and exit 2 with the failing gate named when the release gate fails), append-event.py and validate-record.py (PostToolUse per PRD). Create the four subagent files per build-plan 3.4 (read-only tools; drafter returns text to parent). Create the five skills as .claude/skills/<name>/SKILL.md; claim-normalization implements D9: verifiability filter, decontextualization (no unresolved pronoun subjects), confidence-gated extraction (ambiguous sentences become question nodes), materiality triage per materiality-policy.md; put literature notes in an adjacent references.md, keep SKILL.md under 500 lines. Set disable-model-invocation: true and user-invocable: true on produce-review-packet and generate-approval-summary, then verify manual slash invocation works.

**Human checkpoint:** confirm export is blocked without a human approval event via all three paths (hook, CLI, CI); confirm CLAUDE.md does not duplicate AGENTS.md; run the planted-secret test live.
**Exit:** criteria 5, 15; the ladder in 4.2 fully populated.

### Phase 4: canonical example end to end (1 to 2 weeks)

**Goal:** the association board brief through to a release package, exercising every schema addition.

**Kickoff prompt:**
> Read docs/build-plan.md A4-equivalents in section 6 (criteria 8, 18, 19, 20) and docs/prd-v0_3.md section 12. Complete examples/association-board-brief end to end using the three workflows: one surfaced contradiction with a disposition, one accepted override, one agent_extracted claim later edited by a human (origin becomes hybrid), one source refreshed after failing the freshness policy, a human approval record, and the exported package with its digest list rendered in provenance-index.md. Build the hand-built reference claim register for one section and the extraction-quality fixture comparing the committed register against it (coverage of high-materiality claims; no unresolved pronoun subjects). Record the precision number in the walkthrough.

**Codex checkpoint:** phase-gate read #2, plus an optional Codex cloud reproduction of the two-command proof in a clean container.
**Exit:** criteria 2, 3, 4, 8, 9, 18, 19, 20.

### Phase 5: docs and DX (1 to 2 weeks)

**Goal:** a stranger can run the example unaided; the regulatory layer is accurate and date-stamped.

**Tasks (multiple sessions):** quickstart; claude-code-setup.md and codex-setup.md (adapt section 2 of this plan); architecture.md (including the honest export round-trip statement: PROV lossless for history, OTel lossy by design, in-toto natural for the release event); schema-reference.md; security-model.md (cooperative honesty plus the D6 upgrade path); docs/standards-alignment.md with the four crosswalks (NIST AI 600-1 including its Content Provenance consideration, OMB M-25-21 high-impact documentation practices, ABA Op. 512 duties, the three-row accessibility mapping: Section 508 WCAG 2.0 AA baseline, ADA Title II WCAG 2.1 AA with the extended April 2027/2028 dates, WCAG 2.2 AA recommendation); docs/faq.md with the three required answers (tamper-proof: no; reproducible: replay only; C2PA: no); instructions/review.accessibility-and-disclosure.md updated with the corrected dates; every regulatory reference carrying an as-of date.
**Human checkpoint:** clean-clone timed quickstart run by whichever of you did not write it.
**Exit:** criteria 10, 12; timed adoption number recorded.

### Phase 6: OSS launch candidate (days)

v0.1 tag (release script rewrites schema `$id` values to the tag URI, D7), changelog, release notes, demo walkthrough, blog outline leading with the honesty stance. **Codex checkpoint:** phase-gate read #3 plus a license/packaging/docs read. **Human approval recorded as a PGF approval event on the repo's own release, eating the dog food.**
**Exit:** all 21 criteria; public.

---

## 6. Consolidated acceptance criteria (final, replaces PRD section 25.1)

1. A fresh clone installs and runs the canonical example.
2. `python -m pgf check examples/association-board-brief` passes.
3. `python -m pgf export examples/association-board-brief` emits a complete release package.
4. Removing a required supporting-evidence event makes `pgf check` fail and name the offending claim.
5. Removing the human approval event makes export fail (via CLI and via the hook).
6. The same event log materializes to byte-identical nodes.json, edges.json, and state.json across two runs.
7. The same event log materializes to byte-identical output on a second machine or a clean CI runner.
8. The canonical example includes at least one surfaced contradiction and one recorded override.
9. The release package's human-readable trio is complete and readable without opening graph/.
10. The accessibility note states that only automated checks ran and human audit is still required.
11. AGENTS.md is canonical and under 200 lines; CLAUDE.md imports it and does not duplicate it.
12. The docs state the cooperative-honesty scope and the replay-not-regeneration determinism scope.
13. The fast CI lane passes, including the determinism diff gate.
14. No real client data, CUI, or secrets exist anywhere in the repo.
15. The secret-scan hook is PreToolUse and blocks a planted test secret before the write; the permissions deny list hides .env and secrets paths.
16. `pgf validate` and `pgf check` pass on the canonical example with networking disabled; a schema $ref requiring a network fetch is a test failure.
17. The exported package records SHA-256 digests for every packaged file; altering one byte of a packaged file causes package verification to fail and name the file.
18. Every claim node carries an origin value; the canonical example contains at least one agent_extracted claim subsequently edited by a human.
19. Every source node carries retrieved_at; a source staler than the artifact policy causes `pgf check` to fail and name the source.
20. The claim-normalization fixture passes: the committed register covers all high-materiality claims in the hand-built reference, and no claim text has an unresolved pronoun as its subject.
21. Concatenating the nodes.json of two artifacts produces zero node-ID collisions.

## 7. ROADMAP.md Next block (final)

- Tamper-evidence (v1.0 candidate): hash-chained event log; release-package attestation as an in-toto Statement (subject = the digest list recorded by release.exported) in a DSSE envelope; Sigstore keyless signing and optional Rekor anchoring where a buyer requires an external log. No bespoke signature formats.
- Exporters behind `pgf export --format`: prov-jsonld (W3C PROV interchange), otel (event-to-span replay once the GenAI semantic conventions stabilize; Development status as of mid-2026), in-toto (the attestation above).
- Eval lane: Promptfoo + Inspect; consumes claim origin and the extraction-quality fixture as ground truth; add evaluation.recorded to the event-type registry when built.
- Cross-artifact edges: promote the pgf check warning on external endpoints to a supported derived_from between artifacts.
- Materiality-downgrade check: promote the Phase 2 warning to a hard pgf check failure once the legal pack defines downgrade policy.
- Skills location: revisit .claude/skills vs the .agents/skills cross-agent convention when Claude Code documents shared-skills support, or when any review procedure is pasted into Codex a fourth time (then also ship it as an .agents/skills skill).
- Legal and GovCon instruction packs. Legal priority raised: California COPRAC's March 2026 proposed rule amendments move AI verification duties toward disciplinary force. GovCon pack speaks CMMC Phase 2 (C3PAO Level 2 from Nov 10, 2026) and NIST SP 800-171 documentation language without implying certification relevance.
- GOVERNANCE.md and a conformance test suite (spec-level MUST checklist runnable against any implementation) as v1.0 credibility items.
- Standards participation calendar: NIST CAISI AI Agent Standards Initiative (interoperability profile expected Q4 2026), AI RMF revision comment windows, OTel GenAI SIG tracking. One substantive NIST comment within two quarters of launch or redirect the attention to OTel.

## 8. Threat model additions (append to PRD section 22.2)

- Provenance theater (low-quality machine-extracted claim nodes creating false assurance): controls: the claim-normalization skill's verifiability, decontextualization, and materiality rules; the extraction-quality fixture; claim origin visible to every reviewer; human review of high-materiality claims.
- Reproducibility overclaim (deterministic materialization misdescribed as deterministic provenance): controls: the AGENTS.md replay-vs-regeneration rule; claim origin and extraction metadata; the FAQ answer; Phase 5 docs review greps for "reproducible" without the replay qualifier.
- Materiality-downgrade bypass (lowering a claim's materiality removes it from gate scrutiny): controls: verifier question 5; the pgf check downgrade warning; append-only history making every downgrade visible.

## 9. What changed since the review document, and verification notes

Improvements in this final version, verified against official docs in July 2026:

1. **Permissions deny-list added as enforcement layer 2** (3.3): Claude Code evaluates deny rules first and hides matched files, which is stronger for path-known secrets than the PreToolUse hook; the hook remains for content-based detection. Source: Claude Code settings/permissions documentation and current best-practice references.
2. **Hook exit-code contract updated** (3.3): exit 1 is allow-with-warning, exit 2 blocks; the decision/reason JSON return style is deprecated. The PRD's "exit 1 blocks nothing" was correct but incomplete.
3. **Subagent creation is file-first** (3.4): the /agents interactive wizard was removed in recent releases; the four agent files are written directly, which suits a committed, reviewed repo anyway.
4. **Codex Review guidelines section added to AGENTS.md** (3.1): Codex's GitHub code review reads a `## Review guidelines` section from AGENTS.md and scopes P0/P1 comments to it; PGF's review priorities now live once and drive both local and GitHub review surfaces. Source: developers.openai.com/codex/integrations/github.
5. **Codex skills path corrected** (2.3, D17): current Codex docs place repo-shared skills at `.agents/skills/` and personal skills at `~/.agents/skills/` (the PRD said `.codex/skills` or `.agents/skills`). No v0.1 behavior change; the ROADMAP trigger is sharper.
6. **Codex workflow facts folded into 4.5**: one thread per task; prompts structured like GitHub issues; Codex trained to run AGENTS.md-listed checks before finishing; `codex exec` available for scripted checks; local review flow available pre-commit.
7. **TDD-against-fixtures elevated to the standard loop** (4.4), matching both vendors' current guidance and PGF's golden-fixture design.
8. **Phase kickoff prompts added** (5) so each phase starts as a paste, not a retranslation of the PRD.

Not re-verified this pass and treated accordingly: the PRD's specific Claude Code bug reference (#26251) for disable-model-invocation (the belt-and-suspenders pattern in 3.5 is robust whether or not the bug persists); exact current model names behind the `sonnet` alias (aliases used instead); Codex plan tiers beyond "Plus/Pro include Codex." Everything else in sections 2 to 4 traces to the doc links at the top of this file.
