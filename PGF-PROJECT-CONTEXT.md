# PGF-PROJECT-CONTEXT.md
## Fast-orientation context for PGF development

This repo file is the canonical fast-orientation context for the Provenance Graph Framework (PGF). Synchronized project copies are non-authoritative caches and must be refreshed from the current merged main commit after any governance change. A fresh chat in any synchronized project should read this first: it states what PGF is, the locked decisions (D1-D20), the non-negotiable guardrails, and the current build status. The living decision log (PGF-DECISION-LOG.md) records everything decided after the D1-D20 baseline; the repo is the source of truth for what exists; this file is the orientation layer over both.

When section 6 changes at a phase boundary, refresh every synchronized project copy from the merged main commit (replace the old copy, do not add a second).

---

## 1. What PGF is

The Provenance Graph Framework is a language-agnostic, repo-native framework for governed AI-assisted work products. It makes claims, sources, evidence, reviews, approvals, and release state traceable from intake through release. The human-readable release packet is the deliverable; the provenance graph is the supporting infrastructure.

PGF is work-product and process provenance. It is not a content-credentials or media-marking system (not C2PA, not EU AI Act Article 50 marking), and it is not an agent runtime.

---

## 2. Integrity scope (read this first)

PGF v0.1 provides cooperative-honesty provenance: a faithful record of good-faith work. It is NOT tamper-evident. The event log is plaintext and editable, and hooks are bypassable. PGF output is never described as tamper-proof or as a chain of custody. Tamper-evidence is a future option (v1.0: release-package digests wrapped in an in-toto Statement, signed as a DSSE envelope, optionally anchored in a transparency log), not a v0.1 promise. v0.1 records SHA-256 digests of exported release-package files for convenience only; recorded digests in an editable log are not an integrity control.

Materialization is deterministic replay of a recorded history. Claim extraction is not deterministic. PGF output is never described as "reproducible" beyond replay; the graph records what was decided, not what a model would decide again.

---

## 3. Non-negotiable guardrails (all output)

- PGF v0.1 is cooperative-honesty provenance, never tamper-evident. Never describe output as tamper-proof or chain-of-custody.
- Materialization is deterministic replay, not deterministic regeneration. Never call PGF output "reproducible" without the replay qualifier.
- PGF is work-product/process provenance, not a content-credentials or media-marking system (not C2PA, not EU AI Act Article 50 marking).
- Regulatory facts live only in date-stamped docs and instruction files, never in schemas or gates. Every regulatory claim carries an as-of date; time-sensitive claims are web-verified, not trusted from memory.
- Enforcement lives in tools (permissions, hooks, CLI, CI); guidance lives in prose.
- No secrets, real client data, CUI, or privileged material in any example. Examples are synthetic or anonymized.
- No agent marks anything release-ready. Release readiness is decided by pgf check, hooks, CI, and a human approval event.
- Do not fabricate citations, sources, authorities, commands, or test results. Do not hand-author the output of a tool that does not exist yet.
- Actor IDs use typed prefixes (human:, agent:, service:). An agent acting for a person records on_behalf_of in actor_detail.

---

## 4. Locked decisions (D1-D20 baseline, as of 2026-07-06)

These are the accepted baseline. A chat that proposes something already covered cites the D# rather than treating it as open. Revisiting a D# requires an explicit entry in PGF-DECISION-LOG.md with a `Supersedes: D#` line.

| # | Decision | Status |
|---|---|---|
| D1 | v0.1 is lean: schemas, thin CLI, hooks, four subagents, five skills, one association example, one fast CI lane. No server, DB, evals, MCP, legal/GovCon packs. | Locked (PRD) |
| D2 | Cooperative-honesty integrity scope; not tamper-evident; say so everywhere. | Locked (PRD) |
| D3 | AGENTS.md canonical and under 200 lines; CLAUDE.md is a thin `@AGENTS.md` shim (Claude Code does not read AGENTS.md natively as of July 2026; the import shim is the documented pattern). | Locked (PRD, verified) |
| D4 | Release packet is the product; graph is infrastructure. | Locked (PRD) |
| D5 | Enforcement in tools (permissions, hooks, CLI, CI); guidance in prose. | Locked (PRD) |
| D6 | v1.0 tamper-evidence path = in-toto Statement in a DSSE envelope, Sigstore signing; v0.1 records release-package SHA-256 digests only, described as convenience, never as integrity. | Locked (review, top finding 1) |
| D7 | Schema `$id` = tag-form identifier URI; `pgf validate` resolves all schemas from a bundled local registry; zero network in the core CLI, tested with networking disabled. | Locked (review, top finding 2) |
| D8 | Regulatory facts live only in date-stamped docs and instruction files, never in schemas or gates (Colorado repeal-replace, EU Omnibus deferral, and the DOJ Title II extension are the proof cases). | Locked (review, top finding 3) |
| D9 | Claim-normalization skill encodes verifiability filtering, decontextualization, confidence-gated extraction, and materiality triage, with a hand-built reference-register fixture. | Locked (review, top finding 4) |
| D10 | `actor` is a typed-prefix string (`human:`, `agent:`, `service:`) with an optional `actor_detail` extension object including `on_behalf_of`. | Locked (review, top finding 5) |
| D11 | Claim nodes carry required `origin` (human_authored, agent_extracted, hybrid) and optional `extraction` metadata; docs say deterministic replay, never deterministic regeneration. | Locked (review) |
| D12 | Source nodes require `retrieved_at` and `access`; optional `uri`, `content_digest`, `snapshot_ref`. | Locked (review) |
| D13 | Node IDs embed the artifact ID (globally unique); `event_id` is a ULID; single-writer assumption documented. `seq` is the order key, ULID is identity. | Locked (review) |
| D14 | `event_type` validated by pattern in schema, by registry in the materializer. | Locked (review) |
| D15 | PROV mapping table in graph-model.md; PROV-O adoption rejected; exporters (`prov-jsonld`, `otel`, `in-toto`) are Next behind a reserved `pgf export --format` flag. | Locked (review) |
| D16 | Optional `trace_id` / `span_id` in the event `tool` block (W3C Trace Context); OTel as store rejected. | Locked (review) |
| D17 | Skills stay in `.claude/skills/` for Claude Code; Codex prompts in `prompts/codex/`; migration to a shared `.agents/skills/` convention is a ROADMAP trigger, not a v0.1 move. | Locked (review) |
| D18 | Codex is a second reader, not a control; controls are the human, the deterministic CLI, and CI. | Locked (PRD) |
| D19 | Spec posture now (RFC 2119 language in `provenance/`), conformance suite at v1.0; NIST is the single standards-participation venue. | Locked (review, Part C) |
| D20 | Apache-2.0; moat is vertical packs plus delivery fluency, not the core schema. | Locked (PRD + review) |

---

## 5. Phase structure (PRD)

- **Phase 0 — scope lock (days).** Governed skeleton; first session runs under AGENTS.md, permissions, stub hooks. COMPLETE.
- **Phase 1 — loose schema plus one real artifact (~2 weeks).** Node/edge model discovered by building the association example against tolerant schemas. COMPLETE and merged.
- **Phase 2 — thin CLI (2-3 weeks).** The seven commands, deterministic materialization, golden fixtures, offline validation, digest recording, fast CI lane. NEXT (after the governance-hygiene PR).
- **Phase 3 — hooks and enforcement.** Append, validate, secret-block, release-block hooks; release gate holds via CLI and CI, not only hooks.
- **Phase 4 — canonical example end to end (~1-2 weeks).** Association board brief through to a release package, with a surfaced contradiction, a recorded override, a human approval record. `pgf export` produces the release package and digests.
- **Phase 5 — docs and developer experience (~1-2 weeks).** Quickstart, setup guides, architecture, schema reference, security model, example walkthrough.
- **Phase 6 — OSS launch candidate (days).** v0.1 tag, changelog, release notes, demo walkthrough.

Next (not planned in v0.1): legal and GovCon packs, Promptfoo and Inspect lanes, multi-lane CI, and the v1.0 tamper-evidence stack.

---

## 6. Current status

*Current after governance-hygiene reconciliation; Phase 1 baseline: commit `b39d1d3` (PR #3).*

- **Phase 1 is complete and merged** at `b39d1d3` (PR #3). Phase 0 is NOT "current"; Phase 1 is NOT "open." Codex advisory review returned clean at commit `28aa553`.
- **Canonical example (`association-board-brief`):** a hand-authored **50-event** append-only log (seq 1..50, dense) that **contains 26 node records and 11 edge records** (independently counted by the offline harness; no committed `pgf materialize` output exists yet), exercising **all 11 node types and all 6 edge types** (supports, contradicts, derived_from, reviewed_by, overrides, released_as).
- **Source snapshots:** **3 committed synthetic CSVs** — `s002-member-survey-2026.csv`, `s004-peer-dues-benchmark.csv`, `s005-tiered-dues-projection-2026.csv`. (s001 and s003 are citation-only by design.) Every **snapshot-backed** evidence excerpt resolves to its cited snapshot.
- **Model status: baseline established, freeze posture accepted.** Phase 1 established the *exercised v0.1 model baseline*; node/edge/event schemas remain tolerant v0 drafts. The Phase 2 implementation-freeze posture was accepted 2026-07-09: eight implementation-shaping decisions remain open (below) and MUST be resolved before dependent materializer or checker code. Open freeze-list items (Bin B, resolved against Phase 2 code, not by memo): `.updated` snapshot-vs-delta representation (the FIRST materializer milestone); review-role/accessibility-preflight satisfaction (condition 3); as-of-seq evaluation for all gate conditions; enum promotions for edge.type, review.decision, and approval.decision; assumption-to-evidence linkage (assumption_ref vs an "assumes" edge type); dedicated schemas for question/assumption/constraint/draft_span; artifact.status enum expansion; additionalProperties:false freeze. (`tool.runtime` is already a schema-enforced enum under PRD 10.6, not an open promotion question; its citation catch-up in the in-repo stub is hygiene work. See the 2026-07-09 baseline and 2026-07-10 reconciliation entries in PGF-DECISION-LOG.md.)
- **No implemented CLI.** The `pgf` entrypoint is a fail-closed Phase-0 stub (`cli/pgf/__main__.py` exits 2; check/validate/gates/events/schemas/materializer are one-line "(placeholder, Phase 2)" files). `pgf check` / `pgf validate` / `pgf materialize` do not exist yet.
- **No real hooks and no CI.** There are no `.github/workflows/`. Standing up the CI lane is a Phase 2 gate. Release checks in the Phase 1 example are hand-authored human checkpoints; no service actor is exercised in Phase 1 (the A1.1 pattern still permits `service:`; real `service:pgf-ci` coverage is added in Phase 2 through a separate fixture or newly appended checker evidence, NOT by rewriting the merged Phase 1 log).
- **Materialized graph outputs** (`nodes.json` / `edges.json` / `state.json`) are **Phase 2 `pgf materialize`** outputs — de-committed / absent in Phase 1. **Release-package outputs** (`release-package/` + `file_digests`) are **Phase 4 `pgf export`** outputs.
- **`.updated` deterministic replay is the first materializer milestone** (Phase 2).
- **In-repo decision log** is now the full Phase 1 log, expanded from the two-entry stub (schema-constraints + terminality) by this governance-hygiene PR.
- **Repo governance files are canonical.** As of this hygiene merge, the repo copies of PGF-PROJECT-CONTEXT.md and PGF-DECISION-LOG.md are authoritative for accepted governance; synchronized project copies are non-authoritative caches and must be refreshed from the current merged main commit after any governance change.
- **Merge posture:** admin bypass through Phase 2 (solo-approver phase; second approver Adaora not yet active). Branch protection remains on.

**Next: Phase 2 opens with the implementation-freeze checkpoint.** With this hygiene PR merged, the eight open Bin B items (above) are settled at the Phase 2 opening implementation-freeze checkpoint before dependent materializer or checker code is written; the FIRST Phase 2 implementation PR creates real CI alongside real tests. (Do not gate the freeze checkpoint on CI that does not yet exist.)
