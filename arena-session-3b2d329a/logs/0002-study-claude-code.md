# LOG-0002 — Studying `anthropics/claude-code` and adapting its nature

| Field | Value |
|---|---|
| id | `0002` |
| ts_utc | 2026-10-14T16:33Z → 16:35Z |
| phase | P1 — Claude Code study |
| status | ✅ done |
| commit | _(this commit)_ |

## Task

User request: *"do make yourself work entirely as [github.com/anthropics/claude-code] —
adapt its nature and sense, all its features and working — pushed here."* Plus: study it
**first**, before the audit task.

## Plan

1. Fetch the repo's own metadata, README, CLAUDE.md, its `.claude/` commands, its plugin
   structure (`plugins/*`), hook examples, and the CHANGELOG for the current feature set.
2. Extract the *working model* (not just the features): memory file, todo tracking, plan
   mode, slash commands, subagents, skills, hooks, transcripts/resume.
3. Materialise that model inside `arena-session-3b2d329a/`.
4. Document the mapping in `notes/claude-code-study.md` with evidence links.

## Commands run (verbatim)

```bash
gh api repos/anthropics/claude-code --jq '{stars:.stargazers_count,created:.created_at,pushed:.pushed_at}'
gh api "repos/anthropics/claude-code/git/trees/HEAD" --jq '.tree[] | "\(.type)\t\(.size // 0)\t\(.path)"'
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/README.md
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/CLAUDE.md
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/CHANGELOG.md | head -120
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/.claude/commands/commit-push-pr.md
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/plugins/README.md
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/plugins/code-review/.claude-plugin/plugin.json
gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-code/contents/examples/hooks/bash_command_validator_example.py
```

## Results

Raw findings (with quotes) are in `notes/claude-code-study.md`. Key facts observed:

- Repo: **150,806 stars**, created 2025-02-22, **pushed 2026-10-14** (active daily);
  top level = `CLAUDE.md`, `plugins/`, `examples/` (hooks, settings, MDM, gateway),
  `.claude/commands/`, `.claude-plugin/marketplace.json`, `CHANGELOG.md` (1.0 MB, ~v2.1.299).
- Its `CLAUDE.md` = **a memory/instruction file for agents**, kept short and imperative
  ("Keep each workflow's `permissions:` block minimal...").
- Plugin anatomy (their README): `.claude-plugin/plugin.json` + optional `commands/`,
  `agents/`, `skills/`, `hooks/`, `.mcp.json`, `README.md`.
- Commands = Markdown + YAML frontmatter (`description`, `allowed-tools`) with inline
  shell context executed via `` !`cmd` `` blocks and a `## Your task` section.
- Hooks = JSON event bindings (`SessionStart`, `PreToolUse`, `Stop`, ...) → scripts that
  read JSON on stdin; **exit 0 pass / 2 block with feedback**.
- Changelog shows the product's working model: sessions + **resume**, transcripts,
  context compaction, todos, plan mode, subagents, skills, permissions, scheduled tasks,
  background sessions, worktrees. Everything is *stateful and resumable by design*.

## Adaptation implemented (mapping)

| Claude Code concept | Implementation here |
|---|---|
| `CLAUDE.md` memory file | `CLAUDE.md` — rules + environment facts for any agent |
| Session resume / transcript | `SESSION_STATE.md` + append-only `logs/000N-*.md` + `logs/INDEX.md` |
| Todo tracking | `TASKS.json` (+ `PLAN.md` phases) |
| Slash commands | `commands/*.md` (same frontmatter + `!`cmd`` + `## Your task` shape) |
| Subagents | `agents/*.md` (memory-keeper, repo-auditor, license-auditor) |
| Skills | `skills/session-memory/SKILL.md` + `references/` |
| Hooks | `hooks/hooks.json`, `hooks/pre_commit_log.py`, `hooks/install.sh` |
| Plugin manifest | `.claude-plugin/plugin.json` (metadata describing this folder) |
| Plan mode | `PLAN.md` (phases, statuses) |

## Decisions

- Mirror the **formats** (frontmatter, hook exit codes, plugin layout) but keep the content
  honest: this folder is a *memory system for this session*, not a claim to be Claude Code.
- Log entries must include **verbatim commands** — that is the part that makes a resume
  actually possible.

## Next

- LOG-0003: Python-repo audit — inventory, upstream mapping, full blob-hash diff.
