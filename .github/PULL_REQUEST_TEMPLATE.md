<!-- Keep PRs small: one concern per PR. Name the phase task in the title. -->

## Summary

<!-- What does this change do, and why? Link the phase task in docs/build-plan.md. -->

## Checks run

Paste terminal evidence. If a check could not run, say exactly why.

- [ ] `ruff check .`
- [ ] `pytest`
- [ ] `python -m pgf check examples/association-board-brief`
- [ ] `python -m pgf materialize examples/association-board-brief`
- [ ] Offline validation (`pgf validate` / `pgf check` with networking disabled)

## Review guidelines (see AGENTS.md)

- [ ] No P0 issues: no fabricated citations/sources; no release-gate bypass; no
      secrets or real client data; no network calls in the core CLI; no
      nondeterministic materializer output; no schema change without a decision
      note in `provenance/`.
- [ ] No P1 issues: new CLI command has tests; golden fixtures current; AGENTS.md
      ≤ 200 lines; docs make no tamper-evidence or beyond-replay reproducibility
      claim.

## Release readiness

- [ ] This PR does **not** assert release-readiness. Release readiness is decided
      by `pgf check`, hooks, CI, and a **human approval event** — not by this PR.
