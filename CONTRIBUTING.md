# Contributing to PGF

Thanks for your interest in the Provenance Graph Framework. This project is in
early (v0.1) development; contributions should track the phase plan in
[docs/build-plan.md](docs/build-plan.md).

## Ground rules

- **Read [AGENTS.md](AGENTS.md) first.** It is the canonical instruction source
  for both human and agent contributors, and it governs the non-negotiable
  principles, coding standards, and review priorities.
- **One concern per pull request.** Small, human-reviewable diffs. Name the
  phase task in the branch name and commit messages (e.g.
  `phase2: pgf materialize determinism + golden fixtures`).
- **Synthetic examples only.** Never commit secrets, real client data, CUI,
  privileged material, or confidential matter data.
- **No release-readiness claims.** Release readiness is decided by `pgf check`,
  hooks, CI, and a human approval event — not by any contributor or agent.

## Development setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the checks before finishing any task, in order:

```bash
ruff check .
pytest
python -m pgf check examples/association-board-brief
python -m pgf materialize examples/association-board-brief
```

If a check cannot run, say exactly why. Validation is offline: `pgf validate`
and `pgf check` must pass with networking disabled.

## ADR-breadcrumb rule (schema changes)

Any change to a schema in `schemas/` **must** be accompanied by a decision note
(a short ADR / architecture decision record) in `provenance/`, recording what
changed, why, and the migration implication. A schema change without a decision
note is a P0 review finding. This keeps the public contract auditable and gives
reviewers the rationale trail the diff alone cannot show.

## Developer Certificate of Origin (DCO)

This project uses the [Developer Certificate of Origin](https://developercertificate.org/).
Every commit must be signed off, certifying that you wrote the change or have
the right to submit it under the project's license. Add the sign-off with:

```bash
git commit -s -m "phaseN: your message"
```

which appends a trailer of the form:

```
Signed-off-by: Your Name <you@example.com>
```

Use your real name and an email you can be reached at. Commits without a valid
`Signed-off-by` trailer will be asked to amend before merge.
