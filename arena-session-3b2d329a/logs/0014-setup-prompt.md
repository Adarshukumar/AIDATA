# LOG-0014 — SETUP.md now carries the setup prompt (verbatim) + "how to work in it"

| Field | Value |
|---|---|
| id | `0014` |
| ts_utc | 2026-10-14T21:45Z |
| phase | P9 — documentation |
| status | ✅ done |
| commit | _(this commit)_ |

## Task

User: *"wtf i told u i want the setup file bro … do tell him how to work in it"* — i.e. the
setup file must contain the **prompt that created this folder** and instructions for how to
work inside it.

## Done

`arena-session-3b2d329a/SETUP.md` restructured (14,160 bytes). It now opens with:

- **§0 — The setup prompt (verbatim)** — the user's original instruction, quoted exactly
  (typos preserved), followed by a table mapping **each line of the prompt to how it is
  implemented** in the folder (folder naming, real-time commit loop, disconnect recovery,
  structuring, Claude Code adaptation, per-step logging, phase order, onboarding).
- **§0b — How to work in this folder** — the arrival checklist for a new agent
  (read `CLAUDE.md` → `SESSION_STATE.md` → newest logs → `TASKS.json` → work the loop), the
  loop diagram (do → log → update state → commit → push), the eight non-optional rules
  (real time, verbatim commands, log failures, never rewrite, state never stale, checkpoints
  before risky work, no secrets, post-restart recovery), and how to use `commands/` in
  Claude Code / other agents / by hand.

The previous operational content is unchanged below it: §1 what you get, §2–§6 activation
and the working loop, §7 recovery, §8 runtime hooks, §9 cheat-sheet, §10 troubleshooting,
§11 design rules.

## Decisions

- The prompt is quoted **verbatim**, including spelling — it is a record of the instruction,
  not something to tidy up. The translation into requirements happens in the table beside
  it, so a resumed session sees both the original intent and the current implementation.
- Kept `SETUP.md` as the single setup file instead of adding a second document, so there is
  exactly one place to read on arrival.

## Next

- Push; verify on GitHub. Standing items unchanged (READMEs for the 184 projects offered;
  `Adarshukumar/Python` writes still blocked by the AIDATA-scoped token).
