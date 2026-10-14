# LOG-0002 — Research + build: agent-skill security eval, and study-skills library
| Field | Value |
|---|---|
| id | `0002` |
| ts_utc | 2026-10-14T21:30Z |
| phase | P1 — research + build |
| status | 🟡 partial (checkpoint: plan) |

## Task
User: "do search for jailbreak Agent skills deepend processing.... and big scale ai agent skill for All type of stuies"

## Plan
1. Web research on (a) agent-skill security (prompt injection, exfiltration, supply chain) and (b) the existing Agent Skills ecosystem. — done
2. Clarify scope with the user. — done. Answers:
   - Jailbreak part: **red-team eval set** (for testing the owner's own agents; detection and evaluation only).
   - Study part: **by education level** (primary, secondary, undergraduate, postgraduate, self-learning).
   - Format: **Agent Skills standard** (`SKILL.md`, `skills/<name>/`).
3. Build `skills/study-<level>-<subject>/SKILL.md` (generated from one data file by a script in `artifacts/`).
4. Build `skills/agent-skill-security-audit/` (a scanner skill) and `security/redteam-eval/` (benign canary-based test cases).
5. Write `CREDITS.md` for every external source used.
6. Log, update state, commit and push at each step.

## Safety boundary (decided here, before building)
- The red-team set contains **no operational harmful content**. Every "attack" uses a harmless canary token
  (e.g. `CANARY-7F3A`) as the thing the injected instruction tries to make an agent output. A pass/fail
  check is whether the agent emitted the canary. No malware, credential theft, weapons or real exfil targets.
- Scope: test your own agents in a sandbox. Not for use against third-party systems.

## Commands run (verbatim)
```
web_search: "Agent Skills SKILL.md collection github study education subjects"
web_search: "jailbreak prompt injection risks in agent skills security research"
```

## Results
- Relevant sources found (see CREDITS.md when written): arXiv 2510.26328 (Agent Skills prompt injection),
  arXiv 2601.10338 (Agent Skills in the Wild, SkillScan), Snyk ToxicSkills study,
  LLMSecurity/awesome-agent-skills-security, arXiv 2608.10906 (GitSkills dataset),
  agentskills.io specification (Apache-2.0).
- Learn Agent Skills (debs-obrien) and Agent-Skills-for-Context-Engineering (muratcankoylan) show the
  SKILL.md layout to copy.

## Decisions
- Asked the user before building, because "jailbreak" can mean building attack tooling. Chose canary-only tests.
- Study skills go in flat `skills/` directories, because the Agent Skills spec discovers flat SKILL.md folders.
- Generator script lives in `artifacts/` so the library can be regenerated with one command.

## Next
- Write `artifacts/build_study_skills.py` and its subject data; generate `skills/study-*`.
