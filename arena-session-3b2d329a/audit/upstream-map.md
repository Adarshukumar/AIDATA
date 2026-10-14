# audit/upstream-map.md — folder → upstream repo map

Evidence for every row: the folder's own README/self-references (fetched via
`gh api -H "Accept: application/vnd.github.raw" repos/Adarshukumar/Python/contents/<path>`)
**and** blob-hash matches. Both were needed: self-references identify the project, hashes
prove the copying.

| Folder in `Adarshukumar/Python` | Files | Upstream repository | Evidence |
|---|---:|---|---|
| `30-Days-Of-Python` | 440 | `asabeneh/30-Days-Of-Python` | folder name + 401/438 blobs identical |
| `TheAlgorithms-Python` | 1733 | `TheAlgorithms/Python` | README links repo; 1654/1733 identical @2026-10-05 |
| `algorithms` | 444 | `keon/algorithms` | README: "https://github.com/keon/algorithms"; 443/444 identical |
| `CoreySchafer-code-snippets` | 965 | `CoreyMSchafer/code_snippets` | 954/965 identical |
| `Python-Learning` | 54 | — (author's own) | docstrings "Author: Adarsh"; no upstream match |
| `PythonDataScienceHandbook` | 264 | `jakevdp/PythonDataScienceHandbook` | 264/264 identical |
| `dive-into-deep-learning` | 836 | `d2l-ai/d2l-en` | 836/836 identical |
| `fastbook` | 490 | `fastai/fastbook` | 488/490 identical |
| `flasky` | 85 | `miguelgrinberg/flasky` | 85/85 identical |
| `homemade-machine-learning` | 185 | `trekhleb/homemade-machine-learning` | 185/185 identical |
| `interactive-coding-challenges` | 516 | `donnemartin/interactive-coding-challenges` | 516/516 identical |
| `learn-python` | 82 | `trekhleb/learn-python` | 82/82 identical |
| `micrograd` | 13 | `karpathy/micrograd` | 13/13 identical |
| `ml-book-3rd-edition` | 373 | `rasbt/python-machine-learning-book-3rd-edition` | 371/373 identical |
| `nlp-tutorial` | 42 | `graykode/nlp-tutorial` | 42/42 identical |
| `nn-zero-to-hero` | 9 | `karpathy/nn-zero-to-hero` | 9/9 identical |
| `project-based-learning` | 14 | `practical-tutorials/project-based-learning` | 13/14 identical |
| `pydata-book` | 43 | `wesm/pydata-book` | 43/43 identical |
| `python-cheatsheet` | 92 | `gto76/python-cheatsheet` | 86/92 identical |
| `python-mini-projects` | 1448 | `Python-World/python-mini-projects` | 1422/1448 identical |
| `pytudes` | 204 | `norvig/pytudes` | 199/204 identical |
| `spinningup` | 181 | `openai/spinningup` | 180/181 identical |
| `tiny-python-projects` | 315 | `kyclark/tiny_python_projects` | 315/315 identical |
| `wtf-python` | 44 | `satwikkansal/wtfpython` | 44/44 identical |
| `awesome-for-beginners` | 10 | `MunGell/awesome-for-beginners` | 10/10 identical |
| `awesome-python` | 119 | `vinta/awesome-python` | 99/119 identical |
| `build-your-own-x` | 4 | `codecrafters-io/build-your-own-x` | 4/4 identical |
| root `README.md`, `.gitignore` | 2 | — (author's own) | — |

Notes:

- `tiny-python-projects` is **not** from `norvig/pytudes` (my earlier guess) — it is
  `kyclark/tiny_python_projects` (Manning book companion), 315/315 blobs identical.
- `ml-book-3rd-edition` matches the **3rd-edition** repo, not the current
  `rasbt/machine-learning-book` — an earlier mapping was wrong and was corrected.
- `python-mini-projects` upstream has not been pushed since 2022-05-25, which is why its
  "differences" are the *upstream's own history* (e.g. files he has that HEAD deleted).
