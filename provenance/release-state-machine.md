# Release State Machine

Status: v0 loose draft (Phase 1). Normative statements use RFC 2119 keywords. This document defines
the artifact lifecycle, the conditions that block release, and the honest limits of the release
record. Release readiness is decided by `pgf check`, hooks, CI, and a human approval event — **no
agent marks anything release-ready.**

## 1. States and transitions

The normative state machine is the `artifact` node's `status` enum (`artifact.schema.json`, seven
values). A conforming artifact's `status` moves through:

```
intake -> drafting -> verification -> review -> approved -> released -> archived
```

`archived` is the sole terminal state and has no outgoing transitions. `released` is terminal for the
normal release flow except for a single permitted post-release transition, `released -> archived`
(archival after release). A conforming transition MUST move forward through the machine or record an
explicit, reasoned step-back — for example `review -> verification` when a review escalates. Transitions are recorded as `artifact.updated` events; the materializer replays them in
`seq` order.

**Non-normative workflow narrative.** The PRD's fuller lifecycle prose mentions finer stages —
`evidence_planning`, `claim_graph`, `contradiction_resolution`, and `packaged`. These are **workflow
sub-phases**, not `status` values: they are **not** part of the enum and are **not** stored on the
node. They describe work happening within the normative checkpoints (e.g. evidence planning and
claim-graph building happen while `status` is `drafting`/`verification`; packaging happens between
`approved` and `released`).

Whether the `artifact` `status` enum should later expand to the fuller lifecycle (PRD §10.1's short
seven-value enum vs PRD §11's longer lifecycle) is a **phase-end freeze decision, deferred and not
settled here.**

## 2. Release-blocking conditions (all MUST hold)

Release is **blocked** unless every one of these holds:

1. Every `high`- or `critical`-materiality claim is supported to a degree appropriate to its
   `claim_type`:
   - Empirical claim types (`factual`, `financial`, `market`, `technical`, `legal`, `policy`,
     `procedural`) MUST have at least one `supports` edge from an `evidence` node.
   - A `recommendation`-type claim MUST be supported by either:
     1. at least one direct `supports` edge from an `evidence` node, when the recommendation itself
        asserts an empirical basis; or
     2. a recommendation-support path: a passing `review.recorded` connected by a `reviewed_by` edge,
        AND a graph-traceable `derived_from` or `overrides` path to at least one `high`/`critical`
        claim that is itself evidence-supported.

   Reviewer notes MAY explain the judgment but do NOT satisfy the gate by themselves. A recommendation
   with a passing review but no graph-traceable path to an evidence-supported claim is NOT releasable.
   See `materiality-policy.md`.
2. Every contradiction has a recorded disposition (resolved, or an accepted `override`, or an
   explicit documented divergence).
3. Every required review role is satisfied by a `review.recorded` event with an acceptable decision.
4. Required accessibility and disclosure checks are complete, recorded as an automated **preflight**
   with the human-audit caveat carried into the note (automated checks are not a conformance claim).
5. No required evidence is stale beyond the artifact's freshness policy (see `source-hierarchy.md`).
6. No unresolved confidentiality or CUI issue.
7. A **human approval event** (`approval.recorded` by a `human:` actor) exists and authorizes the
   release. This is mandatory and MUST NOT be produced by an agent.
8. `pgf check` passes.
9. CI passes.

If any condition fails, `pgf check` (Phase 2) exits non-zero and names the failing condition; the
release hook blocks the export. These are enforcement points in tools, not prose.

## 3. The release record and its integrity limits

A `release.exported` event carries the `release` node under `payload.node`. The release node MAY
record `file_digests` (SHA-256 per packaged file).

**Honesty limit (MUST state, MUST NOT overstate).** Recorded digests are a **convenience** for change
detection. They are **not** an integrity control, a chain of custody, or evidence of
tamper-evidence: the event log is plaintext and editable in v0.1, and a recorded digest in an
editable log proves nothing about tampering. Do not describe a v0.1 release package as tamper-proof
or tamper-evident. Tamper-evidence is a future (v1.0) option — release-package digests wrapped in an
in-toto Statement, signed as a DSSE envelope — not a v0.1 promise. See `AGENTS.md` integrity scope.

## 4. Human approval is mandatory

No client-facing artifact reaches `released` without a human `approval.recorded` event. A `release`
node SHOULD reference the authorizing approval via `approval_ref`. An approval is distinct from a
review: a passing review is necessary but not sufficient; only a human approval authorizes release.
