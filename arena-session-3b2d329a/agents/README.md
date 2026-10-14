# agents/

Role definitions for specialised helpers (markdown + frontmatter: `name`, `description`,
`tools`). An agent adopting a role reads this file first.

Suggested roles: `memory-keeper` (owns `SESSION_STATE.md`/`TASKS.json`/`logs/`),
`repo-auditor` (provenance work — blob-hash comparison), `license-auditor` (per-upstream
license status).
