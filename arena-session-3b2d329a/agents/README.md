# agents/

Role definitions for specialised helpers (markdown + frontmatter: `name`, `description`,
`tools`). Used by convention: an agent adopting a role reads this file first.

Suggested roles: `memory-keeper` (owns `SESSION_STATE.md`/`TASKS.json`/`logs/`),
`repo-auditor` (provenance work — blob-hash comparison), `license-auditor` (per-upstream
license status). Full versions: Git history, `SETUP.md` §6.
