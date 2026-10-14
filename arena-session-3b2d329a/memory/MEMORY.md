# MEMORY.md — condensed long-term memory of session `3b2d329a`

> This is the "if you read only one file" memory. Facts only, newest knowledge included.
> Keep it short — details belong in `logs/` and `notes/`.

**Last updated:** 2026-10-14T16:35Z (see `SESSION_STATE.md` for the live pointer).

## The user and the work

- User: **Adarsh** (GitHub `Adarshukumar`), non-native English speaker, terse messages;
  intent is usually clear even when spelling is not. Asked for: a session folder in
  `AIDATA` that holds *everything* in real time, Claude Code-style, and an audit of his
  Python repo (copied vs. his own files).
- Standing instruction: **commit + push every step, never batch.**

## Repos in play

| Repo | Role | Notes |
|---|---|---|
| `Adarshukumar/AIDATA` | this repo; the "main repository" | branch `arena/3b2d329a-aidata`, base `ca68b43` |
| `Adarshukumar/Python` | **audit target** | 9,007 files, 27 top-level folders, 2 commits (`77b9f07` "Init", `188fd04` "init"), created 2026-10-05, ~398 MB |
| `anthropics/claude-code` | design reference | see `notes/claude-code-study.md` |

## Facts learned about `Adarshukumar/Python` (P3, in progress)

- 27 top-level folders, all vendored third-party OSS collections + 1 own folder
  (`Python-Learning`, 54 files) + root `README.md` + `.gitignore`.
- Blob-hash spot checks (verified via `gh api`, not eyeballed):
  - 8,741 files byte-identical to **live** upstream HEAD; the remaining differing files
    sampled (20/20) were byte-identical to **older upstream revisions** (blob exists in
    upstream object DB).
  - Own content: `Python-Learning/` (54 files, authored "Adarsh"), root `README.md`,
    root `.gitignore`.
- Upstreams with **no license file** (redistribution not permitted by default):
  `asabeneh/30-Days-Of-Python`, `MunGell/awesome-for-beginners`,
  `codecrafters-io/build-your-own-x`, `gto76/python-cheatsheet`.
- Most other sources are MIT (list in `audit/licenses.md`); 22 folder LICENSE files were
  kept when copying.

## Decisions made

1. Folder name: `arena-session-3b2d329a` (session id = branch suffix).
2. Append-only logs, numbered, never rewritten; `SESSION_STATE.md` = resume pointer.
3. Every deliverable lives under this folder, committed in the same step that produces it.

## Environment facts

- Sandbox root `/home/user`; repo `/home/user/AIDATA`; scratch `/tmp` (not persisted).
- Network allow-list: github.com, codeload.github.com, api.github.com, registry.npmjs.org,
  pypi.org, files.pythonhosted.org. `gh` authenticated as `Adarshukumar`.
