#!/usr/bin/env python3
"""validate-record hook (STUB, Phase 0).

Wiring: PostToolUse, matcher Write|Edit.
Phase 3 contract: for a changed JSON or YAML record, run `pgf validate` against
the bundled local schema registry (no network) and surface errors to Claude.
Exit 1 to warn on validation failure so the session sees the message.
Hook I/O: JSON event on stdin. Exit 0 allow, 1 warn. Use exit codes.
STUB: read stdin, do nothing, exit 0. Implement in Phase 3.
"""
import sys


def main() -> int:
    _ = sys.stdin.read()
    # TODO(Phase 3): run `pgf validate` on the changed record; exit 1 on error.
    return 0


if __name__ == "__main__":
    sys.exit(main())
