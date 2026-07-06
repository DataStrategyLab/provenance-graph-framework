#!/usr/bin/env python3
"""append-event hook (STUB, Phase 0).

Wiring: PostToolUse, matcher Write|Edit.
Phase 3 contract: when an artifact or record file under an example changes,
append the provenance event to that artifact's events.jsonl (append-only,
monotonic seq, ULID event_id, UTC ts). PostToolUse is correct: append after.
Hook I/O: JSON event on stdin. Exit 0 allow, 1 warn. Use exit codes.
STUB: read stdin, do nothing, exit 0. Implement in Phase 3.
"""
import sys


def main() -> int:
    _ = sys.stdin.read()
    # TODO(Phase 3): derive and append the provenance event for the change.
    return 0


if __name__ == "__main__":
    sys.exit(main())
