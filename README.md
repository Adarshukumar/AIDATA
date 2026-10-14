<div align="center">

# 🐍 AIDATA

### My Python workspace — a learning library, a personal set of lessons, and a session-memory system that survives disconnects

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Branch](https://img.shields.io/badge/branch-arena%2F3b2d329a--aidata-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)

**Hi, I'm Adarsh 👋**

This repo has three parts:

| | What it is | Where |
|---|---|---|
| 📚 | **`python-projects/`** — 183 open-source projects (credited) + **my own 54 lesson files** | [`python-projects/`](./python-projects) |
| 🧠 | **Session memory** — the work log, plan and state of my agent sessions | [`arena-session-3b2d329a/`](./arena-session-3b2d329a) |
| ⚙️ | **This file** — how to build and start everything | you're reading it |

</div>

---

## ⚡ Quick start (30 seconds)

```bash
git clone https://github.com/Adarshukumar/AIDATA.git
cd AIDATA

# 1. run the memory system's installer (one command, idempotent)
bash arena-session-3b2d329a/hooks/install.sh

# 2. read the live state of the session
cat arena-session-3b2d329a/SESSION_STATE.md

# 3. browse the projects
open python-projects/PROJECTS.md     # or: cat / less
```

That's it — no dependencies, no build step, no server. Everything is plain files in Git.

---

## 🏗️ How the system is built

### The memory system (`arena-session-3b2d329a/`)

A disconnect-proof memory for agent sessions. The idea is simple: **Git is the only state
store**, so anything not committed doesn't exist.

```
arena-session-3b2d329a/
├── SETUP.md            ← full guide (activation, verification, recovery, troubleshooting)
├── SESSION_STATE.md    ← LIVE POINTER: last done · in progress · next · blocked
├── CLAUDE.md           ← the rules any agent must follow in this folder
├── PLAN.md             ← phases and status
├── TASKS.json          ← machine-readable task truth
├── logs/               ← append-only work log: 000N-slug.md + INDEX.md
│   └── auto-commit-log.md   ← written automatically by the git hook
├── memory/MEMORY.md    ← condensed long-term memory
├── notes/              ← reasoning, lessons learned
├── commands/           ← slash-command definitions (resume · status · log · audit · checkpoint)
├── agents/             ← role definitions (memory-keeper · repo-auditor · license-auditor)
├── skills/             ← session-memory skill + references (logging format, recovery drill)
├── hooks/              ← the always-on git hook + agent-runtime hooks
├── artifacts/          ← deliverables produced by sessions (scripts, curation files)
└── audit/              ← the provenance audit of my Python repo
```

**Design rules:** append-only logs (history is never rewritten) · one resume pointer
(`SESSION_STATE.md`) · verbatim commands in every entry · failures logged like successes.

### The library (`python-projects/`)

```
python-projects/
├── PROJECTS.md      ← all 183 projects, grouped in 9 categories
├── CREDITS.md       ← who wrote what, licenses, sources
├── python-learning/ ← MY OWN 54 files: roadmap, 50 lessons, cheatsheet, 40 challenges
└── collections/
    ├── python-mini-project/          ← 131 projects · MIT · @ndleah + 100 contributors
    └── all-in-one-python-projects/   ←  59 projects · MIT · @king04aman + contributors
```

The collections are **other people's work**, kept complete with their license files and
credited in [`CREDITS.md`](./python-projects/CREDITS.md). My own code is
[`python-learning/`](./python-projects/python-learning).

---

## 🚀 How to start the system

### A. Use the memory system (any agent, any tool)

**Step 1 — activate the hook** (once per clone — `.git/hooks/` is not part of the repo):

```bash
bash arena-session-3b2d329a/hooks/install.sh
# installed: .git/hooks/pre-commit → logs every commit to logs/auto-commit-log.md
```

From now on **every commit leaves a trail automatically**, even commits made by a human
with no agent running.

**Step 2 — the working loop.** This is the whole method:

```
DO the step
   ↓
write logs/NNNN-slug.md          (template: skills/session-memory/references/logging-format.md)
   ↓
update SESSION_STATE.md + TASKS.json + logs/INDEX.md
   ↓
git add -A && git commit -m "session(NNNN): <slug>" && git push
```

Real time — one logical step per commit, never batched for later.

**Step 3 — use the commands.** `commands/` is written in Claude Code's format
(YAML frontmatter + `## Context` + `## Your task`):

| Command | Use it when |
|---|---|
| `/resume` | you or a fresh agent are resuming after a disconnect |
| `/status` | you want one screen: state + tasks + last log + uncommitted work |
| `/log` | you finished a step and want the log + commit done properly |
| `/commit-memory` | before a long or risky operation |
| `/audit-python-repo` | re-run the provenance audit |

Inside Claude Code: copy `commands/` to `.claude/commands/` at a repo root. Anywhere else:
paste the file into the chat as the prompt — the `!`cmd`` lines say exactly what context to
gather. As a human: run those commands by hand; the files double as runbooks.

### B. Recover after a disconnect

```bash
git fetch origin && git checkout arena/3b2d329a-aidata && git pull
cat arena-session-3b2d329a/SESSION_STATE.md         # last done / now / next / blocked
cat arena-session-3b2d329a/CLAUDE.md                # the rules
ls -t arena-session-3b2d329a/logs | head            # newest entries
cat arena-session-3b2d329a/logs/$(ls arena-session-3b2d329a/logs | grep -E '^[0-9]{4}-' | sort | tail -1)
```

The full drill with pass criteria lives in
[`skills/session-memory/references/recovery.md`](./arena-session-3b2d329a/skills/session-memory/references/recovery.md)
— it was executed against a fresh clone and passed (see `logs/0006`).

### C. Run the Python lessons

```bash
python python-projects/python-learning/01_hello_world.py
# every 01–50 file is runnable with Python 3 only — no pip install needed
```

Collection projects have their own requirements (`requirements.txt` inside each folder) and
their own READMEs — read those first.

---

## 📖 Full documentation

| Document | What's inside |
|---|---|
| [`SETUP.md`](./arena-session-3b2d329a/SETUP.md) | Complete activation guide: verification checklist, hook wiring, cheat-sheet, troubleshooting |
| [`CLAUDE.md`](./arena-session-3b2d329a/CLAUDE.md) | Rules + environment facts for any agent working here |
| [`SESSION_STATE.md`](./arena-session-3b2d329a/SESSION_STATE.md) | Current live state |
| [`PLAN.md`](./arena-session-3b2d329a/PLAN.md) / [`TASKS.json`](./arena-session-3b2d329a/TASKS.json) | Plan and task status |
| [`logs/INDEX.md`](./arena-session-3b2d329a/logs/INDEX.md) | Every work-log entry, newest last |
| [`python-projects/PROJECTS.md`](./python-projects/PROJECTS.md) | All 183 projects by category |
| [`python-projects/CREDITS.md`](./python-projects/CREDITS.md) | Attribution: folder → upstream → license → authors |
| [`audit/AUDIT_REPORT.md`](./arena-session-3b2d329a/audit/AUDIT_REPORT.md) | Provenance audit of my Python repo (blob-hash method) |

---

<div align="center">

**Built to be understood six months from now — by me, or by anyone else.**

*— Adarsh* 🐍

</div>
