---
description: Rebuild full context after a disconnect and continue the session
allowed-tools: Bash(git fetch:*), Bash(git pull:*), Bash(cat:*), Bash(ls:*), Bash(tail:*)
---

## Context

- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
- Last 10 files touched in the session folder: !`git log --name-only --pretty=format: -5 -- arena-session-3b2d329a | grep -v '^$' | sort -u | tail -10`
- Live state: !`cat arena-session-3b2d329a/SESSION_STATE.md`
- Task truth: !`cat arena-session-3b2d329a/TASKS.json`

## Your task

Rebuild the session's memory from Git alone, then continue:

1. Read `CLAUDE.md` (rules) and `memory/MEMORY.md` (facts).
2. List `logs/` and read the **last two** entries in full — they contain the verbatim
   commands and results of the most recent work.
3. State, in order: what was last completed, what was in progress, what the immediate next
   action is, and anything blocked.
4. Continue from the "Next actions" section of `SESSION_STATE.md` **without asking** unless
   a user decision is explicitly pending (those are listed under "Open questions").
5. Log the resumed work as a new `logs/000N-*.md` entry before doing anything else.
