# LOG-0010 — Curation built and ready; blocked by repo write access (403)

| Field | Value |
|---|---|
| id | `0010` |
| ts_utc | 2026-10-14T18:45Z → 19:35Z |
| phase | P8 — Python repo curation |
| status | 🟡 artifacts ready · ⛔ push blocked (no write access to `Adarshukumar/Python`) |
| commit | _(this commit)_ |

## Task

Execute LOG-0009: curate `Adarshukumar/Python` (remove unlicensed + very popular copies,
add full attribution) and vendor the two new collections — with credit, not as claimed
authorship.

## What was built (all committed here)

1. **Removal analysis** (`/tmp/meta.tsv`, reproduced by the command below):
   stars + license per upstream → documented rule R1 (no license) + R2 (≥ 30k stars)
   → **10 folders, 3,236 files** to remove:

   | Folder | Stars | License | Rule |
   |---|---:|---|---|
   | `30-Days-Of-Python` | 76,222 | **none** | R1 |
   | `awesome-for-beginners` | 90,251 | **none** | R1 |
   | `build-your-own-x` | 553,229 | **none** | R1 |
   | `python-cheatsheet` | 38,695 | **none** | R1 |
   | `TheAlgorithms-Python` | 225,250 | MIT | R2 |
   | `awesome-python` | 327,411 | CC BY | R2 |
   | `project-based-learning` | 286,700 | MIT | R2 |
   | `PythonDataScienceHandbook` | 50,140 | MIT | R2 |
   | `wtf-python` | 37,123 | WTFPL | R2 |
   | `interactive-coding-challenges` | 31,912 | custom | R2 |

2. **`artifacts/curation/CREDITS.md`** — every one of the 16 surviving folders mapped to
   upstream repo, license and authors; removals listed with links and reasons; an explicit
   statement that the third-party code is not the author's.
3. **`artifacts/curation/README.md`** — honest rewrite of the repository front page.
4. **`artifacts/curation/PR_BODY_cleanup.md`** — the PR description.
5. **`artifacts/scripts/curate_python_repo.sh`** — one command to apply the whole cleanup
   as a PR (branch `arena/attribution-cleanup`).
6. **`artifacts/scripts/vendor_collections.sh`** — one command to vendor
   `ndleah/python-mini-project` + `king04aman/All-In-One-Python-Projects` with their
   LICENSE files, per-folder `SOURCE.md`, CREDITS rows, junk stripped, >20 MB files dropped.
7. **The branch itself is already built locally** in `/tmp/px` (blobless clone +
   `read-tree`/`rm --cached`/`hash-object`/`write-tree`, no 400 MB upload):
   `609ac88 Curate the collection…` on top of `188fd04` — 5,772 files, diff = 3,238 files
   changed, 1,450,147 deletions. **Untested against the remote** because of the 403 below.

## ⛔ The blocker (root cause found)

```bash
git push origin arena/attribution-cleanup
# remote: Permission to Adarshukumar/Python.git denied to Adarshukumar.
# fatal: ... The requested URL returned error: 403

gh api -X POST repos/Adarshukumar/Python/git/blobs -f content=test -f encoding=utf-8
# {"message":"Resource not accessible by integration","status":"403"}
```

The sandbox's GitHub credential is a **GitHub App installation token**, scoped to this
repository (`AIDATA`) only. It can *read* public repos (that is how the whole audit was
possible) but has **no write access to `Adarshukumar/Python`** — not via git, not via API,
so neither the branch push nor PR creation can happen from here.

**Fix (user action, 1 minute):** reconnect GitHub in Arena and grant the app access to
`Adarshukumar/Python` (or *all repositories*). Then the agent can run
`bash artifacts/scripts/curate_python_repo.sh` and the PR appears.

**Alternative (no reconnect):** run the same script locally — it only needs `git` + `gh`
with the user's own login:

```bash
gh auth login                                     # if not already
git clone https://github.com/Adarshukumar/AIDATA.git && cd AIDATA
bash arena-session-3b2d329a/artifacts/scripts/curate_python_repo.sh
bash arena-session-3b2d329a/artifacts/scripts/vendor_collections.sh
```

## Commands run (verbatim, load-bearing)

```bash
# stars + license per upstream (26 calls)
gh api repos/<upstream> --jq '"\(.stargazers_count)|\(.license.spdx_id // "NONE")"'

# build the branch without a full checkout
git clone -q --filter=blob:none --no-checkout https://github.com/Adarshukumar/Python.git /tmp/px
git read-tree HEAD && git rm -r -q --cached <10 folders>      # 9007 -> 5771 entries
git hash-object -w CREDITS.md; git update-index --add --cacheinfo 100644,<sha>,CREDITS.md
git write-tree | git commit-tree <tree> -p HEAD -m "Curate the collection…"
git push origin arena/attribution-cleanup                     # 403
gh api -X POST repos/Adarshukumar/Python/git/blobs …          # 403 (confirmed read-only)
```

## Decisions

- Removal rule is written down and reproducible (R1/R2) — not a judgement call per folder.
- Nothing was renamed or disguised; every kept folder keeps its LICENSE file, and the two
  new collections get an explicit `SOURCE.md` saying "this is not my work".
- Delivered as **pull requests**, not direct pushes to `main` — reviewable and reversible.
- Since write access was missing, the deliverables were made **runnable by the user** in
  two commands instead of stalling.

## Next

- User reconnects GitHub (or runs the two scripts) → PRs appear; then I verify the merged
  state, re-run the audit to confirm the new file counts, and log the result.
- `TASKS.json` entries T8.1–T8.5 track this.
