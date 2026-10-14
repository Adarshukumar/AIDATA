---
name: session-memory
description: Discipline for keeping a Git-backed, disconnect-proof memory of an agent session. Use whenever working inside arena-session-3b2d329a/ or when asked to "log this", "save progress", or "remember for later".
---

# Session memory

A session is **recoverable** when a fresh agent, given only the repository, can answer:
*what was happening, what was already tried, what worked, what is next?*

## The loop (run after every step)

```
DO the step  →  WRITE logs/NNNN-slug.md  →  UPDATE SESSION_STATE.md (+TASKS.json)
            →  git add -A  →  git commit -m "session(NNNN): slug"  →  git push
```

Real time. If you are about to do something that may take long (a clone, 200 API calls),
run the **checkpoint** variant first: write down what you are about to attempt, commit,
then attempt.

## What every entry must contain

1. The task as the user actually asked it (quote or faithful paraphrase).
2. The plan, in numbered steps.
3. **Verbatim commands** that were run.
4. Raw results (numbers, outputs, errors) — not a summary of a summary.
5. Decisions made, with the reason and the alternative that was rejected.
6. The next action.

See `references/logging-format.md` for the exact template and
`references/recovery.md` for the cold-start drill.

## Failure is content

A failed command with its stderr is often the single most useful line after a disconnect.
Never delete or "clean up" a failed entry; add a correction entry instead.
