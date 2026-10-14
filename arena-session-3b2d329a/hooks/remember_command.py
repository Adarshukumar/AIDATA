#!/usr/bin/env python3
"""Claude Code-style PostToolUse hook: remember every Bash command.

Reads the hook payload as JSON on stdin (same contract as Claude Code hooks:
{"tool_name": "Bash", "tool_input": {"command": "..."}}), and appends the command
to memory/command-history.md with a UTC timestamp.

Always exits 0 — this hook observes, it never blocks.
"""

import json
import os
import sys
from datetime import datetime, timezone

LOG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "memory",
    "command-history.md",
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # No/invalid payload: nothing to remember. Never block.
        return 0

    if payload.get("tool_name") not in (None, "Bash"):
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        return 0

    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    new_file = not os.path.exists(LOG)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(LOG, "a", encoding="utf-8") as fh:
        if new_file:
            fh.write(
                "# command-history.md — raw trail of every Bash command\n\n"
                "> Appended automatically by `hooks/remember_command.py`.\n"
                "> Commands containing obvious secrets are redacted before writing.\n\n"
            )
        safe = redact(command)
        fh.write(f"### {ts}\n\n```bash\n{safe}\n```\n\n")
    return 0


def redact(command: str) -> str:
    """Defence in depth: never persist anything that looks like a credential."""
    lowered = command.lower()
    for needle in ("ghp_", "github_pat_", "gho_", "sk-ant", "sk-proj", "api_key=", "token="):
        if needle in lowered:
            return "[REDACTED: command contained what looks like a credential]"
    return command


if __name__ == "__main__":
    sys.exit(main())
