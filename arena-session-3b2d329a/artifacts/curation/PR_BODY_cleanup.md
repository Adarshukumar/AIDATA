# Pull request — curate the collection (attribution + removals)

This PR does three things, all of them about **honesty, legality and usefulness** rather
than about looks:

## 1. Adds `CREDITS.md`

A single file that maps **every folder in the repository to its upstream project**, with
the license and the main authors:

| kept folder | upstream | license |
|---|---|---|
| `algorithms` | keon/algorithms | MIT |
| `CoreySchafer-code-snippets` | CoreyMSchafer/code_snippets | MIT |
| `dive-into-deep-learning` | d2l-ai/d2l-en | CC BY-SA 4.0 |
| `fastbook` | fastai/fastbook | GPL-3.0 (code) |
| `flasky` | miguelgrinberg/flasky | MIT |
| `homemade-machine-learning` | trekhleb/homemade-machine-learning | MIT |
| `learn-python` | trekhleb/learn-python | MIT |
| `micrograd` | karpathy/micrograd | MIT |
| `ml-book-3rd-edition` | rasbt/python-machine-learning-book-3rd-edition | MIT |
| `nlp-tutorial` | graykode/nlp-tutorial | MIT |
| `nn-zero-to-hero` | karpathy/nn-zero-to-hero | MIT |
| `pydata-book` | wesm/pydata-book | MIT (code examples) |
| `python-mini-projects` | Python-World/python-mini-projects | MIT |
| `pytudes` | norvig/pytudes | MIT |
| `spinningup` | openai/spinningup | MIT |
| `tiny-python-projects` | kyclark/tiny_python_projects | MIT |

Every kept folder already retains its upstream `LICENSE` file — that, plus this file, is
the attribution those licenses require.

## 2. Removes 10 folders (3,236 files) for two documented reasons

**No license upstream** — the authors granted no redistribution rights, so these cannot
stay in a public repo:
`30-Days-Of-Python`, `awesome-for-beginners`, `build-your-own-x`, `python-cheatsheet`

**Extremely popular upstreams** — a verbatim copy adds nothing over the link, and these
are the projects everyone already knows:
`TheAlgorithms-Python` (225k ★), `awesome-python` (327k ★),
`project-based-learning` (287k ★), `PythonDataScienceHandbook` (50k ★),
`interactive-coding-challenges` (32k ★), `wtf-python` (37k ★)

All ten are listed with their links in `CREDITS.md`, so nothing is lost.

## 3. Rewrites `README.md`

The old README said *"a mix of my own study notes, hand-written practice code"* and
described the folders as if they were original. The new one states plainly that the
library folders are **other people's projects, credited**, and that the author's own work
is `Python-Learning/`. It also points readers at the upstream repos to star/fork/contribute.

---

**Net effect:** 9,007 files → 5,772; no unlicensed content; no authorship claims over
third-party code; nothing removed without its link recorded. Same learning library, but it
now survives someone checking it.
