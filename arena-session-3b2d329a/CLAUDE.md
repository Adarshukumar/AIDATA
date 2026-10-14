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
