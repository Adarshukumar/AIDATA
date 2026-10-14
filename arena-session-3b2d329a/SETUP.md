# SETUP.md — the setup prompt, and how to work in this folder

Everything in `arena-session-3b2d329a/` is **plain files in Git**. There is no service to
start, no database, no install step that can fail silently.

This file has two jobs:

1. **§0 — the prompt that created this folder** (verbatim), and what each line actually
   means in practice.
2. **§0b — how to work in it**: the instructions for anyone (agent or human) who joins.
3. **§1 onward** — the full operational guide: activation, verification, recovery,
   troubleshooting.

---

## §0 — The setup prompt (verbatim)

This is the instruction that created this folder, quoted exactly as it was written:

> okiew look do crete a folder in our main reposrity as this branch
>
> for now do cretate a folder For this session name it soemthing..
>
> look u have to make sure ur eveything thinking and all tasks and all the things is going
> to be pushed in that folder... evert command all of the things what u r doing pushing
> inside it make sure to push it and commit it direclty no wait in real time... okk ??
>
> so that even we got disconnected can we recover our memory...
>
> and u will take that memory.. and in that folder work it in nice struturing system..
>
> and do make ur self work entirely as a [https://github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)
> adapt its nautre and sense all the featuring and all the working pushed here..
>
> and one more thing ur eveystepis going to pushed here as what does the task was and how u
> r completeing it and whats ur plan and what thinsg happenming and how its eveythign going
> okk ??
>
> see everythin... in depend manner do first ebeire claude... first then do this task...
>
> and do tell him how to work.. in it

### What each line means in practice

| The prompt says | Implemented as |
|---|---|
| "create a folder… for this session, name it something" | `arena-session-3b2d329a/` — named after the session id in the branch (`arena/3b2d329a-aidata`) |
| "everything… every command… pushed in that folder… commit directly, no wait, in real time" | The working loop in §0b: one log entry + one commit + one push per step. Nothing is batched for later. |
| "so that even if we get disconnected we can recover our memory" | `SESSION_STATE.md` (resume pointer) + append-only `logs/` + `TASKS.json`. The drill in §7 was run against a fresh clone and passed (LOG-0006); a real sandbox restart was recovered with zero loss (LOG-0008). |
| "work it in a nice structuring system" | Fixed layout: logs · memory · notes · commands · agents · skills · hooks · artifacts · audit |
| "work entirely as claude-code, adapt its nature and features" | Study of that repo is in `notes/claude-code-study.md`; its shapes are mirrored here: `CLAUDE.md` memory file, YAML-frontmatter commands, subagents, skills, hooks with the exit-code contract (0 = allow, 2 = block), plugin manifest |
| "every step pushed: what the task was, how you complete it, what's the plan, what's happening" | The log template (`skills/session-memory/references/logging-format.md`): Task · Plan · verbatim Commands · Results · Decisions · Next |
| "see everything, in a dependent manner — first beware claude, first, then do this task" | Phase order in `PLAN.md`: P0 bootstrap → P1 Claude Code study → P2 memory guarantee → then the actual tasks (P3 audit onward) |
| "and do tell him how to work in it" | §0b below — the same instructions a new agent gets on arrival |

---

## §0b — How to work in this folder

**If you are an agent joining this session, do these five things before anything else:**

```
1. READ   CLAUDE.md                 → the rules and the environment facts
2. READ   SESSION_STATE.md          → last done · in progress · next · blocked
3. READ   logs/INDEX.md, then the newest logs/000N-*.md in full
                                    → the verbatim commands and results of the last work
4. READ   TASKS.json                → the machine-readable task truth
5. WORK   the loop below, one step at a time
```

**The loop — this is the whole method:**

```
DO the step
   ↓
write logs/NNNN-slug.md             (next free number; template in skills/session-memory/references/logging-format.md)
   ↓
update SESSION_STATE.md             (last done / in progress / next actions / blocked)
update TASKS.json  (+ logs/INDEX.md row)
   ↓
git add -A
git commit -m "session(NNNN): <slug>"
git push origin arena/3b2d329a-aidata
```

**Rules that are not optional:**

1. **Real time.** One logical step = one log entry = one commit = one push. Never batch.
2. **Verbatim commands** in the log, raw results — not summaries of summaries.
3. **Log failures too.** A failed command with its error is the most useful line after a
   disconnect. See `logs/0004` and `notes/lessons.md`.
4. **Never rewrite** a published log entry, and never renumber. Corrections are new entries
   that cite the old one.
5. **`SESSION_STATE.md` must never be stale.** If it is, that is a bug: fix it in the same
   commit as the log entry that exposed it.
6. **Before anything long or risky** (a clone, 100+ API calls): write what you are about to
   attempt, commit it, *then* attempt it — the checkpoint variant
   (`commands/commit-memory.md`).
7. **No secrets** in this folder, ever.
8. **After a sandbox restart:** `git fetch && git status -sb` first (local `.git` may be
   behind origin), reconcile with `reset --soft` — never `--hard` — then re-run
   `hooks/install.sh` (hooks live in `.git/`, which is not part of the tree).

**Using the commands** (`commands/` — Claude Code format):

| File | Purpose |
|---|---|
| `resume.md` | rebuild context from Git alone and continue |
| `status.md` | one screen: state + tasks + last log + uncommitted work |
| `log.md` | write the next numbered entry and commit it |
| `commit-memory.md` | checkpoint before a long/risky operation |
| `audit-python-repo.md` | re-run the provenance audit |

Copy `commands/` into `.claude/commands/` to use them as slash commands in Claude Code;
paste them into any other agent's chat as prompts; run the listed commands by hand if you
are a human. The files are runbooks either way.

---

## 1. What you get

| Capability | Where it lives | Active out of the box? |
|---|---|---|
| Real-time work log (every step, verbatim commands) | `logs/000N-*.md` + `logs/INDEX.md` | ✅ yes (written by the agent each step) |
| Live resume pointer (last done / now / next / blocked) | `SESSION_STATE.md` | ✅ yes |
| Machine-readable task truth | `TASKS.json` | ✅ yes |
| Rules for any agent working here | `CLAUDE.md` | ✅ yes |
| Long-term condensed memory | `memory/MEMORY.md` | ✅ yes |
| Slash-command definitions | `commands/*.md` | ✅ yes (as documents) |
| Subagent definitions | `agents/*.md` | ✅ yes (as documents) |
| Skill + references | `skills/session-memory/` | ✅ yes |
| **Auto-log of every commit** | `hooks/pre_commit_log.py` → `.git/hooks/pre-commit` | ⚠️ **needs one command** (step 3) |
| Agent-runtime hooks (session start / tool guards) | `hooks/hooks.json` | ⚠️ only inside a runtime that reads this format |
| Plugin manifest | `.claude-plugin/plugin.json` | informational |

---

## 2. Step 0 — get the repo

```bash
git clone https://github.com/Adarshukumar/AIDATA.git
cd AIDATA
git checkout arena/3b2d329a-aidata        # the session branch
```

## 3. Step 1 — activate the always-on hook (the only required command)

```bash
bash arena-session-3b2d329a/hooks/install.sh
# installed: .git/hooks/pre-commit → logs every commit to logs/auto-commit-log.md
```

From now on **every commit on this branch appends a line to
`arena-session-3b2d329a/logs/auto-commit-log.md`** (timestamp + staged files), even a
commit made by a human with no agent attached. That is the safety net: even if the agent
forgets to log, the commits still leave a trail.

> The hook is local to your clone (`.git/hooks/` is never committed). Re-run the installer
> after a fresh clone. It is idempotent.

## 4. Step 2 — verify the system

```bash
cd arena-session-3b2d329a

# a) state file is fresh
head -20 SESSION_STATE.md

# b) the index lists every entry, and the newest entry exists
tail -5 logs/INDEX.md
ls logs/ | grep -E '^[0-9]{4}-' | sort | tail -1

# c) tasks parse as JSON
python3 -m json.tool TASKS.json > /dev/null && echo "TASKS.json OK"

# d) hook is installed and executable
test -x ../.git/hooks/pre-commit && echo "hook installed"

# e) audit deliverables are present
ls audit/
```

All five should succeed. If (d) fails, re-run step 1.

## 5. Step 3 — the working loop (this is the whole method)

```
DO the step
   ↓
write logs/NNNN-slug.md        (template: skills/session-memory/references/logging-format.md)
   ↓
update SESSION_STATE.md + TASKS.json + logs/INDEX.md
   ↓
git add -A && git commit -m "session(NNNN): <slug>" && git push origin arena/3b2d329a-aidata
```

**Real time.** Not at the end of the session. One logical step = one commit.

Before anything long or risky (a clone, 100+ API calls), run the checkpoint variant:
write down what you are about to attempt, commit it, *then* attempt it.

## 6. Step 4 — using the commands (any agent, any tool)

The files in `commands/` are written in Claude Code's format (YAML frontmatter with
`description` / `allowed-tools`, then a `## Context` block whose `` !`cmd` `` lines are
shell that gets executed, then `## Your task`). Three ways to use them:

1. **Inside Claude Code** — copy `commands/` to `.claude/commands/` at a repo root, then
   type `/resume`, `/status`, `/log`, `/audit-python-repo`, `/commit-memory`.
2. **Any other agent (Cursor, Copilot, GPT, …)** — paste the file's content into the chat
   as the prompt. The `!`cmd`` lines document exactly what context to gather.
3. **A human** — just run the commands listed in each file's Context block by hand; the
   files double as runbooks.

| Command | Use it when |
|---|---|
| `/resume` | you (or a fresh agent) are resuming after a disconnect or a gap |
| `/status` | you want one screen: state + tasks + last log + uncommitted work |
| `/log` | you finished a step and want the entry + commit done properly |
| `/commit-memory` | before a long/risky operation |
| `/audit-python-repo` | re-run the provenance audit of `Adarshukumar/Python` |

## 7. Step 5 — recovery after a disconnect

```bash
git fetch origin && git checkout arena/3b2d329a-aidata && git pull
cat arena-session-3b2d329a/SESSION_STATE.md      # last done / now / next / blocked
cat arena-session-3b2d329a/CLAUDE.md             # the rules
ls -t arena-session-3b2d329a/logs | head          # newest entries
cat arena-session-3b2d329a/logs/$(ls arena-session-3b2d329a/logs | grep -E '^[0-9]{4}-' | sort | tail -1)
python3 -m json.tool arena-session-3b2d329a/TASKS.json | tail -40
```

The full drill with pass criteria: `skills/session-memory/references/recovery.md`.
It was executed against a fresh clone on 2026-10-14 and passed (LOG-0006).

## 8. Step 6 — the agent-runtime hooks (optional, for Claude Code-style runtimes)

`hooks/hooks.json` declares four events in Claude Code's format:

| Event | Script | Effect |
|---|---|---|
| `SessionStart` | `session_start_context.sh` | prints `SESSION_STATE.md` + newest log so a resumed session starts with memory loaded |
| `PreToolUse` (Bash) | `guard_destructive.py` | **blocks** (exit 2) force-push, `reset --hard`, `filter-branch`, branch deletion, switching to `main` |
| `PostToolUse` (Bash) | `remember_command.py` | appends every Bash command to `memory/command-history.md` |
| `Stop` | `stop_checkpoint.sh` | warns if the memory folder has uncommitted changes |

To wire them into a Claude Code project, make a `.claude/settings.json` that points at
these scripts (matcher + `type: command`), e.g.:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [{ "type": "command",
                    "command": "python3 $CLAUDE_PROJECT_DIR/arena-session-3b2d329a/hooks/guard_destructive.py" }] }
    ]
  }
}
```

They are inert outside such a runtime — nothing breaks if you ignore them. The exit-code
contract is the real Claude Code one: **0 = allow, 2 = block and send stderr back to the
model.**

## 9. Daily cheat-sheet

```bash
# am I safe? (nothing uncommitted)
git status --short -- arena-session-3b2d329a

# what happened last?
tail -3 arena-session-3b2d329a/logs/INDEX.md

# what's next?
sed -n '/## Next actions/,/## Open/p' arena-session-3b2d329a/SESSION_STATE.md

# push memory only
git add arena-session-3b2d329a && git commit -m "session(checkpoint): ..." && git push
```

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `install.sh` says "not found" | running from the wrong directory | run it from the repo root: `bash arena-session-3b2d329a/hooks/install.sh` |
| `logs/auto-commit-log.md` not growing | hook not installed, or committing on another branch | re-run step 1; the hook only logs branch `arena/3b2d329a-aidata` |
| `SESSION_STATE.md` looks stale | a step was committed without updating it | treat as a bug: write a log entry, fix the state file, commit |
| Log numbers skipped/duplicated | two steps raced | never renumber; add a correction entry that cites the old one |
| `/tmp` scratch was wiped (sandbox restart) | expected — `/tmp` is not persisted | rebuild with `artifacts/scripts/audit_clone_heads.sh` (~20 s) + `audit_classify.py`; then re-probe |
| GitHub API returns 403 rate-limit | 5,150/hr exhausted | `gh api rate_limit --jq '.resources.core.reset'` and wait; keep batch sizes small |

## 11. Design rules (why it is built this way)

1. **Git is the only state store.** If it isn't committed, it doesn't exist.
2. **Append-only logs.** History is never rewritten, so a disconnect can't corrupt it.
3. **One resume pointer.** `SESSION_STATE.md` is the single file a fresh agent must read.
4. **Evidence over memory.** Log entries carry verbatim commands, not summaries of
   summaries — that is what makes resume actually work.
5. **Failures are first-class.** See `logs/0004` + `notes/lessons.md`.
6. **Formats borrowed from Claude Code, content is honest.** The folder *is* a memory
   system; it does not claim to be Claude Code.
