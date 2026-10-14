# PLAN.md — what this session is doing

Status legend: ✅ done · 🟡 in progress · ⬜ not started · ⛔ blocked

## P0 — Bootstrap (✅ done)

| # | Task | Status |
|---|------|--------|
| T0.1 | Create `arena-session-3b2d329a/` in `Adarshukumar/AIDATA` | ✅ |
| T0.2 | Memory system: `CLAUDE.md`, `SESSION_STATE.md`, `TASKS.json`, `logs/` | ✅ |
| T0.3 | Claude Code-style layer: `commands/`, `agents/`, `skills/`, `hooks/` | ✅ |

## P1 — Study Claude Code, adapt its nature (✅ done)

| # | Task | Status |
|---|------|--------|
| T1.1 | Fetch + read `anthropics/claude-code` repo: README, CLAUDE.md, plugin format, changelog | ✅ |
| T1.2 | Extract its working model: memory file, todos, slash commands, subagents, hooks, skills, plan mode, transcripts | ✅ |
| T1.3 | Write the adaptation notes → `notes/claude-code-study.md` | ✅ |

## P2 — Guarantee real-time recoverable memory (✅ done, enforced continuously)

| # | Task | Status |
|---|------|--------|
| T2.1 | Rule: log → update state → commit → push, after **every** step | ✅ |
| T2.2 | Hook script + installer so commits auto-append to `logs/auto-commit-log.md` | ✅ |

## P3 — Audit `Adarshukumar/Python`: copied vs original (🟡 in progress)

| # | Task | Status |
|---|------|--------|
| T3.1 | Inventory: tree, sizes, commits, licenses (via `gh api`) | ✅ |
| T3.2 | Map all 27 folders → upstream repos | ✅ |
| T3.3 | Blob-hash diff of all 9,007 files vs upstream HEAD | 🟡 |
| T3.4 | Classify the non-identical files (older revision / removed upstream / edited / original) | ⬜ |
| T3.5 | Deliverables: `AUDIT_REPORT.md`, `files.csv`, `originals.md`, `modified-files.md`, `licenses.md` | ⬜ |
| T3.6 | Third-pass review of files not explained by upstream history | ⬜ |

## P4 — Optional enrichment (⬜)

| # | Task | Status |
|---|------|--------|
| T4.1 | Date-stamp sample of "older upstream revision" files via blobless clones (`--filter=blob:none`) | ⬜ |
| T4.2 | License risk table per folder (MIT retained / unlicensed source) | ⬜ |

## P5 — Memory consolidation (⬜)

| # | Task | Status |
|---|------|--------|
| T5.1 | Rewrite `memory/MEMORY.md` as the single condensed truth | ⬜ |
| T5.2 | Simulate a "cold resume": prove the folder alone rebuilds context | ⬜ |
| T5.3 | Hand-off summary for the user | ⬜ |

---

## Standing instruction from the user (verbatim intent)

> "make sure everything — every command, all tasks, all thinking — is pushed into that
> folder and committed directly, in real time, so that even if we get disconnected we can
> recover our memory."

This is treated as a hard requirement on **every** future step in this session.
