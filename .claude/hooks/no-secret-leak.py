#!/usr/bin/env python3
"""no-secret-leak hook (STUB, Phase 0).

Wiring: PreToolUse, matcher Write|Edit|Read.
Phase 3 contract: inspect tool_input for secret patterns (API keys, tokens,
private keys, the planted test secret) and real client data / CUI. If found,
exit 2 to BLOCK before the write or read. PreToolUse is mandatory: PostToolUse
fires after the write and cannot undo a leak.
Hook I/O: JSON event on stdin. Exit 0 allow, 1 warn, 2 block. Use exit codes.
STUB: read stdin, allow everything, exit 0. Implement in Phase 3.
"""
import sys


def main() -> int:
    _ = sys.stdin.read()
    # TODO(Phase 3): scan tool_input; exit 2 on secret/client-data match.
    return 0


if __name__ == "__main__":
    sys.exit(main())
