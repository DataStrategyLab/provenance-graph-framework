# PGF Decision Log

Authoritative record of settled decisions for the Provenance Graph Framework. On any conflict between this log and another doc or a chat, this log governs.

Disposition tags: [v0.1 change] | [Next] | [design-for] | [reject].
Status: proposed | accepted | built | revisited.

> This file is initialized in the Phase 1 PR with the decisions this PR enacts on public artifacts: the schema-contract rationale and the release-state-machine terminality fix. The complete Phase 1 decision set (payload shape, decision-field tolerance, no-framework-status, source-taint doctrine, release honesty, recommendation-support path, and others) is added as its own reviewed change in the governance-hygiene PR.

### [2026-07-07] Schema constraints only where a decision locks them  |  [design-for]  |  built
Decision: In schemas/v0, a JSON Schema enum or pattern appears only where a locked decision (D-number, A-number) or a PRD §10.1/§10.5 sketch requires it; every other field stays a tolerant string in v0.1, with additionalProperties permissive and no additionalProperties:false yet. This governs the nine schemas made public in the Phase 1 PR. Schema-enforced constraints (verifiable by grep -RE '"enum"|"pattern"' schemas/v0): source access enum (A1.3), actor and event_type patterns (A1.1/A1.9), trace_id/span_id hex patterns (A1.6), and the claim and artifact enums (PRD 10.5/10.1). Documented-and-deferred, NOT schema-enforced in v0.1: event_id is a ULID (D13, stated in event-taxonomy.md, checked by ids.py in Phase 2), and the node-ID-embeds-artifact-ID rule (checked by ids.py). Deliberately tolerant (no enum by design): edge.type, review.decision, approval.decision, and the W3C all-zero trace/span rule.
Dissent: hard enums would surface vocabulary mismatches earlier.
Test: every schema-enforced enum/pattern found by grep -RE '"enum"|"pattern"' schemas/v0 traces to a citation above; event_id and node-ID rules are documented not schema-enforced, so they correctly do not appear in that grep.
Migration: the v0 schemas are tolerant drafts, NOT a frozen contract; consumers should expect additive tightening at the phase-end freeze, not breaking changes within v0.1.
Supersedes: n/a; records the rationale for the public schema contract introduced in the Phase 1 PR.

### [2026-07-07] Release state machine: archived is the sole terminal state  |  [v0.1 change]  |  built
Decision: In release-state-machine.md §1 the normative machine uses the seven locked artifact.status values; archived is the SOLE terminal state; released permits exactly one post-release transition (released -> archived); archived has no outgoing transition. Corrects an internal contradiction (Codex P2) where both released and archived were declared terminal, which made archived unreachable and unenforceable by a future checker.
Dissent: making released terminal and treating archival as out-of-band is simpler, but drops a real lifecycle state.
Test: every non-terminal state has at least one outgoing transition; archived has none; released has exactly one (to archived); a checker can enforce terminality without contradiction.
Supersedes: fixes the terminality claim in release-state-machine.md §1 as first authored.
