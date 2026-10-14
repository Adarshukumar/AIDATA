---
description: Run (or re-run) the Adarshukumar/Python copy-vs-original audit end-to-end
allowed-tools: Bash(gh api:*), Bash(python3:*), Bash(bash:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
---

## Context

- Existing audit outputs: !`ls -la arena-session-3b2d329a/audit/ 2>/dev/null`
- Audit scripts: !`ls arena-session-3b2d329a/artifacts/scripts/ 2>/dev/null`
- Target repo meta: !`gh api repos/Adarshukumar/Python --jq '{files_url:.trees_url,size:.size,created:.created_at}'`

## Your task

The audit answers, for **every file** in `Adarshukumar/Python`: *is it a copy of a known
upstream repo, or the author's own?* Method (blob hashes — never eyeballing):

1. Fetch the target's full recursive tree (`/git/trees/main?recursive=1`) → map of
   `path → blob sha`.
2. For each of the 27 top-level folders, fetch the upstream repo's `HEAD` tree → map of
   `path → blob sha` (upstream list: `audit/upstream-map.md`).
3. Classify per path:
   - `COPY_IDENTICAL` — same path, same blob sha as upstream HEAD.
   - `COPY_OLD_REVISION` — same path, different sha, but the target's blob **exists in the
     upstream object database** (`GET /repos/{o}/{r}/git/blobs/{sha}` returns 200) → the
     file is an upstream artefact (an earlier revision), not the author's edit.
   - `COPY_REMOVED_UPSTREAM` — path gone from upstream HEAD but blob exists in upstream.
   - `ORIGINAL` — path inside `Python-Learning/` or repo root files that are not from any
     upstream.
   - `UNKNOWN` — blob exists in no upstream repo → third-pass manual review required.
4. Emit `audit/files.csv` (every file, one row: path, folder, size, sha, class, upstream
   repo, upstream path), `audit/AUDIT_REPORT.md` (the human report), `audit/originals.md`,
   `audit/modified-files.md`, `audit/licenses.md`.
5. Log the run as a new `logs/NNNN` entry, update `SESSION_STATE.md` + `TASKS.json`, and
   commit+push.

Rules: probe blobs for differing files **in parallel** (xargs -P8) to respect time, keep
raw intermediates in `/tmp/audit/` (not in Git), and never guess — an unverifiable file
stays `UNKNOWN` and gets reviewed by content.
