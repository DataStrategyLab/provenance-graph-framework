# Security Policy

## Integrity scope: cooperative-honesty, not tamper-evidence

PGF v0.1 provides **cooperative-honesty provenance**: it faithfully records the
work of people and agents who are cooperating with the process. Read this scope
before relying on any PGF output for an assurance argument.

**PGF v0.1 is NOT tamper-evident.** The event log (`events.jsonl`) is a plaintext
file that a determined actor can edit, and the hooks that append to it can be
bypassed by writing the file directly or by running an agent without the hooks
loaded. Do not describe PGF output as tamper-proof, and do not describe it as a
chain of custody. A reviewer who assumes "audit trail" means "cannot have been
altered" is wrong about v0.1.

v0.1 records SHA-256 digests of exported release-package files for convenience.
Recorded digests in an editable log are **not** an integrity control and must not
be presented as one.

## Determinism scope: replay, not regeneration

Materialization is deterministic **replay** of a recorded history: the same event
log produces byte-identical `nodes.json`, `edges.json`, and `state.json`. This is
not reproducibility of the underlying work. Claim extraction is not deterministic;
the graph records what was decided, not what a model would decide again. Do not
describe PGF output as "reproducible" beyond replay.

## Future tamper-evidence path (not a v0.1 promise)

Tamper-evidence is a v1.0 candidate, gated on a buyer who needs it — not part of
v0.1. The intended path:

- Hash-chain the event log (each event carries the hash of the prior event).
- Attest the release package as an **in-toto Statement** (subject = the digest
  list recorded by `release.exported`) wrapped in a **DSSE envelope**.
- Sign with **Sigstore** keyless signing, with optional Rekor transparency-log
  anchoring where an external log is required.

No bespoke signature formats. This section names the direction; it is not a
current capability.

## Reporting a vulnerability

If you find a security issue in this repository, please report it privately
rather than opening a public issue: use GitHub's private security advisory
("Report a vulnerability") on this repository. Include a description, affected
files or commands, and steps to reproduce. Because v0.1 is not tamper-evident,
reports about log editability or hook bypass describe **documented, in-scope
limitations** rather than vulnerabilities; see the integrity scope above.

Do not include secrets, real client data, CUI, or privileged material in a
report. Examples in this repository are synthetic by policy.
