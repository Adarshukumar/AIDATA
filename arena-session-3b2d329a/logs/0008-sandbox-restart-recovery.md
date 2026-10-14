# LOG-0008 — Sandbox restart incident: recovery worked as designed

| Field | Value |
|---|---|
| id | `0008` |
| ts_utc | 2026-10-14T18:30Z → 18:36Z |
| phase | P7 — operations |
| status | ✅ recovered |
| commit | _(this commit)_ |

## What happened

Between LOG-0007 and the push that followed it, the sandbox restarted. Effects:

1. **`/tmp` was wiped** — `/tmp/audit/out/*` and the 91 MB of partial clones were gone
   (expected; `SESSION_STATE.md` §"Scratch state" had documented them as rebuildable).
2. **The local `.git` was reset to the base commit `ca68b43`** while the *working tree*
   was restored at the end of the previous turn. Result: local branch had
   `ca68b43 → 328b021 (my new commit)`, while `origin/arena/3b2d329a-aidata` was 4 commits
   ahead (`c1206e5, 4d6a9bf, e18e1d3, 822f953`).
3. **`git push` was rejected**:
   ```
   ! [rejected] arena/3b2d329a-aidata -> arena/3b2d329a-aidata (fetch first)
   ```
4. The local `.git/hooks/pre-commit` was gone too (hooks live in `.git/`).

## Recovery (no data lost)

```bash
git fetch -q origin
git log --oneline origin/arena/3b2d329a-aidata -6      # origin is the truth: 822f953 …
git diff --stat HEAD origin/arena/3b2d329a-aidata -- arena-session-3b2d329a
#   -> only 6 files differ, and they are exactly this turn's new/updated files
git reset --soft origin/arena/3b2d329a-aidata          # keep tree+index, move branch to origin
git status --short                                     # staged delta = the 6 files
git commit -m "session(0007): …"
git push origin arena/3b2d329a-aidata                  # accepted → 95001ed
bash arena-session-3b2d329a/hooks/install.sh           # re-install the pre-commit hook
```

## Why nothing was lost

- Every step's work was **already pushed**; origin therefore held the complete history.
- The working tree was restored, so the *content* of the new files survived.
- `git diff` between my tree and origin proved the delta was exactly the intended 6 files —
  the check that made `reset --soft` safe instead of a guess.

## Lessons (added to `notes/lessons.md`)

1. **After any sandbox restart, assume local `.git` is behind.** First command of a turn
   should be `git fetch && git status -sb` before committing anything.
2. **Re-run `hooks/install.sh` after a restart** — `.git/hooks/` is not part of the tree.
3. The `/tmp`-wiped scenario was already documented; the rebuild cost was only 4 API calls
   (tree dumps) because the scripts are committed.
4. `reset --soft` (never `--hard`) is the safe reconciliation move: it moves the pointer
   and keeps the files, so a mistake is still recoverable.

## Next

- Update `notes/lessons.md`, `TASKS.json`, `SESSION_STATE.md`; commit + push.
