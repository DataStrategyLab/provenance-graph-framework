# Phase 1 freeze record

Status: reference index for the Phase 1 → Phase 2 boundary. This document **does not decide anything**
and **does not restate any normative rule**. Under the one-authoritative-home rule (PGF-DECISION-LOG.md,
2026-07-07 "Normative rules have one authoritative home; other docs defer, not duplicate") every rule
named here lives authoritatively in `provenance/*.md`, `docs/build-plan.md`, the PRD, or the decision
log; this file only points at those homes.

It was produced by the governance-hygiene reconciliation, which makes **no schema, event-log,
source-snapshot, or gate-semantic changes; the only example-path edit is the documented count correction
in `examples/association-board-brief/expected/README.md`.**

## 1. Phase 1 exercised baseline

Phase 1 discovered the v0.1 model by building one synthetic example against tolerant schemas. The model
is **exercised, not frozen**. As merged at `b39d1d3` (PR #3):

- `examples/association-board-brief` — a **50-event** append-only log, seq **1..50 dense**, materializing
  to **26 node records** and **11 edge records**, exercising **all 11 node types and all 6 edge types**
  (counts independently verified by the offline harness; see `reports/phase1-ground-truth-inventory.md`).
- **9** tolerant v0 JSON schemas (`schemas/v0/`), **6** provenance model docs (`provenance/`), **1**
  synthetic worked example.

## 2. Settled-decision index

The decisions below are **settled**. They are referenced by decision-log title + date only and are
**not restated normatively** here; read the named entry in `PGF-DECISION-LOG.md` for its Decision /
Dissent / Test / Supersedes. The index is partitioned into model/example decisions and
process/governance decisions.

### 2a. Settled model and example decisions

- [2026-07-06] A1.8 event ordering: seq is the order key, ULID is identity
- [2026-07-07] Event payload shape: records nest under payload.node / payload.edge
- [2026-07-07] Schema constraints only where a decision locks them
- [2026-07-07] review.decision and approval.decision stay tolerant strings in v0.1
- [2026-07-07] Source text is untrusted input (model-layer doctrine)
- [2026-07-07] Release state machine uses the locked artifact status enum; archived is sole terminal
- [2026-07-07] Canonical example release must pass the gate honestly
- [2026-07-07] Recommendation claims require a graph-traceable support path, present before the gate
- [2026-07-07] Release support gate scoped to ACTIVE claims, evaluated as-of-seq
- [2026-07-07] Release node records only materialized fields; no claims about nonexistent packages
- [2026-07-07] Release lifecycle events are human-authored checkpoints in Phase 1
- [2026-07-07] Materialized fixtures are de-committed, not hand-authored
- [2026-07-07] Source snapshots are committed and parser-visibly synthetic
- [2026-07-07] A1.8 is exercised by a Phase 2 pgf check test, not by deforming the example
- [2026-07-07] Evidence excerpts must match committed source snapshots
- [2026-07-09] Phase 1 establishes the exercised model baseline; Phase 2 begins with an implementation freeze

### 2b. Settled process and governance decisions

- [2026-07-07] No framework or spec status in durable docs
- [2026-07-07] Git history is provenance: structured commit trailers, no squash, no manifest
- [2026-07-07] Phase 1 merged via admin bypass (solo-approver phase)
- [2026-07-07] Decision log created in the Phase 1 PR (in-repo stub), not deferred wholesale
- [2026-07-07] Normative rules have one authoritative home; other docs defer, not duplicate
- [2026-07-09] Preserve Phase 1 history when adding service-actor coverage
- [2026-07-09] Repo governance files become canonical after hygiene reconciliation

The three 2026-07-10 reconciliation entries are the hygiene reconciliations this record accompanies;
they are recorded in `PGF-DECISION-LOG.md`, not re-listed here as baseline.

## 3. Open implementation-freeze items (Bin B — exactly eight)

These eight surfaced during Phase 1 review and are **deliberately unresolved**. Each is settled at the
Phase 2 opening implementation-freeze checkpoint, against a targeted materializer/checker milestone,
spike, or fixture — not by memo and not by one example (see the decision log's "Open freeze-list items"
section and the 2026-07-09 baseline entry for the authoritative detail):

1. Review-role / accessibility-preflight satisfaction (condition 3)
2. As-of-seq evaluation for all release-gate conditions
3. `.updated` snapshot-vs-delta representation (the FIRST materializer milestone)
4. Enum promotions for `edge.type`, `review.decision`, `approval.decision`
5. Dedicated schemas for `question` / `assumption` / `constraint` / `draft_span`
6. `artifact.status` enum expansion
7. `additionalProperties:false` freeze on node/edge schemas
8. Evidence-to-assumption linkage (`assumption_ref` vs an `assumes` edge type)

**`tool.runtime` is not a Bin B item.** It is already a schema-enforced enum in
`schemas/v0/graph-event.schema.json` under PRD 10.6; it is excluded from the Bin B enum-promotion
question (see the schema-constraints entry and the 2026-07-10 reconciliation entry in the decision log).

## 4. Accepted Phase 2 implementation-coverage commitments (outside Bin B)

Approach settled; only implementation detail remains — kept out of the Bin B open list:

- **Service-actor coverage.** The Phase 1 example exercises human and agent actors only (no CI exists).
  When Phase 2 builds `pgf check` as a CI service, real `service:pgf-ci` coverage is added through a
  separate Phase 2 fixture, a new artifact run, or newly appended truthful checker-produced execution
  evidence; the merged 50-event Phase 1 log stays byte-identical (2026-07-09 "Preserve Phase 1 history
  when adding service-actor coverage").

## 5. Phase 2 `pgf check` invariants

The Phase 2 checker enforces **21 primary invariants**, consolidated at the Phase 1 → Phase 2 boundary
and imported from the offline-harness analysis (`reports/phase1-offline-validation.md` Part 2, categories
A–H) using **that source's own A1…H22 numbering**. Each invariant below is anchored to its authoritative
home via its rule ID — this table is a reference, not a normative restatement. Each of the 21 primaries
is tagged **PRIMARY**; item B10 (ET-6) is tagged **MINOR SUB-ITEM** (which is why 22 numbered rows carry
21 primary invariants).

> **This 21-invariant checker set is distinct from the 21 consolidated acceptance criteria in
> `docs/build-plan.md` section 6.** The two share the count **21 by coincidence**; they are different
> artifacts (checker invariants vs. build/release acceptance criteria). Do not conflate them.

| ID | Invariant | Rule ID(s) → authoritative home | Class | MUST-enforce |
| --- | --- | --- | --- | --- |
| A1 | Edge endpoint typing | GM-1 → graph-model.md | [PRIMARY] | |
| A2 | Referential integrity | GM-1 (cross-artifact WARN GM-4) → graph-model.md | [PRIMARY] | ✔ edge referential integrity |
| A3 | Node-ID artifact embedding + global uniqueness | GM-3, crit-21 → graph-model.md / build-plan §6 | [PRIMARY] | |
| A4 | artifact_id cross-check | GM-9 → graph-model.md | [PRIMARY] | |
| A5 | One-edge-per-event / non-duplication | GM-8 → graph-model.md | [PRIMARY] | ✔ one-edge-one-event |
| A6 | Payload-carrier conformance | ET-7, ET-8, GM-5/6/7 → event-taxonomy.md / graph-model.md | [PRIMARY] | ✔ single-record-per-event |
| B7 | event_id is a ULID and unique | ET-4 → event-taxonomy.md | [PRIMARY] | |
| B8 | seq collision / non-monotonic detection (per artifact) | ET-3 → event-taxonomy.md | [PRIMARY] | |
| B9 | Delegation recorded (on_behalf_of) | ET-5 → event-taxonomy.md | [PRIMARY] | |
| B10 | all-zero trace/span IDs invalid | ET-6 → event-taxonomy.md | [MINOR SUB-ITEM] | |
| C11 | Active high/critical claim support (at the release-check seq) | RSM-4 Cond-1, MP-3 → release-state-machine.md / materiality-policy.md | [PRIMARY] | ✔ gate honesty as-of-seq (explicit instance) |
| C12 | Confidence-band consistency | CS-2, CS-3 → confidence-scale.md | [PRIMARY] | |
| C13 | Materiality-downgrade without review | MP-1, MP-2 → materiality-policy.md | [PRIMARY] | |
| D14 | Every contradiction disposed | RSM-4 Cond-2, MP-4 → release-state-machine.md / materiality-policy.md | [PRIMARY] | |
| E15 | Valid status transitions | RSM-1/2/3 → release-state-machine.md | [PRIMARY] | |
| E16 | Required review roles satisfied | RSM-4 Cond-3 → release-state-machine.md | [PRIMARY] | |
| E17 | Human approval exists and is human-authored | RSM-4 Cond-7, RSM-6 → release-state-machine.md | [PRIMARY] | |
| F18 | Source freshness / staleness | SH-6, MP-5, RSM-4 Cond-5 → source-hierarchy.md / materiality-policy.md / release-state-machine.md | [PRIMARY] | |
| F19 | Accessibility/disclosure preflight + confidentiality/CUI clear | RSM-4 Cond-4/6 → release-state-machine.md | [PRIMARY] | |
| G20 | Offline schema resolution (exit 3) | crit-16, PRD Phase-2 → build-plan §6 / PRD | [PRIMARY] | |
| G21 | Exit-code + offender-naming contract | PRD §15.2 → docs/prd-v0_3.md §15.2 | [PRIMARY] | |
| H22 | Excerpt/snapshot resolution rule | SH-1; integrity scope → source-hierarchy.md | [PRIMARY] | |

### Early-highlighted MUST-enforce subset (four)

`PGF-DECISION-LOG.md` flags four of these invariants early (its "Phase 2 pgf check MUST-enforce
invariants" section): **single-record-per-event** (A6), **one-edge-one-event** (A5), **edge referential
integrity** (A2), and **gate honesty as-of-seq** (C11). They are an early-highlighted subset of the 21,
not the whole set and not the acceptance criteria.

**Gate honesty as-of-seq is cross-cutting**, not owned by C11 alone: a `release.check_passed` is
evaluated against replayed state at its recorded seq. **C11 (RSM-4 Cond-1) is the settled condition-1
instance**; the exact evaluation point for all remaining gate conditions is the open Bin B as-of-seq item
(§3, item 2), settled at the Phase 2 freeze checkpoint — **not by this document**.

## 6. Routed item (note only)

The `provenance/materiality-policy.md` disposed-status restatement (drift-audit optional item) is routed
**out of governance-hygiene scope** by prior disposition; it is recorded here as routed and nothing more.
