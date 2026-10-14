# LOG-0001 — Environment reset and bootstrap

| Field | Value |
|---|---|
| id | `0001` |
| ts_utc | 2026-10-14T21:02Z |
| phase | P0 — environment |
| status | ✅ done |
| commit | _(this commit)_ |

## Task

User: *"i want u to delete this entire work we have done and put the SETUP.md file to setup
our entire environment of this"* — i.e. wipe the accumulated session work, and make
`SETUP.md` the single file from which the whole working environment is set up, then set it
up.

## Plan

1. Rewrite `arena-session-3b2d329a/SETUP.md` as the self-contained setup file:
   the setup prompt verbatim, a line-by-line table of what it requires, the environment
   spec, the working loop, the standing repository facts, recovery, and a history map.
2. Add `bootstrap.sh` — the executable that materialises the environment (tree + starter
   files + git hook), idempotent, never overwriting existing state.
3. Delete the accumulated work: all previous files in this folder except `SETUP.md`.
4. Run the bootstrap → fresh environment.
5. Log the reset (this entry), update state and the index, commit and push.

## Commands run (verbatim)

```bash
git log --oneline -8
git ls-files arena-session-3b2d329a | grep -vE 'SETUP\.md$' | wc -l        # 65 files
git ls-files arena-session-3b2d329a | grep -vE 'arena-session-3b2d329a/(SETUP\.md|bootstrap\.sh)$' \
  | xargs -r git rm -q --ignore-unmatch
rm -rf arena-session-3b2d329a/.claude-plugin
chmod +x arena-session-3b2d329a/bootstrap.sh
bash arena-session-3b2d329a/bootstrap.sh
```

## Results

- **65 tracked files removed** from `arena-session-3b2d329a/` — the 14 log entries, the
  audit deliverables, the curation package, commands/agents/skills/hooks implementations,
  the README/CLAUDE/PLAN/TASKS/STATE files and the plugin manifest.
- **`SETUP.md` rewritten** (11.6 KB): prompt verbatim + requirement table, environment spec
  and design rules, one-command bootstrap, "how to work in it" (arrival checklist, the loop,
  log template, the 8 rules, command usage), standing repository facts, recovery procedure,
  and a history map of where the removed work lives in Git.
- **`bootstrap.sh` added** (10.1 KB), ran cleanly: 14 files created, 0 overwritten,
  git pre-commit hook installed.
- The environment in the folder is now fresh: `CLAUDE.md`, `SESSION_STATE.md`, `TASKS.json`
  (empty task list), `logs/INDEX.md`, `memory/MEMORY.md`, and `commands/ agents/ skills/
  notes/ artifacts/ audit/ hooks/` with their hint files.

## Decisions

- **Nothing is actually lost:** the removed work remains in Git history and is reachable
  with the recovery commands now recorded in `SETUP.md` §5 and the history map in §6
  (audit → `e18e1d3`, curation → `6e70b0c`, index generator → `56e0a44`, complete pre-reset
  folder → `9d94765`).
- `bootstrap.sh` **never overwrites existing state** — the same command refreshes the hook
  after a sandbox restart without disturbing logs or state.
- `python-projects/` was **left untouched** by this reset: it is the library the user asked
  to build, not session work. It stays unless the user asks for its removal.

## Next

- Continue with the user's next instruction; log every step as `logs/0002-…`.
