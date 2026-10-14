# LOG-0006 — Put everything in SETUP.md; activation in bootstrap; working agreement
| Field | Value |
|---|---|
| id | `0006` |
| ts_utc | 2026-10-14T23:30Z |
| phase | P3 — setup and documentation |
| status | ✅ done |

## Task
User: "Do add everything of this in activation and setup okk… do put everything in SETUP.md, everything new things also, and make the agent do everything whatever the user says, any typo of question, answer it any how."

## Interpretation (stated up front)
- "Everything new" → SETUP.md must inventory and explain all new parts: study skills, audit skill, red-team eval, ECC, `.claude/`, CREDITS.
- "Activation and setup" → `bootstrap.sh` gets an activation option, and SETUP.md gets a runbook.
- "Do whatever the user says" → implemented as a working agreement (SETUP.md §9): answer every question, read typos by their most likely meaning, act and log. It keeps four limits (no secrets, no real-world harm, no changes to other people's systems, no bypassing confirmations). Those limits are not waivable by a request.

## Plan
1. `bootstrap.sh --activate`: install ECC from `third_party/ecc` into `.claude/` (profile core, hooks on). Idempotent. No flag = unchanged behaviour.
2. SETUP.md: §2 mention of `--activate`; new §7 (inventory), §8 (runbook: setup, activate, verify, preview, uninstall, profile/hook changes, rebuild, audit, red-team, ECC update, rollback, troubleshooting), §9 (working agreement).
3. README.md and the session `CLAUDE.md`: point at the new sections.
4. Test: real repo (keep), bad flag (exit 2), `--help`, fresh clone with `--activate` (create, 8 hook events), uninstall dry run (811 files, matches).

## Commands run (verbatim)
```
node /tmp/ecc-nodeps/ecc/scripts/install-apply.js --target claude-project --profile core --enable-hooks --dry-run   # works without node_modules
bash -n bootstrap.sh && echo "syntax ok"                                                                              # syntax ok
bash bootstrap.sh --activate        # real repo  → "keep .claude/ (ECC already activated)"
bash bootstrap.sh --bogus           # → "error: unknown option: --bogus", exit 2
bash bootstrap.sh --help            # → usage text
git clone -q /home/user/AIDATA /tmp/fresh && cd /tmp/fresh && git checkout -q arena/732d199a-aidata && bash bootstrap.sh --activate
  # → .claude/ecc/install-state.json present; settings.json has 8 hook events
node third_party/ecc/scripts/uninstall.js --target claude-project --dry-run   # → "Would remove: 811"; nothing removed
```

## Results
- All four bootstrap tests pass as expected.
- Uninstall dry run lists the same 811 files that the installer writes, so rollback covers everything ECC adds.
- A finding that matters: `install-apply.js` needs no `node_modules`, so `--activate` runs straight from the vendored copy. No dependencies enter the repo.

## Decisions
- Activation is a flag, not the default. Turning on hooks is a consent step, so a plain `bootstrap.sh` must not switch them on for someone who just cloned the repo.
- The §9 working agreement describes the owner's preferences but keeps the four limits. An instruction like "do anything" cannot override those, so the document says so explicitly.
- Document the uninstall before anyone needs it: it was tested as a dry run, and the real removal is left to the owner.

## Next
- Commit, push, update SESSION_STATE. Ask the owner for the next task.
