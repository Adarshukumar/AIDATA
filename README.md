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
| `SETUP.md` | The whole setup: prompt, environment, rules, working loop, recovery, history map |
| `bootstrap.sh` | Creates / refreshes the environment |
| `arena-session-3b2d329a/` | The environment (created by `bootstrap.sh`) |

Earlier work — a project library, an audit, a curation package — is not in the working tree
any more; it is reachable from Git history. The map is in `SETUP.md` §6.
