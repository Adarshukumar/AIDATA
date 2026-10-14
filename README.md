<div align="center">

# AIDATA

**Everything in this repository is set up by one file.**

</div>

## Start here

```bash
cat  SETUP.md          # the setup prompt, the rules, the working loop, recovery
bash bootstrap.sh      # creates the whole working environment
```

`SETUP.md` contains the setup prompt verbatim, the environment spec, how to work in it, the
standing rules, and the recovery procedure. `bootstrap.sh` builds the environment
(`arena-session-3b2d329a/`: memory, real-time log, state pointer, hooks) and installs a git
hook that logs every commit automatically. Re-running it is safe — it never overwrites
existing state.

## Then

```bash
cat arena-session-3b2d329a/SESSION_STATE.md    # where things stand
ls  arena-session-3b2d329a/logs/               # what happened so far
```

## Contents

| Path | What it is |
|---|---|
| `SETUP.md` | The whole setup: prompt, environment, rules, working loop, recovery, history map, **everything in the repo (§7), step-by-step activation (§8), and the working agreement for agents (§9)** |
| `bootstrap.sh` | Creates / refreshes the environment. `--activate` also installs ECC into `.claude/` |
| `arena-session-3b2d329a/` | The environment (created by `bootstrap.sh`) |
| `skills/` | 88 study skills (5 levels × 16 subjects + 8 methods) and the agent-skill security audit |
| `security/redteam-eval/` | Canary-only prompt-injection test set and runner, for testing your own agents |
| `third_party/ecc/` | ECC v2.2.3 (MIT), vendored unmodified. Notice in `third_party/ecc/NOTICE.md` |
| `.claude/` | ECC activated for this repo (hooks on). Created by `bootstrap.sh --activate` |
| `CREDITS.md` | Every external source and licence |

Earlier work — a project library, an audit, a curation package — is not in the working tree
any more; it is reachable from Git history. The map is in `SETUP.md` §6.
