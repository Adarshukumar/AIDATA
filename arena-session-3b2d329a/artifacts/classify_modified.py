#!/usr/bin/env python3
"""Classify files whose path exists upstream but whose bytes differ (status == 'modified').

For each such file, fetch the upstream blob (via the GitHub API) and the local blob (via git), then label:
  - line_endings_only : identical after converting CRLF to LF (the owner's copy uses LF, upstream uses CRLF)
  - trailing_whitespace_only : identical after stripping trailing spaces on each line
  - small_edit        : differs by <= 10 changed lines
  - large_change      : differs by more than 10 changed lines
  - binary_or_unreadable

  python3 arena-session-3b2d329a/artifacts/classify_modified.py /tmp/py \
      --audit arena-session-3b2d329a/audit/python-repo

Reads  <audit>/files.csv   (from audit_upstream_clones.py)
Writes <audit>/modified.csv and prints a per-folder summary.
"""
from __future__ import annotations

import argparse
import base64
import csv
import difflib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


def gh_json(args: list[str]):
    proc = subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip()[:200])
    return json.loads(proc.stdout)


def local_blob(clone: Path, sha: str) -> bytes:
    return subprocess.run(["git", "-C", str(clone), "cat-file", "blob", sha],
                          capture_output=True, check=True).stdout


def normalise(data: bytes) -> list[str]:
    text = data.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
    return [line.rstrip() for line in text.split("\n")]


def classify(local: bytes, remote: bytes) -> tuple[str, int]:
    if b"\0" in local[:8000] or b"\0" in remote[:8000]:
        return "binary_or_unreadable", -1
    if local == remote:
        return "identical", 0
    if local.replace(b"\r\n", b"\n") == remote.replace(b"\r\n", b"\n"):
        return "line_endings_only", 0
    a, b = normalise(local), normalise(remote)
    if a == b:
        return "trailing_whitespace_only", 0
    changed = sum(1 for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
                  if op[0] != "equal" for _ in range(max(op[2] - op[1], op[4] - op[3])))
    return ("small_edit" if changed <= 10 else "large_change"), changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clone", type=Path)
    ap.add_argument("--audit", type=Path, required=True, help="folder with files.csv")
    args = ap.parse_args()

    rows = list(csv.DictReader((args.audit / "files.csv").open(encoding="utf-8")))
    todo = [r for r in rows if r["status"] == "modified"]
    upstream_for = {r["expected_upstream"] for r in todo}

    # upstream path -> blob sha, per repo
    upstream_sha: dict[str, dict[str, str]] = {}
    for repo in sorted(upstream_for):
        meta = gh_json([f"repos/{repo}"])
        tree = gh_json([f"repos/{repo}/git/trees/{meta['default_branch']}?recursive=1"])
        upstream_sha[repo] = {e["path"]: e["sha"] for e in tree.get("tree", []) if e.get("type") == "blob"}

    out_rows = []
    for r in todo:
        repo = r["expected_upstream"]
        rel = r["path"].split("/", 1)[1]
        remote_sha = upstream_sha[repo][rel]
        try:
            remote = base64.b64decode(gh_json([f"repos/{repo}/git/blobs/{remote_sha}"])["content"])
            label, changed = classify(local_blob(args.clone, r["blob_sha"]), remote)
        except Exception as exc:  # keep going; record the error
            label, changed = f"error: {str(exc)[:80]}", -1
        out_rows.append({"path": r["path"], "folder": r["folder"], "upstream": repo,
                         "upstream_path": rel, "class": label, "changed_lines": changed})

    with (args.audit / "modified.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()) if out_rows else ["path"])
        w.writeheader()
        w.writerows(out_rows)

    per = defaultdict(Counter)
    for o in out_rows:
        per[o["folder"]][o["class"]] += 1
    print(f"modified files classified: {len(out_rows)}")
    for folder, c in sorted(per.items(), key=lambda kv: -sum(kv[1].values())):
        print(f"  {folder:<28} {dict(c)}")
    print("overall:", dict(Counter(o["class"] for o in out_rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
