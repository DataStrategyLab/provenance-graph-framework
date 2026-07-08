# Graph Model

Status: v0 loose draft (Phase 1). The node and edge model is discovered by building the canonical
example against tolerant schemas and is frozen only at the end of Phase 1. Normative statements use
RFC 2119 keywords (MUST, SHOULD, MAY). This document plus `schemas/v0/` is the spec; `cli/` is its
reference implementation.

Scope note (integrity): PGF v0.1 is cooperative-honesty provenance — a faithful record of
good-faith work. It is not tamper-evident: `events.jsonl` is plaintext and editable. This model
records what was decided; it does not prove that the record was not altered. See `AGENTS.md`.

## 1. Nodes and edges

The graph is a set of **nodes** (typed records) connected by directed **edges** (typed
relationships). The human-readable release packet is the deliverable; the graph is the supporting
infrastructure that makes the packet trustworthy.

### 1.1 Node types (v0.1)

| Node type | Dedicated schema | Meaning |
| --- | --- | --- |
| `artifact` | `artifact.schema.json` | The governed work product. |
| `claim` | `claim.schema.json` | A material statement, supported by evidence or marked unresolved. |
| `source` | `source.schema.json` | Where evidence came from, when and how retrieved. |
| `evidence` | `evidence.schema.json` | A specific excerpt from a source bearing on a claim. |
| `review` | `review.schema.json` | A recorded review by a reviewer role. |
| `approval` | `approval.schema.json` | A human approval/rejection decision. |
| `release` | `release.schema.json` | An exported release-package record. |
| `question` | none (v0.1) | An open question raised during the work. |
| `assumption` | none (v0.1) | A stated assumption the work rests on. |
| `constraint` | none (v0.1) | A constraint the artifact must satisfy. |
| `draft_span` | none (v0.1) | A span of draft text linked to a claim. |

`question`, `assumption`, `constraint`, and `draft_span` have **no dedicated schema in v0.1**. They
are carried as event payloads validated loosely by the graph-event schema's permissive `payload`
object. Whether any of them earns a dedicated schema is a phase-end freeze decision.

### 1.2 Edge types (v0.1)

The v0.1 edge-type registry (six values). `edge.type` is validated as an open **string** in the
schema (parity with the open `event_type` pattern), documented — not enum-enforced — here:

| Edge type | From → To | Meaning |
| --- | --- | --- |
| `supports` | evidence → claim | The evidence supports the claim. |
| `contradicts` | evidence/claim → claim | The endpoint contradicts the claim. |
| `derived_from` | node → node | The source node was derived from the target (e.g. claim from source, artifact from artifact). |
| `reviewed_by` | claim/artifact → review | The node was reviewed by the review event. |
| `overrides` | claim → claim | The source claim supersedes the target claim after an accepted override. |
| `released_as` | artifact → release | The artifact was released as the release record. |

Edge endpoints (`from`, `to`) accept **any well-formed node ID**, including IDs outside the current
artifact (see §2). A conforming `edge` MUST carry `type`, `from`, and `to`.

## 2. Node IDs and cross-artifact endpoints

Every node ID is globally unique because it **embeds its artifact ID**:

```
<node_type>:<artifact_id>:<local_id>
claim:association-board-brief-001:c014
source:association-board-brief-001:s003
edge:association-board-brief-001:x004
```

A conforming node ID MUST embed the artifact ID of the artifact that introduced the node. This rule
is documented here and enforced by `cli/pgf/core/ids.py` in Phase 2; it is **not** regex-enforced in
the v0.1 schemas (the `id` field is a plain string), keeping the loose phase tolerant.

Real organizations produce artifacts that cite other artifacts (a board brief citing last quarter's
advisory). v0.1 does not need cross-artifact edges, but it MUST NOT make them impossible. Therefore
edge endpoints MAY reference node IDs belonging to another artifact. In v0.1, `pgf check` **warns,
and MUST NOT fail**, on an edge endpoint whose embedded artifact ID differs from the current
artifact. A future `derived_from` edge between artifacts then requires zero schema migration.

## 3. Where records live: the event payload

Nodes and edges are not stored as free-standing files in v0.1; they are **created by events** in the
append-only `events.jsonl` log and reconstructed by deterministic replay (§5). A record-creating
event carries its record under a **named key** in the event `payload`, alongside event-specific
sibling fields. This mirrors the envelope-plus-data pattern used by event formats such as
CloudEvents: the event envelope and the data record serialize independently.

**Placement rule.**

- An event that creates a first-class **node** MUST carry the node record under `payload.node`. This
  includes the unschematized node types (`question`, `assumption`, `constraint`, `draft_span`).
- An event that creates a first-class **edge** MUST carry the edge record under `payload.edge`.
- **Event-specific context** (for example `reason`, `prior_status`, `superseded_id`,
  `detection_method`, `changed_fields`, `target_id`, `notes`) lives as **sibling fields under
  `payload`**, never inside the `node`/`edge` record. This keeps the record clean so node/edge
  schemas can later freeze `additionalProperties: false` without losing event-level context.

**Non-duplication invariant (MUST, not freeze-dependent).** One edge is created by exactly one
event. A given edge MUST NOT be created by both a semantic edge-bearing event and a separate
`edge.added`. Concretely: if `contradiction.detected` creates the `contradicts` edge, no separate
`edge.added` creates it; if `override.accepted` creates the `overrides` edge, no separate
`edge.added` creates it. (A separate `claim.updated` changing the superseded claim's `status` is a
node change, not a duplicate edge, and is allowed.)

**`artifact_id` cross-check (SHOULD).** When both are present, `event.artifact_id` SHOULD equal
`payload.node.artifact_id` (or `payload.edge.artifact_id`). A mismatch is a detectable integrity
problem; a future `pgf check` reports it.

**Update events.** In v0.1, `.updated` payloads are event-specific and permissive (`target_id`,
`changed_fields`, `prior_status`, `reason`) and are validated against the graph-event schema only —
they are deltas, not full records. Whether `.updated` events should instead carry a full post-update
snapshot under `payload.node` (so they too validate against the node schema) is **deferred to the
phase-end freeze**; `payload.node` is reserved for that possibility. RFC 6902 (JSON Patch) and
RFC 7396 (JSON Merge Patch) are reserved patch-format options for that decision; v0.1 does not invent
or freeze a custom patch format.

## 4. Claim origin semantics

Every `claim` carries a required `origin`:

- `human_authored` — a person wrote the claim.
- `agent_extracted` — an agent proposed the claim (optionally via a `skill`/`model` recorded in
  `extraction`).
- `hybrid` — an agent proposed the claim and a human then edited it.

`origin` exists so the claim register never lets the first fact launder the second: **materialization
is deterministic, claim extraction is not.** A reviewer reading the register MUST be able to see which
claims a model proposed. The `extraction` object records *what* proposed a claim; it does **not**
imply the claim could be regenerated identically. See §5.

## 5. Deterministic replay, not regeneration

A conforming **materializer** MUST produce byte-identical output for identical logs, on the same
machine and across machines (fixed key order, LF line endings, UTF-8, pinned number/timestamp
formatting, stable node/edge sort order, no injected UUIDs or wall-clock time). This determinism is a
property of **replay**: re-applying a recorded history yields the same graph.

Determinism MUST NOT be described as **regeneration**. The graph records what was *decided*, not what
a model *would decide again*. Claim extraction, drafting, and review judgments are not reproducible;
only the replay of their recorded outcomes is. Do not describe PGF output as "reproducible" beyond
replay.

## 6. W3C PROV mapping (document, do not adopt)

PGF's model is a near-neighbor of W3C PROV (stable since 2013). The mapping is provided so
standards-literate reviewers can place PGF; **PROV-O is not adopted** as the internal model (the
RDF/ontology machinery would sink the lean, file-first, JSON-Schema core, and no v0.1 ICP consumes
PROV-O natively). A PROV-JSONLD exporter is a Next item behind the reserved `pgf export --format`
flag; PROV-O adoption is rejected.

| PGF concept | Nearest W3C PROV concept |
| --- | --- |
| `claim`, `source`, `evidence` nodes | `prov:Entity` |
| `review`, `approval`, `release`, and record-creating events | `prov:Activity` |
| `actor` (human/agent/service) | `prov:Agent` |
| `derived_from` edge | `prov:wasDerivedFrom` |
| event `actor` attribution | `prov:wasAttributedTo` |
| record-creating event → node | `prov:wasGeneratedBy` |

**Three deliberate divergences** (PGF concepts with no PROV equivalent, because PROV records history
while PGF also *gates* it):

1. **Materiality** — PGF ranks claims by consequence (`low`/`medium`/`high`/`critical`) to drive
   release gating; PROV has no materiality notion.
2. **Confidence bands** — PGF records epistemic confidence (`low`/`medium`/`high`/`verified`) per
   claim; PROV does not model confidence.
3. **Release gating** — PGF's state machine blocks release on unmet conditions (unsupported material
   claims, undispositioned contradictions, missing human approval); PROV describes what happened, it
   does not withhold a release.

## 7. Related model docs

- `event-taxonomy.md` — event types, the single-writer assumption, `seq`/ULID ordering, and which
  event types carry `payload.node` vs `payload.edge` vs envelope-only.
- `confidence-scale.md`, `source-hierarchy.md`, `materiality-policy.md`, `release-state-machine.md` —
  the vocabularies and the state machine referenced above.
