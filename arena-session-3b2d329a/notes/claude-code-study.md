# Study — `anthropics/claude-code`, and how its nature was adapted here

Researched 2026-10-14 (UTC) via GitHub API. Everything below is evidence-backed; the
commands used are in `../logs/0002-study-claude-code.md`.

## 1. What the repo is

- **Description (their words):** "Claude Code is an agentic coding tool that lives in your
  terminal, understands your codebase, and helps you code faster by executing routine
  tasks, explaining complex code, and handling git workflows — all through natural language
  commands."
- 150,806 stars · created 2025-02-22 · last push 2026-10-14T13:25Z · `CHANGELOG.md` at
  v2.1.299 (1.0 MB of history — they ship constantly).
- Layout: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `plugins/`, `examples/`, `scripts/`,
  `.claude/`, `.claude-plugin/`, `mods/`, `feed.xml`.

## 2. Its working model (the "nature" to adapt)

| # | Concept | Evidence | What it means operationally |
|---|---------|----------|------------------------------|
| 1 | **Memory file** | `CLAUDE.md` (2.2 KB) — imperatives for agents, e.g. "Do not skip or weaken the check." | A short, always-read file that constrains agent behaviour in the repo. |
| 2 | **Session + resume** | CHANGELOG: "`claude --resume`", "resuming a conversation", idle compaction, transcripts | Work is a *session* whose state survives restarts. |
| 3 | **Todos / plan mode** | CHANGELOG mentions plan mode, background sessions, scheduled tasks | Planning is a first-class artefact. |
| 4 | **Slash commands** | `.claude/commands/commit-push-pr.md`: frontmatter `allowed-tools`, `description`; inline `` !`git status` `` context; `## Your task` steps | Commands are small Markdown programs with declared tools. |
| 5 | **Subagents** | `plugins/code-review/agents/*`: "5 parallel Sonnet agents for CLAUDE.md compliance, bug detection, historical context..." | Specialised agents, each with a narrow job. |
| 6 | **Skills** | `plugins/*/skills/<name>/SKILL.md` + `references/` | Auto-invoked know-how, with reference files. |
| 7 | **Hooks** | `examples/hooks/bash_command_validator_example.py`: reads JSON on stdin for `PreToolUse`; **exit 2 blocks** and feeds stderr back | Deterministic guardrails around the model, not prompts. |
| 8 | **Plugin anatomy** | `plugins/README.md`: `.claude-plugin/plugin.json` → `commands/` · `agents/` · `skills/` · `hooks/` · `.mcp.json` · `README.md` | A standard, boring, discoverable folder shape. |
| 9 | **Permissions** | README/CLAUDE.md: `--permission-mode auto`, allow-lists, egress firewall | Safety is config, reviewed like code. |
| 10 | **Git-native workflow** | `commit-push-pr.md`: status → commit → push → PR in one shot | The repo *is* the state store. |

## 3. Adaptation into this session folder

The same shapes, filled with this session's reality:

```
arena-session-3b2d329a/
├── .claude-plugin/plugin.json      # manifest (mirrors Claude Code layout)
├── CLAUDE.md                       # [1] memory file: rules + env facts
├── SESSION_STATE.md                # [2] resume pointer (what/now/next/blocked)
├── PLAN.md                         # [3] plan mode, phase statuses
├── TASKS.json                      # [3] machine-readable todos
├── commands/                       # [4] /resume /status /log /audit-python-repo /commit-memory
├── agents/                         # [5] memory-keeper · repo-auditor · license-auditor
├── skills/session-memory/          # [6] SKILL.md + references/{logging-format,recovery}.md
├── hooks/                          # [7] hooks.json + pre_commit_log.py (+installer)
├── logs/                           # [2] append-only transcript: 000N-slug.md + INDEX.md
├── memory/MEMORY.md                # [1] condensed long-term memory
├── notes/                          # reasoning, decisions
├── artifacts/                      # general deliverables
└── audit/                          # the Python-repo audit deliverables
```

## 4. Honest caveats

- This folder cannot *be* Claude Code: it has no runtime, no tool-permission system, no
  model. What is adapted is **the discipline**: memory file, plan, todos, commands,
  subagents, skills, hooks, real-time Git state.
- The `hooks/hooks.json` file is a faithful-shaped config, but it only *executes* if an
  agent runtime that understands it is driving the folder. What is guaranteed to execute
  today is `hooks/install.sh` → a real **git pre-commit hook** that appends every commit to
  `logs/auto-commit-log.md`.
- Verified sources: `README.md`, `CLAUDE.md`, `CHANGELOG.md` (head), `.claude/commands/`,
  `plugins/README.md`, hook example — all fetched 2026-10-14 and quoted in
  `../logs/0002-study-claude-code.md`.
