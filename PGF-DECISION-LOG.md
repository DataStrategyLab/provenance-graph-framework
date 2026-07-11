# PGF-DECISION-LOG.md
## Living decision log for PGF development

This is the one knowledge-base file you edit over time. When a design chat in either project settles something, append a dated entry here and re-upload to **both** the Claude project and the ChatGPT project (replace the old copy, do not add a second). That keeps both brains current with one action.

**Format for each entry:**
```
### [YYYY-MM-DD] Short title  |  disposition tag  |  status
Decision: one or two sentences, the winner.
Dissent: the strongest case against it, one line.
Test: the falsifiable check that would prove it right or wrong.
Supersedes: (if it changes a prior D# or log entry) name it.
```

Disposition tags: [v0.1 change] [Next] [design-for] [reject]. Status: proposed / accepted / built / revisited.

---

## Baseline: the locked decisions

The 20 locked decisions D1 to D20 live in PGF-PROJECT-CONTEXT.md section 4 and are treated as the accepted baseline as of 2026-07-06. Do not recopy them here. This log records only what changes or is newly decided **after** that baseline. If a chat revisits a D#, record the revisit here with a `Supersedes: D#` line so the two files stay reconcilable.

---

## Log entries

### [2026-07-06] Log initialized  |  n/a  |  accepted
Decision: This log starts empty above the baseline. All build decisions to date are captured as D1 to D20 in the context file and in the three planning documents in the knowledge base.
Dissent: A log that starts empty risks looking like nothing has been decided; it hasn't, the baseline holds it.
Test: If a chat proposes something already covered by D1 to D20, the project should cite the D# rather than treat it as open. If that fails, the context file needs to be more prominent in the KB.

### [2026-07-06] Claude Code surface: VS Code extension primary, CLI alongside  |  [v0.1 change]  |  built
Decision: Primary Claude Code surface is the VS Code extension (plan-mode markdown review and inline diffs fit PGF's mandatory-plan, reviewable-diff workflow); standalone CLI installed alongside for CLI-only paths (full slash-command set for skill-gate testing, worktrees, headless checks). Prereq add: VS Code 1.98.0+.
Dissent: The extension exposes only a subset of slash commands and cannot add MCP servers, so a terminal-only setup is simpler and loses little.
Test: In the extension a schema-change plan opens as an editable markdown plan and an edit renders as a rejectable side-by-side diff; release-critical skill slash-invocation is verified in the integrated terminal, not the extension menu. Verified: extension installed and authed, plan mode default confirmed, AGENTS.md shim resolved in a live session.
Supersedes: refines build plan 2.2 (adds the extension and VS Code 1.98.0+ prereq; targets docs/claude-code-setup.md).

### [2026-07-06] Contributor git identity: entity-correct and GitHub-linked  |  [design-for]  |  built
Decision: Commits to this repo use a GitHub-verified, entity-correct author identity (andrew@datastrategylab.com), set per-repo so a shared machine's other-entity (Rohic) work is not mis-stamped. The bootstrap commit's hostname-derived .local identity was reset before push. To document in docs/claude-code-setup.md (Phase 5): set repo-local user.name and a GitHub-linked user.email matching the owning entity before the first commit.
Dissent: Commit authorship is not part of PGF's cooperative-honesty provenance model, so enforcing it risks looking like git-hygiene scope creep.
Test: git log -1 in this repo shows andrew@datastrategylab.com; the same command in a Rohic repo does not; the pushed commit attributes to tsintsiruk on github.com with no .local address.
Supersedes: n/a (new).

### [2026-07-06] Branch-protection posture: classic rule, admin bypass staged  |  [design-for]  |  built
Decision: main has a classic branch protection rule (require PR, 1 approval, ci status check required from Phase 2, force-push and deletion blocked, signed commits off). Admin bypass on through Phase 2, off from Phase 3. Set via gh api --input - (JSON body; -f/-F mistype the nested integer).
Dissent: Rulesets are GitHub's forward path (org-wide reuse, JSON export, rule aggregation); classic means a later migration if DSL adds repos.
Test: readout shows 1/false/false; from Phase 3 (enforce_admins=true) a direct push to main is rejected with GH006; a PR with green ci and one approval merges.
Supersedes: refines build plan 2.4 step 4 with concrete toggles and admin-bypass staging.

### [2026-07-06] Hook stubs created at bootstrap  |  [v0.1 change]  |  built
Decision: The four .claude/hooks/*.py files ship as exit-0 stubs from the bootstrap commit so settings.json hook references resolve on the first governed session.
Dissent: Duplicates a sliver of the Phase 0 kickoff, so hook files are touched twice.
Test: a 31-check bootstrap gate passed; a live session created a file with no hook-execution error.
Supersedes: refines build plan 2.4 / Phase 0 pre-work sequencing.

### [2026-07-06] Ignore plan-mode scratch files  |  [design-for]  |  built
Decision: .gitignore excludes .claude/plans/ so plan-mode files are never swept in by `git add .claude`. Plan mode stays mandatory; only its scratch output is kept out of git. Verified: plans write to ~/.claude/plans/ on this machine, outside the repo.
Dissent: An open Claude Code feature request argues plans belong at the repo root for discoverability.
Test: trigger plan mode, approve a trivial plan, run git status --porcelain; no plan .md appears untracked.
Supersedes: refines .gitignore from build plan 2.4 step 5.

### [2026-07-06] Repo stays public during build  |  [design-for]  |  accepted
Decision: The repo stays public throughout the build rather than going private until Phase 6. Matches the context-file "published to GitHub first" posture; license stays Apache-2.0 (D20); only timing was ever in question and nothing changes.
Dissent: A half-built public repo exposes bootstrap history and any force-pushed fixups to anonymous viewers before launch.
Test: no visibility toggle needed at any phase; if pre-launch exposure causes a concrete problem (an incomplete claim scraped and cited as shipped), revisit for the next repo.
Supersedes: resolves the private-vs-public question against public.

### [2026-07-06] README positioning paragraph: full A0.1 text, not the AGENTS.md bullet  |  [v0.1 change]  |  built
Decision: The README's process-provenance-vs-content-credentials paragraph uses the full A0.1 text (pasted into the Phase 0 kickoff), not the terse AGENTS.md guardrail bullet, because the README needs the reader-facing "what PGF does vs is not" framing.
Dissent: The AGENTS.md bullet is the only text literally committed, so quoting it is the most verbatim-faithful answer.
Test: a first-time README reader can state both what PGF does (claim-to-evidence-to-approval traceability) and what it is not (media/content-credentials). Verified: README line 9 carries the A0.1 paragraph verbatim.
Supersedes: corrects the Phase 0 kickoff, which cited build-plan A0.1 though A0.1 lives in the uncommitted review doc; flags committing docs/review-and-execution-plan.md as a follow-up.

### [2026-07-06] Phase 0 package markers: PRD-literal, no extra __init__.py  |  [design-for]  |  built
Decision: The Phase 0 skeleton adds __init__.py only where PRD section 8 lists it (cli/pgf/ and cli/pgf/tests/), not in commands/ or core/. pyproject uses package-dir cli/ (package-dir = {"" = "cli"} plus packages.find where=["cli"]) so `import pgf` and `python -m pgf` resolve; full packaging is Phase 2.
Dissent: Without markers in commands/ and core/, those are not importable packages until Phase 2, and some tooling prefers explicit markers now.
Test: Phase 2 adds markers during packaging; no Phase 0 placeholder needs a cross-package import. If one does, the skeleton was over-built.
Supersedes: clarifies PRD section 8 for the two judgment calls Claude Code surfaced in the Phase 0 plan.

### [2026-07-06] Codex review via hosted GitHub flow, advisory only  |  [design-for]  |  built
Decision: Codex reviews PRs through Codex Cloud's built-in GitHub code review (@codex review), not a custom openai/codex-action workflow, so no OPENAI_API_KEY sits in the public repo and Codex follows the repo's AGENTS.md ## Review guidelines. Codex stays advisory under D18: not a required branch-protection check, and it does not push fixes directly in v0.1; accepted findings are implemented by Claude Code and approved by a human. Automatic reviews off for now; manual @codex review at phase gates.
Dissent: The GitHub Action route gives full control over model, prompt, and CI gating, but it adds a repo secret and treats correlated-model review like a control.
Test: @codex review on an open PR gets a reaction and posted review; repo secrets contain no OPENAI_API_KEY; branch protection lists no Codex-required check. Verified on the Phase 0 PR: Codex posted P1/P2 findings scoped to AGENTS.md guidelines.
Supersedes: implements build plan 2.3 and 4.5; consistent with D18.

### [2026-07-06] pgf entrypoint fails closed until Phase 2  |  [v0.1 change]  |  built
Decision: cli/pgf/__main__.py writes a "CLI not implemented (Phase 2)" message to stderr and exits 2 for any invocation, instead of a comment-only module that exits 0. An exit-0 placeholder makes pgf check / pgf materialize (the Makefile and PR-template gates) falsely report success after an editable install, the provenance-theater failure the threat model names. Only entrypoint exit behavior changed; command dispatch stays Phase 2 per PRD section 20. First accepted Codex finding, implemented by Claude Code under D18.
Dissent: The PR/AGENTS.md already mark the CLI as a Phase 2 placeholder and nobody installs the package in Phase 0, so the fail-open stub cannot mislead a gate yet; the fix could wait for Phase 2.
Test: PYTHONPATH=cli python -m pgf check foo; echo $? prints exit 2 (not 0), with the not-implemented message on stderr; no command logic implemented. Verified in commit a2e599d.
Supersedes: refines the Phase 0 skeleton; first Codex-to-Claude-Code fix loop under D18.

### [2026-07-06] Drop the no-op CI workflow; no ci check until Phase 2  |  [v0.1 change]  |  built
Decision: .github/workflows/ci.yml is deleted in Phase 0 rather than shipping a green no-op. A passing check that runs only an echo can be mistaken for a gate while ruff/pytest/pgf check/determinism are unimplemented. Phase 2 creates the real ci.yml (full lane) and adds the branch-protection required-check requirement in the same PR. Surfaced by Codex re-review (P2), taking its "leave CI absent" option. Deleted in commit 26093d3; main ships with no CI workflow.
Dissent: Keeping a green no-op preserves the filename slot and Actions wiring so Phase 2 is a content change, not a new-file change; and a green check reads as "nothing broken" to casual viewers.
Test: the merged main publishes no ci check (not green, not red); at Phase 2 the same PR adds the real lane and the required-check requirement. If a green check ever has to be explained as testing nothing, deleting was right.
Supersedes: reverses the two 2026-07-06 CI entries below ("CI placeholder is a valid no-op workflow" and "Placeholder CI stays green, fail-closed deferred"); both are withdrawn in favor of no CI file until Phase 2.

### [2026-07-06] CI placeholder is a valid no-op workflow, not a bare comment  |  [v0.1 change]  |  revisited
Decision: (WITHDRAWN) .github/workflows/ci.yml was briefly shipped as a valid no-op workflow (real on: triggers, one echo job) to replace a bare-comment placeholder that failed with "No event triggers defined in 'on'". This was reversed the same day: the no-op was deleted entirely because a green check that tests nothing can be mistaken for a gate.
Dissent: A no-op workflow is real content in a placeholders-only phase; the strictly minimal option is no ci.yml until Phase 2, which is where this landed.
Test: superseded; see the drop-the-no-op-CI entry above.
Supersedes: corrected the bare-comment ci.yml; itself superseded by "Drop the no-op CI workflow; no ci check until Phase 2".

### [2026-07-06] Placeholder CI stays green (no-op), fail-closed deferred to Phase 2  |  [design-for]  |  revisited
Decision: (WITHDRAWN) Briefly decided to keep the green no-op ci.yml and defer fail-closed to Phase 2, on the reasoning that branch protection required no status check yet. Reversed the same day in favor of deleting ci.yml outright, which removes the false-gate risk instead of managing it by sequencing.
Dissent: Fail-closed-everywhere is a cleaner invariant; deleting the file achieved that more simply than a documented green no-op.
Test: superseded; see the drop-the-no-op-CI entry above.
Supersedes: refined the CI-placeholder and branch-protection entries; itself superseded by "Drop the no-op CI workflow; no ci check until Phase 2".

### [2026-07-06] security-model.md: "traceability" not "reproducibility" for process  |  [v0.1 change]  |  built
Decision: docs/security-model.md's defensibility sentence uses "traceability of process," not "reproducibility of process." "Reproducible" is reserved for the determinism section where it carries the deterministic-replay qualifier (D11). Surfaced by a closing Codex re-review (P1) against the AGENTS.md replay-not-regeneration rule.
Dissent: Keeping "reproducibility (deterministic replay only)" inline would preserve the word; reserving it to one defining place is cleaner discipline.
Test: grep -ni "reproducib" docs/security-model.md returns only replay-qualified hits (line 52); the defensibility sentence no longer contains the word. Verified in commit 26093d3.
Supersedes: refines the Phase 0 skeleton docs; Codex finding under D18.

### [2026-07-06] README regulatory references carry an as-of date  |  [v0.1 change]  |  built
Decision: The README positioning paragraph's EU AI Act Article 50 and California AI Transparency Act references carry "(regulatory landscape as of July 2026)". Effective-date detail stays in Phase 5 date-stamped docs (D8); the README needs only the as-of anchor. Surfaced by Codex re-review (P2), enforcing the AGENTS.md as-of-date rule.
Dissent: Per-reference effective dates are more precise, but that is Phase 5 compliance-doc detail, not README positioning.
Test: the sentence naming Article 50 and the AI Transparency Act carries an as-of date; a reader can state what point in time the framing is scoped to. Verified in commit 26093d3.
Supersedes: refines the README A0.1 positioning entry; Codex finding under D18.

### [2026-07-06] First PR merged via admin bypass  |  [design-for]  |  built
Decision: The Phase 0 skeleton PR merged into locked main via admin bypass, since the 1-approval rule cannot be satisfied solo (GitHub blocks self-approval) and Adaora is not yet active. Recorded so the bypass is visible, not silent.
Dissent: Admin-merging one's own PR weakens the gate the same day it was set; dropping the requirement to 0 approvals until two people are active would be more honest about the actual control.
Test: git log --merges shows the skeleton merge; from Phase 3 (enforce_admins=true) admin bypass is off and no self-merge is possible. Merged as squash commit 992123c (PR #1).
Supersedes: refines the branch-protection posture entry with the first real merge under it.

### [2026-07-06] A1.8 event ordering: seq is the order key, ULID is identity  |  [design-for]  |  accepted
Decision: Correcting the A1.8 acceptance test. Event order under the single-writer assumption is given by seq (monotonic per artifact), not by ULID lexicographic order; ULID event_id (D13) guarantees distinct identity and rough time-sortability but does NOT preserve cross-process sub-millisecond creation order. Phase 1's provenance/event-taxonomy.md documents the single-writer assumption, uses seq as the order key, and its acceptance test drops the "lexicographic order matches creation order across concurrent generators" claim, keeping only: zero collisions, and seq-based total order under single-writer with seq-collision detectable as an integrity error. Surfaced by Codex (P2) reviewing the committed rationale doc.
Dissent: Keeping ULID as a secondary sort gives a deterministic fallback when seq collides; relying on seq alone means order holds only under the single-writer assumption.
Test: single writer, 10,000 events: seq dense and gap-free, sort-by-seq equals creation order; two writers: seq collision is flagged as an integrity error and ULIDs keep events distinct for diagnosis. No test claims cross-process sub-ms lexicographic ordering.
Supersedes: corrects the A1.8 test in docs/review-and-execution-plan.md (the rationale doc; per its header, this log governs on conflict); feeds Phase 1 provenance/event-taxonomy.md and is consistent with D13.

### [2026-07-06] Commit the review-and-execution-plan as a dated rationale record  |  [design-for]  |  built
Decision: pgf-v0_3-review-and-execution-plan.md is committed as docs/review-and-execution-plan.md so A-number rationale (A0.1, A1.x) resolves in-repo for Phase 1+ kickoffs. A prepended header marks it a dated rationale record: docs/build-plan.md and PGF-DECISION-LOG.md govern on conflict, and its regulatory claims are as-of July 6, 2026 and must be re-verified before reuse (D8, satisfied because the doc is date-stamped).
Dissent: It duplicates content now split across the build plan and decision log; a lean repo would paste only the needed A-number text per prompt.
Test: the Phase 1 kickoff cites "A1.1" and Claude Code resolves it from the committed file without asking for text; a reader treating a regulatory date here as currently true means the header failed. Verified: merged as PR #2 (main 7a0e385); header is line 1, grep "A1." returns 25 hits.
Supersedes: closes the follow-up flagged in the README-A0.1 log entry.


### [2026-07-06] Context file carries a phase-status marker  |  [design-for]  |  built
Decision: PGF-PROJECT-CONTEXT.md section 6 carries a "Current status" marker naming the phase in progress and what is on main, updated at each phase boundary, so a fresh chat orients without synthesizing the full decision log. It also corrects the CI implication: no ci.yml ships until Phase 2, created fresh alongside the required-check.
Dissent: The log already encodes state; a status line duplicates it and goes stale if not updated at each boundary.
Test: a new chat answers "what phase am I in and what's next" correctly from the context file alone; a stale marker (names a phase already merged) means the update step was skipped.
Supersedes: refines PGF-PROJECT-CONTEXT.md section 6.

---

## Phase 1 entries (2026-07-07): tolerant schemas, provenance model docs, one synthetic example

Phase 1 built nine tolerant v0 JSON schemas (`schemas/v0/`), six provenance model docs (`provenance/`), and one fully synthetic worked example (`examples/association-board-brief/`). The model is deliberately NOT frozen; enforcement (the `pgf` CLI, hooks, CI) is Phase 2+. These entries record what was settled during authoring and across multiple rounds of Codex advisory review on the Phase 1 PR (branch `phase1-schemas-example`).

**Repo-file reconciliation note:** the in-repo `PGF-DECISION-LOG.md` on the Phase 1 branch is a two-entry stub (schema-constraints + terminality), created in the Phase 1 PR to answer a Codex P0 (a public schema contract must not merge without an in-repo decision record). The full Phase 1 set below lands in the repo via the governance-hygiene PR, which expands the stub. This KB file is the authoritative living log; the repo file is a subset until the hygiene PR reconciles them.

**Phase 1 status:** MERGED to main at merge commit `b39d1d3` (PR #3, 2026-07-08), via admin bypass. The example is a 50-event append-only log (grew from 46 during Codex review); the offline harness passes all 50, seq dense 1..50, full node/edge coverage. Codex advisory review returned clean at commit `28aa553`. Next: the governance-hygiene PR expands the in-repo two-entry stub into the full log below and adds the remaining governance files.

### [2026-07-07] Event payload shape: records nest under payload.node / payload.edge  |  [design-for]  |  built
Decision: Record-bearing events carry the node record under `payload.node` or the edge record under `payload.edge`; event context (`reason`, `prior_status`, `superseded_id`, `detection_method`, `changed_fields`, `notes`, `scope`) stays as sibling fields under `payload`, never inside the record. Each v0.1 event carries at most one such record (single-record-per-event). Keeps Phase 1 tolerant while letting node/edge schemas freeze closed later without absorbing event metadata. Follows the common envelope-plus-data event pattern; no external spec is a dependency and no spec-status claim enters the docs.
Dissent: payload-as-record is simpler and matches the shallowest reading of the PRD graph-event sketch.
Test: an `override.accepted` carrying `payload.edge` plus sibling `superseded_id` and `reason` validates the edge record with no event-context fields inside the edge object, and survives a future `additionalProperties:false` edge schema.
Supersedes: refines the payload structure left open in PRD section 10.6.

### [2026-07-07] Schema constraints only where a decision locks them  |  [design-for]  |  built
Decision: In `schemas/v0`, a JSON Schema enum or pattern appears only where a locked decision (D-number, A-number) or a PRD 10.1/10.5 sketch requires it; every other field stays a tolerant string in v0.1, with `additionalProperties` permissive and no `additionalProperties:false` yet. Schema-enforced (grep-verifiable): source access enum (A1.3), actor and event_type patterns (A1.1/A1.9), trace_id/span_id hex patterns (A1.6), claim and artifact enums (PRD 10.5/10.1), and the tool.runtime enum in graph-event.schema.json (origin PRD 10.6, docs/prd-v0_3.md:397). PRD 10.6 (the graph-event node sketch) is a locking authority for schema constraints alongside 10.1/10.5. Documented-and-deferred, NOT schema-enforced: `event_id` is a ULID (D13, stated in event-taxonomy.md, checked by `ids.py` in Phase 2) and the node-ID-embeds-artifact-ID rule (checked by `ids.py`). Deliberately tolerant (no enum by design): `edge.type`, `review.decision`, `approval.decision`, the W3C all-zero trace/span rule.
Dissent: hard enums would surface vocabulary mismatches earlier.
Test: `grep -RE '"enum"|"pattern"' schemas/v0` shows every hit traceable to a citation above, INCLUDING graph-event.schema.json:74 tool.runtime tracing to PRD 10.6; `event_id` and node-ID rules are documented, not schema-enforced, so they correctly do not appear in that grep.
Migration: the v0 schemas are tolerant drafts, NOT a frozen contract; consumers should expect additive tightening at the phase-end freeze, not breaking changes within v0.1. [Preserved verbatim 2026-07-10 from the Phase 1 in-repo stub during the governance-hygiene log expansion.]
Supersedes: unifies the field-by-field tolerance calls; consistent with D1 and D14/A1.9. This is one of the two entries in the in-repo Phase 1 stub.

### [2026-07-07] review.decision and approval.decision stay tolerant strings in v0.1  |  [v0.1 change]  |  built
Decision: `review.decision` and `approval.decision` are tolerant strings, not hard enums; candidate values (review: pass/warn/fail/escalate; approval: approved/rejected/changes_requested) documented in prose, enum freeze deferred to the phase-end freeze. Neither traces to a D/A-number or PRD 10.1/10.5 node sketch (PRD 13.2 is a role description), so under the governing schema rule they are discovery vocabularies, consistent with `edge.type`.
Dissent: a hard enum catches malformed decision values at author time; the proposed sets are reasonable.
Test: `grep -RE '"enum"' schemas/v0` shows no enum for `review.decision` or `approval.decision`; every remaining enum traces to a citation.
Supersedes: corrects the older Phase 1 plan text that hard-enum'd both decision fields.

### [2026-07-07] No framework or spec status in durable docs  |  [v0.1 change]  |  built
Decision: Provenance docs reference the envelope-plus-data pattern as a bare analogy ("event formats such as CloudEvents") with no version, CNCF, graduation, or spec-status claim. Framework/spec status is a dated maintenance fact and belongs only in a dated references note or ROADMAP item. The PROV mapping (stable 2013 model) stays.
Dissent: naming CloudEvents' maturity lends credibility to standards-literate reviewers.
Test: `grep -RiE "CNCF|spec v1|graduated|v1\.0" provenance/` returns nothing.
Supersedes: reverses the earlier suggestion to cite CloudEvents' CNCF/graduation status in graph-model.md.

### [2026-07-07] Source text is untrusted input (model-layer doctrine)  |  [v0.1 change]  |  built
Decision: `provenance/source-hierarchy.md` section 4 states that text in a `source` node is untrusted external input, data not instructions, and MUST NOT be treated by an agent as commands even if it claims authority or mimics a system message. Doctrine is stated at the model layer; enforcing controls live in Phase 3 hooks and `docs/security-model.md`. The one-line echo in `graph-model.md` is PENDING (added in the governance-hygiene PR); until then this entry's two-file test is half-satisfied.
Dissent: prompt-injection defense is tool-level enforcement, so the statement could live only in security-model.md.
Test: `grep -RiE "untrusted|must not be treated as instructions" provenance/source-hierarchy.md` returns a hit now; the same grep over `graph-model.md` returns a hit after the hygiene PR.
Supersedes: n/a; aligns the model docs with D5 and the 2026 agent-workflow threat model.

### [2026-07-07] Release state machine uses the locked artifact status enum; archived is sole terminal  |  [v0.1 change]  |  built
Decision: The normative state machine in `release-state-machine.md` section 1 uses only the seven locked `artifact.schema.json` status values (intake, drafting, verification, review, approved, released, archived; PRD 10.1). Finer stages (evidence_planning, claim_graph, contradiction_resolution, packaged) are non-normative workflow narrative; "human_review" is not a state (the enum value is "review"). `archived` is the SOLE terminal state; `released` permits exactly one post-release transition (released -> archived); `archived` has no outgoing transition. Whether to expand to the fuller PRD 11 lifecycle is deferred to the phase-end freeze.
Dissent: the finer pipeline is more descriptive; flattening loses workflow fidelity in the normative diagram.
Test: every state in the normative diagram is a value in the artifact status enum; `archived` has no outgoing transition; `released` has exactly one (to archived); `human_review` does not appear as a status.
Supersedes: keeps the PRD 10.1-vs-11 fight-list item open; incorporates the terminality fix from Codex P2. This is the second of the two entries in the in-repo Phase 1 stub.

### [2026-07-07] Canonical example release must pass the gate honestly  |  [v0.1 change]  |  built
Decision: The association-board-brief example satisfies `release-state-machine.md` section 2 before `release.check_passed`. High/critical claims receive supporting evidence and a passing review before approval; the example never shows a critical claim releasing unsupported. Type coverage preserved.
Dissent: the example's job is type coverage, not modeling a fully gate-passing artifact; gate honesty is Phase 2's concern.
Test: replaying the example, every active high/critical claim has a supports edge or recorded disposition at the seq of `release.check_passed`; a checker evaluating section 2 against the log returns pass truthfully, not by assertion.
Supersedes: corrects the first-authored example where `release.check_passed` was true by assertion.

### [2026-07-07] Recommendation claims require a graph-traceable support path, present before the gate  |  [v0.1 change]  |  built
Decision: High/critical recommendation claims are releasable only when supported by a direct evidence `supports` edge, or a passing `review.recorded` (via `reviewed_by`) PLUS a graph-traceable `derived_from`/`overrides` path to an evidence-supported high/critical claim. Reviewer notes do not satisfy the gate. In the event-sourced log the support edge MUST exist at a lower seq than any event asserting the claim is supported or that the release check passed; materialization is deterministic replay in seq order, so an event's assertion must be true at its own seq. The canonical example gains a c005->c004 `derived_from` edge (seq 37) before c005's supported status change (seq 38) and before the first `release.check_passed` (seq 43). Event order is by seq only; ULID is identity/rough-sortability, never the order key (A1.8/D13).
Dissent: adds graph-path gate logic and a temporal ordering rule before the reference CLI exists.
Test: replaying by seq, at the first `release.check_passed` every active high/critical claim already has its required support; c005's `derived_from` edge has a lower seq than both its supported status change (38) and the check (43); event_ids are unique and ULID-shaped; sorting the log by event_id lexical order and materializing by seq yields the identical graph.
Supersedes: replaces the earlier c005 wording that allowed a prose note to satisfy the gate and required no temporal ordering.

### [2026-07-07] Release support gate scoped to ACTIVE claims, evaluated as-of-seq  |  [v0.1 change]  |  built
Decision: `release-state-machine.md` section 2 condition 1 applies only to ACTIVE high/critical claims. A claim is ACTIVE for release-gate support if, at the release-check event's seq, its latest replayed status is not a disposed state; the disposed statuses in v0.1 are `contradicted` and `rejected` (per claim.schema.json). Disposed claims are retained for provenance and covered by condition 2 (contradiction disposition), not the support gate. `materiality-policy.md` carries the same ACTIVE/disposed carve-out and DEFERS to release-state-machine section 2 as the single authority rather than restating the rule.
Dissent: a support gate scoped by claim lifecycle is more complex than a blanket rule; a naive checker could mis-scope "active".
Test: c002 (contradicted, high-materiality, no supports edge) passes via its override disposition; a live high-materiality claim with no support path still fails; `grep` for an unqualified "every high/critical claim MUST be supported" across `provenance/` returns nothing (both docs scope to ACTIVE and one defers to the other).
Supersedes: refines the recommendation-support entry above (Codex P1); fixes a doc-contradiction where materiality-policy restated the rule unqualified and drifted from release-state-machine.

### [2026-07-07] Release node records only materialized fields; no claims about nonexistent packages  |  [v0.1 change]  |  built
Decision: The `release.exported` node records only fields true at Phase 1 (id, schema_version, artifact_id, released_at, channel, approval_ref). `package_ref` and `file_digests` are REMOVED from the canonical example because no release package or artifact file is materialized in Phase 1; a digest for a nonexistent file is integrity theater (release-state-machine section 3: a digest in an editable log proves nothing). The Phase 4 explanation lives in a `payload.notes` sibling. Release package files and digests are produced by `pgf export` in Phase 4.
Dissent: keeping an empty `file_digests` map exercises the optional schema field.
Test: `grep -Rn "package_ref|file_digests" examples/association-board-brief/events.jsonl` returns nothing until `pgf export` creates real files; the release node validates against release.schema.json with both fields absent (both optional).
Supersedes: corrects the first-authored release node (Codex P2); consistent with D2/D6 integrity scope.

### [2026-07-07] Release lifecycle events are human-authored checkpoints in Phase 1  |  [v0.1 change]  |  built
Decision: The release-lifecycle events (release.check_requested, release.check_passed, release.exported, the released_as edge, and the artifact.updated -> released transition; seq 42-46) are actored by a human (`human:board-liaison-01`), not `service:pgf-ci`, because no pgf check / pgf export CI exists in Phase 1. They are hand-authored human checkpoints, not fabricated tool runs; `tool` is `{"runtime":"human"}` with no `tool_name`. Each carries a `payload.notes` sibling stating they are human-asserted because no CI exists yet, and that a real `service:pgf-ci` execution is added in Phase 2 through a separate fixture or newly appended checker-produced evidence, NOT by rewriting these merged Phase 1 events. Consequence: the Phase 1 example exercises human and agent actors only, no service actor. The A1.1 actor-prefix pattern still permits `service:` actors; the example simply does not exercise one until Phase 2.
Dissent: the target architecture runs release checks as a CI service, so a human-actored check models the wrong actor for the eventual system, and the example loses service-actor coverage.
Test: `grep -Rn "service:" examples/association-board-brief/events.jsonl` returns nothing; `pgf check`/`pgf export` appear only in `payload.notes` prose, never in a `tool_name`; the example still exercises >=3 distinct actor IDs (two human, one agent).
Supersedes: corrects the first-authored release events that asserted an executed `service:pgf-ci` run (Codex P1). Service-actor coverage returns in Phase 2 (freeze-list / Bin B item). [Relocated 2026-07-10: service-actor coverage is now an accepted Phase 2 implementation-coverage commitment, not a Bin B freeze item.]

### [2026-07-07] Materialized fixtures are de-committed, not hand-authored  |  [v0.1 change]  |  built
Decision: The `expected/` materialized outputs (nodes.json, edges.json, state.json) are DELETED from the repo, not committed as empty placeholders. An absent fixture cannot be falsely compared; an empty committed one can. They are the deterministic output of `pgf materialize` (Phase 2), and become Phase 2 golden fixtures only after replay behavior exists and is tested. They are never hand-authored: authoring graph output by hand would invent the tool's result and risk the real materializer later being "fixed" to match a guess. `expected/README.md` explains they are uncommitted and regenerated by `pgf materialize` in Phase 2. Phase 2's first materializer milestone regenerates them before any comparison test is wired.
Dissent: a committed (even empty) fixture preserves the directory shape and a populated golden fixture would be a stronger test.
Test: no committed `nodes.json`/`edges.json`/`state.json` exists under `expected/`; `expected/README.md` states they are Phase 2 `pgf materialize` output; no hand-authored graph output is committed.
Supersedes: replaces the Phase 0 skeleton's empty placeholder fixtures (Codex P1, two rounds).

### [2026-07-07] Source snapshots are committed and parser-visibly synthetic  |  [v0.1 change]  |  built
Decision: `snapshot_ref` values in the example resolve to committed files. Synthetic CSV snapshots are committed at the referenced paths (`sources/s002-member-survey-2026.csv`, `sources/s004-peer-dues-benchmark.csv`) so source evidence is recoverable as `source-hierarchy.md` intends. Each CSV is unmistakably synthetic in a way a parser sees (a `source_label` column set to `SYNTHETIC-EXAMPLE` on every row), not just via filename. Interview sources (s003) correctly use a `citation` and no `snapshot_ref`.
Dissent: committing synthetic CSVs adds scaffolding; omitting the refs is less to maintain.
Test: for every `snapshot_ref` in events.jsonl, the referenced file exists; every row of each snapshot CSV carries a parser-visible synthetic marker; no real organizations or people appear.
Supersedes: corrects dangling `snapshot_ref`s in the first-authored example (Codex P2).

### [2026-07-07] A1.8 is exercised by a Phase 2 pgf check test, not by deforming the example  |  [design-for]  |  accepted
Decision: The seq-over-ULID ordering guarantee (A1.8/D13) is verified by a dedicated `pgf check` test in Phase 2, not by inserting a deliberately out-of-lexical-order ULID into the canonical example. The example uses plain unique ULID-shaped event_ids; replay order is seq. Keeps the canonical example modeling the clean common case rather than an edge case a reader or tool could misread as a defect.
Dissent: the guarantee stays asserted-but-unexercised in-repo until the Phase 2 test lands; if Phase 2 slips, nothing demonstrates seq-over-ULID.
Test: no canonical example event is intentionally anomalous; a grep for an out-of-order-ULID note in `examples/` returns nothing; the Phase 2 `pgf check` suite materializes a log whose ULID order contradicts seq order and confirms replay follows seq.
Supersedes: reverses the in-session recommendation to exercise A1.8 by deforming the example.

### [2026-07-07] Git history is provenance: structured commit trailers, no squash, no manifest  |  [design-for]  |  accepted
Decision: Phase commits carry a structured trailer naming the corrections applied and pointing to decision-log entries; branch history is kept granular (not squashed) so the edit-by-edit governed authoring is preserved; no hand-authored file manifest is added, since git, the PR body, and this log already record file provenance and a fourth parallel record would drift.
Dissent: a squashed history and a manifest file are tidier and machine-readable.
Test: the Phase 1 merge history shows the corrections as distinct commits; no `phase-1-manifest.json` exists; each commit trailer names the settled decisions.
Supersedes: n/a; sets the commit-provenance convention for later phases.

### [2026-07-07] Phase 1 merged via admin bypass (solo-approver phase)  |  [design-for]  |  built
Decision: Phase 1 PR #3 merged to main at merge commit `b39d1d3` (2026-07-08) via admin bypass, because main requires one approval, GitHub blocks self-approval, and the second approver (Adaora) is not yet active. Merged as a merge commit (not squash) to preserve the granular Codex-fix history. This remains the staged posture through Phase 2; it transitions to normal approval when the second approver is active.
Dissent: merging without an independent approval weakens the gate even in the solo phase.
Test: PR #3 shows Codex advisory review clean at `28aa553` and an admin-bypass merge, not a self-approval; branch protection remains on; `git log --merges` on main includes `b39d1d3`.
Supersedes: instantiates the Phase 0 admin-bypass-through-Phase-2 decision (D-baseline) for the Phase 1 PR; consistent with the Phase 0 "first PR merged via admin bypass" entry.

### [2026-07-07] Decision log created in the Phase 1 PR (in-repo stub), not deferred wholesale  |  [v0.1 change]  |  built
Decision: An in-repo `PGF-DECISION-LOG.md` is initialized in the Phase 1 schema PR (a two-entry stub: schema-constraints + terminality) in response to a Codex P0, so the public Apache-2.0 schema contract does not merge with its decision record living only in a future PR. The full Phase 1 decision set (this KB file's Phase 1 entries) lands in the repo via the governance-hygiene PR, which expands the stub, so the log itself goes through review rather than being appended wholesale to the schema PR.
Dissent: the plan batched all governance into the hygiene PR; creating the stub here reverses that and splits governance work across two PRs.
Test: cloning the repo at the Phase 1 merge commit yields an in-repo decision record for the public schema contract; the hygiene PR expands the stub into the full log and adds only the remaining non-log governance items.
Supersedes: reverses the earlier plan decision to defer the entire in-repo decision log to the governance-hygiene PR.

### [2026-07-07] Normative rules have one authoritative home; other docs defer, not duplicate  |  [design-for]  |  accepted
Decision: When a normative rule is relevant to more than one doc, exactly one doc states it authoritatively and the others defer by reference rather than restating it. The release support rule lives in `release-state-machine.md` section 2; `materiality-policy.md` defers to it. Restating normative rules in two places caused the support-gate rule to drift twice (the original materiality-policy reconcile, then the ACTIVE-claim scoping), each time because only one copy was updated.
Dissent: a reader of one doc alone gets a reference instead of the full rule; some duplication aids local readability.
Test: grep for a rule's normative keywords across `provenance/` finds one authoritative statement; other mentions are references to it, not independent restatements.
Supersedes: n/a; standing maintenance rule for the doc set, prompted by two support-gate drifts Codex caught.

### [2026-07-07] Evidence excerpts must match committed source snapshots  |  [v0.1 change]  |  built
Decision: Evidence excerpts in the canonical example are limited to facts present in their cited committed snapshots, or receive a separate source/evidence path for the missing facts; a high/critical financial claim is never narrowed to dodge evidence work. e002 now matches the s004 peer benchmark snapshot (three peers, average 18%); e004 is narrowed to the s002 attrition fact only; a new projection source s005 and evidence e005 carry the $82k gap-closure arithmetic under an explicit FULL-LOSS scenario-comparison assumption (m002), counting full base dues lost to attrition in each scenario rather than the favorable marginal-churn framing. c004 is supported by both e004 (attrition) and e005 (gap-closure). The load-bearing modeling assumption is captured as an assumption node, record-linked from e005 via `assumption_ref`.
Dissent: adding a synthetic projection worksheet and a modeling assumption increases example complexity and creates another arithmetic surface to maintain.
Test: e002 states the peer count and statistic found in s004; e004's excerpt is limited to the attrition fact present in s002; e005 cites s005; the tiered_increase row shows $2,027,400 after attrition versus $1,940,000 no-change, net +$87,400, gap $82,000, surplus $5,400; c004 has a supports edge from e005 at a lower seq than the event marking c004 supported; grep for "within the revenue-gap closure threshold" returns no hits.
Supersedes: corrects e002's median/12-peer wording and e004's claim that s002 established revenue-gap closure; resolves the evidence-recoverability item formerly open on the freeze-list. Chose full-loss over marginal-churn because the marginal-churn model counted the increase on retained members without counting base dues lost to attrition.

### [2026-07-09] Phase 1 establishes the exercised model baseline; Phase 2 begins with an implementation freeze  |  [v0.1 change]  |  accepted
Decision: The merged Phase 1 schemas, provenance docs, and canonical example establish the exercised v0.1 model baseline. The eight remaining implementation-shaping questions (.updated representation; review-role/accessibility-preflight; as-of-seq evaluation; enum promotions; assumption-to-evidence linkage; dedicated schemas for question/assumption/constraint/draft_span; artifact.status enum expansion; additionalProperties:false closure) are resolved at a Phase 2 implementation-freeze checkpoint before dependent materializer or checker code is written. (The tool.runtime enum citation is a separate hygiene correction, not one of the eight.)
Dissent: Carrying model decisions into Phase 2 extends discovery beyond the planned Phase 1 boundary and risks implementation-driven contract changes.
Test: Before dependent implementation begins, every implementation-freeze item has a recorded decision and named fixture; after the first golden fixtures merge, no schema or gate semantic changes without a migration note.
Supersedes: none; refines the Phase 1 exit wording in docs/build-plan.md. Does NOT supersede D1 (D1 defines scope, not the freeze checkpoint).

### [2026-07-09] Preserve Phase 1 history when adding service-actor coverage  |  [v0.1 change]  |  accepted
Decision: Phase 2 does not rewrite the human-authored Phase 1 release-check events as service-authored history. Real `service:pgf-ci` coverage is added through a separate Phase 2 fixture, a new artifact run, or newly appended truthful execution evidence produced by the implemented checker. The exact fixture path is an implementation choice.
Dissent: A separate fixture makes the canonical example less compact and duplicates part of the release lifecycle.
Test: The merged 50-event Phase 1 log remains byte-identical; a Phase 2 fixture records a real checker execution by `service:pgf-ci` and passes replay and release-gate tests.
Supersedes: refines the Phase 1 service-actor coverage wording (the human-authored-release-checkpoints entry and the service-actor-returns freeze item). [2026-07-10: the service-actor item is no longer a freeze item; see Phase 2 implementation-coverage commitments.]

### [2026-07-09] Repo governance files become canonical after hygiene reconciliation  |  [design-for]  |  accepted
Decision: After the governance-hygiene PR merges, the repo copies of PGF-PROJECT-CONTEXT.md and PGF-DECISION-LOG.md are authoritative for accepted governance. The Claude Project and ChatGPT Project copies are synchronized caches replaced from a specific main commit. Proposed RFCs may remain outside the repo, but an accepted decision must be promoted promptly through a governance PR.
Dissent: Requiring a repo update for every accepted decision adds friction during fast product discovery.
Test: Every uploaded governance file can be matched to a main commit, and no project contains an accepted decision absent from the repo.
Supersedes: replaces the temporary KB-authoritative / repo-subset arrangement used before the hygiene PR.

### [2026-07-10] Governance-hygiene reconciliation: enum status, freeze posture, service-actor placement, checker invariants, and digest language  |  [v0.1 change]  |  accepted
Decision: Five hygiene reconciliations of already-accepted decisions, no D# changed and no new model decision. (a) tool.runtime is already a schema-enforced enum (graph-event.schema.json, PRD 10.6); it is not a freeze item. Removed from the Bin B enum-promotions bullet, which now covers only edge.type / review.decision / approval.decision. (b) PGF-PROJECT-CONTEXT.md section 6 is refreshed to state the Phase 2 implementation-freeze posture was accepted 2026-07-09 with the eight items still open; the stale "governance conflict to resolve" and undefined "Stage-2" wording are removed. (c) The Bin B service-actor bullet moves out of the open freeze list into a Phase 2 implementation-coverage-commitments section; its approach is already accepted (see the 2026-07-09 "Preserve Phase 1 history" entry). (d) The context section 6 line-98 phrase "the 21 Phase 2 pgf-check invariants" is corrected: the 21 are the consolidated acceptance criteria (build plan section 6 / review plan), a distinct artifact from the pgf check MUST-enforce invariants (four currently enumerated in this log). docs/phase-1-freeze.md enumerates the checker-invariant set derived at the Phase 2 boundary from this log, the provenance docs, the offline harness, and the build criteria; the count is the extraction result, not a hard-coded 21. Until that lands, this log's four are a highlighted subset of the checker-invariant set (not a subset of the 21 acceptance criteria). [Clause (d) superseded 2026-07-10 by the checker-invariant reconciliation entry below: the 21 pgf check invariants ARE real (offline-validation Part 2, imported by readiness bucket b); the claim here that the phrase meant the acceptance-criteria count was mistaken. Clauses (a), (b), (c), (e) stand.] (e) Every Phase 4 pgf export digest reference states the SHA-256 file_digests are convenience metadata only and never an integrity control in the editable v0.1 log.
Dissent: These reconcile accepted decisions rather than deciding anything new, so they could be corrected in place without a log entry.
Test: grep '"enum"' schemas/v0/graph-event.schema.json returns tool.runtime; the Bin B enum-promotions bullet names only the three tolerant fields and no longer lists tool.runtime; the open freeze list contains exactly eight design bullets; service-actor coverage sits under a coverage-commitments heading; context section 6 says the posture was accepted 2026-07-09 and no longer says "21 pgf-check invariants"; docs/phase-1-freeze.md names the checker invariants with a count traceable to its extraction, distinct from the 21 acceptance criteria; every export-digest description says convenience-only and denies integrity-control status.
Supersedes: corrects the Bin B enum-promotions and service-actor bullets, the context section 6 model-status paragraph and the line-98 invariant mislabel, and any unqualified export-digest description. Reinforces, does not supersede, the 2026-07-09 exercised-baseline entry. No D# touched.

### [2026-07-10] Reconciliation follow-ups: Bin B sequencing wording and stale service-actor pointers  |  [v0.1 change]  |  accepted
Decision: Three cleanup dispositions from the post-reconciliation verify. (1) Bin B's heading and intro are reworded to match the 2026-07-09 baseline entry: the eight items are settled at the Phase 2 opening implementation-freeze checkpoint, each decided against a targeted milestone, spike, or fixture that exercises the question (`.updated` is settled by Phase 2's FIRST materializer milestone), and dependent code built on a frozen decision does not precede that decision. This removes the ambiguity between "settled against running Phase 2 code" and "resolved before dependent materializer or checker code"; both hold once the settling milestone is distinguished from the dependent code built on it. (2) The two stale Supersedes-line pointers that call service-actor coverage a Bin B / freeze item (in the "Release lifecycle events" and "Preserve Phase 1 history" entries) receive non-destructive inline 2026-07-10 relocation markers rather than rewrites, preserving append-only history. (3) [reject] The retired invariant-count phrase (the one asserting a fixed count of 21 checker invariants) stays quoted inside the 2026-07-10 reconciliation entry as the correction target; it is not a live claim, and stripping it to satisfy a zero-match grep would reduce traceability. [Item (3) superseded 2026-07-10: the 21-invariant count is NOT retired; it is accurate (offline-validation Part 2). See the checker-invariant reconciliation entry below. Items (1) and (2) stand.]
Dissent: (1) and (2) are wording-only and could have been made silently; (3) leaves one literal grep hit for a retired phrase.
Test: the Bin B intro names the milestone/spike mechanism and no longer settles the eight items against unqualified "running Phase 2 code"; both service-actor pointer lines carry a 2026-07-10 relocation marker; the retired invariant-count phrase appears exactly once in the file, inside the 2026-07-10 reconciliation entry, as a quoted correction target.
Supersedes: refines the 2026-07-10 reconciliation entry's Bin B and service-actor wording; no decision changed, no D# touched.

### [2026-07-10] Checker-invariant reconciliation: the 21 pgf check invariants are real (ground-truth reports)  |  [v0.1 change]  |  accepted
Decision: Corrects clause (d) of the 2026-07-10 governance-hygiene reconciliation entry and item (3) of its follow-up. The phase-boundary reports establish that there ARE 21 Phase 2 pgf check invariants: the offline-validation report (Prompt 3) Part 2 enumerates 21 primary requirements across categories A-H (item B10 a minor sub-item), and the Phase 2 readiness report (Prompt 4) bucket (b) imports them verbatim from that source. The context file's original "the 21 Phase 2 pgf-check invariants" was therefore accurate. This is a distinct set from the 21 consolidated acceptance criteria (build plan section 6); the two collide on the count by coincidence, which is the footgun that produced the earlier mistaken "mislabel" claim. docs/phase-1-freeze.md enumerates the 21 checker invariants from offline-validation Part 2; the four in this log's MUST-enforce section are an early-highlighted subset of those 21, not the whole set and not the acceptance criteria.
Dissent: two sets of exactly 21 invites the same confusion again; some readers will still conflate them without the explicit note.
Test: offline-validation Part 2 lists 21 primary pgf check requirements; readiness bucket (b) says it imports 21 primary requirements directly from that report; docs/phase-1-freeze.md, once authored, contains those 21 individually named with rule IDs, distinct from build-plan section 6's 21 acceptance criteria; context section 6 references the 21 checker invariants, not the acceptance-criteria count.
Supersedes: corrects clause (d) of the 2026-07-10 governance-hygiene reconciliation entry and item (3) of its follow-up (both marked superseded in place). Root cause: the earlier reconciliation reasoned from the KB and build plan without the offline-validation and readiness reports in scope. No D# touched.

---

## Open freeze-list items (Bin B: eight items, settled at the Phase 2 opening implementation-freeze checkpoint, not by memo)

These surfaced during Phase 1 review and are deliberately NOT resolved in Phase 1. They are recorded here so they are not lost, and are settled at the Phase 2 opening implementation-freeze checkpoint (per the 2026-07-09 baseline entry): each is decided against a targeted materializer or checker milestone, spike, or fixture that exercises the question (for example, `.updated` representation is settled by Phase 2's FIRST materializer milestone), not by a design memo and not by one example. Dependent materializer or checker code built on a frozen decision does not precede that decision.

- **Review-role / accessibility-preflight satisfaction (condition 3).** Under strict graph-checkable reading the example does not satisfy condition 3: no `review.recorded` carries `role="accessibility"` (only prose in r002's notes), and no passing `role="verification"` review closes r001's `escalate` after the override arc. Three parts to settle: (1) does a combined-role review satisfy both roles, or is a distinct `role="accessibility"` event required; (2) does an `escalate` resolved by a later override satisfy the verification role, or is a re-run passing verification review required; (3) like condition 1, role satisfaction should be evaluated as of the release-check event's seq. Resolution: add graph-checkable review coverage before `release.check_passed`, or explicitly narrow the Phase 1 role-satisfaction rule. Deliberately not fixed in the example (authoring events now would hard-code one interpretation before the rule is defined).
- **As-of-seq evaluation for all release-gate conditions.** Condition 1 is now evaluated as of the release-check event's seq. Conditions 3 (and any others) should adopt the same as-of-seq framing so the whole gate is evaluated against replayed state at the check event, not the final graph. Phase 2 `pgf check` MUST evaluate release-gate conditions as of the check event's seq.
- **`.updated` snapshot-vs-delta.** The example leans on envelope-only `.updated` deltas (artifact.updated, claim.updated) for status transitions, including release-gating ones. Whether `.updated` is a full snapshot, RFC 6902 JSON Patch, RFC 7396 Merge Patch, or descriptive typed deltas is settled against the materializer's `.updated` replay, sequenced as Phase 2's FIRST materializer milestone. Current evidence favors deltas.
- **Enum promotions.** Whether `edge.type`, `review.decision`, and `approval.decision` promote from tolerant strings to locked enums, decided at the freeze against the vocabulary exercised in code, not by one example. (`tool.runtime` is already a schema-enforced enum under PRD 10.6 and is not part of this promotion question; see the schema-constraints entry and the 2026-07-10 reconciliation entry.)
- **Dedicated schemas for question / assumption / constraint / draft_span.** These node types validate envelope-only in v0.1 (no dedicated node schema). Freeze decision: keep envelope-only, or promote one or more to a dedicated schema. Affects per-record validation coverage in the Phase 2 checker.
- **artifact.status enum expansion.** Keep the locked seven-value status machine, or expand to the fuller PRD section 11 lifecycle. The Phase 2 checker's status-transition table depends on the frozen enum; sub-phase names (evidence_planning, packaged) must be rejected as status values under the seven-value set.
- **additionalProperties:false freeze on node/edge schemas.** Node/edge schemas are tolerant (additionalProperties permissive) in v0.1. Freeze decision: close them to additionalProperties:false once event-context siblings are confirmed to live under payload (not inside records). Premature closure breaks the tolerant-draft promise; late closure loosens integrity guarantees.
- **Evidence-to-assumption linkage (open).** Patch 7 uses `e005.assumption_ref` to record that projection evidence depends on assumption node m002. This validates under the tolerant Phase 1 evidence schema, but v0.1 has no explicit `assumes` edge type, and `derived_from` would encode false lineage. Freeze decision: keep `assumption_ref` as a documented evidence field, add an `assumes` edge type, or model assumptions only as prose context. Recorded so the record-linkage choice is revisited against Phase 2 code.

## Phase 2 implementation-coverage commitments (accepted, not open freeze items)

These are accepted decisions whose approach is settled; only the implementation detail remains. They are kept out of the Bin B open-freeze list so that list reads as the eight unresolved design decisions.

- **Service-actor coverage.** The Phase 1 example exercises human and agent actors only (no CI exists). When Phase 2 builds `pgf check` as a CI service, real `service:pgf-ci` coverage is added through a separate Phase 2 fixture, a new artifact run, or newly appended truthful checker-produced execution evidence. The merged 50-event Phase 1 log remains byte-identical. Exact fixture path is an implementation choice. (Accepted 2026-07-09; see "Preserve Phase 1 history when adding service-actor coverage".)

## Phase 2 pgf check MUST-enforce invariants (early-highlighted four; the full set is the 21 in docs/phase-1-freeze.md)

These four are invariants flagged early during Phase 1 review, recorded so they are not lost. They are an early-highlighted subset of the complete `pgf check` invariant set. The complete set is the 21 primary invariants enumerated in the offline-validation report Part 2 (categories A-H, item B10 a minor sub-item), imported verbatim by the Phase 2 readiness report bucket (b) and authored into docs/phase-1-freeze.md. That 21-item checker set is distinct from the 21 consolidated acceptance criteria in build-plan section 6, which coincidentally shares the count.

- single-record-per-event (at most one of payload.node / payload.edge)
- one-edge-one-event (no edge id introduced by more than one event)
- edge referential integrity (every from/to resolves to a node at a lower seq in the same artifact; cross-artifact endpoints warn, not fail)
- gate honesty as-of-seq (a `release.check_passed` must be true at the seq it was recorded, evaluated against replayed state at that seq)
