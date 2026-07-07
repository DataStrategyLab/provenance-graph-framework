# PGF Security Model

This document states what PGF v0.1 does and does not guarantee. It is the
long-form companion to [SECURITY.md](../SECURITY.md); where the two overlap,
they agree by design. Every claim here is scoped to v0.1.

## Cooperative-honesty provenance

PGF v0.1 provides **cooperative-honesty provenance**: it is a faithful record of
good-faith work by people and agents who are cooperating with the process. It
raises the floor on defensibility and traceability of *process*. It documents
that work was done a certain way by cooperating participants.

It does **not** prove that the record was not altered afterward. `events.jsonl`
is plaintext, one JSON object per line, appended by hooks and editable by anyone
with write access. The hooks that append to it can be bypassed — by writing the
file directly, or by running an agent (or the CLI) without the hooks loaded.
Therefore:

- Do **not** describe PGF output as tamper-proof.
- Do **not** describe it as a chain of custody.
- Do **not** treat recorded SHA-256 digests as an integrity control. v0.1 records
  digests of exported release-package files as a **convenience** for spotting
  accidental change, not as evidence against a motivated editor of the log.

## Why the gate lives in three places

Because hooks only enforce the process when work runs through Claude Code with
the project settings loaded, the release gate is **not** a hook alone. The same
gate is enforced at three points, weakest to strongest:

1. **Hook** (`block-release.py`, PreToolUse on Bash): blocks `pgf export` when the
   release gate fails inside a Claude Code session.
2. **CLI** (`pgf check` / `pgf export`): holds even when someone runs the CLI
   directly or drives it from another agent.
3. **CI**: holds on every pull request and push to `main`, independent of any
   local environment.

No agent — including Claude Code or Codex — marks anything release-ready. Release
readiness is decided by `pgf check`, hooks, CI, and a recorded **human approval
event**.

## Determinism scope: replay, not regeneration

Materialization is deterministic **replay** of a recorded history: the same event
log materializes to byte-identical `nodes.json`, `edges.json`, and `state.json`
across two runs and across machines. This is a property of the materializer, not
of the underlying work.

Claim extraction is **not** deterministic. The graph records what was decided,
not what a model would decide again if asked. Do not describe PGF output as
"reproducible" beyond replay; a "reproducible" claim without the replay qualifier
is a documentation defect.

## Selected threats and where the real control sits

- **Prompt injection in source documents** — treat all source text and model
  output as untrusted until reviewed; human review of material claims.
- **Secret or client-data leakage** — permissions deny-list hides `.env` and
  `secrets/` paths; the PreToolUse `no-secret-leak.py` hook catches content-based
  leaks path rules cannot see; synthetic-only examples.
- **Release-gate bypass** — the three enforcement points above (hook, CLI, CI).
- **Provenance theater** (low-quality machine-extracted claim nodes creating
  false assurance) — the claim-normalization skill's verifiability,
  decontextualization, and materiality rules; the extraction-quality fixture;
  claim `origin` visible to every reviewer; human review of high-materiality
  claims.
- **Log tampering** — acknowledged **out of scope** for v0.1. Tamper-evidence is
  the v1.0+ answer.

Note one deliberately **excluded** control: Codex second-reads are a useful
second opinion, not an independent safety layer. Two frontier models share
failure modes, so correlated review is not counted among the controls. The
controls are the human, the deterministic CLI, and CI.

## Upgrade path (future, not a v0.1 promise)

If a buyer needs tamper-evidence, the intended v1.0 path is: hash-chain the event
log; attest the release package as an **in-toto Statement** (subject = the digest
list recorded by `release.exported`) in a **DSSE envelope**; sign with **Sigstore**
keyless signing, with optional Rekor anchoring. This is named as a direction, not
built in v0.1.
