# LOG-0005 — Add and activate ECC (affaan-m/ECC) in this repository
| Field | Value |
|---|---|
| id | `0005` |
| ts_utc | 2026-10-14T22:30Z |
| phase | P2 — third-party integration |
| status | ✅ done (ECC vendored, activated for this repo with hooks; verified) |

## Task
User: "[https://github.com/affaan-m/ecc] Add this … understand this and see this and active this also".

## Understanding (what ECC is)
- Upstream: `affaan-m/ECC` (repo name is case-insensitive on GitHub: `ECC`). MIT licence, © 2026 Affaan Mustafa.
- Commit reviewed: `b92f181` (merge of PR #3520, 12 Oct 2026). VERSION file: `2.2.3`.
- A Claude Code harness plus multi-harness support (Codex, Kimi Code, Cursor, OpenCode and others). Contents:
  613 skills, 71 agents, 97 commands, 122 rule files, hooks, scripts, tests and docs.
- "Activate" = the project-level install into `./.claude/` (target `claude-project`), with the hook runtime enabled.
  The README's global route (`npx ecc-universal@2.2.3 setup`) changes `~/.claude` for every session, so it is not used.

## User decisions (via ask_user)
- How to add: **full copy** (chosen over core subset and reference-only). Expect about 70 MB working tree, 4,615 files.
- How to activate: **this repo, with hooks** (chosen over no-hooks, not-yet, and global).

## Plan
1. Commit the scanner fix on its own (see Results).
2. Copy upstream into `third_party/ecc/` without `.git` and `node_modules`. Keep upstream `LICENSE` in place. Add `third_party/ecc/NOTICE.md` (source, commit, licence).
3. Install from the scratch clone with cwd = this repo: `node /tmp/ecc/scripts/install-apply.js --target claude-project --profile core --enable-hooks`.
   The installer's project root is `process.cwd()`, so the output lands in `AIDATA/.claude/`. No `node_modules` enters the repo.
4. Verify: `.claude/settings.json` has hooks; a hook runs on a benign payload; no writes to `~/.claude`.
5. Commit `.claude/` and push. Note: committed hooks run for anyone who opens this repo with Claude Code and trusts it.

## Safety review (before activation)
Scanner run on `scripts/hooks`, `scripts/lib` and `hooks` (after tightening two rules, see Results):
- Network: only two hooks open sockets. `plan-canvas-pending.js` talks to **loopback only**. `mcp-health-check.js` sends
  GET requests to MCP server URLs from the user's own MCP config (a health check, not a data upload).
- No hook posts data to a fixed external host. External URLs in hooks are doc or help links only.
- `spawnSync`/`execFileSync` calls run fixed local tools (`which`, `tmux`, `osascript`, `pwsh`, the bundled bash scripts).
- Sensitive-path regexes (`id_rsa`, `.env`, `credentials`) in `governance-capture.js` and `gateguard-target-class.js` **detect** such paths. They do not read them.
- Hooks write state under `~/.claude` or `CLAUDE_CONFIG_DIR` (9 files). This is expected for ECC and is noted here.
- Result: no evidence of exfiltration or hidden execution. Residual risk: hooks run on every Bash/Write/Edit call, and this review is not a full audit.

## Commands run (verbatim)
```
git clone -q --depth 1 https://github.com/affaan-m/ECC.git /tmp/ecc      # commit b92f181
bash install.sh --target claude-project --dry-run --profile core          # 810 operations, hook decision required
python3 skills/agent-skill-security-audit/scripts/scan_skill.py scripts/hooks scripts/lib hooks --json
```

## Results
- Dry run (core profile, claude-project): 810 operations into `.claude/` (agents 71, commands 97, rules 122, scripts 284, skills 110, hooks 7, settings 1). Hook decision required (`--enable-hooks` or `--no-hooks`).
- First scanner run on ECC: 382 findings, 332 critical. **Most were false positives from my own rule, which I fixed:**
  1. `reads-secret-files` matched `process.env` (the `\.env` pattern had no word boundary).
  2. `dumps-environment` matched `env || process.env` (the `env\s*\|` pattern matched `||`).
  Both are now tightened, and the tests pass (`process.env.HOME` no longer matches; `env | curl` still matches).
- After the fix: 52 findings (2 critical, 8 high, 39 medium). Each one was reviewed by hand, as above.

## Decisions
- Use the scratch clone as the installer source, not a copy under `third_party/`. This avoids committing `node_modules`, which the upstream installer creates.
- Profile `core`, because the user did not pick one. `full` is available later with `--profile full`.
- Commit `.claude/` so the activation is visible in the repo. The trade-off is that the hooks travel with the repo.

## Results (after install)
- Step 1 `d7e66dd`: scanner fix + checkpoint. Step 2 `f0ad426`: `third_party/ecc/` = `git archive b92f181`, 4,615 files, 70 MB, LICENSE byte-identical to upstream, `NOTICE.md` added.
- Step 3 install: `node /tmp/ecc/scripts/install-apply.js --target claude-project --profile core --enable-hooks`, run with cwd `/home/user/AIDATA`. Dry run and real run both show the root as `/home/user/AIDATA/.claude`. 811 files written. Exit 0.
- `.claude/settings.json` (valid JSON): 27 hook commands on 8 events (PreToolUse 10, Stop 8, SessionStart 2, PostToolUse 2, PostToolUseFailure 2, UserPromptSubmit 1, PreCompact 1, SessionEnd 1). Each command is bound to `/home/user/AIDATA/.claude` via an encoded path.
- Settings change to note: `includeCoAuthoredBy: false` (Claude Code will not add co-author trailers to commits).
- Smoke test (hook command run by hand, with a JSON payload on stdin):
  - benign `ls -la`: exit 0, allowed (stderr: a bootstrap notice about raw input).
  - `rm -rf ~`: denied by the gateguard hook (`permissionDecision: deny`, "Destructive command detected").
- Writes outside the repo: `~/.claude/ecc/state.db` (ECC's state database, created by the hooks). `~/.claude` itself was created at 21:32 and is otherwise empty. Remove it if you don't want ECC state on this machine.
- Secret scan of `.claude/` (137 findings, mostly doc-style examples): no provider tokens, private keys or obfuscated exec.

## Next
- Commit `.claude/` and this log, then push. Recommended follow-up: review `settings.json` and any hook you do not want.

