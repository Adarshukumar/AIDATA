# arena-session-3b2d329a — Persistent Work Memory

> **What this is:** the durable, in-repo memory + work-log of an Arena Agent Mode session
> (session id `3b2d329a`) working on the repo `Adarshukumar/AIDATA`, branch
> `arena/3b2d329a-aidata`.
>
> **Why it exists:** if the session disconnects, runs out of context, or is resumed later,
> *everything* needed to continue lives in Git — no external memory required. Every command,
> plan, decision, result and artifact is committed here in real time.

---

## 🧭 How to resume after a disconnect (3 steps)

```bash
git fetch origin && git checkout arena/3b2d329a-aidata && git pull

cat arena-session-3b2d329a/SESSION_STATE.md     # 1. live state: what was last done, what's next
cat arena-session-3b2d329a/CLAUDE.md            # 2. rules an agent must follow in this folder
ls   arena-session-3b2d329a/logs/ | tail -5     # 3. last log entries = exact commands + results
```

Then read `TASKS.json` for machine-readable task status, and `PLAN.md` for the full plan.

---

## 📁 Structure

| Path | Purpose |
|------|---------|
| `SESSION_STATE.md` | **Live state.** Last action, next action, open questions. Updated every commit. |
| `CLAUDE.md` | Memory/instruction file for any agent (or human) working here. |
| `PLAN.md` | The plan, split into phases with status. |
| `TASKS.json` | Machine-readable task list (todo / in_progress / blocked / done). |
| `logs/` | **Real-time work log** — one file per entry: task, commands run, results, decisions, next. |
| `notes/` | Findings & reasoning (e.g. study of Claude Code, decisions log). |
| `memory/MEMORY.md` | Condensed long-term memory: all facts learned, so far. |
| `commands/` | Slash-command definitions (Claude Code format: YAML frontmatter + prompt body). |
| `agents/` | Subagent definitions (Claude Code format) used by this session. |
| `skills/session-memory/` | Skill describing the memory discipline + references. |
| `hooks/` | Hook scripts + installer (git pre-commit auto-logger). |
| `artifacts/` | Deliverables produced by this session (reports, datasets). |
| `audit/` | Deliverable: full copy-vs-original audit of `Adarshukumar/Python`. |

Conventions (folder layout, frontmatter, hooks, logs) are **adapted from
[anthropics/claude-code](https://github.com/anthropics/claude-code)** — see
`notes/claude-code-study.md`.

---

## ⚡ Rules of this folder (short version)

1. **Log first, act second, commit immediately.** Nothing happens without a log entry.
2. **One log entry per logical step**, numbered `NNNN-slug.md`, never renumbered.
3. **Commit + push after every entry.** Real time — never batch for later.
4. **`SESSION_STATE.md` is updated in the same commit** as the log entry it describes.
5. **Secrets never go here** (no tokens, no keys, no credentials — paths and names only).

---

*Maintained by the Arena Agent Mode session on branch `arena/3b2d329a-aidata`.*
