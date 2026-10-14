# License situation — every upstream repository copied into `Adarshukumar/Python`

Generated 2026-10-14 by session `3b2d329a`. SPDX ids come from the GitHub API
(`GET /repos/{owner}/{repo}` → `.license`); the "license kept in copy" column was checked
offline against the target repo's tree (`git ls-tree`), looking for real
`LICENSE`/`LICENCE`/`COPYING` files at the root of each copied folder.

## Risk summary

| Risk | Meaning | Folders |
|---|---|---|
| 🟢 GREEN | Permissive license (MIT/BSD-like), license text kept inside the copy | 20 |
| 🟡 AMBER | License kept, but has conditions (share-alike / copyleft / custom) that the copy must respect | 6 |
| 🔴 RED | **No license at all** — default copyright, no permission to redistribute | 4 |

## Per folder

| Folder in the copy | Upstream | License | License file inside copy? | Risk |
|---|---|---|---|---|
| `30-Days-Of-Python` | asabeneh/30-Days-Of-Python | **none** | no | 🔴 RED |
| `awesome-for-beginners` | MunGell/awesome-for-beginners | **none** | no | 🔴 RED |
| `build-your-own-x` | codecrafters-io/build-your-own-x | **none** | no | 🔴 RED |
| `python-cheatsheet` | gto76/python-cheatsheet | **none** (repo-level) | no — only two *font* licences under `web/OnlineWebFonts_*` | 🔴 RED |
| `awesome-python` | vinta/awesome-python | CC BY 4.0 (""Other"") | yes — `LICENSE` | 🟡 AMBER — attribution required |
| `dive-into-deep-learning` | d2l-ai/d2l-en | CC BY-SA 4.0 | yes — `LICENSE` (+ `LICENSE-SAMPLECODE`, `LICENSE-SUMMARY`) | 🟡 AMBER — **share-alike** |
| `fastbook` | fastai/fastbook | GPL (code; prose excluded) — "Other" | yes — `LICENSE` | 🟡 AMBER — **copyleft** |
| `interactive-coding-challenges` | donnemartin/interactive-coding-challenges | custom permissive — "Other" | yes — `LICENSE` | 🟡 AMBER — read the text |
| `pydata-book` | wesm/pydata-book | MIT (code examples) — "Other" | yes — `COPYING` | 🟡 AMBER — text says "code examples" only |
| `wtf-python` | satwikkansal/wtfpython | WTFPL | yes — `LICENSE` | 🟡 AMBER — unusual but permissive |
| `TheAlgorithms-Python` | TheAlgorithms/Python | MIT | yes — `LICENSE.md` | 🟢 GREEN |
| `algorithms` | keon/algorithms | MIT | yes — `LICENSE` | 🟢 GREEN |
| `CoreySchafer-code-snippets` | CoreyMSchafer/code_snippets | MIT | yes — `LICENSE.txt` | 🟢 GREEN |
| `flasky` | miguelgrinberg/flasky | MIT | yes — `LICENSE` | 🟢 GREEN |
| `homemade-machine-learning` | trekhleb/homemade-machine-learning | MIT | yes — `LICENSE` | 🟢 GREEN |
| `learn-python` | trekhleb/learn-python | MIT | yes — `LICENSE` | 🟢 GREEN |
| `micrograd` | karpathy/micrograd | MIT | yes — `LICENSE` | 🟢 GREEN |
| `ml-book-3rd-edition` | rasbt/python-machine-learning-book-3rd-edition | MIT | yes — `LICENSE.txt` | 🟢 GREEN |
| `nlp-tutorial` | graykode/nlp-tutorial | MIT | yes — `LICENSE` | 🟢 GREEN |
| `nn-zero-to-hero` | karpathy/nn-zero-to-hero | MIT | yes — `LICENSE` | 🟢 GREEN |
| `project-based-learning` | practical-tutorials/project-based-learning | MIT | yes — `LICENSE.md` | 🟢 GREEN |
| `python-mini-projects` | Python-World/python-mini-projects | MIT | yes — `LICENSE` (+ one inside `projects/Speed_Game`) | 🟢 GREEN |
| `pytudes` | norvig/pytudes | MIT | yes — `LICENSE` | 🟢 GREEN |
| `spinningup` | openai/spinningup | MIT | yes — `LICENSE` | 🟢 GREEN |
| `tiny-python-projects` | kyclark/tiny_python_projects | MIT | yes — `LICENSE` | 🟢 GREEN |
| `PythonDataScienceHandbook` | jakevdp/PythonDataScienceHandbook | MIT (dual LICENSE-CODE / LICENSE-TEXT) | yes — both files | 🟢 GREEN |
| `Python-Learning`, root files | — | the author's own | — | — |

## What this means practically

1. **The four RED folders have no license.** Upstream grants no rights by default, so
   redistributing them inside `Adarshukumar/Python` is not covered by any permission —
   that is the one part of this repo with a real legal problem. Removing them (or writing
   to the authors for permission) is the only clean fix.
2. **The AMBER folders are redistributable but conditional.** GPL code (fastbook) carries
   copyleft duty; CC BY-SA (d2l-en) requires share-alike on derivatives; CC BY
   (awesome-python) requires attribution; "custom" licenses must be read before reuse.
   The copies do keep the license texts, which satisfies the "include the license" part,
   but they do **not** add any attribution to the original authors in the repo READMEs.
3. Attribution in a `CREDITS.md` (folder → upstream → license) would fix point 2 for
   every AMBER/🟢 folder in one file.
