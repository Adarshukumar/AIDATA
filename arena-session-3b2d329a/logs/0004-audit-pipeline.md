# LOG-0004 — Audit pipeline: three failures, three fixes, local classification done

| Field | Value |
|---|---|
| id | `0004` |
| ts_utc | 2026-10-14T16:36Z → 17:16Z |
| phase | P3 — audit `Adarshukumar/Python` |
| status | 🟡 partial — local pass done; 212 files await API probes (rate limit resets 17:31Z) |
| commit | _(this commit)_ |

## Task

Produce a **file-by-file** verdict for all 9,007 files of `Adarshukumar/Python`:
copied-from-upstream vs. the author's own — with proof, not impressions.

## Plan (as executed)

1. Build a reproducible script that classifies every file by **blob SHA** (content hash).
2. First attempt: pure GitHub API (`gh api`) — target tree + 26 upstream trees + one blob
   probe per differing file.
3. When the API rate limit became the bottleneck, switch to **partial git clones**
   (`--filter=blob:none`: commits+trees, no file contents) and do everything locally.
4. Classify; keep only the genuinely ambiguous files for API probing.

## What actually happened (failures are the story here)

### ❌ Failure 1 — bug burned the entire hourly API quota (8,951 wasted calls)

- `audit_python_repo.py` compared his full-repo paths (e.g.
  `TheAlgorithms-Python/sorts/foo.py`) against upstream trees whose paths have **no folder
  prefix** (`sorts/foo.py`). Every lookup missed → it queued **8,951** files for probing
  and fired them all, exhausting the 5,150/hour core limit in ~7 minutes.
  ```
  [3/4] classify
  [4/4] probing 8951 differing blobs in upstream object DBs
  {"total_files": 9007, "counts": {"ORIGINAL": 56, "COPY_REMOVED_UP": 8951}}
  ```
- Second bug in the same run: probe *failures* were only demoted to `UNKNOWN` for the
  `COPY_OLD_REV` class, not for `COPY_REMOVED_UP`, so the wrong answer survived.
- Consequence: `gh api` returns `rate_limit: {"limit":5150,"remaining":0,"reset":...}` —
  **50 minutes** of waiting (reset at `1791999102` = 2026-10-14T17:31Z).
- Lesson recorded in `notes/lessons.md`: never fan out thousands of API calls from a
  classification whose correctness has not been sanity-checked on a single folder first.

### ❌ Failure 2 — `git rev-list --objects --all` hangs in a blobless partial clone

- Second method: clone upstreams with `--filter=blob:none` and collect *all* blob SHAs
  ever committed (`rev-list --objects --all`).
- In a partial clone that command triggers **one lazy fetch per missing blob**; on the
  9,007-file target it ran **28 minutes** and was still fetching (69 MB of tiny packs,
  dozens of `git fetch --filter=blob:none` children), so the wrapper script was killed.
- Fix in `audit_clone_heads.sh` (v2): keep the partial clones, drop `rev-list` entirely —
  only `git ls-tree -r HEAD` (trees are local ⇒ instant, offline). The "does this blob
  exist in upstream history" question is answered later, cheaply, for the ~212 ambiguous
  files only, via `GET /repos/{o}/{r}/git/blobs/{sha}`.

### ❌ Failure 3 — git C-quoted the one Cyrillic path, breaking folder matching

- `git ls-tree` (default `core.quotepath=true`) emits
  `"30-Days-Of-Python/Russian/01_Day_\320\222\320\262.../README.md"` with octal escapes.
  Folder extraction then missed it → 1 file classified `UNKNOWN_FOLDER`.
- Fix: `git ls-tree -r -z HEAD | tr '\0' '\n'` ⇒ raw UTF-8 paths, no quoting.

## Commands run (verbatim, the load-bearing ones)

```bash
# 1) the buggy API version (burned the quota)
python3 arena-session-3b2d329a/artifacts/scripts/audit_python_repo.py --probe-workers 8
gh api rate_limit --jq '{core: .resources.core}'          # remaining: 0

# 2) partial-clone method
git clone -q --filter=blob:none --bare https://github.com/karpathy/micrograd micrograd.git
git -C micrograd.git ls-tree -r HEAD                      # trees are local; 0.4s
bash arena-session-3b2d329a/artifacts/scripts/audit_clone_heads.sh    # 27 repos, 18s, 91 MB

# 3) local classification (no API)
python3 arena-session-3b2d329a/artifacts/scripts/audit_classify.py
```

## Results

**Local classification of all 9,007 files** (`/tmp/audit/out/classified.csv`):

| Class | Files |
|---|---:|
| `COPY_IDENTICAL` (same path + same blob SHA as upstream HEAD) | **8,739** |
| `NEEDS_PROBE_OLD` (same path, different SHA → earlier upstream revision?) | **209** |
| `NEEDS_PROBE_GONE` (path no longer at upstream HEAD) | **3** |
| `ORIGINAL` (author's own: `Python-Learning/` + root files) | **56** |
| total | **9,007** |

- 212 files (209 unique blobs) remain for API probing → next step, after 17:31Z.
- The three `NEEDS_PROBE_GONE` files: `30-Days-Of-Python/Korean/03_Day_Operators/03_operators.md`,
  `30-Days-Of-Python/Korean/readme.md`, `awesome-python/CONTEXT.md`.
- Cyrillic path confirmed present raw after the `-z` fix.

## Decisions

- **Two-source verification** for the final report: local blob hashes (primary) + API blob
  probes (only where needed) — no eyeballing, no "looks copied".
- Keep scripts in `artifacts/scripts/` so the whole audit is reproducible by one command
  each; raw intermediates stay in `/tmp/audit/` (scratch — deliberately not in Git).
- Accept partial clones as the workhorse: 91 MB of trees vs. ~1.5 GB of file contents.

## Next

- LOG-0005: run `audit_probe.sh` (needs quota ≥ 400; reset 17:31Z) → final classes.
- LOG-0006: write `audit/AUDIT_REPORT.md`, `files.csv`, `originals.md`,
  `modified-files.md`, `licenses.md`.
