#!/usr/bin/env python3
"""block-release hook (STUB, Phase 0).

Wiring: PreToolUse, matcher Bash.
Phase 3 contract: parse tool_input.command. If it invokes `pgf export` and the
release gate fails (unmet materiality bands, undisposed contradiction, missing
human approval event, or a release-package digest-verification mismatch),
exit 2 naming the failing gate. One of three enforcement points (hook, CLI, CI).
Hook I/O: JSON event on stdin. Exit 0 allow, 1 warn, 2 block. Use exit codes.
STUB: read stdin, allow everything, exit 0. Implement in Phase 3.
"""
import sys


def main() -> int:
    _ = sys.stdin.read()
    # TODO(Phase 3): if pgf export and gate fails, exit 2 naming the gate.
    return 0


if __name__ == "__main__":
    sys.exit(main())
