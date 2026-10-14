---
description: Commit the memory folder exactly as it stands (safety net before long operations)
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git status:*)
---

## Context

- Status: !`git status --short`
- Branch: !`git branch --show-current`

## Your task

Use this before any long-running, risky, or many-step operation (big audits, clones,
100+ API calls) so a disconnect can never lose more than the current step:

1. If there are uncommitted changes under `arena-session-3b2d329a/`, write a short
   `logs/NNNN-checkpoint.md` entry describing **what is about to be attempted** and what
   the expected duration is.
2. `git add -A && git commit -m "session(checkpoint): <what is about to run>"`
3. `git push origin arena/3b2d329a-aidata`
4. Then, and only then, start the risky operation.
