# Provenance Graph Framework (PGF)

An open-source, language-agnostic, repo-native framework for making high-stakes AI-assisted work products traceable from evidence intake to human-approved release.

**Status: v0.1 in development.** The repository is a skeleton under active construction; commands and schemas are not yet implemented. See [ROADMAP.md](ROADMAP.md) and [docs/build-plan.md](docs/build-plan.md) for the phase plan.

## What PGF is (and is not)

PGF records the provenance of work products and the process that produced them: claims, sources, evidence, reviews, approvals, and releases. It is not a content-credentials system. It does not sign media, embed C2PA manifests, or mark AI-generated content for EU AI Act Article 50 or California AI Transparency Act purposes. Those standards answer "where did this file come from and was it AI-generated." PGF answers "which evidence supports each claim in this deliverable, who reviewed it, and who approved its release." The two are complementary and PGF may reference content-credential metadata on sources in a future version.

## Integrity scope

PGF v0.1 provides **cooperative-honesty provenance**: a faithful record of good-faith work by people and agents cooperating with the process. It is **not tamper-evident** — the event log is plaintext and editable, and the hooks that append to it are bypassable. Do not describe PGF output as tamper-proof or as a chain of custody. Tamper-evidence is a future option, not a v0.1 promise. See [SECURITY.md](SECURITY.md) and [docs/security-model.md](docs/security-model.md).

## Deliverable

The unit of value is the human-readable release packet: a defensible memo, brief, or proposal section with its sources, its open questions, its reviewer sign-off, and a record of what changed before release. The provenance graph is the supporting infrastructure that makes that packet trustworthy; it is not the thing a reader opens first.

## Governance

- [AGENTS.md](AGENTS.md) is the canonical cross-agent instruction source.
- [CONTRIBUTING.md](CONTRIBUTING.md) covers contribution basics, the ADR-breadcrumb rule for schema changes, and DCO sign-off.
- No client-facing artifact is released without a human approval event. Release readiness is decided by `pgf check`, hooks, CI, and human approval — no agent marks anything release-ready.

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
