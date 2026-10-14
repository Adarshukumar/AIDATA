# Logging format (fixed template)

Filename: `logs/NNNN-slug.md` — `NNNN` zero-padded, monotonic, never reused.
The `logs/INDEX.md` table gets one row per entry.

```markdown
# LOG-NNNN — <short title>

| Field | Value |
|---|---|
| id | `NNNN` |
| ts_utc | YYYY-MM-DDTHH:MMZ → (end) |
| phase | P0…P5 — <name> |
| status | ✅ done / 🟡 partial / ❌ failed / ⛔ blocked |
| commit | <sha or "(this commit)"> |

## Task
What was asked. Quote the user when possible, faithfully.

## Plan
Numbered steps, as intended *before* running them.

## Commands run (verbatim)
```bash
# exact commands, copy-pasteable
```

## Results
Raw numbers/outputs/errors per command. No adjectives where a number will do.

## Decisions
- <decision> — because <reason>; rejected: <alternative>.

## Next
- LOG-NNNN+1: <what happens next>.
```

Rules:

- One logical step per entry. Two unrelated things = two entries.
- Verbatim commands. If a command was long, truncate the *output*, never the command.
- Never edit a published entry. Corrections are new entries that cite the old one.
