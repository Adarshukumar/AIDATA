---
description: Show current session status (state, tasks, last log) in one screen
allowed-tools: Bash(cat:*), Bash(ls:*), Bash(git status:*), Bash(git log:*)
---

## Context

- Git status: !`git status --short`
- Branch: !`git branch --show-current`
- Task status: !`cat arena-session-3b2d329a/TASKS.json`
- Log files: !`ls arena-session-3b2d329a/logs/`

## Your task

Print a compact status report with four sections and nothing else:

1. **State** — copy the fields table from `SESSION_STATE.md`.
2. **Tasks** — from `TASKS.json`: id, title, status (grouped by phase; show counts).
3. **Last log** — filename + its one-line summary from `logs/INDEX.md`.
4. **Uncommitted work** — anything in `git status` inside `arena-session-3b2d329a/`
   (this must normally be empty; if not, commit it immediately before reporting further).
