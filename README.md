<div align="center">

# 🐍 AIDATA

### My Python library — plus the setup file that builds the working environment

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Branch](https://img.shields.io/badge/branch-arena%2F3b2d329a--aidata-blueviolet?style=for-the-badge)

</div>

---

## 📚 `python-projects/` — the library

| | What it is | Count |
|---|---|---|
| 🎓 | **My own lessons** — roadmap, numbered lesson files, cheatsheet, practice challenges | 54 files |
| 🧩 | **Community collection** — [ndleah/python-mini-project](https://github.com/ndleah/python-mini-project) · MIT | 131 projects |
| 📦 | **Community collection** — [king04aman/All-In-One-Python-Projects](https://github.com/king04aman/All-In-One-Python-Projects) · MIT | 65 projects |

- **Index of everything:** [`python-projects/PROJECTS.md`](./python-projects/PROJECTS.md) — all 183 projects, grouped in 9 categories
- **Who wrote what:** [`python-projects/CREDITS.md`](./python-projects/CREDITS.md) — every folder → upstream repo → license → authors
- The two collections are **other people's work**, kept complete with their license files; my own files are [`python-projects/python-learning/`](./python-projects/python-learning)

```bash
python python-projects/python-learning/01_hello_world.py     # my lessons, Python 3 only
```

---

## ⚙️ `arena-session-3b2d329a/` — the working environment

One file sets it up: **[`SETUP.md`](./arena-session-3b2d329a/SETUP.md)** — it contains the
setup prompt verbatim, the rules, the working loop, and the bootstrap command.

```bash
bash arena-session-3b2d329a/bootstrap.sh      # creates/refreshes the environment
cat  arena-session-3b2d329a/SESSION_STATE.md  # read this first after any break
```

`bootstrap.sh` creates the tree and starter files (`CLAUDE.md`, `SESSION_STATE.md`,
`TASKS.json`, `logs/`, `memory/`, `notes/`, `artifacts/`, `commands/`, `agents/`, `skills/`,
`hooks/`) and installs the **git pre-commit hook** that logs every commit automatically. It
never overwrites existing state, so it is safe to re-run any time — that is also the fix
after a sandbox restart, which clears `.git/hooks/`.

| Document | What's inside |
|---|---|
| [`SETUP.md`](./arena-session-3b2d329a/SETUP.md) | The setup prompt, the environment spec, **how to work in it**, recovery, history map |
| [`CLAUDE.md`](./arena-session-3b2d329a/CLAUDE.md) | The rules any agent follows here |
| [`SESSION_STATE.md`](./arena-session-3b2d329a/SESSION_STATE.md) | Live pointer: last done · in progress · next · blocked |
| [`logs/INDEX.md`](./arena-session-3b2d329a/logs/INDEX.md) | Every work-log entry, newest last |

---

## 🚀 Quick start

```bash
git clone https://github.com/Adarshukumar/AIDATA.git
cd AIDATA
bash arena-session-3b2d329a/bootstrap.sh      # 1. set up the environment
cat  arena-session-3b2d329a/SESSION_STATE.md  # 2. see where things stand
cat  python-projects/PROJECTS.md              # 3. browse the library
```

No dependencies, no build step, no server — plain files in Git.

---

<div align="center">

**Everything here is either my own work, or someone else's work with the credit kept.**

*— Adarsh* 🐍

</div>
