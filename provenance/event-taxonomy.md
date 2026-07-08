# Event Taxonomy

Status: v0 loose draft (Phase 1). Normative statements use RFC 2119 keywords (MUST, SHOULD, MAY).
The event log (`events.jsonl`) is the system of record for an artifact within the cooperative-honesty
scope: append-only, one JSON object per line, plaintext and editable, not tamper-evident in v0.1.

Each line is validated against `schemas/v0/graph-event.schema.json`. See `graph-model.md` for how a
record-creating event carries its node under `payload.node` or its edge under `payload.edge`.

## 1. Single-writer assumption and event ordering

**Single-writer assumption (stated out loud).** v0.1 assumes **one writer per artifact** appends to
that artifact's `events.jsonl`. Two agents, or a human and CI, appending to the same artifact
concurrently is out of scope for v0.1 and can collide. This assumption is a real limitation, not an
oversight; multi-writer support is a future concern.

**`seq` is the order key.** `seq` is a per-artifact integer, minimum 1. Under the single-writer
assumption, `seq` is **dense, gap-free, and equal to creation order**: it is the authoritative
ordering of events for an artifact. A materializer MUST replay events in `seq` order.

**`seq` collision is an integrity error.** Two events for the same artifact with the same `seq` is a
**detectable integrity error** (the single-writer assumption was violated, or the log was edited). A
conforming checker MUST be able to detect a duplicate or non-monotonic `seq` and report it; it MUST
NOT silently renumber.

**`event_id` is a ULID, for identity — not for cross-process ordering.** Every `event_id` MUST be a
ULID. The ULID guarantees **distinct identity** even if two events were created in the same
millisecond, and is roughly time-sortable, so ULIDs keep colliding events distinct **for diagnosis**
and give a future multi-writer merge a total order to fall back on **without renumbering history**.

The ULID requirement is normative here but is **not regex-enforced** in the v0.1 schema (`event_id`
is a plain string), keeping the loose phase tolerant.

> **No cross-process lexicographic-ordering guarantee.** v0.1 does **not** claim that ULID
> lexicographic order matches creation order across writers/processes or within sub-millisecond
> clock resolution. `seq`, under the single-writer assumption, is the only ordering guarantee. ULID
> order is a best-effort fallback for a future merge, not a v0.1 ordering promise.

## 2. Actors and delegation

The `actor` on every event is a typed-prefix string matching
`^(human|agent|service):[A-Za-z0-9._:-]+$`:

- `human:` — a person (e.g. `human:board-liaison-01`).
- `agent:` — an autonomous or assistant runtime (e.g. `agent:claude-code-drafter`).
- `service:` — a non-interactive service such as CI (e.g. `service:pgf-ci`).

**Delegation.** An agent acting for a person MUST record the delegation in
`actor_detail.on_behalf_of` (matching `^(human|service):[A-Za-z0-9._:-]+$`). Example: a drafter agent
records `actor: "agent:claude-code-drafter"` with `actor_detail.on_behalf_of: "human:board-liaison-01"`.
`actor_detail` is permissive (`additionalProperties: true`) so future signed-identity assertions land
without a schema break.

## 3. Trace correlation (correlation, not identity)

The optional `tool.trace_id` / `tool.span_id` fields answer the "same primitive wearing two hats?"
question with **no**. An operational telemetry span (e.g. an OpenTelemetry span) is sampled,
retention-limited, and cardinality-constrained; a PGF event is the durable, complete, claim-level
system of record. The correct relationship is **correlation, not identity**: when a runtime emits
trace spans, a PGF event MAY point into the trace, and vice versa.

- `trace_id` — W3C Trace Context trace-id, 16 bytes as 32 lowercase hex chars (`^[0-9a-f]{32}$`).
- `span_id` — W3C Trace Context span-id, 8 bytes as 16 lowercase hex chars (`^[0-9a-f]{16}$`).

**All-zero values are invalid** per W3C Trace Context (an all-zero trace-id or span-id is the
"invalid" sentinel). v0.1 documents this rule but does **not** enforce it in the regex; the pattern
checks only shape (length and hex), not the all-zero exclusion.

## 4. Event-type registry (canonical v0.1)

`event_type` is validated by pattern (`^[a-z_]+\.[a-z_]+$`) in the schema — **no hard enum** — so
Next-phase additions (e.g. `evaluation.recorded`, `risk.added`) extend this registry without a schema
version bump. The materializer (Phase 2) is the layer that rejects an unregistered type; the schema
does not. The **payload carrier** column states where each event's record or context lives:

- `node` → the event carries a node record under `payload.node`.
- `edge` → the event carries an edge record under `payload.edge`.
- `envelope-only` → no full record; payload holds only event-specific delta/reference/gate fields and
  is validated against the graph-event schema only.

| event_type | Payload carrier | Notes |
| --- | --- | --- |
| `artifact.created` | `node` (artifact) | Introduces the artifact. |
| `artifact.updated` | envelope-only | Delta to the artifact node. |
| `source.added` | `node` (source) | |
| `source.updated` | envelope-only | Delta to a source node. |
| `evidence.added` | `node` (evidence) | |
| `claim.added` | `node` (claim) | |
| `claim.updated` | envelope-only | Delta to a claim node (e.g. `prior_status` sibling). |
| `edge.added` | `edge` | Generic edge creation. |
| `edge.removed` | envelope-only | References an edge ID to remove; not a full record. |
| `question.added` | `node` (question) | No dedicated schema in v0.1. |
| `assumption.added` | `node` (assumption) | No dedicated schema in v0.1. |
| `constraint.added` | `node` (constraint) | No dedicated schema in v0.1. |
| `draft_span.added` | `node` (draft_span) | No dedicated schema in v0.1. |
| `review.requested` | envelope-only | A request/gate record, not a review node. |
| `review.recorded` | `node` (review) | |
| `contradiction.detected` | `edge` (contradicts) | Carries the `contradicts` edge plus a `detection_method` sibling; no separate `edge.added`. |
| `override.proposed` | envelope-only | A proposal; the edge is not created until acceptance. |
| `override.accepted` | `edge` (overrides) | Carries the `overrides` edge plus `superseded_id`/`reason` siblings; no separate `edge.added`. |
| `approval.requested` | envelope-only | |
| `approval.recorded` | `node` (approval) | Human approval decision. |
| `release.check_requested` | envelope-only | Release-gate request. |
| `release.check_passed` | envelope-only | Release-gate result. |
| `release.check_failed` | envelope-only | Release-gate result. |
| `release.exported` | `node` (release) | The exported release-package record. |

The non-duplication invariant (one edge per event) and the `payload.node` / `payload.edge` placement
rule are specified in `graph-model.md` §3.
