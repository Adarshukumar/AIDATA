# LOG-0003 — Python repo audit, part 1: inventory + upstream mapping

| Field | Value |
|---|---|
| id | `0003` |
| ts_utc | 2026-10-14T16:10Z → 16:36Z |
| phase | P3 — audit `Adarshukumar/Python` |
| status | 🟡 partial (inventory + mapping done; full file-by-file classification running) |
| commit | _(this commit)_ |

## Task

User request: *"check all the files and do make a diff as which are copied and which are
his own... in a dependent manner"* — i.e. a complete provenance audit of
`Adarshukumar/Python`.

## Plan

1. Inventory the repo (tree, sizes, commits, licenses) via `gh api`.
2. Map each top-level folder → upstream repo (evidence: folder READMEs + blob matches).
3. Blob-hash diff every file against upstream; probe non-identical blobs in the upstream
   object database to distinguish "older upstream revision" from "locally changed".
4. Emit the deliverables into `audit/`.

## Commands run (verbatim, abridged to the load-bearing ones)

```bash
gh api repos/Adarshukumar/Python --jq '{size,created_at,pushed_at,language}'
gh api repos/Adarshukumar/Python/commits --jq '.[] | "\(.sha[0:7]) \(.commit.author.date) :: \(.commit.message|split("\n")[0])"'
gh api "repos/Adarshukumar/Python/git/trees/main?recursive=1" --jq '.tree[].path' > /tmp/pytree.txt
# per-folder: compare his subtree blobs vs upstream HEAD blobs (join on path, compare sha)
join -t$'\t' /tmp/a.tsv /tmp/b.tsv | awk -F'\t' '$2!=$3{print $1}'
# probe a differing blob against the upstream object DB (200 = upstream artefact):
gh api "repos/<upstream>/git/blobs/<sha>" -q '.sha'
```

## Results

- **Repo:** 9,007 files · 27 top-level folders · 2 commits (`77b9f07` Init 2026-10-05,
  `188fd04` init 2026-10-06) · ~398 MB · language: Jupyter Notebook · license: none.
- **Folder → upstream map complete** → `audit/upstream-map.md` (27 rows + evidence).
- **Spot-check result (provisional, full run in progress):**
  - 8,741 files byte-identical to live upstream HEAD at audit time.
  - 20/20 sampled "different" files verified to be byte-identical to **older upstream
    revisions** (their blob hash exists in the upstream object DB).
  - Own content so far: `Python-Learning/` (54 files), root `README.md`,
    root `.gitignore`.
- **Correction found during mapping:** `tiny-python-projects` ⇒ `kyclark/tiny_python_projects`
  (not `norvig/pytudes`); `ml-book-3rd-edition` ⇒ the 3rd-edition repo (not
  `rasbt/machine-learning-book`). Both fixed in the map.

## Decisions

- **Hash equality is the only admissible proof of copying**; README self-references are
  only used for *attribution*, never for the verdict.
- Non-identical-but-valid-upstream-blob files will be classed `COPY_OLD_REVISION`, not
  "modified by the author" — with a separate pass for anything that is neither.

## Next

- LOG-0004: full file-by-file classification → `audit/files.csv` + `AUDIT_REPORT.md`.
