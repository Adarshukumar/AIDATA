# SETUP.md — one file that sets up the entire environment

This file is the whole setup. Read it, run the one command in §2, and the working
environment exists: memory, real-time log, state pointer, rules, hook.

**In the repository root:** `SETUP.md` (this file) + `bootstrap.sh` (the script).
Everything else is created by the script, inside `arena-session-3b2d329a/`.

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
| "create a folder… for this session, name it something" | `bootstrap.sh` creates `arena-session-3b2d329a/` (rename with `SESSION_DIR=<name> bash bootstrap.sh`) |
| "everything… every command… pushed in that folder… commit directly, no wait, in real time" | The loop in §3: every step writes a log entry and commits + pushes before the next step. The git hook additionally logs every commit automatically, even with no agent running. |
| "so that even if we get disconnected we can recover our memory" | `SESSION_STATE.md` (single resume pointer) + append-only `logs/` + `TASKS.json`. §5 is the recovery procedure. |
| "work it in a nice structuring system" | The fixed layout in §1 — every file has one job. |
| "work entirely as anthropics/claude-code, adapt its nature and features" | `CLAUDE.md` as the memory/instruction file, YAML-frontmatter `commands/`, `agents/`, `skills/`, `hooks/` with the exit-code contract (0 = allow, 2 = block). §6 points to the full implementation in history. |
| "every step pushed: what the task was, how you complete it, the plan, what's happening" | The log template: Task · Plan · verbatim Commands · Results · Decisions · Next. §3. |
| "see everything, in a dependent manner — first beware claude, first, then do this task" | Order of operations on arrival: read `CLAUDE.md` → `SESSION_STATE.md` → newest logs → `TASKS.json` → then start the task. §3. |
| "and do tell him how to work in it" | §3 is written for exactly that: hand it to an agent, or follow it yourself. |

---

## §1 — What this environment is

Created by `bootstrap.sh` (never overwrites existing state):

```
arena-session-3b2d329a/
├── CLAUDE.md             ← rules + environment facts for any agent working here
├── SESSION_STATE.md      ← LIVE POINTER: last done · in progress · next · blocked
├── TASKS.json            ← machine-readable task truth
├── logs/                 ← append-only work log: 000N-slug.md + INDEX.md + auto-commit-log.md
├── memory/MEMORY.md      ← condensed long-term memory
├── notes/                ← reasoning, lessons learned
├── artifacts/            ← deliverables produced by work (scripts, reports)
├── commands/             ← command definitions (resume · status · log · checkpoint)
├── agents/               ← role definitions (memory-keeper · auditor)
├── skills/               ← reusable know-how (the session-memory skill = §3 + §5)
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
bash bootstrap.sh
```

What it does:

- creates the tree in §1 and the starter files (`CLAUDE.md`, `SESSION_STATE.md`,
  `TASKS.json`, `logs/INDEX.md`, `memory/MEMORY.md`, and the `commands/` `agents/` `skills/`
  `notes/` `artifacts/` `audit/` hints)
- installs the **git pre-commit hook** so every commit appends a line to
  `logs/auto-commit-log.md` — the trail survives even if no agent is running
- **never overwrites existing state** — re-running is safe and only fills in what is
  missing (that is also the fix after a sandbox restart, which clears `.git/hooks/`)

Requirements: `bash`, `git`, `python3`. Nothing else. No server, no dependencies.

To also **activate ECC** (the Claude Code harness vendored in `third_party/ecc/`, see §7–§8):

```bash
bash bootstrap.sh --activate        # needs Node.js 18+; writes .claude/; hooks ON
```

It is idempotent: if `.claude/ecc/install-state.json` already exists, it keeps the current activation.

---

## §3 — How to work in it

**If you are an agent joining this environment, do this in order:**

```
1. READ  arena-session-3b2d329a/CLAUDE.md            the rules and the environment facts
2. READ  arena-session-3b2d329a/SESSION_STATE.md     last done · in progress · next · blocked
3. READ  logs/INDEX.md, then the newest logs/000N-*.md in full (verbatim commands + results)
4. READ  TASKS.json                                  the machine-readable task truth
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
git push
```

**Log entry template:**

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
   `bash bootstrap.sh` to restore the git hook.

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

- **Third-party code added to this repository keeps its license and its credit.** When a
  folder is brought in from an upstream project, its `LICENSE` file (or an equivalent
  credit entry) stays in place — that is a condition of the license, not decoration.
- **The owner's own work is kept separate** from third-party material, so it is obvious
  which is which.
- **The GitHub token in a sandbox is scoped to `AIDATA`**; writes to other repositories
  (e.g. `Adarshukumar/Python`) return 403 until the connection is extended to them.
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
behind origin. Run `git fetch && git status -sb` first, reconcile with `reset --soft` (never
`--hard`), then `bash bootstrap.sh` — it restores the hook without touching the logs.

**If the environment folder is missing entirely:** `bash bootstrap.sh` recreates it. The
logs that existed before are still in Git history if they were committed — find them with
`git log --oneline --all | less`.

---

## §6 — History map (what earlier commits hold)

A full reset was performed on request: the project content was deleted and this setup file
now lives at the repository root. Nothing is lost — it is all in Git history:

| What | Commit | Path it was at |
|---|---|---|
| `python-projects/` — 862 files: two MIT collections (131 + 65 projects) + 54 own lesson files, plus `PROJECTS.md` index | `56e0a44` | `python-projects/` |
| Curation package — `CREDITS.md`, honest `README.md`, PR runner scripts | `6e70b0c` | `arena-session-3b2d329a/artifacts/{curation,scripts}/` |
| Provenance audit of `Adarshukumar/Python` — 9,007 files classified by blob hash, report + `files.csv` | `e18e1d3` | `arena-session-3b2d329a/audit/` |
| Complete earlier session folder — 14 log entries, full Claude Code-style layer (commands, agents, skills, hooks, plugin manifest) | `9d94765` | `arena-session-3b2d329a/` |
| First reset (SETUP.md v2 + bootstrap at the session path) | `dadb773` | `arena-session-3b2d329a/` |

Restoring anything:

```bash
git log --oneline --all | less                          # find the commit you want
git checkout 56e0a44 -- python-projects                  # e.g. the project library
git checkout e18e1d3 -- arena-session-3b2d329a/audit     # e.g. the audit
```

---

---

## §7 — Everything in this repository

| Path | What it is | Owner / source | How to rebuild or change it |
|---|---|---|---|
| `SETUP.md`, `README.md`, `bootstrap.sh` | This setup guide, the front page, and the setup script | Owner | Edit directly |
| `arena-session-3b2d329a/` | Session memory: logs, state pointer, memory, git hook | Created by `bootstrap.sh` | `bash bootstrap.sh` (never overwrites) |
| `skills/study-<level>-<subject>/` (80) and `skills/study-method-*` (8) | Agent Skills for studying: subject coaches for 5 levels × 16 subjects, plus 8 study methods | Owner (original) | `python3 arena-session-3b2d329a/artifacts/build_study_skills.py`. Edit the generator, not the output. |
| `skills/README.md` | Index of the study skills and the security skill | Generated | Same generator |
| `skills/agent-skill-security-audit/` | Scanner (`scripts/scan_skill.py`) and an audit skill for checking third-party skills | Owner (original) | Edit directly |
| `security/redteam-eval/` | 29 canary-only prompt-injection cases, the runner, and a results log | Owner (original) | `python3 security/redteam-eval/build_cases.py`; runner: `run_eval.py` |
| `third_party/ecc/` | ECC v2.2.3 (`affaan-m/ECC` at `b92f181`), MIT, unmodified | Upstream | Do not edit. See `third_party/ecc/NOTICE.md` for how to update. |
| `.claude/` | ECC activated for this repo: skills, agents, commands, rules, scripts, and `settings.json` with the hooks | Generated by the ECC installer | `bash bootstrap.sh --activate`, or the installer (§8) |
| `CREDITS.md` | Every external source, its licence, and how it was used | Owner | Add a row in the same commit as any new source |
| `logs/` (in the session folder) | The append-only work log (`0001`–`0005` and onwards) | Agent | §3 |

What is **not** in the repo: `node_modules`, `~/.claude/` (ECC's per-user state, such as `~/.claude/ecc/state.db`). The `.claude/` folder is in the repo, so the hooks travel with it.

---

## §8 — Setup and activation, step by step

Run these from the repository root. Each step is safe to repeat.

```bash
# 1. Session environment and the git hook (no flags, no hooks are switched on)
bash bootstrap.sh

# 2. Activate ECC for this repo: skills, agents, commands, rules, and hooks in .claude/
bash bootstrap.sh --activate

# 3. Check the activation
python3 -c "import json; json.load(open('.claude/settings.json')); print('settings.json ok')"
ls .claude/ecc/install-state.json

# 4. Start a NEW Claude Code session in this repo. Hooks load when a session starts.
```

**Preview without writing anything** (ECC):

```bash
node third_party/ecc/scripts/install-apply.js --target claude-project --profile core --enable-hooks --dry-run
```

**Remove the ECC activation from this repo** (dry run first; it removes only the files listed in `install-state.json`):

```bash
node third_party/ecc/scripts/uninstall.js --target claude-project --dry-run
node third_party/ecc/scripts/uninstall.js --target claude-project
```

**Change the profile or turn hooks off:** run the installer manually with the other flags (`--profile full`, or `--no-hooks` to skip the hook runtime). Check with `--dry-run` first. The installer tracks what it wrote in `install-state.json`.

**Rebuild the study skills:**

```bash
python3 arena-session-3b2d329a/artifacts/build_study_skills.py
```

**Audit a skill folder before you trust it:**

```bash
python3 skills/agent-skill-security-audit/scripts/scan_skill.py <skill-folder>
python3 skills/agent-skill-security-audit/scripts/scan_skill.py skills/ --exclude scan_skill.py   # the study library scans clean
```

**Red-team harness:**

```bash
cd security/redteam-eval
python3 run_eval.py --demo vulnerable                       # harness self-test (about 90%)
python3 run_eval.py --agent-cmd "<your agent command>" --fail-above 0.05
```

**Update ECC** (only from an official source; see the warning in ECC's README):

1. Clone the new commit to a scratch folder, then `git archive <sha> | tar -x -C third_party/ecc` (delete the old copy first, in the same commit).
2. Update the commit, version and date in `third_party/ecc/NOTICE.md` and `CREDITS.md`.
3. Scan the copy: `python3 skills/agent-skill-security-audit/scripts/scan_skill.py third_party/ecc`. Read the hook scripts' diff before you accept it.
4. Re-run the installer (step 2 above, or the manual command) and check the dry run first.

**Rollback everything ECC added:** run the uninstall above, then `rm -rf third_party/ecc` and commit.

**Troubleshooting**

| Symptom | Fix |
|---|---|
| `--activate` says Node is missing | Install Node.js 18+ and re-run |
| `third_party/ecc is missing` | `git checkout arena/732d199a-aidata -- third_party/ecc` |
| Hooks don't run in Claude Code | Start a new session; check `.claude/settings.json` parses |
| A hook blocks a command you need | Read the reason it prints; re-run the uninstall or the installer with `--no-hooks` if you have decided to turn hooks off |
| `git push` rejected | Run `git fetch`, then re-base your local commits on the remote tip (`git rebase origin/<branch>`). Never force-push. |

---

## §9 — Working agreement for agents

This section applies to every agent that works in this repository. The owner asked for it directly: answer everything, act on requests as they are typed, and stay easy to work with.

1. **Answer every question.** Typos, shorthand, half-sentences and mixed languages (English, Hindi, Hinglish) are normal. Work out the most likely meaning, state the assumption in one line, then act on it.
2. **Do the requested work.** If the request is clear enough to act on, do it. Then log it as §3 says (a `logs/NNNN` entry, `SESSION_STATE.md`, a commit, and a push).
3. **Ask only when it matters.** Ask one short question, with options, when the target is ambiguous and a wrong guess would be costly: deleting or overwriting files, force-pushes, changes outside this repository, anything that runs code on the owner's machine, or anything that touches credentials.
4. **Limits that always apply.** No secrets in the repository. No content that gives real-world harm (for example, working malware, or attack payloads aimed at real systems). No changes to other people's systems. Do not bypass confirmations the owner has set up. When a request hits one of these limits, say which one in one sentence and offer the closest safe alternative.
5. **Third-party code** keeps its licence and its credit (§4). Vendored code is not edited in place; changes go in your own folders.
6. **Real time.** One step is one log entry, one commit, one push. Never batch work for later.

---

<div align="center">

**One file to read, one command to run, everything else is created.**

</div>
