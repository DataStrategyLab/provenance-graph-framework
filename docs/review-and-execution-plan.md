# PGF v0.3 Review: Blindspot Findings and Execution Plan

**Reviewed document:** Provenance Graph Framework, Lean v0.1 PRD v0.3 (July 6, 2026)
**Review date:** July 6, 2026
**Purpose:** Repo planning document. Part A is the execution plan, actionable by Claude Code against the PRD's Phase 0 to 6 roadmap and section 8 repo architecture. Part B is the blindspot and forward-fit analysis that justifies it. Part C is the category-leadership read. Part D lists what could not be verified.
**Disposition tags:** [v0.1 change] ship now. [Next] roadmap, do not build. [design-for] shape v0.1 cheaply for a predictable future. [reject] plausible idea, wrong for this project.

---

## Top 5 findings, priority order

1. **[v0.1 change]** The section 22.1 tamper-evidence upgrade path describes a bespoke hash-chain plus signed approvals; rewrite it to name the in-toto attestation Statement in a DSSE envelope (the format GitHub artifact attestations, SLSA, and Sigstore have converged on) as the v1.0 mechanism, and start recording SHA-256 digests of release-package files in the `release.exported` event now so a future attestation has a subject to bind to.
2. **[v0.1 change]** The schema `$id` strategy pins `raw.githubusercontent.com/.../main/...`, but `main` is a moving ref, and any remote `$ref` resolution violates the PRD's own no-hidden-network-calls rule (section 21); switch `$id` to tag-form identifier URIs and make `pgf validate` resolve every schema from a bundled local registry, verified by a network-disabled acceptance test.
3. **[v0.1 change]** Three regulatory anchors the PRD's ICP layer leans on moved in the last 60 days (EU AI Act Annex III high-risk deferred to December 2, 2027 while Article 50 transparency holds at August 2, 2026; DOJ extended ADA Title II deadlines to April 2027/2028; Colorado's AI Act was repealed and replaced before it ever took effect); correct the accessibility instruction and ICP context docs so PGF never ships a stale compliance date.
4. **[v0.1 change]** The claim-normalization skill, the PRD's own named highest risk, should adopt the three properties the 2024 to 2026 claim-extraction literature has converged on (verifiability filtering per VeriScore, decontextualization, confidence-gated extraction per Claimify) plus PGF's own materiality triage, and ship with a measurable extraction-quality fixture against the canonical example.
5. **[design-for]** Keep `actor` a string in v0.1 but make it forward-compatible now (enforced typed-prefix pattern plus an optional structured extension point for verification metadata), because agent identity is actively standardizing (OAuth 2.1 in MCP, A2A agent cards, four IETF drafts, MCP-I donated to DIF in March 2026) and an unconstrained bare string is the one schema break you can already predict.

---

# Part A. Execution plan (primary deliverable)

Organized by the PRD's phases and repo architecture. Every item carries: a binary recommendation with one winner, a one-line dissent, a falsifiable test, and a disposition tag. Copy-ready text is marked as such.

## Phase 0: scope lock

### A0.1 Positioning paragraph: process provenance, not content credentials [v0.1 change]
**Files:** `README.md`, `docs/faq.md` (Phase 5 placeholder note now)
**Task:** Add a positioning paragraph to the README distinguishing PGF from C2PA-style content credentials. The word "provenance" now strongly connotes signed media manifests to regulators and buyers: EU AI Act Article 50 machine-readable marking applies from August 2, 2026, California's AI Transparency Act (SB 942 as amended by AB 853) becomes operative August 2, 2026 with platform provenance-detection duties starting 2027, and C2PA has a live conformance program and trust list. A GovCon or association buyer who hears "provenance framework" may expect Content Credentials.
**Copy-ready README text:**

> PGF records the provenance of *work products and the process that produced them*: claims, sources, evidence, reviews, approvals, and releases. It is not a content-credentials system. It does not sign media, embed C2PA manifests, or mark AI-generated content for EU AI Act Article 50 or California AI Transparency Act purposes. Those standards answer "where did this file come from and was it AI-generated." PGF answers "which evidence supports each claim in this deliverable, who reviewed it, and who approved its release." The two are complementary and PGF may reference content-credential metadata on sources in a future version.

**Recommendation:** Add the paragraph. **Dissent:** It spends README real estate explaining what PGF is not. **Test:** In the Phase 5 clean-clone usability test, ask the tester what PGF does before and after reading the README; if any tester says "AI watermarking" or "content credentials," the paragraph failed or is missing.

### A0.2 Do not rename away from "provenance" [reject]
Renaming to avoid the C2PA collision (for example "Evidence Graph Framework") is plausible and wrong. "Provenance" is exactly the word NIST AI 600-1 uses (Content Provenance is one of its four primary considerations), it is the word W3C PROV owns academically, and the collision is survivable with one paragraph (A0.1). **Test:** If, after launch, more than a quarter of inbound questions confuse PGF with content credentials despite the README paragraph, revisit.

### A0.3 GOVERNANCE.md [Next] with a one-line design-for
Do not write a governance model now; a two-person project with a governance charter reads as cosplay. Add `GOVERNANCE.md` to ROADMAP.md as a v1.0 item (maintainer model, DCO already chosen, path to neutral stewardship if adoption warrants). **Design-for now:** in `CONTRIBUTING.md`, one sentence: schema changes require an ADR-style note in `provenance/` so future governance has a decision record to inherit. **Dissent:** Standards people check for governance early. **Test:** First external contributor of a schema-affecting PR; if the process is unclear to them, promote GOVERNANCE.md.

## Phase 1: loose schema plus one real artifact

### A1.1 Actor field: typed-prefix pattern plus extension point [design-for]
**Files:** `schemas/v0/graph-event.schema.json`, `provenance/event-taxonomy.md`, `AGENTS.md`
**Task:** Keep `actor` a string. Constrain it with a pattern requiring a typed prefix, and add an optional `actor_detail` object as an explicit extension point:

```json
"actor": { "type": "string", "pattern": "^(human|agent|service):[A-Za-z0-9._:-]+$" },
"actor_detail": {
  "type": "object",
  "properties": {
    "display_name": { "type": "string" },
    "runtime": { "type": "string" },
    "on_behalf_of": { "type": "string", "pattern": "^(human|service):[A-Za-z0-9._:-]+$" }
  },
  "additionalProperties": true
}
```

`on_behalf_of` captures the delegation fact (agent acting for a human) that every agent-identity effort treats as the core primitive. The `additionalProperties: true` block is where signed identity assertions, DIDs, or workload identity claims land later without a schema break. Why now: MCP adopted OAuth 2.1, A2A agent cards remain self-declared with no attestation binding, four IETF drafts (AIMS, WIMSE, Agentic JWT, SCIM for agents) appeared in early 2026, and MCP-I was donated to the Decentralized Identity Foundation in March 2026. None of these is settled, which is exactly why v0.1 should buy an extension point rather than a dependency.
**Recommendation:** Pattern plus `actor_detail`, winner over both a bare string and a required structured object. **Dissent:** The pattern adds friction for a solo user who just wants `actor: "andrew"`. **Test:** Write the canonical example with a human owner, a Claude Code drafter acting on behalf of the owner, and a CI actor; if any of the three cannot be expressed without abusing a field, the model is wrong.

### A1.2 Reject W3C Verifiable Credentials / DIDs for approver identity [reject]
Adopting VC/DID for signed approvals is the obvious "standards-aligned" move and it is wrong for this project: the agent-identity literature itself flags DID blockchain dependencies and circular trust bootstrapping, and DID/VC infrastructure is not production-ready for a repo-native tool. The v1.0 path is DSSE-signed approval events (A2.2's digest groundwork plus Sigstore keyless signing), which reuses the exact stack GitHub already runs for artifact attestations. **Test:** If a named buyer requires VC-format approvals in a procurement document, revisit; until then, no.

### A1.3 Source schema: retrieval provenance fields [v0.1 change]
**Files:** `schemas/v0/source.schema.json`, `provenance/source-hierarchy.md`
**Task:** The release gate already blocks on stale evidence, but staleness is undecidable unless sources record when and how they were retrieved. Require on the source node: `retrieved_at` (date-time), `access` (enum: `url`, `paywalled`, `internal_document`, `interview`, `dataset`, `other`), and add optional `uri`, `content_digest` (SHA-256 of the retrieved text snapshot), and `snapshot_ref` (path to a stored excerpt or snapshot within the artifact directory). This is the minimum honest RAG-layer provenance: where the evidence actually came from, when, and whether the text you cited is the text you saw.
**Recommendation:** Require `retrieved_at` and `access`; keep the rest optional. **Dissent:** `content_digest` without storing the snapshot invites a hash pointing at nothing. **Test:** Acceptance criterion 25.x below: deleting `retrieved_at` from a source in the canonical example makes `pgf validate` fail; setting it beyond the artifact's freshness policy makes `pgf check` fail with the source named.

### A1.4 Claim origin: honest machine/human attribution [v0.1 change]
**Files:** `schemas/v0/claim.schema.json`, `provenance/graph-model.md`
**Task:** Add to the claim node:

```json
"origin": { "type": "string", "enum": ["human_authored", "agent_extracted", "hybrid"] },
"extraction": {
  "type": "object",
  "properties": {
    "method": { "type": "string" },
    "model": { "type": "string" },
    "skill": { "type": "string" }
  },
  "additionalProperties": true
}
```

`origin` required, `extraction` optional. Rationale: materialization is deterministic but claim extraction is not, and the docs must not let the first fact launder the second. A reviewer looking at the claim register needs to know which claims a model proposed. This also gives the future eval lane its ground-truth axis for free.
**Recommendation:** Required `origin` enum. **Dissent:** One more required field on the highest-churn schema during the loose phase. **Test:** The canonical example contains at least one `agent_extracted` claim that a human subsequently edited (becoming `hybrid`), and the walkthrough narrates it.

### A1.5 Globally unique node IDs for cross-artifact provenance [design-for]
**Files:** `provenance/graph-model.md`, `cli/pgf/core/ids.py`
**Task:** Real orgs produce artifacts that cite other artifacts (a board brief citing last quarter's advisory). v0.1 does not need cross-artifact edges, but it must not make them impossible. Rule, stated in graph-model.md and enforced in `ids.py`: every node ID is globally unique because it embeds its artifact ID (`claim:association-board-brief-001:c014`), and edge endpoint fields are defined as accepting any well-formed node ID, with `pgf check` in v0.1 warning (not failing) on endpoints outside the current artifact. A future `derived_from` edge between artifacts then requires zero schema migration.
**Recommendation:** Embed artifact ID in node IDs now. **Dissent:** Longer IDs are uglier in fixtures. **Test:** Concatenate two artifacts' `nodes.json` files; zero ID collisions.

### A1.6 OTel correlation: a trace pointer, not a telemetry dependency [design-for]
**Files:** `schemas/v0/graph-event.schema.json`, `provenance/event-taxonomy.md`
**Task:** Answer the "same primitive wearing two hats" question explicitly in event-taxonomy.md: no. An OTel GenAI span (still Development status at semconv v1.41.x, with `create_agent` / `invoke_agent` / `execute_tool` lifecycle spans and MCP conventions also in Development) is operational telemetry: sampled, retention-limited, cardinality-constrained, and by OTel's own guidance sensitive payloads should live in external storage with a pointer. A PGF event is the system of record: complete, durable, claim-level. The correct relationship is correlation, not identity. Add to the existing `tool` block two optional fields: `trace_id` and `span_id` (W3C Trace Context format). When a runtime emits OTel spans (Claude Code exports OTel metrics and logs, with tracing in beta), the provenance event can point into the trace and vice versa.
**Recommendation:** Two optional string fields inside `tool`. **Dissent:** Nobody may populate them for a year. **Test:** The fields validate when absent and when present with valid W3C Trace Context hex strings; the docs show one example event carrying them.

### A1.7 Reject OTel as the event transport or store [reject]
Emitting provenance events as OTel spans and letting a collector be the log is a tempting unification and it destroys the framework's core property: the event log must be complete and durable in-repo, and OTel backends are lossy by design (sampling, retention windows, attribute limits). PGF stays file-first; OTel gets a pointer (A1.6) and, later, an optional exporter (A5.4). **Test:** If a buyer's compliance regime ever accepts a Datadog retention window as a system of record, this rejection was too conservative; do not hold your breath.

### A1.8 Event taxonomy: single-writer assumption and mergeable event IDs [design-for]
**Files:** `provenance/event-taxonomy.md`
**Task:** `seq` is monotonic per artifact, which silently assumes a single writer. Two agents or a human plus CI appending concurrently will collide. v0.1 keeps the single-writer assumption but states it out loud in event-taxonomy.md, and requires `event_id` to be a ULID (time-ordered, collision-resistant) so a future multi-writer merge has a total order to fall back on without renumbering history.
**Recommendation:** Document the assumption, mandate ULID event IDs. **Dissent:** ULIDs add a dependency-shaped concept (implementable in 20 lines of stdlib, so no actual dependency). **Test:** Generate 10,000 event IDs in a tight loop across two processes; zero collisions, lexicographic order matches creation order within clock resolution.

### A1.9 Event types: closed set, open pattern [design-for]
**Files:** `schemas/v0/graph-event.schema.json`, `provenance/event-taxonomy.md`
**Task:** Validate `event_type` with a pattern (`^[a-z_]+\.[a-z_]+$`) plus a documented registry in event-taxonomy.md, rather than a hard enum in the schema. The materializer rejects unknown types (that is a CLI decision), but the schema does not, so Next-phase additions (`evaluation.recorded` for the eval lane, `risk.added` for the GovCon pack) extend the registry without a schema version bump.
**Recommendation:** Pattern in schema, enum in materializer. **Dissent:** Splitting validation across two layers is subtler than one enum. **Test:** Appending an event with a well-formed but unregistered type passes `pgf validate` and fails `pgf materialize` with an actionable error naming the registry doc.

### A1.10 PROV mapping: document, do not adopt [v0.1 change for the doc; reject for adoption]
**Files:** `provenance/graph-model.md`
**Task:** PGF's node and edge model is a near-neighbor of W3C PROV (stable since 2013): claim/source/evidence nodes are PROV Entities, review/approval events are Activities, actors are Agents, and `derived_from` is `prov:wasDerivedFrom` almost verbatim. Adopting PROV-O as the internal model is **[reject]**: the RDF/ontology machinery would sink the lean, file-first, JSON Schema core, and nobody in the ICP set consumes PROV-O natively. But silently reinventing the vocabulary invites the "why didn't you use PROV" review from exactly the standards-literate audiences PGF wants. Add a half-page mapping table to graph-model.md (PGF node/edge type to nearest PROV concept, and where PGF deliberately diverges: materiality, confidence bands, and release gating have no PROV equivalent because PROV records history, PGF also gates it). Name `pgf export --format prov-jsonld` as a Next exporter in ROADMAP.md (A5.4).
**Recommendation:** Mapping table now, exporter Next, adoption never. **Dissent:** The table is unpaid homework for an audience that may never show up. **Test:** A reviewer familiar with PROV can state PGF's three deliberate divergences after reading one page.

### A1.11 Conformance language in the model docs [design-for]
**Files:** `provenance/graph-model.md`, `provenance/release-state-machine.md`, `provenance/event-taxonomy.md`
**Task:** Write normative statements in the `provenance/` docs using RFC 2119 keywords (MUST, SHOULD, MAY) and phrase them implementation-neutrally ("a conforming materializer MUST produce byte-identical output for identical logs"), so that `provenance/` plus `schemas/` reads as a spec and `cli/` reads as its reference implementation. This is the cheapest possible version of the spec-plus-reference-implementation posture (see Part C) and costs only word choice.
**Recommendation:** RFC 2119 phrasing throughout `provenance/`. **Dissent:** Normative language on an unfrozen model can look pompous. **Test:** After Phase 1 freeze, extract every MUST into a checklist; each one maps to at least one test or acceptance criterion, or it gets demoted to SHOULD.

## Phase 2: thin CLI

### A2.1 Schema $id and offline resolution [v0.1 change]
**Files:** `schemas/v0/*.schema.json`, `cli/pgf/core/schemas.py`, `docs/schema-reference.md`, section 9.6 of the PRD
**Task:** Two corrections to section 9.6. First, `main` is a moving ref, not a pin; the PRD's stated rationale ("pin the branch rather than a moving ref") is internally wrong. Use the tagged-release form as the `$id` from the start (`https://raw.githubusercontent.com/DataStrategyLab/provenance-graph-framework/refs/tags/v0.1.0/schemas/v0/claim.schema.json`), updated by the release script at tag time; before the first tag, a `v0.0.0-dev` placeholder is fine because of the second correction. Second, and more important: `$id` is an identifier, not a fetch instruction. `pgf validate` MUST resolve all `$ref`s from a bundled local registry (all v0 schemas registered from disk into the jsonschema resolver) and MUST NOT make network calls; a remote-resolving validator both violates section 21's no-hidden-network-calls rule and breaks in the air-gapped environments GovCon buyers actually run.
**Copy-ready replacement for the section 9.6 $id convention paragraph:**

> Schema `$id` convention: `$id` is a stable identifier, not a fetch URL. IDs use the tagged-release raw-content form (`.../refs/tags/vX.Y.Z/schemas/v0/<name>.schema.json`) so an ID names an immutable document. The CLI never resolves `$ref` over the network: `pgf validate` registers all bundled schemas from disk and fails with exit code 3 if a reference cannot be resolved locally. Cross-schema `$ref`s use relative paths. If DSL later wants rename-proof IDs, GitHub Pages at `datastrategylab.github.io` is the upgrade, requiring only an `$id` rewrite at a major version.

**Recommendation:** Tag-form IDs plus mandatory local resolution. **Dissent:** Rewriting `$id` at each tag adds a release-script step. **Test:** New acceptance criterion: `pgf validate` and `pgf check` pass on the canonical example with networking disabled (run under `unshare -n` or equivalent in CI).

### A2.2 Release-package digests in the export path [v0.1 change]
**Files:** `cli/pgf/core/materializer.py`, `cli/pgf/commands/export.py`, `schemas/v0/release.schema.json`, `templates/release-package-index.md`
**Task:** When `pgf export` writes the release package, compute SHA-256 digests of every file in the package and record them (path, digest, byte length) in the `release.exported` event payload and in `state.json`, and render them in `provenance-index.md`. This does not make v0.1 tamper-evident and the docs must not claim it does; a digest list in an editable log is a convenience, not a control. What it buys: the v1.0 tamper-evidence step becomes "wrap the existing digest list in an in-toto Statement and sign the DSSE envelope," a format decision instead of a schema migration, and it reuses the stack (in-toto Statement, DSSE, Sigstore keyless signing, Rekor transparency log) that GitHub artifact attestations already run in every Actions environment and that GitHub has been moving toward default-on for public repos.
**Recommendation:** Digests in `release.exported` now; signing stays v1.0. **Dissent:** Unsigned digests may be misread as integrity protection despite the docs. **Test:** Acceptance criterion: modify one byte of `artifact.md` inside an exported package; `pgf check --package <dir>` (or the export re-verification path) reports the mismatch and names the file. And the security-model doc explicitly states the digest list is not tamper-evidence.

### A2.3 Reject partial tamper-evidence in v0.1 [reject]
Hash-chaining the JSONL now ("each event carries the previous event's hash, it's 15 lines of code") is the most tempting scope creep in the whole PRD and it should stay rejected. A hash chain without signing and without external anchoring stops exactly nobody (rewrite the file, recompute the chain) while inviting the docs, or a hopeful buyer, to describe the log as tamper-evident. Cooperative honesty with digests recorded (A2.2) is the honest v0.1 maximum. **Test:** If a design partner puts tamper-evidence in a written requirement with budget attached, build the full v1.0 stack (chain plus DSSE signing plus optional Rekor anchoring), not the chain alone.

### A2.4 Export format flag reserved [design-for]
**Files:** `cli/pgf/commands/export.py`, `ROADMAP.md`
**Task:** Give `pgf export` a `--format` flag with a single valid value, `release-package` (the default). Document in ROADMAP.md the planned Next values: `prov-jsonld` (A1.10), `otel` (span-per-event replay for trace tooling), `in-toto` (v1.0 attestation). The flag existing means adapters never need to touch the default command's contract.
**Recommendation:** Reserve the flag now. **Dissent:** A one-value flag is dead weight if Next never comes. **Test:** `pgf export --format prov-jsonld` today exits 3 with a message pointing at ROADMAP.md, not a stack trace.

## Phase 3: Claude Code enforcement

### A3.1 Claim-normalization skill: align with the extraction frontier [v0.1 change]
**Files:** `.claude/skills/claim-normalization/SKILL.md` plus an adjacent `references.md`, `provenance/materiality-policy.md`
**Task:** The PRD ships "a first-cut heuristic" for its highest-risk component. The 2024 to 2026 literature already tells you the heuristic's required properties; encode them as the skill's procedure rather than rediscovering them:

1. **Verifiability filter** (VeriScore, Song et al. 2024): extract only claims a third party could check against evidence; opinions, hedges, and recommendations become `recommendation`-type claims or open questions, not factual claim nodes.
2. **Decontextualization** (a failure FActScore's own successors document): every claim node's `text` must be self-contained; resolve pronouns and implicit subjects so the claim is checkable without the surrounding paragraph.
3. **Confidence-gated extraction** (Claimify, Metropolitansky and Larson 2025): when the sentence's meaning is ambiguous, do not guess a claim; emit an open question node instead. Claimify's coverage-and-decontextualization evaluation framing is also the right rubric for the fixture below.
4. **Materiality triage** (PGF's own contribution, absent from the literature because research optimizes recall): the skill assigns materiality per `materiality-policy.md` and only high or critical claims are mandatory graph citizens; low-materiality statements may be batched or skipped, which is the answer to "not 300 nodes nobody maintains."

Then make quality measurable: hand-build a reference claim register for one section of the canonical example (this is Phase 1 output anyway) and add a pytest that runs no model but checks the *committed* skill-produced register against the reference for coverage of high-materiality claims and for decontextualization (no bare pronouns as claim subjects). Model-in-the-loop evaluation stays Next; the fixture makes the current heuristic's quality a number instead of a vibe.
**Recommendation:** Encode the four properties as the skill procedure; ship the reference-register fixture. **Dissent:** Freezing a rubric against a fast-moving literature risks encoding 2025's answer. **Test:** On the canonical example, the skill-produced register covers 100% of the hand-built high-materiality claims and 0% of its claim texts contain an unresolved pronoun subject; record precision as a baseline number in the walkthrough even if no threshold gates CI.

### A3.2 Verifier: materiality-downgrade check [v0.1 change]
**Files:** `.claude/agents/verifier.md`, `instructions/review.materiality.md`
**Task:** The release gate keys off materiality ("every high or critical claim has supporting evidence"), which creates a soft bypass: an actor, honest or not, lowers a claim's materiality and the gate stops looking at it. Add verifier question 5: has any claim's materiality been lowered after it was added, and if so, is the downgrade justified against materiality-policy.md? The materialized state already contains the history to answer this (events are append-only), so also add a `pgf check` warning when a claim's materiality decreased across its event history and the final state lacks a recorded review touching that claim.
**Recommendation:** Verifier question now, CLI warning now, CLI hard-fail Next. **Dissent:** Legitimate downgrades are common early in drafting and a warning may become noise. **Test:** Fixture: a log where a contradicted claim is downgraded from high to low with no review event; `pgf check` emits the warning naming the claim.

### A3.3 Hooks: no changes to the four-hook design [confirmation, no tag]
The PreToolUse/PostToolUse split, exit-code-2 semantics, settings.json vs settings.local.json separation, and three-enforcement-point framing are correct as written and consistent with current hook behavior. One addition folded into A2.2: `block-release.py` should treat a digest-verification failure the same as a gate failure. No other change.

### A3.4 Skills location: stay in .claude/skills for v0.1 [reject]
Moving skills to the emerging cross-agent `.agents/skills/` convention (which Codex reads alongside `.codex/skills/`) is plausible and premature: the convention is young, Claude Code's support for it is not established, and the PRD's honest position ("do not claim skill portability the directory conventions do not deliver") is the right one. Add one ROADMAP.md line: revisit skills location when either Claude Code or the AGENTS.md/Agentic AI Foundation ecosystem documents a shared skills path. **Test:** The moment Claude Code documents reading a cross-agent skills directory, migrate in a patch release; until then, no.

### A3.5 AGENTS.md: replacement and added lines [v0.1 change, copy-ready]
**Files:** `AGENTS.md` (stays under 200 lines; net change is about +7 lines)

Add to **Non-negotiable principles**:

```markdown
- Materialization is deterministic replay of a recorded history. Claim extraction is not deterministic. Never describe PGF output as "reproducible" beyond replay; the graph records what was decided, not what a model would decide again.
- Actor IDs use typed prefixes (human:, agent:, service:). An agent acting for a person records on_behalf_of in actor_detail.
- PGF is work-product and process provenance. It is not a content-credentials or media-marking system (C2PA, EU AI Act Article 50 marking); do not describe it as one.
```

Replace the **Integrity scope** section's last sentence with:

```markdown
Tamper-evidence is a future option (v1.0: release-package digests wrapped in an in-toto Statement, signed as a DSSE envelope), not a v0.1 promise. v0.1 records SHA-256 digests of exported release-package files for convenience; recorded digests in an editable log are not an integrity control.
```

Add to **Build and test commands** (after the existing check line):

```markdown
Validation is offline: `pgf validate` and `pgf check` must pass with networking disabled.
```

**Recommendation:** These exact lines. **Dissent:** Every added AGENTS.md line spends the 200-line budget. **Test:** Line count stays under 200; the Phase 3 checkpoint's Claude Code session, asked "is PGF output reproducible?", answers with the replay distinction unprompted.

### A3.6 CLAUDE.md: one added line [v0.1 change, copy-ready]

```markdown
Never claim a release package is tamper-evident or that claim extraction is reproducible; see AGENTS.md integrity scope.
```

## Phase 4: canonical example

### A4.1 Example must exercise the new fields [v0.1 change]
**Files:** `examples/association-board-brief/*`
**Task:** The canonical example already requires one contradiction and one override. Add three more required exhibits so every schema addition above is exercised, not decorative: (1) at least one `agent_extracted` claim later edited by a human (`origin: hybrid`), narrated in the walkthrough; (2) one source with `retrieved_at` older than the artifact's freshness policy that gets refreshed during verification (showing the staleness gate working); (3) the exported package's digest list rendered in `provenance-index.md`.
**Recommendation:** All three. **Dissent:** Each exhibit lengthens the example a new user must absorb. **Test:** Golden fixtures cover all three; deleting any one breaks a named acceptance criterion.

### A4.2 Acceptance criteria additions (section 25) [v0.1 change, copy-ready]
Append to section 25.1:

```markdown
16. `pgf validate` and `pgf check` pass on the canonical example with networking disabled; a schema `$ref` that would require a network fetch is a test failure.
17. The exported release package records SHA-256 digests for every packaged file in the release.exported event and provenance-index.md; altering one byte of a packaged file causes the package verification path to fail and name the file.
18. Every claim node carries an `origin` value; the canonical example contains at least one `agent_extracted` claim subsequently edited by a human.
19. Every source node carries `retrieved_at`; a source staler than the artifact policy causes `pgf check` to fail and name the source.
20. The claim-normalization fixture passes: the committed claim register covers all high-materiality claims in the hand-built reference register, and no claim text has an unresolved pronoun as its subject.
21. Concatenating the nodes.json of two artifacts produces zero node-ID collisions.
```

## Phase 5: docs and developer experience

### A5.1 Regulatory corrections in the ICP and accessibility layer [v0.1 change]
**Files:** `instructions/review.accessibility-and-disclosure.md`, `docs/faq.md`, section 29 source notes, any ICP context doc
**Task:** Encode nothing; document accurately. Corrections and confirmations as of July 6, 2026, all of which belong in the documentation layer (instruction files and docs), never in schemas:

| Anchor | Current state | PGF stance |
|---|---|---|
| EU AI Act high-risk (Annex III) | Deferred by the Digital Omnibus political agreement (May 7, 2026; Parliament June 16, Council June 29; Official Journal publication expected July 2026) from Aug 2, 2026 to **Dec 2, 2027**; Annex I embedded systems to Aug 2, 2028 | Document. Note the deferral binds only on OJ publication. |
| EU AI Act Article 50 transparency | **Unchanged: applies Aug 2, 2026.** Art 50(2) marking for legacy systems slips to Dec 2, 2026. AI literacy (Art 4) already applies | Document; relevant to the C2PA distinction (A0.1), not to PGF's core |
| Section 508 | Baseline still WCAG 2.0 AA (2017 refresh); no 2026 changes planned | Document; the PRD's 2.0-baseline vs 2.2-recommendation mapping stands |
| ADA Title II web rule | DOJ interim final rule effective **April 20, 2026** extended compliance: entities ≥50k population Apr 24, 2026 → **Apr 26, 2027**; smaller entities → **Apr 26, 2028**; standard remains WCAG 2.1 AA | Correct any April 2026 reference; the accessibility instruction should map 508 (2.0 AA) / Title II (2.1 AA) / recommendation (2.2 AA) as three rows |
| Colorado AI Act | **Repealed and replaced** (SB 26-189, signed May 14, 2026) before ever taking effect; replacement ADMT disclosure law effective Jan 1, 2027; the NIST-RMF safe harbor did not survive | Document; a cautionary note that state AI law is volatile and PGF instruction files date-stamp their regulatory references |
| Texas TRAIGA, California AB 2013, Illinois HB 3773 | In force since Jan 1, 2026 | Document only |
| California AI Transparency Act (SB 942 / AB 853) | Operative **Aug 2, 2026**; platform provenance-detection duties from 2027 | Document; feeds A0.1's naming distinction |
| Federal preemption | EO 14365 (Dec 11, 2025) and a March 2026 framework push preemption; **not settled law**; litigation ongoing | Document with the uncertainty stated |
| OMB M-25-21 / M-25-22 | In force; procurement memo applies to solicitations issued on or after Sept 30, 2025; high-impact AI minimum practices include pre-deployment testing, impact assessment, ongoing monitoring; agency AI strategies and compliance plans published through late 2025 | Document; the release packet maps naturally onto vendor-side evidence for these practices (see A5.2) |
| CMMC | Phase 1 live since Nov 10, 2025 (self-assessments, DFARS 252.204-7021/7025); **Phase 2 Nov 10, 2026** requires C3PAO Level 2 certification for most CUI contracts, with flow-down to subs | Document in the GovCon Next pack; also directly relevant to DSL's own subcontractor posture |
| ABA Formal Opinion 512 | Stands as the national baseline; 25+ state bars have issued guidance; **California COPRAC approved proposed amendments to six ethics rules (March 13, 2026)** that would carry disciplinary force, explicitly covering agentic AI and requiring independent verification of AI output | Document; the strongest single legal-ICP tailwind (see B4) |

**Recommendation:** Ship the table (adapted) inside the docs, date-stamped, with a standing rule in the instruction-file template: every regulatory reference carries an as-of date. **Dissent:** Date-stamped compliance content creates maintenance debt in an OSS repo. **Test:** Grep the repo for "August 2026", "April 2026", and "Colorado AI Act"; every hit either carries the corrected fact or an as-of date.

### A5.2 docs/standards-alignment.md: the citation surface [v0.1 change]
**Files:** new `docs/standards-alignment.md` (add to section 8 tree)
**Task:** One document, four short crosswalks, each a table from a PGF artifact to an external framework's language. This is the artifact a NIST author, an agency reviewer, or a bar-association committee can cite, and it is what separates "framework someone built" from "reference point" (Part C):

1. **NIST AI RMF / AI 600-1:** the GenAI Profile's four primary considerations are Governance, Content Provenance, Pre-deployment Testing, and Incident Disclosure; map the release packet, review events, and approval record to the provenance and governance actions, and note the AI RMF 1.0 is currently under revision so the crosswalk pins AI 600-1 (July 2024) and will track the revision.
2. **OMB M-25-21 minimum risk practices:** map the release package contents to the documentation a vendor would hand an agency for a high-impact AI use case (testing evidence, human oversight record, change history).
3. **ABA Op. 512 and state analogs:** map Verifier questions and the approval record to the competence, verification, supervision, and communication duties.
4. **Accessibility:** the three-row 508 / Title II / recommendation mapping from A5.1.

**Recommendation:** Ship it in v0.1 (it is a docs task, not a build task). **Dissent:** Crosswalks age; each framework revision creates a stale row. **Test:** Every row cites a section or action ID in the external document, not a vibe; a reader can check each mapping in under a minute.

### A5.3 docs/faq.md required entries [v0.1 change]
Three answers, drafted from the AGENTS.md language: "Is this tamper-proof?" (no; cooperative honesty; v1.0 path named), "Is this reproducible?" (replay yes, regeneration no), "Is this C2PA / content credentials?" (no; A0.1 text).

### A5.4 ROADMAP.md Next additions [Next, copy-ready]
Append under Next:

```markdown
- Tamper-evidence (v1.0 candidate): hash-chained event log; release-package attestation as an in-toto Statement (subject = the digest list already recorded by release.exported) in a DSSE envelope; Sigstore keyless signing and optional Rekor anchoring where a buyer requires an external log. No bespoke signature formats.
- Exporters behind `pgf export --format`: prov-jsonld (W3C PROV interchange), otel (event-to-span replay using GenAI semantic conventions once they stabilize; Development status as of mid-2026), in-toto (the attestation above).
- Eval lane (unchanged from v0.3): Promptfoo + Inspect; the eval lane consumes claim `origin` and the extraction-quality fixture as its ground truth; add `evaluation.recorded` to the event-type registry when built.
- Cross-artifact edges: promote the pgf check warning on external endpoints to a supported `derived_from` between artifacts.
- Skills location: revisit `.claude/skills/` vs the emerging cross-agent `.agents/skills/` convention when Claude Code documents shared-skills support.
- GOVERNANCE.md and a conformance test suite (spec-level MUST checklist runnable against any implementation) as v1.0 credibility items.
- GovCon pack: CMMC Phase 2 (C3PAO Level 2, from Nov 10, 2026) and CUI-handling documentation patterns; NIST SP 800-171 mapping.
- Standards participation calendar: NIST CAISI AI Agent Standards Initiative (agent interoperability profile expected Q4 2026), AI RMF revision comment windows, OTel GenAI SIG tracking.
```

### A5.5 Threat model additions (section 22.2) [v0.1 change, copy-ready]
Append two entries:

```markdown
Provenance theater (a graph of low-quality machine-extracted claim nodes that creates false assurance while documenting nothing decision-relevant): control: the claim-normalization skill's verifiability, decontextualization, and materiality rules; the extraction-quality fixture; claim `origin` visible to every reviewer; human review of high-materiality claims.
Reproducibility overclaim (deterministic materialization misdescribed as deterministic provenance, hiding the non-determinism of extraction): control: the AGENTS.md replay-vs-regeneration rule, claim `origin` and `extraction` metadata, and the FAQ answer; docs review at Phase 5 checks for the word "reproducible" used without the replay qualifier.
Materiality-downgrade bypass (the release gate keys on materiality, so lowering a claim's materiality removes it from scrutiny): control: verifier question 5, the pgf check downgrade warning, and append-only history making every downgrade visible.
```

## Phase 6: OSS launch candidate

### A6.1 Launch post angle [Next, one-line guidance]
The blog post should lead with the honesty stance (cooperative honesty, replay vs regeneration, automated-accessibility-only) because in July 2026 the credibility gap in this category is overclaim, not underclaim: 500+ documented court-filing hallucination incidents, a state bar moving verification duties into disciplinary rules, and agencies required to evidence high-impact AI practices. PGF's differentiator is that it refuses to promise what it cannot prove. No PRD change; a note for the Phase 6 outline.

---

# Part B. Blindspot and forward-fit analysis (justification)

The plan above is the deliverable; this section is why. Organized by the territories in the review brief, plus additions. Each item names the failure if ignored and carries its disposition (matching the Part A item where one exists).

## B1. Provenance and attestation standards adjacency

**W3C PROV / PROV-O.** PGF is quietly reinventing about 60% of the PROV vocabulary (Entity/Activity/Agent; wasDerivedFrom, wasAttributedTo, wasGeneratedBy) with different names. Failure if ignored: the first standards-literate reviewer, and NIST authors are standards-literate, asks why a "provenance" framework ignores the W3C provenance ontology, and the answer "we did not check" is disqualifying while the answer "here is the mapping and here is why we diverge" is a credibility asset. PROV has been stable since 2013, so this reconciliation is a one-time cost. Disposition: mapping table now [v0.1 change, A1.10]; PROV-JSONLD exporter [Next]; PROV-O adoption [reject].

**in-toto / DSSE / SLSA / Sigstore.** The software supply chain settled its envelope war: an in-toto Statement (subject digests plus a typed predicate) inside a DSSE envelope, signed via Sigstore keyless flows, logged to Rekor, is how SLSA provenance and GitHub artifact attestations ship, and GitHub has been tightening attestation defaults through 2025 and 2026. Failure if ignored: PGF v1.0 invents a bespoke signed-approval format, and every security reviewer asks why it is not an in-toto predicate; worse, PGF misses free infrastructure (the signing, logging, and verification tooling already exists in every GitHub Actions runner). The v0.1 move is not to sign anything but to record the subject (digests, A2.2) and to say the right words in the upgrade path (A5.4). Dispositions: digests [v0.1 change]; attestation [Next]; bespoke format [reject]; partial hash-chain now [reject, A2.3].

**C2PA / Content Credentials.** C2PA is at spec 2.3/2.4 with a live conformance program, a production trust list that replaced the interim list (frozen January 1, 2026), 6,000+ coalition members, and regulatory wind at its back (EU AI Act Article 50 from August 2, 2026; California's transparency laws). Failure if ignored: category confusion (buyers hear "provenance" and expect media manifests) and a missed lesson (C2PA's spec-plus-conformance-plus-trust-list structure is the maturity model PGF should imitate at v1.0, Part C). Signing PGF release packages with C2PA is [reject]: C2PA binds provenance to media assets and its trust model is built around claim generators in creative tooling; a markdown-and-JSON release package is the wrong asset class, and the story ("your PDF deliverable could carry Content Credentials") is a distant [Next] at best. Distinction paragraph: [v0.1 change, A0.1].

**W3C Verifiable Credentials / DIDs.** VC 2.0 exists as a W3C standard (not re-verified this pass; see Part D), but the agent-identity literature in 2026 itself documents DID trust-bootstrapping circularity and infrastructure immaturity, and no PGF ICP asks for VC-format approvals. [reject, A1.2] for approver identity; the actor extension point [design-for, A1.1] keeps the door open.

## B2. Observability overlap

The direct answer to the brief's question: provenance events and OTel spans are not the same primitive. They share a shape (timestamped, attributed, structured) and should share correlation IDs, but they differ in every property that matters: completeness (spans are sampled; the event log must be total), retention (telemetry backends expire; the log is the record), semantics (spans describe operations; PGF events describe epistemic state changes: claim added, contradiction detected, approval recorded), and audience (SREs vs reviewers and approvers). The OTel GenAI semantic conventions are also still Development status at v1.41.x with a formal experimental opt-in mechanism, so binding PGF's schema to them now would chain a stable public contract to an unstable one. Failure if ignored in the other direction: with zero correlation, a buyer running Claude Code's OTel export cannot connect a trace showing what the agent did to the event log showing what it recorded, and PGF looks like it ignores the observability stack every platform team already runs. Dispositions: trace pointer fields [design-for, A1.6]; OTel exporter [Next]; OTel as store [reject, A1.7].

## B3. Agent interop and identity

AGENTS.md itself: now stewarded under the Linux Foundation's Agentic AI Foundation, read natively by roughly 30 tools, present in tens of thousands of repos. Claude Code, as of mid-2026, still does not read it natively (the open feature request is one of the most-watched on the tracker), so the PRD's CLAUDE.md-imports-AGENTS.md shim is verified correct and is also the officially recommended pattern. Failure if ignored: none today; the forward-fit item is that native Claude Code support may land during 2026, at which point the shim becomes redundant but harmless. One caution: some third-party writeups claim Claude Code falls back to AGENTS.md when CLAUDE.md is absent; this is contested across sources, so keep the explicit import and do not rely on fallback behavior. [confirmation; no change]

Actor identity: today the `actor` string is honest about the state of the world, because even A2A agent cards are self-declared with no attestation binding, and MCP's auth story (OAuth 2.1 with PKCE) authenticates connections, not provenance-grade actor identity. But the standardization tempo is high: four IETF drafts in early 2026, MCP-I donated to DIF in March 2026, an MCP/A2A joint specification effort expected in Q3 2026, and NIST's CAISI launched an AI Agent Standards Initiative in February 2026 with an agent interoperability profile expected in Q4 2026. What breaks if actors need to be verifiable and PGF's field is an unconstrained string: every historical log becomes unparseable into (who, what kind, for whom), and the fix is a breaking schema migration across all committed fixtures. The typed prefix plus `actor_detail` extension point [design-for, A1.1] converts that break into an additive change.

## B4. Regulatory and procurement timeline (verified state, July 6, 2026)

Full table and dispositions in A5.1; the analysis-level points:

- **The EU deferral is not relief for PGF's story; it is repositioning.** With Annex III high-risk obligations moved to December 2, 2027, the near-term EU pressure that actually lands in the next 12 months is Article 50 transparency (August 2, 2026) and Article 4 AI literacy (already live), both of which are about disclosure and organizational competence, exactly the layer PGF's release packet and documentation serve. Encode nothing; document the mapping.
- **US federal procurement is the strongest live tailwind.** M-25-21's minimum practices for high-impact AI (pre-deployment testing, impact assessment, monitoring, documentation) and M-25-22's contract-lifecycle requirements are in force on new solicitations, agencies published strategies and compliance plans through late 2025, and GAO's April 2026 audit found agencies struggling with performance monitoring and lessons-learned discipline. A vendor-side evidence packet is precisely what a cross-functional acquisition team can consume. Failure if ignored: PGF's GovCon story stays abstract while the concrete artifact (the crosswalk, A5.2) costs one docs day.
- **CMMC Phase 2 (November 10, 2026)** lands inside the forward-fit window and flows down to subcontractors. PGF must not imply CMMC relevance beyond documentation hygiene (CMMC is about securing CUI systems, not work-product provenance), but the GovCon Next pack should speak its language, and DSL itself, as a would-be sub, should track it independently of PGF.
- **State AI law is volatile enough to prove the encode-nothing rule.** Colorado's flagship comprehensive law was repealed and replaced before taking effect, with a federal court pausing enforcement weeks before the deadline and a federal preemption EO looming over the whole layer. Any schema field or gate keyed to a named state statute would already be wrong. The date-stamp rule (A5.1) is the durable answer.
- **The legal ICP tailwind strengthened materially.** Beyond ABA Op. 512 and 25+ state analogs, California's COPRAC approved proposed amendments (March 13, 2026) that would move AI verification and supervision duties into rules carrying disciplinary force and explicitly contemplate agentic AI, against a backdrop of 500+ documented hallucination incidents in court filings. When the legal pack ships (Next), "reviewer lineage and source-to-proposition traceability" is no longer a nice-to-have pitch; it is the evidentiary posture a supervising attorney needs under a disciplinary rule. No v0.1 build change; this raises the priority of the legal pack within Next.

## B5. Claim granularity (the named highest risk)

The frontier moved from FActScore's atomic-facts-for-biographies (2023) through SAFE (2024) to two results that matter directly: VeriScore (2024) showed that extracting *verifiable* claims, rather than all atomic facts, is the domain-general formulation (and documented FActScore's unresolved-pronoun failure), and Claimify (2025) showed that extraction should be confidence-gated (only extract when the interpretation is unambiguous) and evaluated on coverage and decontextualization, with FEVERFact (2025) providing a benchmark framing around atomicity, fluency, and faithfulness. 2026 work continues in domain-specific directions (financial, scientific-citation, adversarial-claim evaluation) but the core properties are stable. Failure if ignored: the skill's first-cut heuristic rediscovers the pronoun bug, over-extracts unverifiable statements, and the graph becomes exactly the decorative artifact the PRD fears, with no number telling you it happened. The materiality triage is PGF's genuine contribution: the literature optimizes recall because benchmarks reward it; a governance tool must optimize decision-relevance. Disposition: [v0.1 change, A3.1], with the evaluation-lane integration [Next].

## B6. Evaluation deferral

The deferral is still right, with one sharpening. LLM-as-judge reliability remains contested enough that a model-graded lane in v0.1 would put a non-deterministic dependency inside a framework whose brand is determinism-where-promised. What v0.1 must do so the lane snaps in later: (a) the extraction-quality fixture (A3.1) gives the eval lane its first ground truth; (b) claim `origin` (A1.4) gives it its stratification axis; (c) the open event-type registry (A1.9) reserves `evaluation.recorded`; (d) the OTel GenAI conventions are growing an evaluation-results strand, so the Next-phase lane should emit in that shape once stable. Dispositions: deferral [reject pulling evals into v0.1]; the four hooks above [design-for / v0.1 change as tagged].

## B7. Model-level non-determinism

Materialization determinism is necessary and the PRD's treatment (section 15.3) is strong. The gap is narrative: "deterministic" will be read by buyers as "reproducible," and claim extraction is not reproducible. The honest formulation, which should appear anywhere the docs say deterministic: PGF guarantees deterministic *replay* of a recorded history, not deterministic *regeneration* of the analysis. The graph should also record enough to make the non-determinism inspectable: which claims a model proposed (`origin`), with what method (`extraction`), and optionally under which model version (the `tool` block already permits this via additionalProperties; recommend `tool.model` and `tool.model_version` in the taxonomy doc). Failure if ignored: one procurement reviewer asks "if I rerun this, do I get the same claims?" and the answer discredits the word deterministic everywhere else in the docs. Dispositions: [v0.1 change, A1.4, A3.5, A5.3].

## B8. Architecture gaps

- **Cross-artifact provenance:** [design-for, A1.5]. Failure: the second customer engagement produces artifact B citing artifact A, and node-ID collisions force a migration across golden fixtures.
- **RAG/retrieval provenance:** [v0.1 change, A1.3]. Failure: the staleness gate in section 11 is unenforceable because no field records retrieval time, making one of the release gate's listed conditions dead code.
- **Export interop round-trip:** [design-for, A2.4; Next for the exporters]. The honest answer to "can a PGF event round-trip to OTel, PROV, or in-toto" is: to PROV, losslessly for the history subset (PROV cannot carry gates); to OTel, lossily by design (spans are not a system of record); to in-toto, the release event maps to a Statement subject naturally once digests exist. Say this in architecture.md rather than promising round-trips the semantics do not support.

## B9. Forward-fit: the next six months (Job 2), consolidated

Dated events between now and early 2027 that PGF's v0.1 shape should anticipate, all already reflected in Part A tasks:

| Window | Event | PGF shaping |
|---|---|---|
| July 2026 | Digital Omnibus publication in the EU Official Journal expected | A5.1 date-stamped docs |
| Aug 2, 2026 | EU AI Act Article 50 transparency applies; California AI Transparency Act operative | A0.1 distinction paragraph prevents category confusion at exactly the moment "provenance" peaks in the news |
| Q3 2026 | MCP/A2A joint specification effort expected | A1.1 actor extension point |
| Fall 2026 | Possible native AGENTS.md support in Claude Code; `.agents/skills` convention maturing | A3.4 roadmap trigger; shim already robust either way |
| Nov 10, 2026 | CMMC Phase 2: C3PAO Level 2 mandatory on applicable CUI contracts | GovCon Next pack language (A5.4) |
| Q4 2026 | NIST CAISI agent interoperability profile expected; AI RMF revision in progress | A5.2 crosswalk pins versions; standards calendar in ROADMAP (A5.4) |
| Dec 2, 2026 | EU Art 50(2) marking for legacy systems; new NCII/CSAM prohibition | Documentation only |
| Jan 1, 2027 | Colorado SB 26-189 ADMT law effective | A5.1 date-stamp rule |
| Through 2026 | OTel GenAI semconv moving toward stability; GitHub attestations tightening defaults | A1.6 trace pointer; A2.2 digests make the attestation on-ramp trivial |

The pattern across all nine rows: every predictable change is absorbed by an envelope field, an extension point, or a documentation rule. None requires building a feature early. That is the design-for-not-against posture the brief asked for.

# Part C. Category leadership (Job 3)

What separates a framework that a NIST profile, an agency, or a bar association cites from one that dies quiet, with binary recommendations.

**C1. Spec plus reference implementation plus conformance, or just a framework?**
**Recommendation:** Structure v0.1 as spec plus reference implementation *in posture* (RFC 2119 language in `provenance/`, A1.11; schemas as the public contract, already the PRD's stance) and commit to a conformance test suite as a v1.0 gate, not a v0.1 build. Winner: posture now, program later. The evidence is C2PA's arc: the thing that converted it from coalition to infrastructure was the conformance program and trust list separating verified implementations from marketing claims, and the thing that made AGENTS.md citable was neutral stewardship of a small spec, not any implementation. Nobody cites a CLI; they cite a spec with a way to test conformance. **Dissent:** Spec posture on an unfrozen v0 model risks looking pretentious; the mitigation is that the posture is word choice, not process. **Test:** By v1.0, a second implementation (even a toy TypeScript materializer written in a weekend) passes the conformance checklist; if writing that checklist proves impossible, the spec was never separable from the implementation and the claim should be dropped.

**C2. Standards participation: where to spend the only scarce resource (attention).**
**Recommendation:** NIST is the single primary venue; OTel GenAI SIG and the in-toto community are tracked, not worked. Winner: NIST. Rationale: the ICPs are public-sector-adjacent, the AI RMF is in open revision, CAISI's agent standards initiative has an active comment pipeline, and NIST profiles cite external frameworks that show up with crosswalks (A5.2 is the entry ticket). A two-person team that "participates" in four standards bodies participates in none. **Dissent:** OTel is where the developers are, and developer adoption is the OSS growth engine. **Test:** One substantive public comment filed against a NIST document (Cyber AI Profile finalization, AI RMF revision, or the agent profile) within two quarters of launch, citing PGF by name; if no comment window materializes, redirect the attention to OTel.

**C3. DSL's moat when the code is free.**
**Recommendation:** The moat is the vertical instruction packs plus delivery fluency, and the core graph model should be treated as deliberately commodity. Winner: packs and delivery. The core schema is 9 JSON files anyone can fork; what a law firm or association actually buys is the encoded judgment (what counts as authoritative for this artifact class, what escalates, what a defensible packet looks like for this audience) plus a firm that has run the process. This is also why Apache-2.0 is correct rather than merely acceptable: a protective license would defend the commodity and starve the moat. **Dissent:** If a funded competitor ships better vertical packs on top of PGF's own spec, DSL stewards a standard it does not monetize. **Test:** Within two quarters of launch, at least one inbound engagement conversation cites the repo or a pack by name; if inbound cites only the blog post and never the artifacts, the moat thesis is wrong and DSL is doing content marketing with extra steps.

**C4. Governance signal without governance theater.**
**Recommendation:** DCO plus CONTRIBUTING plus the ADR breadcrumb now (A0.3); GOVERNANCE.md and any neutral-stewardship conversation only on demonstrated external contribution. Winner: earned governance. AGENTS.md is the cautionary positive example: it moved to foundation stewardship *after* adoption, not to cause it. **Dissent:** Agencies sometimes screen for governance maturity before adoption, creating a chicken-and-egg. **Test:** A0.3's test.

# Part D. What I could not verify

Claims in this review that rest on training knowledge or on the PRD's own assertions rather than a source checked in this pass, plus PRD items suspected stale but unconfirmed:

1. **Claude Code specifics the PRD marks as verified against July 2026 docs** (the skills/commands merge into one slash-command system, the `disable-model-invocation` bug and its issue number #26251, subagent permission-prompt behavior, SubagentStop conversion). These are consistent with my knowledge and with the ecosystem sources reviewed, but I did not re-verify them against Anthropic's current documentation in this pass. The issue numbers I did see in current sources for the AGENTS.md feature request (#6235 in one source, #34235 in another) do not overlap with #26251, so I can neither confirm nor deny that reference.
2. **Codex skills directories** (`.codex/skills`, `.agents/skills`) and the deprecation of Codex custom prompts in favor of skills: partially corroborated by secondary sources referencing a `.agents/skills` convention, not confirmed against OpenAI documentation.
3. **W3C Verifiable Credentials 2.0 Recommendation status**: from training knowledge (Recommendation, mid-2025); not re-verified. Does not affect any recommendation since VC adoption is [reject]ed regardless.
4. **SLSA current minor version**: sources reviewed describe the SLSA 1.0 build track and the in-toto/DSSE format in current use; whether 1.1/1.2 point releases changed anything material was not verified. The Part A recommendations depend only on the envelope format, which is stable.
5. **in-toto's CNCF status** (graduation): from training knowledge; not re-verified; immaterial to the recommendation.
6. **FAR/DFARS AI-specific clause status**: sources confirm M-25-21/M-25-22 in force and anticipated AI-related FAR activity, but I found no confirmation of a final AI-specific FAR rule; the review treats FAR AI rulemaking as pending, and the PRD should too.
7. **Digital Omnibus Official Journal publication**: final Parliament (June 16) and Council (June 29, 2026) approvals are confirmed; whether publication occurred in the days before July 6, 2026 is not; A5.1 words this as expected, which is safe either way.
8. **Whether Claude Code shipped native AGENTS.md support in the last weeks**: sources through late May/June 2026 say no; a very recent change would not have surfaced. The @import shim is correct in either world.
9. **The "500+ hallucinated court filings" figure**: reported by a January 2026 industry report as cited in a secondary legal-industry source; the order of magnitude is corroborated by the existence of a public tracking database, but the exact count was not independently verified. Used only as launch-post color (A6.1).

**PRD items checked and confirmed current (no change needed):** the AGENTS.md-canonical / CLAUDE.md-shim architecture; the PreToolUse secret-scan correction; the Codex correlated-review reframing (no source contradicts it and the reasoning is sound independent of sources); Section 508's WCAG 2.0 AA procurement baseline with 2.2 as recommendation; the cooperative-honesty scope as the right v0.1 integrity claim; Apache-2.0 licensing posture.

## Key sources (time-sensitive claims)

- EU Digital Omnibus: Council of the EU press release (May 7, 2026, updated May 18); Covington Inside Privacy (May 18, 2026); DLA Piper GENIE (July 2026, noting June 16 Parliament and June 29 Council approvals); Gibson Dunn client alert (May 27, 2026).
- ADA Title II extension: Federal Register, DOJ Interim Final Rule, FR Doc. 2026-07663 (effective April 20, 2026).
- Section 508 baseline: Section508.gov; multiple 2026 practitioner guides confirming no 2026 baseline change.
- Colorado SB 26-189: Morrison Foerster (May 15, 2026); Norton Rose Fulbright (May 22, 2026); Troutman (May 12, 2026); Baker McKenzie Employer Report on the April 27, 2026 enforcement pause.
- State laws in force / EO 14365: King & Spalding (Dec 2025); Cooley state-AI tracker (Apr 24, 2026); Vorp Labs US tracker (July 2026).
- OMB M-25-21 / M-25-22: Wiley, Covington, Hunton alerts (April 2025); Ogletree on agency strategies (Dec 2025); GAO-26-107859 (April 2026).
- CMMC phases: Federal Register 48 CFR rule (published Sept 10, 2025; effective Nov 10, 2025); Dorsey client alert (Nov 2025); multiple 2026 practitioner timelines confirming Phase 2 on Nov 10, 2026.
- ABA 512 and state bars: ABA Formal Opinion 512 (July 29, 2024); IXSOR comparative tracker (May 2026); Esquire Solutions on California COPRAC (April 2026).
- NIST: nist.gov AI RMF page (AI RMF 1.0 under revision; Critical Infrastructure profile concept note Apr 7, 2026); NIST IR 8596 preliminary draft (comments closed Jan 30, 2026); CSA Lab Space on CAISI's Feb 2026 agent standards initiative and Q4 2026 profile.
- AGENTS.md ecosystem: anthropics/claude-code issue #34235 (Mar 2026); multiple mid-2026 ecosystem comparisons on Linux Foundation stewardship and Claude Code's non-support plus the @import pattern.
- OTel GenAI: opentelemetry.io GenAI span conventions (Development status); Greptime deep-dive (May 2026, semconv v1.41.x); OTel blog (May 2026, noting Claude Code OTel export with tracing in beta).
- C2PA: spec.c2pa.org (v2.4); SoftwareSeni adoption analysis (Apr 2026, conformance program and trust-list transition); RightsDocket (Mar 2026).
- Agent identity: AIP paper, arXiv 2603.24775 (Mar 2026, surveying IETF drafts, MCP OAuth 2.1, A2A agent cards, DID limitations); arXiv 2604.23280 (MCP-I donation to DIF, Mar 2026); Zylos Research protocol-convergence analysis (Mar 2026).
- Claim extraction: Min et al., FActScore (EMNLP 2023); Song et al., VeriScore (2024); Metropolitansky and Larson, Claimify (2025); Ullrich et al., FEVERFact (2025); 2026 arXiv successors on importance-aware recall and domain-specific grounding.
- in-toto/DSSE/SLSA/Sigstore: in-toto/attestation spec (envelope layer, DSSE v1.0 recommended); docs.sigstore.dev bundle format; Tenki (Apr 2026) on GitHub attestation defaults.
