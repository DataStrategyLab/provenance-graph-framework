# Provenance Graph Framework

@AGENTS.md

## Claude Code operating notes
Use plan mode before changing schemas, hooks, release gates, or example packs.
Use the project skills in `.claude/skills/` for repeatable procedures. Use subagents for research, drafting, verification, and approval-summary preparation; subagents are read-only, the parent session does the writes.
Do not duplicate AGENTS.md here. AGENTS.md is canonical.
Do not mark any artifact as release-ready. Release readiness is determined by `pgf check`, release hooks, CI, and a human approval event.
Never claim a release package is tamper-evident or that claim extraction is reproducible; see AGENTS.md integrity scope.
One task per session. Run /clear between unrelated tasks. Read docs/build-plan.md for the current phase before starting phase work.

## Compact instructions
When summarizing this conversation, preserve: schema or gate changes and their rationale, the list of modified files, failing test output and its resolution. Summarize exploration briefly.
