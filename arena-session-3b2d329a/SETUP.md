# SETUP.md — one file that sets up this entire environment

This file is the whole setup. Read it, run the one command in §2, and the working
environment exists: memory, real-time log, state pointer, rules, hook.

**Files in this folder:** `SETUP.md` (this file) + `bootstrap.sh` (the script).
Everything else is created by the script.

---

## §0 — The setup prompt (verbatim)

The instruction this environment exists to satisfy, quoted exactly as written:

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

### What each line requires, and how this environment delivers it

| The prompt says | Delivered by |
|---|---|
| "create a folder… for this session, name it something" | This folder — `arena-session-3b2d329a/`, named after the session id in the branch `arena/3b2d329a-aidata` |
| "everything… every command… pushed in that folder… commit directly, no wait, in real time" | The loop in §3: every step writes a log entry and commits + pushes before the next step. The git hook logs commits automatically, even without an agent. |
| "so that even if we get disconnected we can recover our memory" | `SESSION_STATE.md` (single resume pointer) + append-only `logs/` + `TASKS.json`. §5 is the recovery procedure. |
| "work it in a nice structuring system" | The fixed layout §1 — every file has one job. |
| "work entirely as anthropics/claude-code, adapt its nature and features" | `CLAUDE.md` as the memory/instruction file, YAML-frontmatter `commands/`, `agents/`, `skills/`, `hooks/` with the exit-code contract (0 = allow, 2 = block). §6 has the full mapping and where the full layer lives in history. |
| "every step pushed: what the task was, how you complete it, the plan, what's happening" | The log template: Task · Plan · verbatim Commands · Results · Decisions · Next. §3. |
| "see everything, in a dependent manner — first beware claude, first, then do this task" | Order of operations on arrival: read `CLAUDE.md` → `SESSION_STATE.md` → newest logs → `TASKS.json` → then start the task. §3. |
| "and do tell him how to work in it" | §3 is written for exactly that: hand it to an agent, or follow it yourself. |

---

## §1 — What this environment is

```
arena-session-3b2d329a/
├── SETUP.md              ← this file: the prompt, the rules, the bootstrap  (always here)
├── bootstrap.sh          ← creates/refreshes the environment below          (always here)
│
├── CLAUDE.md             ← rules + environment facts for any agent working here
├── SESSION_STATE.md      ← LIVE POINTER: last done · in progress · next · blocked
├── TASKS.json            ← machine-readable task truth
├── logs/                 ← append-only work log: 000N-slug.md + INDEX.md + auto-commit-log.md
├── memory/MEMORY.md      ← condensed long-term memory
├── notes/                ← reasoning, lessons learned
├── artifacts/            ← deliverables produced by work (scripts, reports)
├── commands/             ← command definitions (resume · status · log · checkpoint)
├── agents/               ← role definitions (memory-keeper · auditor)
└── hooks/                ← install.sh + the git pre-commit logger
```

Design rules baked into the environment:

1. **Git is the only state store.** If it isn't committed, it doesn't exist.
2. **Append-only logs.** History is never rewritten, so a disconnect can't corrupt it.
3. **One resume pointer.** `SESSION_STATE.md` is the single file a returning agent reads.
4. **Evidence over memory.** Log entries carry verbatim commands, not summaries.
5. **Failures are content.** A failed command with its error is logged like a success.

---

## §2 — Set it up (one command)

```bash
bash arena-session-3b2d329a/bootstrap.sh
```

What it does:

- creates the tree in §1 and the starter files (`CLAUDE.md`, `SESSION_STATE.md`,
  `TASKS.json`, `logs/INDEX.md`, `memory/MEMORY.md`, the `commands/` `agents/` `skills/`
  hints, `hooks/`)
- installs the **git pre-commit hook** so every commit on this branch appends a line to
  `logs/auto-commit-log.md` — the trail survives even if no agent is running
- **never overwrites existing state** — re-running it is safe and only fills in what is
  missing (that is also the fix after a sandbox restart, which clears `.git/hooks/`)

Requirements: `bash`, `git`, `python3`. Nothing else. No server, no dependencies.

---

## §3 — How to work in it

**If you are an agent joining this environment, do this in order:**

```
1. READ  CLAUDE.md            the rules and the environment facts
2. READ  SESSION_STATE.md     last done · in progress · next · blocked
3. READ  logs/INDEX.md, then the newest logs/000N-*.md in full (verbatim commands + results)
4. READ  TASKS.json           the machine-readable task truth
5. WORK  the loop below
```

**The loop — this is the whole method:**

```
DO the step
   ↓
write logs/NNNN-slug.md          (next free number; template below)
   ↓
update SESSION_STATE.md          (last done / in progress / next actions / blocked)
update TASKS.json  + a row in logs/INDEX.md
   ↓
git add -A
git commit -m "session(NNNN): <slug>"
git push origin arena/3b2d329a-aidata
```

**Log entry template** (also in `CLAUDE.md`):

```markdown
# LOG-NNNN — <short title>
| Field | Value |
|---|---|
| id | `NNNN` |
| ts_utc | YYYY-MM-DDTHH:MMZ |
| phase | PX — <name> |
| status | ✅ done / 🟡 partial / ❌ failed / ⛔ blocked |

## Task        — what was asked (quote the user when possible)
## Plan        — numbered steps, as intended before running them
## Commands run (verbatim)  — exact, copy-pasteable
## Results     — raw numbers/outputs/errors
## Decisions   — decision, reason, rejected alternative
## Next        — what happens next
```

**Rules that are not optional:**

1. **Real time.** One logical step = one log entry = one commit = one push. Never batch.
2. **Verbatim commands** in the log; raw results, not summaries of summaries.
3. **Log failures too** — they are the most useful lines after a disconnect.
4. **Never rewrite** a published entry and never renumber; corrections are new entries.
5. **`SESSION_STATE.md` must never be stale.** If it is, that's a bug — fix it in the same
   commit as the entry that exposed it.
6. **Checkpoint before long/risky work:** write what you are about to attempt, commit it,
   then attempt it.
7. **No secrets** in this folder, ever.
8. **After a sandbox restart:** run `git fetch && git status -sb` first (local `.git` can
   be behind origin), reconcile with `git reset --soft` — never `--hard` — then re-run
   `bash arena-session-3b2d329a/bootstrap.sh` to restore the git hook.

**Using the command files** (`commands/`, Claude Code format — YAML frontmatter, a
`## Context` block whose `` !`cmd` `` lines are shell to run, then `## Your task`):

| File | Purpose |
|---|---|
| `resume.md` | rebuild context from Git alone and continue |
| `status.md` | one screen: state + tasks + last log + uncommitted work |
| `log.md` | write the next numbered entry and commit it |
| `commit-memory.md` | checkpoint before a long/risky operation |

Copy them to `.claude/commands/` to use them as slash commands in Claude Code; paste them
into any other agent's chat as prompts; run the listed commands by hand if you're a human.
The files are runbooks either way.

---

## §4 — Standing facts about this repository

Rules that apply to any work here, regardless of task:

- **`python-projects/collections/` is third-party open-source code** (both collections are
  MIT). Their `LICENSE` files, `CREDITS.md` and `SOURCE.md` files stay in place — that is
  the condition of the MIT license, not decoration. Files may be *added* to those folders;
  authors and licenses are not stripped from them.
- **`python-projects/python-learning/` is the owner's own work** and is not third-party
  material.
- **`Adarshukumar/Python`** (the separate Python repo) is writable only when the GitHub
  connection grants access to that repository; the default sandbox token is scoped to
  `AIDATA` and returns 403 on writes there.
- **GitHub API budget:** core limit 5,150 requests/hour. Check
  `gh api rate_limit --jq '.resources.core.remaining'` before any batch of calls.

---

## §5 — Recovery

**After a disconnect (new session):**

```bash
git fetch origin && git checkout arena/3b2d329a-aidata && git pull
cat arena-session-3b2d329a/SESSION_STATE.md
cat arena-session-3b2d329a/CLAUDE.md
ls -t arena-session-3b2d329a/logs | head
cat arena-session-3b2d329a/logs/$(ls arena-session-3b2d329a/logs | grep -E '^[0-9]{4}-' | sort | tail -1)
```

**After a sandbox restart:** `.git/hooks/` and `/tmp` are gone, and local `.git` may be
behind origin. Run `git fetch && git status -sb` first, reconcile with `reset --soft`, then
`bash arena-session-3b2d329a/bootstrap.sh` (re-installs the hook). Rebuild any scratch from
`artifacts/` scripts rather than trying to restore `/tmp`.

**Recovering anything from before the reset** — all earlier content is still in Git
history (full clone required; `--depth 1` clones do not have it):

```bash
git log --oneline --all | less        # every past step
git checkout 9d94765 -- arena-session-3b2d329a   # the complete pre-reset folder
git checkout e18e1d3 -- arena-session-3b2d329a/audit   # the provenance audit + report
git checkout 6e70b0c -- arena-session-3b2d329a/artifacts  # curation scripts (CREDITS.md, PR runners)
git checkout 56e0a44 -- python-projects/PROJECTS.md      # the project index generator output
```

---

## §6 — Where the earlier work lives (history map)

| What | Commit | Path it was at |
|---|---|---|
| Complete pre-reset environment (15 log entries, all docs) | `9d94765` | `arena-session-3b2d329a/` |
| Provenance audit of `Adarshukumar/Python` (9,007 files classified, report, files.csv) | `e18e1d3` | `arena-session-3b2d329a/audit/` |
| Curation package (`CREDITS.md`, honest `README.md`, PR runner scripts) | `6e70b0c` | `arena-session-3b2d329a/artifacts/{curation,scripts}/` |
| Project index generator + `PROJECTS.md` | `56e0a44` | `arena-session-3b2d329a/artifacts/scripts/build_projects_index.py` |
| The full Claude Code-style layer (commands, agents, skills, hooks, plugin manifest) | `9d94765` | `arena-session-3b2d329a/{commands,agents,skills,hooks,.claude-plugin}/` |

The reset itself (what was removed, and why the environment was rebuilt clean) is recorded
in `logs/0001-reset-and-bootstrap.md`.

---

<div align="center">

**One file to read, one command to run, everything else is created.**

</div>
