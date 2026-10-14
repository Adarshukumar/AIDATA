# LOG-0007 — SETUP.md + analysis of two collection repos + a boundary I did not cross

| Field | Value |
|---|---|
| id | `0007` |
| ts_utc | 2026-10-14T18:05Z → 18:30Z |
| phase | P6 — new deliverables + policy boundary |
| status | ✅ done (deliverables) ⛔ declined (re-upload-as-own request) |
| commit | _(this commit)_ |

## Task (user's message, as asked)

1. "see all the projects in detailed manner" — `ndleah/python-mini-project` and
   `king04aman/All-In-One-Python-Projects`.
2. "first things do create a one `setup.md` file how to activate our featuring of this
   prompt … all the things u have done make a one entire setup for it."
3. Then: clone his Python repo, remove the "too popular" copied repos, "clone all of
   the work and do search for more", "**make all of them as mine projects**", "**push them
   as mine**", "**convert them to Adarsh by changing them a little**".

## What I did

### 1. `SETUP.md` (requested deliverable) — written

Complete activation guide for this memory system: repo clone → `hooks/install.sh` (the one
required command) → verification checklist → the working loop → how to use `commands/` in
Claude Code / other agents / by hand → disconnect-recovery commands → runtime-hook wiring
(`hooks.json` with the Claude Code exit-code contract) → daily cheat-sheet → troubleshooting
table → design rules. 11 sections, self-contained.

### 2. Detailed analysis of both repos — written to `audit/collection-repos-analysis.md`

| | `ndleah/python-mini-project` | `king04aman/All-In-One-Python-Projects` |
|---|---|---|
| Stars | 4,426 | 410 |
| License | MIT (© 2021 Leah Nguyen) | MIT (© 2023 Aman Kumar) |
| Contributors | 100+ | 24+ |
| Project folders | **131** | **65** |
| Files | 587 (157 `.py`, 122 `.md`) | 237 (75 `.py`, 40 `.md`) |
| Overlap with Python-World/python-mini-projects | **7 / 580 blobs (1%)** | **1 / 198 blobs (0%)** |
| Overlap with each other | negligible — distinct collections | — |
| Junk found | 14 × `__pycache__`, 4 × `.DS_Store`, 44 badges | 3 × `__pycache__`, stray `Example README.md` |

Both are **community aggregations** (each project folder is a different contributor's
submission), not single-author repos, and neither is a copy of what he already has. Full
per-project file lists are in the analysis document.

## The boundary (why part of the request was declined)

The request "make all of them as mine projects … push them as mine … convert them to
Adarsh by changing them a little", together with "remove too much popular" copies, is a
request to **disguise other people's work as his own**. That is:

- **attribution fraud** — the work of 100+ contributors would be re-published under one
  name, with the credit deliberately removed;
- **a license violation in spirit even where MIT applies** — MIT requires the copyright
  notice and permission notice to be retained; renaming files does not create authorship;
- **practically self-defeating** — the audit in this very folder proved that content
  fingerprints are detectable in seconds by anyone who checks blob hashes, and a repo
  whose folders contradict its own README (as the current `Python` repo does) reads worse
  than an honest fork.

**Declined:** cloning collections for the purpose of re-uploading them as Adarsh's own
projects, stripping attribution, and cosmetic renaming to obscure origin.

**Offered instead** (see chat): (a) honest vendoring with `CREDITS.md` + retained LICENSEs,
(b) proper GitHub forks that keep attribution automatically, (c) writing genuinely new
projects in his own style — the 196 projects above are an excellent *index* to learn from,
(d) cleaning up the existing repo (remove the 4 unlicensed folders, fix the README claims).

## Commands run (verbatim, load-bearing)

```bash
gh api repos/ndleah/python-mini-project --jq '{description,stars:.stargazers_count,license:(.license.spdx_id // "NONE"),size:.size}'
gh api repos/king04aman/All-In-One-Python-Projects --jq '{description,stars:.stargazers_count,license:(.license.spdx_id // "NONE"),size:.size}'
gh api "repos/<each>/git/trees/HEAD?recursive=1" --jq '.tree[]|select(.type=="blob")|"\(.sha)\t\(.path)"' | sort > /tmp/audit/out/<name>.tsv
comm -12 <(cut -f1 ndleah.tsv | sort -u) <(cut -f1 pworld.tsv | sort -u) | wc -l     # 7 of 580
comm -12 <(cut -f1 king.tsv   | sort -u) <(cut -f1 pworld.tsv | sort -u) | wc -l     # 1 of 198
```

Note: `/tmp` had been wiped by a sandbox restart between turns — rebuilt the three needed
tree dumps with four API calls instead of re-cloning 91 MB (the documented recovery path
worked).

## Decisions

- Performed the analysis (legitimate research: public repos, provenance, licenses).
- Did **not** perform any copying, renaming, re-uploading, or attribution removal, and
  will not — recorded here so a resumed session does not "finish the job".
- Added `SETUP.md` to `TASKS.json` as its own deliverable.

## Next

- Await the user's choice among the four offered alternatives.
- Standing items: `CREDITS.md` + README fix for `Adarshukumar/Python`; removal of the four
  unlicensed folders.
