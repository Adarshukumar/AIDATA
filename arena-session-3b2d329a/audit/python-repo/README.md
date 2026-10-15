# Provenance audit: `Adarshukumar/Python`

Audited: `https://github.com/Adarshukumar/Python` (public, not a fork, default branch `main`, two commits, 9,007 files).
Audit date: 2026-10-15 (UTC). Star counts are the values at that date.

## Method

- Every file in the owner's repo was matched by **git blob SHA** against the default branch of each candidate upstream. Identical SHA = byte-identical file. Visual similarity is not used as evidence.
- Candidate upstreams come from the owner's README and from the license headers inside the folders (learn-python, python-mini-projects, tiny-python-projects, CoreySchafer-code-snippets). Those three folders had broken or unknown names at first; the corrected names were confirmed with `gh api repos/<name>` (HTTP 200).
- Script: `artifacts/audit_upstream_clones.py` (writes `summary.csv`, `files.csv`, `unmatched.txt`).
- Second pass: `artifacts/classify_modified.py` fetches the upstream blob for every "modified" file and labels the change (writes `modified.csv`).
- Files: `summary.csv` (per folder), `files.csv` (per file, status and matched upstream), `modified.csv` (the 209 changed files), `unmatched.txt`.

## Result

- **8,741 of 9,007 files (97.0%) are byte-identical to one of 26 upstream repositories.**
- No file matched a *different* folder's upstream (0 cross-matches).
- 8,739 of the exact matches sit at the same relative path inside the folder.
- 266 files are not byte-identical: 209 "modified", 56 with no upstream (the owner's own), 1 added (see below).

## Upstream repositories identified (26)

Share = exact matches / files in the folder. "Other" = files in that folder that are not byte-identical to the upstream.

| Folder in owner's repo | Upstream | Stars | License (GitHub) | Exact / files | Share | Other |
|---|---|---:|---|---:|---:|---|
| build-your-own-x | codecrafters-io/build-your-own-x | 553,304 | none detected; README states CC0 | 4 / 4 | 100% | — |
| project-based-learning | practical-tutorials/project-based-learning | 286,738 | MIT | 13 / 14 | 92.9% | 1 large (link-rot-state.json, 18 lines) |
| awesome-python | vinta/awesome-python | 327,528 | NOASSERTION (LICENSE file present) | 97 / 119 | 81.5% | 18 small, 3 large, 1 added |
| TheAlgorithms-Python | TheAlgorithms/Python | 225,272 | MIT | 1,637 / 1,733 | 94.5% | 78 line-endings, 18 small |
| awesome-for-beginners | MunGell/awesome-for-beginners | 90,279 | none detected; README states CC0 | 10 / 10 | 100% | — |
| 30-Days-Of-Python | Asabeneh/30-Days-Of-Python | 76,246 | none detected; no license stated | 403 / 440 | 91.6% | 37 line-endings |
| wtf-python | satwikkansal/wtfpython | 37,122 | WTFPL | 44 / 44 | 100% | — |
| python-cheatsheet | gto76/python-cheatsheet | 38,699 | none detected | 86 / 92 | 93.5% | 6 line-endings |
| interactive-coding-challenges | donnemartin/interactive-coding-challenges | 31,913 | NOASSERTION (LICENSE file present) | 516 / 516 | 100% | — |
| dive-into-deep-learning | d2l-ai/d2l-en | 29,839 | NOASSERTION (LICENSE, LICENSE-SAMPLECODE, LICENSE-SUMMARY) | 836 / 836 | 100% | — |
| fastbook | fastai/fastbook | 25,387 | NOASSERTION (LICENSE file present) | 488 / 490 | 99.6% | 1 small, 1 line-endings |
| pydata-book | wesm/pydata-book (branch `3rd-edition`) | 25,024 | NOASSERTION (COPYING file present) | 43 / 43 | 100% | — |
| algorithms | keon/algorithms | 25,564 | MIT | 443 / 444 | 99.8% | 1 line-endings |
| homemade-machine-learning | trekhleb/homemade-machine-learning | 24,820 | MIT | 185 / 185 | 100% | — |
| nn-zero-to-hero | karpathy/nn-zero-to-hero | 24,819 | MIT | 9 / 9 | 100% | — |
| pytudes | norvig/pytudes | 24,415 | MIT | 199 / 204 | 97.5% | 1 small, 3 line-endings, 1 large (palsum.ipynb, 522 lines) |
| PythonDataScienceHandbook | jakevdp/PythonDataScienceHandbook | 50,138 | MIT | 264 / 264 | 100% | — |
| micrograd | karpathy/micrograd | 17,911 | MIT | 13 / 13 | 100% | — |
| learn-python | trekhleb/learn-python | 18,381 | MIT | 82 / 82 | 100% | — |
| python-mini-projects | Python-World/python-mini-projects | 19,388 | MIT | 1,422 / 1,448 | 98.2% | 26 line-endings |
| nlp-tutorial | graykode/nlp-tutorial | 14,938 | MIT | 42 / 42 | 100% | — |
| spinningup | openai/spinningup | 12,003 | MIT | 180 / 181 | 99.4% | 1 line-endings |
| CoreySchafer-code-snippets | CoreyMSchafer/code_snippets | 10,611 | MIT (placeholder text, see below) | 954 / 965 | 98.9% | 11 line-endings |
| flasky | miguelgrinberg/flasky | 8,739 | MIT | 85 / 85 | 100% | — |
| ml-book-3rd-edition | rasbt/python-machine-learning-book-3rd-edition | 5,067 | MIT | 371 / 373 | 99.5% | 2 line-endings |
| tiny-python-projects | kyclark/tiny_python_projects | 1,858 | MIT | 315 / 315 | 100% | — |

### Not a copy of any upstream

| Folder | Files | Result |
|---|---:|---|
| Python-Learning | 54 | 0 matches in the 26 upstreams. Owner's own lesson files (`00_ROADMAP.md`, `01_hello_world.py`, ...). Matches the README ("My Python World") and the earlier note that 54 lesson files are the owner's own. |
| (root) | 2 | `README.md` and `.gitignore`. Not matched to any upstream; owner's own. The `.gitignore` was not compared against common templates. |

## What "modified" means (209 files)

These files exist at the same path in the upstream but are not byte-identical. `classify_modified.py` sorted them:

| Class | Files | Meaning |
|---|---:|---|
| `line_endings_only` | 166 | Identical except line endings. The upstream file uses CRLF; the owner's copy uses LF (none of the 166 owner copies contains a CR). This is a conversion, not an edit. |
| `small_edit` | 38 | Up to 10 changed lines. Examples: `TheAlgorithms-Python/sorts/bucket_sort.py` (one line changed in the return statement), `awesome-python/pyproject.toml` (5 lines), `awesome-python/website/build.py` (4 lines). |
| `large_change` | 5 | More than 10 changed lines: `awesome-python/README.md` (19), `awesome-python/uv.lock` (192), `awesome-python/website/static/style.css` (14), `project-based-learning/.github/link-rot-state.json` (18), `pytudes/ipynb/palsum.ipynb` (522). |

Added file: `awesome-python/CONTEXT.md` (no file at that path upstream, and its bytes match no file in any of the 26 upstreams checked).

## Limits of this audit

- Each folder was compared with the **current default branch** of its upstream. A "small_edit" can be the owner's own edit or an older upstream version that has since changed. Telling these apart needs the upstream's history; this audit did not do that.
- Star counts and license values are from the GitHub API on 2026-10-15.
- Only the 26 upstreams above were checked. The 56 unmatched files in Python-Learning and the root are not proven to be the owner's own, only not copies of these 26.
- Blobless clone: all 9,007 blob SHAs came from the tree, and the contents of the modified files were fetched on demand. Nothing outside the audit was changed.

## Licensing notes (for SETUP §4, "keep its license and its credit")

- **No license file in the owner's copy, and none stated upstream:** `30-Days-Of-Python` (upstream README states no license). Under default copyright, the owner should not redistribute it without permission. Options: keep it out of a public repo, or ask the upstream author.
- **No license file in the owner's copy, but CC0 stated in the upstream README:** `awesome-for-beginners`, `build-your-own-x`. CC0 is a public-domain dedication, so copying is allowed; attribution is not required by the license, but the source should still be credited.
- **`python-cheatsheet`:** upstream has no license detected and none in the README. Only the bundled web fonts carry licenses (OnlineWebFonts `License.txt`). The owner's copy keeps those font licenses.
- **`CoreySchafer-code-snippets/LICENSE.txt`:** the text is an unfilled template (`Copyright (c) [year] [fullname]`). Upstream has the same text, so the owner did not break it.
- **NOASSERTION repos** (dive-into-deep-learning, interactive-coding-challenges, fastbook, awesome-python, pydata-book): GitHub could not classify the license, but each copy keeps its own LICENSE or COPYING file. Read those files before redistribution.
- **`python-mini-projects/LICENSE`** says `Copyright (c) 2020 Ravishankar Chavare`. The upstream owner is Python-World, so the copy keeps the original author's credit.

## Recommended next steps (for the owner to decide)

1. Decide what happens to `30-Days-Of-Python` (no license).
2. Add a `CREDITS.md`-style list of the 26 upstreams above, or the table in this file, to the owner's README.
3. Decide whether to keep the line-ending conversion (LF) or restore the upstream CRLF. This matters for diffing against upstream later.
