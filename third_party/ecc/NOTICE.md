# Third-party notice: ECC (Everything Claude Code)

This directory is a **vendored, unmodified copy** of the upstream project. Do not edit files here.
Put repository-specific changes elsewhere (for example `.claude/` or `arena-session-3b2d329a/`).

| Field | Value |
|---|---|
| Project | ECC — "the agent harness performance optimization system" |
| Upstream | https://github.com/affaan-m/ECC (repository name is case-insensitive on GitHub) |
| Commit | `b92f181b3b748d1abbc2afd94af6aa7d8c8fca29` (merge of PR #3520, 12 Oct 2026) |
| Version | `2.2.3` (see `VERSION`) |
| Licence | MIT, © 2026 Affaan Mustafa. Full text in `LICENSE` (unchanged). |
| Copied with | `git archive <commit> | tar -x` (tracked files only, no `.git`, no `node_modules`) |
| Vendored on | 2026-10-14 by LOG-0005 (`arena-session-3b2d329a/logs/0005-add-and-activate-ecc.md`) |

## Activation in this repository

ECC is installed into this repository's `.claude/` folder (project scope, profile `core`, hooks enabled).
The installer was run from a scratch clone of the same commit. See LOG-0005 for the exact command, the
safety review of the hooks, and the trade-offs.

## Updating

Re-vendor from a new upstream commit in one commit, record the new SHA in this file, and re-run the
safety review (`skills/agent-skill-security-audit/scripts/scan_skill.py`).
