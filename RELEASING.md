# Releasing PGF

PGF is pre-1.0. This file records the v0.x release process. PGF v0.1 is **cooperative-honesty
provenance — a faithful record of good-faith work. It is NOT tamper-evident** (see `AGENTS.md`
"Integrity scope" and decision D2). Nothing in the release process changes that scope.

## Version tags and schema `$id`

- Releases are cut as annotated `vX.Y.Z` git tags on `main` for the v0.x line.
- Schema `$id` is a **stable identifier, never a fetch instruction** (D7). Before the first release tag,
  every `schemas/v0/*.schema.json` carries the placeholder
  `.../refs/tags/v0.0.0-dev/schemas/v0/<name>.schema.json`. **The release process MUST update each schema
  `$id` from the `v0.0.0-dev` placeholder to the release tag at tag time** so a released `$id` names an
  immutable document. Phase 6 release tooling will perform this rewrite; no such tooling exists yet.

## Release notes

- Each tag ships a changelog entry and release notes (a Phase 6 deliverable).
- **Every release note MUST carry the integrity language below.** Release notes never describe an artifact
  as release-ready, tamper-proof, or reproducible beyond replay; release readiness is decided by
  `pgf check`, hooks, CI, and a human approval event, not by an agent.

## Required integrity language (in every release note)

- PGF v0.1 is **cooperative-honesty provenance, not tamper-evident**; the event log is plaintext and
  editable and hooks are bypassable.
- Materialization is **deterministic replay, not deterministic regeneration**; do not call PGF output
  "reproducible" without the replay qualifier.
- Release-package SHA-256 `file_digests` are **convenience metadata for change detection, never an
  integrity control** in an editable v0.1 log (D6). Tamper-evidence (an in-toto Statement in a DSSE
  envelope, signed) is a v1.0 option, not a v0.1 promise.
- PGF is **work-product and process provenance, not a content-credentials or media-marking system** (not
  C2PA, not EU AI Act Article 50 marking).

## Merge posture

- Through Phase 2 the repo is in the **solo-approver phase**: `main` requires one approval, GitHub blocks
  self-approval, and the second approver is not yet active, so PRs merge via **admin bypass** (recorded,
  not silent). Branch protection stays on; merges are merge commits, not squashes, to preserve granular
  history.
- When the second approver is active, the posture transitions to **normal one-approval review** (no admin
  bypass).
- From Phase 3, `enforce_admins` is on and admin bypass is off.
