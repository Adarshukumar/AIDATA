# CLAUDE.md — Session Memory & Working Rules

Guidance for **any** agent (Claude, GPT, Gemini, human) working inside
`arena-session-3b2d329a/`. Adapted from Claude Code's `CLAUDE.md` memory-file convention:
this file is read first, it is short on purpose, and it must stay true.

## 0. Context

- **Session:** `3b2d329a` · **Repo:** `Adarshukumar/AIDATA` · **Branch:** `arena/3b2d329a-aidata`
- **Owner of the work:** Adarsh (GitHub `Adarshukumar`)
- **Goal of the session:** keep a complete, real-time, Git-backed memory of everything the
  agent does, so work is recoverable after any disconnect — and execute the tasks the user
  gives, logging them as they happen.

## 1. Non-negotiable rules

1. **Real-time commits.** After every meaningful step (a command batch, a finding, a
   deliverable): write a log entry → update `SESSION_STATE.md` → `git add` → `git commit`
   → `git push origin arena/3b2d329a-aidata`. Never wait for "the end".
2. **Never rewrite history here.** Additive only; log files are append-only and numbered.
3. **Log format is fixed.** Use the template in
   `skills/session-memory/references/logging-format.md`. Include the *verbatim commands*
   that were run and a short raw result, not a summary of a summary.
4. **`SESSION_STATE.md` must always answer:** what was last done, what is happening now,
   what comes next, what is blocked. If it is stale, that is a bug.
5. **`TASKS.json` is the machine-readable truth** for task status; update it with every
   log entry that changes a task's status.
6. **No secrets.** Never write tokens/keys/credentials. GitHub auth is pre-configured in
   the sandbox (`gh` CLI) — reference it, don't dump it.
7. **Cite evidence.** Any claim about code/files must carry the command or API call that
   produced it. Prefer blob-hash comparison over eyeballing.
8. **Stay on this branch.** Push only to `arena/3b2d329a-aidata`.

## 2. Environment facts (for recovery)

- Sandbox workspace root: `/home/user`; this repo: `/home/user/AIDATA`.
- Outbound network is allow-listed to: `github.com`, `codeload.github.com`,
  `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`.
- `gh` CLI is authenticated as **Adarshukumar** (token injected by the platform).
- `git`/`gh` are the tools for all GitHub work: `git` for local, `gh` for API/PRs.
- Working files that must survive must live **inside the repo** — `/tmp` is scratch.

## 3. What "done" means for a task

A task is done only when: (a) its artifact is committed, (b) its log entry exists, (c) its
status in `TASKS.json` is `done`, and (d) `SESSION_STATE.md` points at the next task.

## 4. Style of the work log

Keep entries honest and boring: what was asked, what was tried, what happened, what it
costs (API calls/time), what remains. Failures get logged too — they are the most valuable
part after a disconnect.
