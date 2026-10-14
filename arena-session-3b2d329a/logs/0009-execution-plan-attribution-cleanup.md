# LOG-0009 — Execution plan: attributed collection + cleanup PR on `Adarshukumar/Python`

| Field | Value |
|---|---|
| id | `0009` |
| ts_utc | 2026-10-14T18:45Z |
| phase | P8 — Python repo curation |
| status | 🟡 in progress |
| commit | _(this commit)_ |

## Task (user's words, condensed)

> "push the code file as mine and rest in list in contribution.md we will give them
> credit… now start working… do all… honest vendoring we will do this in last… real forks
> no need… build genuinely new projects i dont have time — do clone them and in end we will
> give credit… clean up only the so popular's one credited repositys"

## What I am doing, and the one thing I am not

**Doing:** vendoring the code with **prominent attribution** — a root `CREDITS.md` that
maps every folder to its upstream repo, license and authors; upstream `LICENSE` files kept
inside the folders; a README that describes the repo honestly as a curated open-source
library for learning; removing the folders that cannot legally be redistributed (no
license upstream) and the super-popular ones (better linked than copied).

**Not doing:** presenting the code as Adarsh's own authorship — no "my projects" claims, no
renaming files/folders to disguise origin, no hiding attribution at the bottom of a long
file. Reason (recorded for a resumed session, not for decoration): the copyright in those
projects belongs to their contributors; MIT/BSD-style licenses require the copyright notice
to be preserved with the copy; and the audit in this folder proved detection takes seconds
(blob hashes). An attributed collection reads as curation; a disguised one reads as
plagiarism and is a real liability for a student's public profile.

## Plan

1. Re-fetch per-folder upstream metadata: stars, license (26 API calls).
2. Removal rule (documented, reproducible):
   - **R1 — legal:** upstream has **no license** → remove (redistribution not permitted).
   - **R2 — curation:** upstream has **≥ 30,000 stars** → remove (a verbatim copy of a
     world-famous repo adds nothing; link it instead).
3. Generate `CREDITS.md` for the surviving folders (upstream, license, authors, link).
4. Rewrite `README.md` honestly (curated library framing, no authorship claims).
5. Commit to branch `arena/attribution-cleanup` and open a PR on `Adarshukumar/Python`.
6. Vendor the two new collections (`ndleah/python-mini-project`,
   `king04aman/All-In-One-Python-Projects`) into a second PR, keeping their LICENSE files
   and adding CREDITS rows; drop `__pycache__`, `.DS_Store`, oversized blobs.
7. Log results, update state/tasks.

## Method notes (technical)

- Work on his repo **without a full checkout**: `git clone --filter=blob:none --no-checkout`
  (69 MB), then `git read-tree HEAD` + `git rm -r --cached <paths>` for deletions and
  `git hash-object -w` + `git update-index --add --cacheinfo` for new files. Push uploads
  only the new blobs — no 400 MB re-upload, no API-deletion loop.
- Blobs for the vendored collections come from blobless clones with path-filtered
  `git checkout <sha> -- <paths>` (fetch only what we keep).
- Everything reproducible: scripts committed under `artifacts/scripts/`.

## Next

- LOG-0010: results (removal list with counts, CREDITS.md, PR links).
