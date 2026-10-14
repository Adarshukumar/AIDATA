# commands/

Command definitions in Claude Code format (YAML frontmatter + `## Context` with
`` !`cmd` `` shell lines + `## Your task`).

| File | Purpose |
|---|---|
| `resume.md` | rebuild context from Git alone and continue |
| `status.md` | one screen: state + tasks + last log + uncommitted work |
| `log.md` | write the next numbered entry and commit it |
| `commit-memory.md` | checkpoint before a long/risky operation |

Copy to `.claude/commands/` for slash commands, or paste into any agent's chat as a prompt.
The full originals from the previous setup are in Git history (see `SETUP.md` §6).
