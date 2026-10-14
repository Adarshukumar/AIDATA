#!/usr/bin/env python3
"""Claude Code-style PreToolUse hook: guard the memory against history rewriting.

Contract (mirrors Claude Code): JSON on stdin, exit 0 = allow, exit 2 = block the tool
call and show stderr to the agent.

Blocks, when the target is this repository:
  * git push --force / --force-with-lease
  * git reset --hard
  * git branch -D  /  git branch --delete --force
  * git filter-branch / filter-repo
  * rm -rf on the repo root or the session folder
"""

import json
import re
import sys

BLOCKED = [
    (r"git\s+push\b[^\n]*--force", "force-push would rewrite shared history"),
    (r"git\s+push\b[^\n]*(\s-f\b)", "force-push would rewrite shared history"),
    (r"git\s+reset\s+--hard", "reset --hard discards work that may not be logged yet"),
    (r"git\s+branch\s+(-D|--delete\s+--force)", "branch deletion destroys recoverable state"),
    (r"git\s+filter-(branch|repo)", "history rewriting destroys the memory's timeline"),
    (r"rm\s+-rf\s+[^\n]*(AIDATA|arena-session-3b2d329a)\b", "refusing to delete the memory"),
    (r"git\s+checkout\s+(main|master)\b", "this session must stay on arena/3b2d329a-aidata"),
    (r"git\s+switch\s+(main|master)\b", "this session must stay on arena/3b2d329a-aidata"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        return 0

    for pattern, reason in BLOCKED:
        if re.search(pattern, command):
            print(
                f"• Blocked by session guard: {reason}\n"
                f"  command: {command}\n"
                f"  If this is genuinely required, do it manually outside the session folder.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
