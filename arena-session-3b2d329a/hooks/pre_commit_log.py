#!/usr/bin/env python3
"""Git pre-commit hook: append every commit to logs/auto-commit-log.md."""
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # <repo>/<session>/hooks/x.py
LOG = Path(__file__).resolve().parent.parent / "logs" / "auto-commit-log.md"


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                          check=False).stdout.strip()


def main() -> int:
    staged = run("git", "diff", "--cached", "--name-only")
    if not staged:
        return 0
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD")
    files = staged.splitlines()
    shown = "\n".join(f"  - {f}" for f in files[:25])
    if len(files) > 25:
        shown += f"\n  - … and {len(files) - 25} more"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"### {ts} — {len(files)} file(s) staged on {branch}\n\n{shown}\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
