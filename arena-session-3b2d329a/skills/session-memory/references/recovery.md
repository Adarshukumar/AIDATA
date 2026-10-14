# Recovery drill (cold start)

Goal: prove that **the repository alone** is enough to resume. Run this drill after any
long gap, at the end of a work session, and once as a deliberate test (`T5.2`).

## The drill

```bash
git clone https://github.com/Adarshukumar/AIDATA.git && cd AIDATA
git checkout arena/3b2d329a-aidata

cat arena-session-3b2d329a/README.md          # what this folder is
cat arena-session-3b2d329a/CLAUDE.md          # the rules
cat arena-session-3b2d329a/SESSION_STATE.md   # last done / now / next / blocked
cat arena-session-3b2d329a/TASKS.json         # task truth
tail -n +1 arena-session-3b2d329a/logs/INDEX.md        # the timeline
ls -t arena-session-3b2d329a/logs/ | head -3            # newest entries
cat arena-session-3b2d329a/logs/$(ls arena-session-3b2d329a/logs/ | grep -E '^[0-9]{4}' | sort | tail -1)
```

## Pass criteria

The drill passes when you can state, without guessing:

1. The user's request(s) and the standing instructions.
2. The last completed step and the exact command that proved it.
3. The current in-progress step, including any partial outputs and where raw
   intermediates live (e.g. `/tmp/audit/` — note: scratch is **not** persisted).
4. The immediate next action, in enough detail to execute it.
5. Anything blocked, and on what (user decision? missing access? failing tool?).

If any of the five cannot be answered, the memory system has a bug: fix it, log the fix,
and re-run the drill.

## Known limits

- `/tmp` is scratch and dies with the sandbox: any intermediate that matters must be
  copied into the session folder before the sandbox ends.
- The GitHub token lives in the sandbox, not in Git. A resumed session must re-establish
  `gh` auth; the folder records *what* was accessed, never the credential.
