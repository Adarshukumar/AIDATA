# LOG-0007 — Provenance audit of `Adarshukumar/Python`: which popular repos are cloned

| Field | Value |
|---|---|
| id | `0007` |
| ts_utc | 2026-10-15T07:45Z |
| phase | P4 — audit (provenance) |
| status | ✅ done |

## Task
User: look at `https://github.com/Adarshukumar/Python` (the README calls it "My Python World") and identify "all the popular repository clones" in it.

## Method
- Match every file by git **blob SHA** against the default branch of each candidate upstream. Byte-identity is the evidence; visual similarity is not used.
- Blobless clone at `/tmp/py` (outside the repo). Tree: 9,007 blobs.
- Candidate upstreams from the owner's README and from license headers in the folders.
- Audit script: `arena-session-3b2d329a/artifacts/audit_upstream_clones.py`.
- Modified-file classifier: `arena-session-3b2d329a/artifacts/classify_modified.py`.

## Commands run (verbatim, abbreviated)
```
gh repo view Adarshukumar/Python                       # public, not a fork, default main
gh api repos/Adarshukumar/Python/git/trees/HEAD?recursive=1   # 9,007 blobs
git clone --filter=blob:none https://github.com/Adarshukumar/Python.git /tmp/py
python3 arena-session-3b2d329a/artifacts/audit_upstream_clones.py /tmp/py --target Adarshukumar/Python --out arena-session-3b2d329a/audit/python-repo
#   run 1: 3 upstream names wrong (404) → 6,063 exact (67.3%)
#   fixed names: kyclark/tiny_python_projects, CoreyMSchafer/code_snippets, trekhleb/learn-python,
#                Python-World/python-mini-projects (replaces karan/Projects)
#   run 2: 8,741 exact (97.0%)
#   run 3 (adds status column: exact / modified / added_or_renamed): same numbers
python3 arena-session-3b2d329a/artifacts/classify_modified.py /tmp/py --audit arena-session-3b2d329a/audit/python-repo
#   209 modified → 166 line_endings_only, 38 small_edit, 5 large_change
gh api repos/<upstream> --jq .license.spdx_id / .stargazers_count    # per upstream
```

## Results
- **8,741 / 9,007 files (97.0%) are byte-identical to one of 26 upstream repos.** No file matched a different folder's upstream.
- Full table with stars, license, and per-folder share: `arena-session-3b2d329a/audit/python-repo/README.md`. Machine-readable: `summary.csv`, `files.csv`, `modified.csv`, `unmatched.txt`.
- Most-starred clones: `codecrafters-io/build-your-own-x` (553k), `practical-tutorials/project-based-learning` (287k), `vinta/awesome-python` (328k), `TheAlgorithms/Python` (225k), `awesome-for-beginners` (90k), `30-Days-Of-Python` (76k).
- **Not clones:** `Python-Learning` (54 files, 0 matches) and the root (`README.md`, `.gitignore`). Both look like the owner's own.
- **Modified files (209):** 166 differ only in line endings (upstream CRLF, owner's copy LF; none of the 166 owner copies contains a CR). 38 have small edits (≤10 lines). 5 have larger changes (`awesome-python` README and `uv.lock`, `style.css`, `project-based-learning` link-rot JSON, `pytudes` notebook).
- One file added: `awesome-python/CONTEXT.md`.

## Licensing findings (SETUP §4)
- `30-Days-Of-Python`: upstream states no license; owner's copy has no LICENSE. Needs a decision.
- `awesome-for-beginners`, `build-your-own-x`: no LICENSE file, but CC0 stated in the upstream README.
- `python-cheatsheet`: no license detected; only bundled web fonts carry licenses.
- `CoreySchafer-code-snippets/LICENSE.txt`: unfilled template text, the same as upstream.
- Five repos show NOASSERTION (GitHub could not classify); each copy keeps its own LICENSE or COPYING file.

## Limits
- Compared against each upstream's **current default branch**. A "small_edit" may be the owner's own edit or an older upstream version. Telling these apart needs upstream history, which was not checked.
- Star counts and license values are as of 2026-10-15.
- The unmatched Python-Learning and root files are "not copies of these 26", not proven to be the owner's own.

## Decisions
- Used corrected upstream names only after `gh api` returned HTTP 200 for each. Did not guess for the rest.
- Committed `files.csv` (2 MB) as the evidence file. It is below the large-artifact threshold, and it is needed to reproduce the claim.
- Did not change any file in the owner's `Python` repo. The audit is read-only with respect to that repo.
- Did not create a new branch. Work stays on `arena/732d199a-aidata`.

## Next (for the owner)
1. Decide what happens to `30-Days-Of-Python` (no license).
2. Decide whether to keep the LF conversion or restore upstream CRLF.
3. Optional: check the 38 small edits and 5 large changes against upstream history.
