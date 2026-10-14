# Provenance audit — `Adarshukumar/Python`

*Generated 2026-10-14 17:34 UTC by session `3b2d329a` — method: git blob SHA comparison.*

## Verdict

Of **9,007 files**, **8,739** are byte-identical to the upstream repository at the same path, **176** are earlier upstream revisions, **33** are upstream files normalised CRLF->LF, **3** are upstream files that were later deleted upstream, and **56** are the author's own (0.62%). Unexplained: **0**.

| Classification | Files | Share |
|---|---:|---:|
| `COPY_IDENTICAL` | 8,739 | 97.02% |
| `COPY_OLD_REV` | 176 | 1.95% |
| `COPY_LINE_ENDINGS` | 33 | 0.37% |
| `COPY_REMOVED_UP` | 3 | 0.03% |
| `ORIGINAL` | 56 | 0.62% |
| **total** | **9,007** | 100% |

## Per folder

| Folder | Files | identical | old rev | CRLF->LF | removed | original | upstream |
|---|---:|---:|---:|---:|---:|---:|---|
| `.gitignore` | 1 | 0 | 0 | 0 | 0 | 1 | — |
| `30-Days-Of-Python` | 440 | 401 | 37 | 0 | 2 | 0 | asabeneh/30-Days-Of-Python |
| `CoreySchafer-code-snippets` | 965 | 954 | 3 | 8 | 0 | 0 | CoreyMSchafer/code_snippets |
| `Python-Learning` | 54 | 0 | 0 | 0 | 0 | 54 | — |
| `PythonDataScienceHandbook` | 264 | 264 | 0 | 0 | 0 | 0 | jakevdp/PythonDataScienceHandbook |
| `README.md` | 1 | 0 | 0 | 0 | 0 | 1 | — |
| `TheAlgorithms-Python` | 1733 | 1637 | 77 | 19 | 0 | 0 | TheAlgorithms/Python |
| `algorithms` | 444 | 443 | 0 | 1 | 0 | 0 | keon/algorithms |
| `awesome-for-beginners` | 10 | 10 | 0 | 0 | 0 | 0 | MunGell/awesome-for-beginners |
| `awesome-python` | 119 | 97 | 21 | 0 | 1 | 0 | vinta/awesome-python |
| `build-your-own-x` | 4 | 4 | 0 | 0 | 0 | 0 | codecrafters-io/build-your-own-x |
| `dive-into-deep-learning` | 836 | 836 | 0 | 0 | 0 | 0 | d2l-ai/d2l-en |
| `fastbook` | 490 | 488 | 2 | 0 | 0 | 0 | fastai/fastbook |
| `flasky` | 85 | 85 | 0 | 0 | 0 | 0 | miguelgrinberg/flasky |
| `homemade-machine-learning` | 185 | 185 | 0 | 0 | 0 | 0 | trekhleb/homemade-machine-learning |
| `interactive-coding-challenges` | 516 | 516 | 0 | 0 | 0 | 0 | donnemartin/interactive-coding-challenges |
| `learn-python` | 82 | 82 | 0 | 0 | 0 | 0 | trekhleb/learn-python |
| `micrograd` | 13 | 13 | 0 | 0 | 0 | 0 | karpathy/micrograd |
| `ml-book-3rd-edition` | 373 | 371 | 0 | 2 | 0 | 0 | rasbt/python-machine-learning-book-3rd-edition |
| `nlp-tutorial` | 42 | 42 | 0 | 0 | 0 | 0 | graykode/nlp-tutorial |
| `nn-zero-to-hero` | 9 | 9 | 0 | 0 | 0 | 0 | karpathy/nn-zero-to-hero |
| `project-based-learning` | 14 | 13 | 1 | 0 | 0 | 0 | practical-tutorials/project-based-learning |
| `pydata-book` | 43 | 43 | 0 | 0 | 0 | 0 | wesm/pydata-book |
| `python-cheatsheet` | 92 | 86 | 6 | 0 | 0 | 0 | gto76/python-cheatsheet |
| `python-mini-projects` | 1448 | 1422 | 26 | 0 | 0 | 0 | Python-World/python-mini-projects |
| `pytudes` | 204 | 199 | 2 | 3 | 0 | 0 | norvig/pytudes |
| `spinningup` | 181 | 180 | 1 | 0 | 0 | 0 | openai/spinningup |
| `tiny-python-projects` | 315 | 315 | 0 | 0 | 0 | 0 | kyclark/tiny_python_projects |
| `wtf-python` | 44 | 44 | 0 | 0 | 0 | 0 | satwikkansal/wtfpython |

## Method (reproducible)

1. `artifacts/scripts/audit_clone_heads.sh` — partial clones (`--filter=blob:none`) of the target + 26 upstreams; `git ls-tree -r -z HEAD` gives every path → blob SHA map offline.
2. `artifacts/scripts/audit_classify.py` — same path + same blob SHA ⇒ copy; same path, different SHA ⇒ candidate earlier revision.
3. `artifacts/scripts/audit_probe.sh` — for candidates only, `GET /repos/{o}/{r}/git/blobs/{sha}` proves the blob exists in the upstream object database (i.e. it *is* upstream content, not the author's edit).

A git blob SHA is SHA-1 over `blob <size>\0<content>` — equality is proof of
byte-identity, so this audit never relies on visual similarity.
