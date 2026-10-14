# LOG-0003 — Study-skills library (88 Agent Skills)
| Field | Value |
|---|---|
| id | `0003` |
| ts_utc | 2026-10-14T21:45Z |
| phase | P1 — build |
| status | ✅ done |

## Task
Part of LOG-0002: "big scale ai agent skill for All type of stuies", organised by education level.

## Plan
1. Write one generator script with subject data, level data and study-method content. (`artifacts/build_study_skills.py`)
2. Generate `skills/study-<level>-<subject>/SKILL.md` for 5 levels × 16 subjects = 80 coach skills, and `skills/study-method-*` (8 methods).
3. Write `skills/README.md` index. Validate frontmatter (name == folder, description ≤ 1024 chars).

## Commands run (verbatim)
```
python3 arena-session-3b2d329a/artifacts/build_study_skills.py
python3 - <<'PY'   # frontmatter validator: name matches dir, description ≤ 1024 chars
  ...
PY
```

## Results
- `wrote 88 skills to skills/ (+ README.md)`
- Validator: `bad: []` (all 88 have matching `name` and a description under 1024 characters).
- Levels: primary, secondary, undergraduate, postgraduate, self-learning.
- Subjects: mathematics, physics, chemistry, biology, english-literature, history, geography, economics,
  computer-science, statistics, accounting-finance, foreign-languages, psychology, law, arts-design, music-theory.

## Decisions
- Content is original (written by the repository owner), so it is not third-party material. Kept under `skills/`, with the generator under `artifacts/`.
- Topics are ordered foundational → advanced, and each level starts where it needs to. This avoids 80 hand-written topic lists.
- Secondary-level text names the Indian boards and entrance exams (CBSE, ICSE, state boards, JEE/NEET), because the user is in India.
- The generator script is the source of truth. Edit it, then regenerate. Do not hand-edit the generated files.

## Next
- LOG-0004: security half. `skills/agent-skill-security-audit/` (scanner) and `security/redteam-eval/` (canary-only test set). Then `CREDITS.md`.
