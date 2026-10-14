# LOG-0004 — Security half: agent-skill audit skill + canary red-team eval, CREDITS.md
| Field | Value |
|---|---|
| id | `0004` |
| ts_utc | 2026-10-14T22:00Z |
| phase | P1 — build |
| status | ✅ done |

## Task
Part of LOG-0002: "search for jailbreak Agent skills deepend processing". Scope the user chose: **red-team eval set** (for testing the owner's own agents).

## Plan
1. `skills/agent-skill-security-audit/` — a scanner (`scripts/scan_skill.py`) and SKILL.md that tells an agent how to audit a skill.
2. `security/redteam-eval/` — 29 canary-only cases (`build_cases.py` → `cases.jsonl`), a runner (`run_eval.py`), a README.
3. Test both with fixtures in /tmp (kept out of the repo) and with stand-in agents.
4. `CREDITS.md` for every external source read.

## Safety boundary (applied)
- Every injected instruction asks for a harmless canary token (`CANARY-<id>`). No code to run, no credentials, no real outbound targets.
- The scanner's patterns are for detection. Snippets redact secret values.

## Commands run (verbatim)
```
python3 skills/agent-skill-security-audit/scripts/scan_skill.py /tmp/fx/evil        # planted bad skill
  → 14 findings (4 critical, 8 high, 1 medium, 1 low); exit 1
python3 skills/agent-skill-security-audit/scripts/scan_skill.py /tmp/fx/clean       # clean skill
  → no findings; exit 0
python3 skills/agent-skill-security-audit/scripts/scan_skill.py skills/ --exclude scan_skill.py --exclude SKILL.md
  → 0 findings for the 88 study skills (after the library scan)
python3 security/redteam-eval/build_cases.py          → wrote 29 cases
python3 security/redteam-eval/run_eval.py --demo vulnerable   → 26/29 (89.7%) succeeded
python3 security/redteam-eval/run_eval.py --demo safe         → 0/29 (0.0%)
python3 security/redteam-eval/run_eval.py --demo vulnerable --fail-above 0.1   → exit 1
python3 security/redteam-eval/run_eval.py --agent-cmd "exit 3"                 → 29 errors, not scored
```

## Results
- Scanner works on planted fixtures (critical/high rules fire on the right lines) and stays quiet on a clean skill.
- Self-scan of the audit skill reports 17 items. Expected: the skill quotes the patterns it detects. The docs now say so.
- Red-team harness: the vulnerable stand-in misses the base64 and zero-width cases, since it cannot decode or see through them. This is a limit of the stand-in, not of the cases. The README says so.
- Bugs found and fixed during testing:
  1. `redact()` hid ordinary quoted code. Narrowed it to secret values only.
  2. A `| tail` pipe hid a non-zero exit code during testing. Re-ran without the pipe.
  3. Study-library scan failed because the scanner's own source matched. Added `--exclude`.

## Decisions
- Canary-only design: the user asked for a "jailbreak" set. Attacks that produce harmful content would be uplift, so only a detectable canary is used.
- `--with-data-hint` lets the owner test a mitigation. The default is the realistic baseline with no hint.
- Results are recorded in the README table, not as raw `results.json` (large replies stay out of Git).

## Next
- Commit and push. Then final state update and summary to the user.
