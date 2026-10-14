#!/usr/bin/env bash
# bootstrap.sh — create (or refresh) the working environment described by SETUP.md.
#
#   bash bootstrap.sh                      # creates ./arena-session-3b2d329a/
#   SESSION_DIR=my-session bash bootstrap.sh
#
# Creates the tree and starter files, installs the git pre-commit logger, and never
# overwrites existing state — safe to re-run at any time (also the fix after a sandbox
# restart, which clears .git/hooks/).
set -euo pipefail

REPO="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SESSION_DIR_NAME="${SESSION_DIR:-arena-session-3b2d329a}"
HERE="$REPO/$SESSION_DIR_NAME"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
BRANCH="$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

created=0; kept=0

write_if_missing() { # <path>   (content on stdin)
  local f="$1"
  mkdir -p "$(dirname "$f")"
  if [ -e "$f" ]; then
    echo "  keep    ${f#"$REPO"/}"
    kept=$((kept + 1))
  else
    cat > "$f"
    echo "  create  ${f#"$REPO"/}"
    created=$((created + 1))
  fi
}

echo "==> bootstrap"
echo "    repo:    $REPO"
echo "    session: $SESSION_DIR_NAME"
echo "    branch:  $BRANCH    time: $NOW"

mkdir -p "$HERE"/{logs,memory,notes,artifacts,audit,commands,agents,skills,hooks}

# ---------------------------------------------------------------- CLAUDE.md
write_if_missing "$HERE/CLAUDE.md" <<'EOF'
# CLAUDE.md — rules for any agent working in this folder

1. **Real time.** After every logical step: write `logs/NNNN-slug.md`, update
   `SESSION_STATE.md` (+ `TASKS.json`, + a row in `logs/INDEX.md`), then
   `git add -A && git commit -m "session(NNNN): <slug>" && git push`.
   Never batch work for later.
2. **Verbatim commands** in the log, raw results — not summaries of summaries.
3. **Log failures too.** A failed command with its error is the most useful line after a
   disconnect.
4. **Never rewrite** a published log entry, never renumber. Corrections are new entries.
5. **`SESSION_STATE.md` must never be stale.** If it is, that is a bug: fix it in the same
   commit as the entry that exposed it.
6. **Checkpoint before long/risky work:** write down what you are about to attempt, commit,
   then attempt.
7. **No secrets** in this folder, ever.
8. **After a sandbox restart:** `git fetch && git status -sb` first, reconcile with
   `git reset --soft` (never `--hard`), then re-run `bootstrap.sh`.

**Log template**

```markdown
# LOG-NNNN — <title>
| Field | Value |
|---|---|
| id | `NNNN` | ts_utc | YYYY-MM-DDTHH:MMZ | phase | status |

## Task · ## Plan · ## Commands run (verbatim) · ## Results · ## Decisions · ## Next
```

**Standing repository facts**

- Third-party code added to this repository keeps its license file and its credit.
- The owner's own work is kept separate from third-party material.
- The GitHub token in this sandbox is scoped to `AIDATA`; writes to other repos (e.g.
  `Adarshukumar/Python`) return 403 until the connection is extended.
- GitHub API core limit: 5,150/hour — check `gh api rate_limit` before batch calls.

Full guide: `../SETUP.md`.
EOF

# ---------------------------------------------------------------- SESSION_STATE.md
write_if_missing "$HERE/SESSION_STATE.md" <<EOF
# SESSION_STATE.md — live state

> Read this first after any disconnect. Updated in the same commit as every log entry.

| Field | Value |
|---|---|
| Branch | \`$BRANCH\` |
| Repo | \`$(basename "$REPO")\` |
| Environment created | $NOW by \`bootstrap.sh\` |
| Last log entry | _(none yet)_ |
| Status | 🟢 ready — fresh environment |
| Updated (UTC) | $NOW |

## Last done

- Environment bootstrapped from \`SETUP.md\`.

## In progress

- Nothing. Start the first task and log it as \`logs/0001-<slug>.md\`.

## Next actions

1. Read \`CLAUDE.md\` and the newest entry in \`logs/\`.
2. Work the loop in \`SETUP.md\` §3: do → log → update state → commit → push.

## Open questions / blocked

- None.
EOF

# ---------------------------------------------------------------- TASKS.json
write_if_missing "$HERE/TASKS.json" <<EOF
{
  "schema": "arena-session-tasks/1",
  "branch": "$BRANCH",
  "repo": "$(basename "$REPO")",
  "updated_at": "$NOW",
  "statuses": ["todo", "in_progress", "blocked", "done"],
  "tasks": []
}
EOF

# ---------------------------------------------------------------- logs
write_if_missing "$HERE/logs/INDEX.md" <<'EOF'
# logs/INDEX.md — work log index

Newest at the bottom. One entry per logical step. **Never renumber, never rewrite.**

| # | Entry | UTC | Phase | Status | Summary |
|---|-------|-----|-------|--------|---------|
EOF

write_if_missing "$HERE/logs/auto-commit-log.md" <<'EOF'
# auto-commit-log.md

> Appended automatically by the git pre-commit hook (`hooks/install.sh`).
> One entry per commit, on any branch.
EOF

# ---------------------------------------------------------------- hooks
write_if_missing "$HERE/hooks/pre_commit_log.py" <<'PYEOF'
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
PYEOF

write_if_missing "$HERE/hooks/install.sh" <<'EOF'
#!/usr/bin/env bash
# Install the always-on memory hook into .git/hooks/ (local to this clone).
set -euo pipefail
SESSION_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(git -C "$SESSION_DIR" rev-parse --show-toplevel)"
SRC="$SESSION_DIR/hooks/pre_commit_log.py"
DST="$REPO/.git/hooks/pre-commit"
REL="${SESSION_DIR#"$REPO"/}"

[ -f "$SRC" ] || { echo "error: $SRC not found" >&2; exit 1; }
cat > "$DST" <<HOOK
#!/usr/bin/env bash
# Managed by $REL — do not edit by hand.
set -euo pipefail
python3 "$SRC"
git add "$REL/logs/auto-commit-log.md" >/dev/null 2>&1 || true
HOOK
chmod +x "$DST"
echo "installed: .git/hooks/pre-commit → logs every commit to $REL/logs/auto-commit-log.md"
EOF

# ---------------------------------------------------------------- memory
write_if_missing "$HERE/memory/MEMORY.md" <<EOF
# MEMORY.md — condensed long-term memory

> Facts only, kept short. Live pointer: \`SESSION_STATE.md\`. Details live in \`logs/\`.

**Created:** $NOW (fresh environment).

## Environment

- Repo \`$(basename "$REPO")\`, branch \`$BRANCH\`, session folder \`$SESSION_DIR_NAME/\`.
- The loop, rules and recovery procedure: \`SETUP.md\` at the repository root.
- Work is only "done" when it is committed and pushed.

## Decisions of record

- The environment is created by \`bootstrap.sh\` at the repository root; it is idempotent and
  safe to re-run after a restart.

## Open items

- _(none yet)_
EOF

# ---------------------------------------------------------------- hints
write_if_missing "$HERE/README.md" <<'EOF'
# Session environment

Created by `bootstrap.sh` from `SETUP.md` at the repository root.

- **Live state:** `SESSION_STATE.md`
- **Rules:** `CLAUDE.md`
- **Work log:** `logs/` (newest entry first in `logs/INDEX.md`)
- **Tasks:** `TASKS.json`
EOF

write_if_missing "$HERE/commands/README.md" <<'EOF'
# commands/

Command definitions in Claude Code format (YAML frontmatter + `## Context` with
`` !`cmd` `` shell lines + `## Your task`).

| File | Purpose |
|---|---|
| `resume.md` | rebuild context from Git alone and continue |
| `status.md` | one screen: state + tasks + last log + uncommitted work |
| `log.md` | write the next numbered entry and commit it |
| `commit-memory.md` | checkpoint before a long/risky operation |

Copy to `.claude/commands/` for slash commands, or paste into any agent's chat as a prompt.
EOF

write_if_missing "$HERE/agents/README.md" <<'EOF'
# agents/

Role definitions for specialised helpers (markdown + frontmatter: `name`, `description`,
`tools`). An agent adopting a role reads this file first.

Suggested roles: `memory-keeper` (owns `SESSION_STATE.md`/`TASKS.json`/`logs/`),
`repo-auditor` (provenance work — blob-hash comparison), `license-auditor` (per-upstream
license status).
EOF

write_if_missing "$HERE/skills/README.md" <<'EOF'
# skills/

Reusable know-how as `SKILL.md` + `references/`. The core skill of this environment is
**session memory**: the loop, the log template, the recovery drill — specified in
`SETUP.md` §3 and §5, which is this skill's canonical text.
EOF

write_if_missing "$HERE/notes/README.md" <<'EOF'
# notes/

Reasoning and lessons learned: decisions with their rejected alternatives, post-mortems of
failures, anything worth keeping that is not itself a log entry or a deliverable.
EOF

write_if_missing "$HERE/artifacts/README.md" <<'EOF'
# artifacts/

Deliverables produced by work in this environment: scripts, reports, generated files.
Scripts belong here so any result can be reproduced with one command.
EOF

write_if_missing "$HERE/audit/README.md" <<'EOF'
# audit/

Provenance/verification work. Method of record: compare git blob SHAs
(`git ls-tree -r -z HEAD`) — byte-identity is proof, visual similarity is not.
EOF

# ---------------------------------------------------------------- git hook
echo "==> git hook"
bash "$HERE/hooks/install.sh"

echo
echo "==> done: $created created, $kept kept"
echo "    next: read SETUP.md §3, then work the loop."
