# 🐍 python-projects

A curated Python library: **my own learning notes** plus **two community collections of
small projects**, kept here with full credit to their authors.

> **Who wrote what**
> - `python-learning/` → **me** (Adarsh). My own lessons, notes and practice challenges.
> - `collections/` → **other people's work**. Two open-source collections, kept complete,
>   each with its upstream `LICENSE` file inside the folder. See [CREDITS.md](./CREDITS.md)
>   and the project index in [PROJECTS.md](./PROJECTS.md).

---

## 📁 Structure

```
python-projects/
├── README.md                                  ← this file
├── CREDITS.md                                 ← who wrote what, licenses, sources
├── PROJECTS.md                                ← all 183 projects by category, one line each
├── python-learning/                           ← my own work (54 files)
│   ├── 00_ROADMAP.md
│   ├── 01_hello_world.py … 50_sqlite3_basics.py
│   ├── PYTHON_CHEATSHEET.md
│   └── PRACTICE_CHALLENGES.md
└── collections/
    ├── README.md                              ← index: categories + counts
    ├── python-mini-project/                   ← ndleah/python-mini-project (MIT)
    │   ├── LICENSE · CODE_OF_CONDUCT.md · SOURCE.md
    │   └── … 131 project folders (complete)
    └── all-in-one-python-projects/            ← king04aman/All-In-One-Python-Projects (MIT)
        ├── LICENSE · CODE_OF_CONDUCT.md · CONTRIBUTING.md · SOURCE.md
        └── … 65 project folders (complete)
```

**860 files · ~190 MB** · every file from both collections is included — videos, PDFs,
notebooks, datasets, images, `.github/` templates, `CODE_OF_CONDUCT.md` and the
`CONTRIBUTING.md` guides. Nothing was skipped or dropped.

---

## 🚀 Run anything

```bash
git clone https://github.com/Adarshukumar/AIDATA.git
cd AIDATA/python-projects

# my own lessons — no dependencies, Python 3 only
python python-learning/01_hello_world.py

# a collection project — read its own README/requirements first
cd collections/python-mini-project/Caesar_Cipher
pip install -r requirements.txt 2>/dev/null; python *.py
```

---

## 📦 What's inside the collections

| Collection | Projects | Written by | License |
|---|---:|---|---|
| [`python-mini-project`](./collections/python-mini-project) | **131** | [@ndleah](https://github.com/ndleah) + 100 contributors | MIT |
| [`all-in-one-python-projects`](./collections/all-in-one-python-projects) | **65** | [@king04aman](https://github.com/king04aman) + contributors | MIT |

Nothing here was renamed, rewritten or re-attributed. The only things not copied are
machine-generated junk (bytecode `__pycache__`/`*.pyc`, macOS `.DS_Store`, notebook
checkpoints) — every real file, including all media and data, is present. Each collection
keeps its original `LICENSE`, `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md`, plus a `SOURCE.md`
pointing at the upstream repository.

## 🚫 What is *not* here (and why)

Extremely popular or unlicensed projects are deliberately **not** copied here — use the
originals:

| Project | Stars | Why not copied |
|---|---:|---|
| [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) | 225k | use the original |
| [vinta/awesome-python](https://github.com/vinta/awesome-python) | 327k | use the original |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 553k | no license upstream |
| [practical-tutorials/project-based-learning](https://github.com/practical-tutorials/project-based-learning) | 287k | use the original |
| [MunGell/awesome-for-beginners](https://github.com/MunGell/awesome-for-beginners) | 90k | no license upstream |
| [asabeneh/30-Days-Of-Python](https://github.com/asabeneh/30-Days-Of-Python) | 76k | no license upstream |
| [jakevdp/PythonDataScienceHandbook](https://github.com/jakevdp/PythonDataScienceHandbook) | 50k | use the original |
| [gto76/python-cheatsheet](https://github.com/gto76/python-cheatsheet) | 39k | no license upstream |
| [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) | 32k | use the original |
| [satwikkansal/wtfpython](https://github.com/satwikkansal/wtfpython) | 37k | use the original |

---

## 🎯 Why this folder exists

I'm learning Python. The fastest way is to read a lot of small, complete programs — then
write my own. So this folder is: **notes I wrote myself** + **a shelf of other people's
projects to learn from**, with the credit kept exactly where it belongs.

If a project here helps you, go star the original repository. The authors earned it.

— Adarsh 🐍
