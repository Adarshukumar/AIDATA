---
description: Append a new numbered log entry and commit it in real time
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(ls:*), Bash(date:*)
---

## Context

- Existing log entries: !`ls arena-session-3b2d329a/logs/`
- Current UTC time: !`date -u +"%Y-%m-%dT%H:%M:%SZ"`
- Branch: !`git branch --show-current`

## Your task

Write the next entry (never reuse a number):

1. Determine the next id `NNNN` from `ls logs/` (zero-padded, monotonic).
2. Create `arena-session-3b2d329a/logs/NNNN-<slug>.md` using the template in
   `skills/session-memory/references/logging-format.md`. Include the **verbatim commands**
   from this step and a short raw result for each.
3. Append a row to `logs/INDEX.md`.
4. Update `SESSION_STATE.md` (last log entry, last done, in progress, next actions) and
   `TASKS.json` if any status changed.
5. `git add -A && git commit -m "session(<NNNN>): <slug>" && git push origin arena/3b2d329a-aidata`.

Do not summarise the work in the chat beyond one line — the log entry is the deliverable.
