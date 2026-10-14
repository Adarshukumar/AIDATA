# notes/lessons.md — what went wrong and what to do instead

A running list. Failures are the most valuable part of a work log after a disconnect.

## 2026-10-14

### 1. Never fan out thousands of API calls before validating the classification

`audit_python_repo.py` queued 8,951 blob probes because of a path-prefix bug and burned
the entire hourly API quota (5,150 requests) in minutes. A 5-second check on one folder
would have caught it.

**Rule:** before any fan-out, run the classifier on a single folder (≤ 50 items) and
eyeball the result. Then scale.

### 2. `git rev-list --objects --all` is unusable in a `--filter=blob:none` clone

It triggers one lazy fetch per missing blob — 28 minutes and still going on a 9,007-file
repo. Trees alone (`git ls-tree -r HEAD`) are local and instant.

**Rule:** in partial clones, stick to tree-level commands (`ls-tree`, `log --raw`).
Never `rev-list --objects`, never `cat-file` on blobs.

### 3. Git C-quotes non-ASCII paths (`core.quotepath=true`)

`ls-tree` emitted `"Russian/01_Day_\320\222\320\262.../README.md"`, silently breaking
path matching for every non-ASCII file (here: exactly one, but it broke the folder lookup).

**Rule:** always use `-z` (NUL-delimited) output and convert, or set
`-c core.quotepath=false`. Never parse C-quoted paths.

### 4. Say the API budget out loud before spending it

Before a batch: `gh api rate_limit --jq '.resources.core.remaining'` and compare with the
planned number of calls. `audit_probe.sh` now refuses to start if quota < needed + 50.
