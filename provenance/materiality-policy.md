# Materiality Policy

Status: v0 loose draft (Phase 1). Normative statements use RFC 2119 keywords. This document defines
the `materiality` enum on the `claim` node (`low`, `medium`, `high`, `critical`), who may assign and
change it, and how it drives release gating. Materiality is about **consequence** (how much a claim
matters to the reader's decision), distinct from **confidence** (how well-supported it is — see
`confidence-scale.md`).

## 1. Levels

| Level | Meaning | Example (association board brief) |
| --- | --- | --- |
| `low` | Incidental; a reader's decision does not turn on it. | Background phrasing, uncontested context. |
| `medium` | Supporting; informs but does not drive the recommendation. | A secondary trend cited in passing. |
| `high` | Decision-relevant; the board's decision depends on it. | The projected budget gap the dues change addresses. |
| `critical` | Consequential and hard to reverse if wrong; legal, financial, or reputational exposure. | A statement that a proposed change complies with the bylaws' amendment procedure. |

## 2. Who may assign and change materiality

- **Initial assignment.** Either a human author or an extraction agent MAY assign an initial
  materiality when a claim is created. An agent-assigned materiality is a proposal, recorded with the
  claim's `origin` (`agent_extracted`/`hybrid`) so a reviewer can see it was machine-proposed.
- **Increase.** A reviewer or the artifact owner MAY raise a claim's materiality at any time. Raising
  materiality is always permitted (it only tightens the gate).
- **Decrease (downgrade).** A materiality **downgrade** (e.g. `high` → `medium`) is a governance
  action: it MUST be performed by a human reviewer or the artifact owner, MUST be recorded as a
  `claim.updated` event carrying the `prior_status`/prior materiality and a `reason` sibling, and
  SHOULD be followed by (or accompany) a `review.recorded` event. An agent MUST NOT unilaterally
  downgrade materiality.
- **Enforcement.** A downgrade lacking a subsequent review event is a defect: `pgf check` (Phase 2)
  **warns** and names the claim. This is a warning, not a hard failure, in v0.1.

## 3. Materiality drives release gating

The release gate (see `release-state-machine.md`) treats materiality as the trigger for evidentiary
rigor:

- Every `high`- or `critical`-materiality claim MUST be supported to a degree appropriate to its
  `claim_type`, per `release-state-machine.md` §2 condition 1: empirical claim types need a direct
  `supports` edge from an `evidence` node; a `recommendation`-type claim needs either a direct
  `supports` edge or the recommendation-support path (a passing review via `reviewed_by` plus a
  graph-traceable `derived_from`/`overrides` path to an evidence-supported high/critical claim). An
  inadequately supported high/critical claim is release-blocking.
- Every contradiction touching a `high`/`critical` claim MUST have a recorded disposition.
- `high`/`critical` claims are subject to the source-freshness check (see `source-hierarchy.md` §3).

For `recommendation`-type claims, materiality is the consequence of the recommended action. A
reviewer MAY approve a `high`/`critical` recommendation only after identifying the graph-traceable
evidence-supported claim path that justifies it. Narrative rationale does not replace a
graph-traceable support path.

A claim that cannot be supported is not silently dropped: it is marked unresolved (kept `open`/
`needs_review`, or paired with an open `question`) and surfaced, never hidden.

## 4. Materiality is not a regulatory determination

Materiality here is an editorial/decision-relevance judgment for governing an internal work product.
It is **not** a legal, securities, or regulatory materiality determination. Any domain-specific
materiality rule (a legal or GovCon standard) lives in a date-stamped instruction file, never in this
schema or in a gate.
