# MEMORY.md — condensed long-term memory of session `3b2d329a`

> The "read only one file" memory. Facts only. Details live in `logs/` and `notes/`.
> Live pointer: `SESSION_STATE.md`. Task truth: `TASKS.json`.

**Last updated:** 2026-10-14T17:45Z.

## The user and the work

- User: **Adarsh** (GitHub `Adarshukumar`), terse messages, non-native English; intent is
  clear even when spelling is not. Two asks so far:
  1. Set up a **session memory folder in `Adarshukumar/AIDATA`** that holds everything
     (plans, commands, decisions, results) committed + pushed in **real time**, in a
     Claude Code-style structure, so a disconnect is recoverable.
  2. **Audit `Adarshukumar/Python`**: which files are copied, which are his own — all files.
- Standing instruction: **commit and push every step; never batch.**

## Repos in play

| Repo | Role |
|---|---|
| `Adarshukumar/AIDATA` | the session-memory repo; branch `arena/3b2d329a-aidata` |
| `Adarshukumar/Python` | the audit target |
| `anthropics/claude-code` | design reference for the folder structure |

## FINAL VERDICT — `Adarshukumar/Python` (audit done 2026-10-14)

9,007 files · 27 top-level folders · 2 commits · ~398 MB · created 2026-10-05.

| Class | Files | Share |
|---|---:|---:|
| `COPY_IDENTICAL` (byte-identical to upstream HEAD, same path) | 8,739 | 97.02% |
| `COPY_OLD_REV` (earlier upstream revision, blob proven in upstream DB) | 176 | 1.95% |
| `COPY_LINE_ENDINGS` (upstream CRLF → his LF; else identical) | 33 | 0.37% |
| `COPY_REMOVED_UP` (upstream deleted it later) | 3 | 0.03% |
| `ORIGINAL` (author's own: `Python-Learning/` 54 files + README + .gitignore) | 56 | 0.62% |
| **total** | **9,007** | **100%** — **0 unexplained** |

- All 26 vendored folders map to known upstreams (see `audit/upstream-map.md`).
- The 33 "no-match" files are **not edits**: committed through a Windows `core.autocrlf`
  checkout (stripping `\r` makes them byte-identical).
- Licenses: **RED (no license upstream)** → `30-Days-Of-Python`, `awesome-for-beginners`,
  `build-your-own-x`, `python-cheatsheet`; **AMBER** → d2l-en (CC BY-SA), fastbook (GPL,
  code), awesome-python (CC BY), interactive-coding-challenges (custom),
  pydata-book (MIT for code examples only), wtf-python (WTFPL); the other 20 are MIT-family
  with license text retained.
- Deliverables: `audit/{AUDIT_REPORT,files.csv,originals.md,modified-files.md,licenses.md}`.
- **Pending user decision:** PR with `CREDITS.md` + corrected README, or strip the repo to
  own work only; and whether to remove the 4 unlicensed folders.

## Decisions of record

1. Session folder: `arena-session-3b2d329a/` (session id = branch suffix).
2. Append-only numbered logs + `SESSION_STATE.md` as the single resume pointer.
3. Audit method: **git blob SHA equality only** — no visual/structural guessing. Local
   partial clones (`--filter=blob:none`, trees only) for path→SHA maps; GitHub API blob
   probes for the ~212 ambiguous files, with a 404/200 control test first.
4. Failures are logged as first-class content (`logs/0004`, `notes/lessons.md`).

## Environment facts (for recovery)

- Workspace `/home/user`; repo `/home/user/AIDATA`; `/tmp` is scratch (not snapshotted).
- Network allow-list: github.com, codeload.github.com, api.github.com, registry.npmjs.org,
  pypi.org, files.pythonhosted.org. `gh` CLI authenticated as `Adarshukumar`.
- GitHub API core limit: 5,150/hour — check `gh api rate_limit` before batch work
  (learned the hard way, LOG-0004).

## How to resume

`README.md` → `SESSION_STATE.md` → newest `logs/000N-*.md` → `TASKS.json`. The cold-resume
drill was executed against a fresh clone of the branch (LOG-0006) and passed.
