# PGF Roadmap

This roadmap tracks work beyond the v0.1 scope. The v0.1 build sequence lives in
[docs/build-plan.md](docs/build-plan.md); the product scope lives in
[docs/prd-v0_3.md](docs/prd-v0_3.md). Items below are directions, not
commitments, and are deliberately unplanned in detail.

## Next

- Tamper-evidence (v1.0 candidate): hash-chained event log; release-package attestation as an in-toto Statement (subject = the digest list recorded by release.exported) in a DSSE envelope; Sigstore keyless signing and optional Rekor anchoring where a buyer requires an external log. No bespoke signature formats.
- Exporters behind `pgf export --format`: prov-jsonld (W3C PROV interchange), otel (event-to-span replay once the GenAI semantic conventions stabilize; Development status as of mid-2026), in-toto (the attestation above).
- Eval lane: Promptfoo + Inspect; consumes claim origin and the extraction-quality fixture as ground truth; add evaluation.recorded to the event-type registry when built.
- Cross-artifact edges: promote the pgf check warning on external endpoints to a supported derived_from between artifacts.
- Materiality-downgrade check: promote the Phase 2 warning to a hard pgf check failure once the legal pack defines downgrade policy.
- Skills location: revisit .claude/skills vs the .agents/skills cross-agent convention when Claude Code documents shared-skills support, or when any review procedure is pasted into Codex a fourth time (then also ship it as an .agents/skills skill).
- Legal and GovCon instruction packs. Legal priority raised: California COPRAC's March 2026 proposed rule amendments move AI verification duties toward disciplinary force. GovCon pack speaks CMMC Phase 2 (C3PAO Level 2 from Nov 10, 2026) and NIST SP 800-171 documentation language without implying certification relevance.
- GOVERNANCE.md and a conformance test suite (spec-level MUST checklist runnable against any implementation) as v1.0 credibility items.
- Standards participation calendar: NIST CAISI AI Agent Standards Initiative (interoperability profile expected Q4 2026), AI RMF revision comment windows, OTel GenAI SIG tracking. One substantive NIST comment within two quarters of launch or redirect the attention to OTel.
