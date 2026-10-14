# LOG-0013 — Main README written: build + start guide for the whole system

| Field | Value |
|---|---|
| id | `0013` |
| ts_utc | 2026-10-14T21:30Z |
| phase | P9 — documentation |
| status | ✅ done |
| commit | _(this commit)_ |

## Task

User: *"put the setup thing in the main file — how to build it nicely, how to start
system"*.

## Done

Root `README.md` replaced (was a 9-byte stub `# AIDATA`) with the main entry point for the
repository:

1. **Overview table** — the three parts of the repo (library, memory system, docs) with
   links.
2. **Quick start (30 seconds)** — clone → `hooks/install.sh` → read `SESSION_STATE.md` →
   browse `PROJECTS.md`. States explicitly that there are no dependencies or build steps.
3. **How the system is built** — annotated tree of `arena-session-3b2d329a/` with the
   design rules (append-only logs, single resume pointer, verbatim commands, failures
   logged), plus the `python-projects/` layout and the own-work vs. credited-collection
   distinction.
4. **How to start the system** — three tracks:
   - A: activate the hook + the working loop + command usage (Claude Code / other agents /
     human runbook),
   - B: disconnect recovery commands + link to the drill,
   - C: running the Python lessons.
5. **Full documentation table** — every important file with a one-line description.

Design: centred header with badges, emoji section markers, tables, code blocks — consistent
with `python-projects/README.md`.

## Decisions

- Put the *activation* steps (one command) before the *description* of the internals: the
  README is meant to be usable, not just readable.
- Kept the credit statement for `collections/` visible in the main README (one line + link)
  — it is a fact about the repo, not fine print.

## Next

- Push and verify the rendered README on GitHub.
