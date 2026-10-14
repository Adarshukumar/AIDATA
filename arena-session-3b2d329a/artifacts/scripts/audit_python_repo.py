#!/usr/bin/env python3
"""Full provenance audit of Adarshukumar/Python against upstream repositories.

Method
------
A git blob SHA is a content hash: two files with the same blob SHA are byte-identical.
This script therefore never "looks" at code to decide copying — it compares blob SHAs.

Classification per file in the target repo:

  ORIGINAL        root files, or files under Python-Learning/ (author's own)
  COPY_IDENTICAL  same path *and* same blob SHA as the upstream repository's HEAD
  COPY_OLD_REV      same path, different SHA, but the target's blob SHA exists in the
                    upstream object database -> an earlier revision of an upstream file
  COPY_REMOVED_UP   path no longer at upstream HEAD, but blob exists in upstream history
  UNKNOWN         no upstream explanation found -> needs manual review

Usage:  python3 audit_python_repo.py [--probe-workers 8]
Writes: <repo>/arena-session-3b2d329a/audit/files.csv
        /tmp/audit/raw/*.json  (raw API responses, scratch only)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TARGET = "Adarshukumar/Python"
TARGET_REF = "main"
REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_CSV = REPO_ROOT / "arena-session-3b2d329a" / "audit" / "files.csv"
RAW = Path("/tmp/audit/raw")

# folder -> upstream repository (from audit/upstream-map.md)
UPSTREAM = {
    "30-Days-Of-Python": "asabeneh/30-Days-Of-Python",
    "TheAlgorithms-Python": "TheAlgorithms/Python",
    "algorithms": "keon/algorithms",
    "CoreySchafer-code-snippets": "CoreyMSchafer/code_snippets",
    "PythonDataScienceHandbook": "jakevdp/PythonDataScienceHandbook",
    "dive-into-deep-learning": "d2l-ai/d2l-en",
    "fastbook": "fastai/fastbook",
    "flasky": "miguelgrinberg/flasky",
    "homemade-machine-learning": "trekhleb/homemade-machine-learning",
    "interactive-coding-challenges": "donnemartin/interactive-coding-challenges",
    "learn-python": "trekhleb/learn-python",
    "micrograd": "karpathy/micrograd",
    "ml-book-3rd-edition": "rasbt/python-machine-learning-book-3rd-edition",
    "nlp-tutorial": "graykode/nlp-tutorial",
    "nn-zero-to-hero": "karpathy/nn-zero-to-hero",
    "project-based-learning": "practical-tutorials/project-based-learning",
    "pydata-book": "wesm/pydata-book",
    "python-cheatsheet": "gto76/python-cheatsheet",
    "python-mini-projects": "Python-World/python-mini-projects",
    "pytudes": "norvig/pytudes",
    "spinningup": "openai/spinningup",
    "tiny-python-projects": "kyclark/tiny_python_projects",
    "wtf-python": "satwikkansal/wtfpython",
    "awesome-for-beginners": "MunGell/awesome-for-beginners",
    "awesome-python": "vinta/awesome-python",
    "build-your-own-x": "codecrafters-io/build-your-own-x",
}
OWN_FOLDERS = {"Python-Learning"}


def gh_json(*args: str):
    """Run `gh api` and parse JSON; raise on failure."""
    proc = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"gh api {' '.join(args)} failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def gh_blob_exists(repo: str, sha: str) -> bool:
    """True if the blob SHA exists in `repo`'s object database."""
    proc = subprocess.run(
        ["gh", "api", f"repos/{repo}/git/blobs/{sha}"],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def fetch_tree(repo: str, ref: str = "HEAD") -> dict[str, dict]:
    """Recursive tree of a repo -> {path: {sha, size}} for blobs."""
    data = gh_json(f"repos/{repo}/git/trees/{ref}?recursive=1")
    if data.get("truncated"):
        print(f"  ! tree truncated for {repo}", file=sys.stderr)
    return {
        e["path"]: {"sha": e["sha"], "size": e.get("size", 0)}
        for e in data.get("tree", [])
        if e["type"] == "blob"
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe-workers", type=int, default=8)
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] target tree: {TARGET}@{TARGET_REF}")
    his = fetch_tree(TARGET, TARGET_REF)
    print(f"      {len(his)} blobs")

    print("[2/4] upstream trees")
    ups: dict[str, dict[str, dict]] = {}
    for folder, repo in UPSTREAM.items():
        ups[repo] = fetch_tree(repo, "HEAD")
        print(f"      {repo}: {len(ups[repo])} blobs")
        (RAW / (repo.replace('/', '__') + ".json")).write_text(
            json.dumps(ups[repo]), encoding="utf-8"
        )

    print("[3/4] classify")
    rows, need_probe = [], []
    for path, info in sorted(his.items()):
        folder = path.split("/", 1)[0] if "/" in path else ""
        sha = info["sha"]
        row = {
            "path": path,
            "folder": folder or "(root)",
            "size": info["size"],
            "blob_sha": sha,
            "classification": "",
            "upstream_repo": "",
            "upstream_sha": "",
        }

        if folder in OWN_FOLDERS or (folder == "" and path != "README.md"):
            row["classification"] = "ORIGINAL"
        elif folder == "":
            row["classification"] = "ORIGINAL"
        else:
            repo = UPSTREAM.get(folder)
            if repo is None:
                row["classification"] = "UNKNOWN"
                row["upstream_repo"] = ""
            else:
                utree = ups[repo]
                row["upstream_repo"] = repo
                if path in utree:
                    row["upstream_sha"] = utree[path]["sha"]
                    row["classification"] = (
                        "COPY_IDENTICAL" if utree[path]["sha"] == sha else "COPY_OLD_REV"
                    )
                    if row["classification"] == "COPY_OLD_REV":
                        need_probe.append((row, repo))
                else:
                    row["classification"] = "COPY_REMOVED_UP"
                    need_probe.append((row, repo))
        rows.append(row)

    print(f"[4/4] probing {len(need_probe)} differing blobs in upstream object DBs")
    with ThreadPoolExecutor(max_workers=args.probe_workers) as ex:
        futures = {
            ex.submit(gh_blob_exists, repo, row["blob_sha"]): (row, repo)
            for row, repo in need_probe
        }
        for fut, (row, repo) in futures.items():
            try:
                exists = fut.result()
            except Exception as exc:  # noqa: BLE001
                print(f"      probe error {row['path']}: {exc}", file=sys.stderr)
                exists = False
            if not exists and row["classification"] == "COPY_OLD_REV":
                row["classification"] = "UNKNOWN"

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = {"total_files": len(rows), "counts": counts}
    (RAW / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
