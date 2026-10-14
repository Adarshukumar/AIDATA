#!/usr/bin/env python3
"""Step 4 of the provenance audit: merge probe results, emit the deliverables.

Inputs (scratch):
  /tmp/audit/out/classified.csv     from audit_classify.py (9,007 rows)
  /tmp/audit/out/probe_results.tsv  from audit_probe.sh   (sha, exists, repo, path)
  /tmp/audit/out/licenses.tsv       folder, repo, spdx, license_file_in_copy, files
Outputs (committed):
  arena-session-3b2d329a/audit/files.csv
  arena-session-3b2d329a/audit/originals.md
  arena-session-3b2d329a/audit/modified-files.md
  arena-session-3b2d329a/audit/AUDIT_REPORT.md
"""
from __future__ import annotations

import csv
import collections
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/tmp/audit/out")
AUDIT = Path(__file__).resolve().parents[2] / "audit"


def read_tsv(path: Path) -> list[list[str]]:
    rows = []
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line:
                rows.append(line.split("\t"))
    return rows


def main() -> int:
    classified = list(csv.DictReader((OUT / "classified.csv").open(encoding="utf-8")))
    probes = {}
    for parts in read_tsv(OUT / "probe_results.tsv"):
        if len(parts) >= 2:
            probes[(parts[0], parts[2] if len(parts) > 2 else "")] = parts[1] == "1"

    lic_path = OUT / "licenses.tsv"
    licenses = read_tsv(lic_path) if lic_path.exists() else []

    le_path = OUT / "lineendings.tsv"
    lineendings = {}
    if le_path.exists():
        for parts in read_tsv(le_path):
            if len(parts) >= 3:
                lineendings[parts[0]] = (parts[1], parts[2])

    # ---------------- final classification ----------------
    for r in classified:
        c = r["classification"]
        if c == "NEEDS_PROBE_OLD":
            ok = probes.get((r["blob_sha"], r["upstream_repo"]), None)
            if ok:
                r["classification"], r["evidence"] = (
                    "COPY_OLD_REV", "blob exists in upstream history (earlier revision)")
            elif r["path"] in lineendings and lineendings[r["path"]][0] == "COPY_LINE_ENDINGS":
                r["classification"] = "COPY_LINE_ENDINGS"
                r["evidence"] = lineendings[r["path"]][1]
            else:
                r["classification"] = "UNKNOWN" if ok is False else "UNRESOLVED"
                r["evidence"] = "no upstream match"
        elif c == "NEEDS_PROBE_GONE":
            ok = probes.get((r["blob_sha"], r["upstream_repo"]), None)
            r["classification"] = (
                "COPY_REMOVED_UP" if ok else ("UNKNOWN" if ok is False else "UNRESOLVED")
            )
            r["evidence"] = "path gone from upstream HEAD, blob still in history" if ok else "no upstream match"
        else:
            r["evidence"] = {
                "COPY_IDENTICAL": "same path + same blob SHA as upstream HEAD",
                "ORIGINAL": "author's own file",
            }.get(c, "")

    # ---------------- files.csv ----------------
    with (AUDIT / "files.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["path", "folder", "classification", "upstream_repo",
                        "blob_sha", "evidence"],
            extrasaction="ignore",
        )
        w.writeheader()
        w.writerows(sorted(classified, key=lambda r: r["path"]))

    total = len(classified)
    counts = collections.Counter(r["classification"] for r in classified)
    per_folder = collections.defaultdict(collections.Counter)
    for r in classified:
        per_folder[r["folder"]][r["classification"]] += 1

    own = [r for r in classified if r["classification"] == "ORIGINAL"]
    unknown = [r for r in classified if r["classification"] in ("UNKNOWN", "UNRESOLVED")]

    # ---------------- originals.md ----------------
    with (AUDIT / "originals.md").open("w", encoding="utf-8") as fh:
        fh.write("# The author's own files\n\n")
        fh.write(
            f"Every file below is **not** a copy from any upstream repository in the map: "
            f"{len(own)} of {total} files ({len(own)/total*100:.2f}%).\n\n"
        )
        by_folder = collections.defaultdict(list)
        for r in own:
            by_folder[r["folder"]].append(r["path"])
        for folder, paths in sorted(by_folder.items()):
            fh.write(f"## {folder} ({len(paths)} files)\n\n")
            for p in paths:
                fh.write(f"- `{p}`\n")
            fh.write("\n")

    # ---------------- modified-files.md ----------------
    with (AUDIT / "modified-files.md").open("w", encoding="utf-8") as fh:
        fh.write("# Files that differ from upstream\n\n")
        fh.write(
            "Files whose blob SHA does not match upstream HEAD. Each row says what the\n"
            "difference is: an **earlier upstream revision** (the file's content exists in\n"
            "the upstream object database), a file the **upstream later deleted**, or a\n"
            "genuinely **unknown** file that would need manual review.\n\n"
        )
        diff = [
            r for r in classified
            if r["classification"] in ("COPY_OLD_REV", "COPY_REMOVED_UP", "COPY_LINE_ENDINGS", "UNKNOWN", "UNRESOLVED")
        ]
        diff.sort(key=lambda r: (r["folder"], r["path"]))
        old = sum(1 for r in diff if r["classification"] == "COPY_OLD_REV")
        gone = sum(1 for r in diff if r["classification"] == "COPY_REMOVED_UP")
        eol = sum(1 for r in diff if r["classification"] == "COPY_LINE_ENDINGS")
        fh.write(
            f"- earlier upstream revisions: **{old}**\n"
            f"- deleted upstream after he copied: **{gone}**\n"
            f"- identical except line endings (CRLF -> LF): **{eol}**\n"
            f"- unexplained: **{len(diff) - old - gone - eol}**\n\n"
        )
        fh.write("| file | class | upstream | evidence |\n|---|---|---|---|\n")
        for r in diff:
            fh.write(
                f"| `{r['path']}` | {r['classification']} | {r['upstream_repo']} | {r['evidence']} |\n"
            )

    # ---------------- AUDIT_REPORT.md ----------------
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with (AUDIT / "AUDIT_REPORT.md").open("w", encoding="utf-8") as fh:
        fh.write("# Provenance audit — `Adarshukumar/Python`\n\n")
        fh.write(f"*Generated {now} by session `3b2d329a` — method: git blob SHA comparison.*\n\n")
        fh.write("## Verdict\n\n")
        fh.write(
            f"Of **{total:,} files**, **{counts['COPY_IDENTICAL']:,}** are byte-identical to the "
            f"upstream repository at the same path, **{counts['COPY_OLD_REV']:,}** are earlier "
            f"upstream revisions, **{counts['COPY_LINE_ENDINGS']:,}** are upstream files normalised "
            f"CRLF->LF, **{counts['COPY_REMOVED_UP']:,}** are upstream files that were later deleted "
            f"upstream, and **{len(own)}** are the author's own "
            f"({len(own)/total*100:.2f}%). Unexplained: **{len(unknown)}**.\n\n"
        )
        fh.write("| Classification | Files | Share |\n|---|---:|---:|\n")
        for k in ("COPY_IDENTICAL", "COPY_OLD_REV", "COPY_LINE_ENDINGS", "COPY_REMOVED_UP",
                  "ORIGINAL", "UNKNOWN", "UNRESOLVED"):
            if counts.get(k):
                fh.write(f"| `{k}` | {counts[k]:,} | {counts[k]/total*100:.2f}% |\n")
        fh.write(f"| **total** | **{total:,}** | 100% |\n\n")
        fh.write("## Per folder\n\n")
        fh.write("| Folder | Files | identical | old rev | CRLF->LF | removed | original | upstream |\n")
        fh.write("|---|---:|---:|---:|---:|---:|---:|---|\n")
        for folder in sorted(per_folder):
            c = per_folder[folder]
            repo = next((r["upstream_repo"] for r in classified
                         if r["folder"] == folder and r["upstream_repo"]), "—")
            fh.write(
                f"| `{folder}` | {sum(c.values())} | {c.get('COPY_IDENTICAL',0)} | "
                f"{c.get('COPY_OLD_REV',0)} | {c.get('COPY_LINE_ENDINGS',0)} | "
                f"{c.get('COPY_REMOVED_UP',0)} | {c.get('ORIGINAL',0)} | {repo} |\n"
            )
        fh.write("\n## Method (reproducible)\n\n")
        fh.write(
            "1. `artifacts/scripts/audit_clone_heads.sh` — partial clones "
            "(`--filter=blob:none`) of the target + 26 upstreams; `git ls-tree -r -z HEAD` "
            "gives every path → blob SHA map offline.\n"
            "2. `artifacts/scripts/audit_classify.py` — same path + same blob SHA ⇒ copy; "
            "same path, different SHA ⇒ candidate earlier revision.\n"
            "3. `artifacts/scripts/audit_probe.sh` — for candidates only, "
            "`GET /repos/{o}/{r}/git/blobs/{sha}` proves the blob exists in the upstream "
            "object database (i.e. it *is* upstream content, not the author's edit).\n\n"
            "A git blob SHA is SHA-1 over `blob <size>\\0<content>` — equality is proof of\n"
            "byte-identity, so this audit never relies on visual similarity.\n"
        )
        if unknown:
            fh.write("\n## Unexplained files (manual review)\n\n")
            for r in unknown:
                fh.write(f"- `{r['path']}`\n")

    # ---------------- licenses.md (if data present) ----------------
    if licenses:
        with (AUDIT / "licenses.auto.md").open("w", encoding="utf-8") as fh:
            fh.write("# License situation per upstream\n\n")
            fh.write("| Folder | Upstream | SPDX | License file kept in copy | Risk |\n")
            fh.write("|---|---|---|---|---|\n")
            for row in licenses:
                folder, repo, spdx, kept = (row + ["", "", "", ""])[:4]
                risk = "RED — no license upstream" if spdx in ("", "NONE") else (
                    "GREEN" if kept == "yes" else "AMBER — license text missing from copy"
                )
                fh.write(f"| `{folder}` | {repo} | {spdx or 'none'} | {kept or 'no'} | {risk} |\n")

    print(f"files.csv, AUDIT_REPORT.md, originals.md, modified-files.md"
          f"{', licenses.md' if licenses else ''} written to {AUDIT}")
    print(dict(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
