#!/usr/bin/env python3
"""Always-on git pre-commit hook: append every commit to logs/auto-commit-log.md.

The Claude Code-format hooks in hooks.json only fire inside an agent runtime that
understands them. This script is the deterministic fallback: install it into
.git/hooks/pre-commit (see hooks/install.sh) and every commit made in this repo leaves
a line in the memory — even a commit made by a human with no agent attached.

Staging the log file happens after the message is written (see install.sh wrapper), so
the entry lands in the *next* commit — the log is always one step behind reality, which
is exactly what a log should be.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repo root
LOG = Path(__file__).resolve().parent.parent / "logs" / "auto-commit-log.md"


def run(*args: str) -> str:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, check=False
    ).stdout.strip()


def main() -> int:
    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "arena/3b2d329a-aidata":
        return 0  # only log this session's branch

    staged = run("git", "diff", "--cached", "--name-only")
    if not staged:
        return 0

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    files = staged.splitlines()
    shown = "\n".join(f"  - {f}" for f in files[:25])
    if len(files) > 25:
        shown += f"\n  - … and {len(files) - 25} more"

    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text(
            "# auto-commit-log.md\n\n"
            "> Appended by the git pre-commit hook (`hooks/install.sh`).\n"
            "> One entry per commit on `arena/3b2d329a-aidata`.\n\n",
            encoding="utf-8",
        )
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"### {ts} — {len(files)} file(s) staged\n\n{shown}\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
