#!/usr/bin/env python3
"""Git pre-commit hook: append every commit on this branch to logs/auto-commit-log.md."""
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = Path(__file__).resolve().parent.parent / "logs" / "auto-commit-log.md"
LOG_BRANCH = "arena/3b2d329a-aidata"


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                          check=False).stdout.strip()


def main() -> int:
    if run("git", "rev-parse", "--abbrev-ref", "HEAD") != LOG_BRANCH:
        return 0
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
        LOG.write_text("# auto-commit-log.md\n\n> Appended by the git pre-commit hook.\n\n",
                       encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"### {ts} — {len(files)} file(s) staged\n\n{shown}\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
