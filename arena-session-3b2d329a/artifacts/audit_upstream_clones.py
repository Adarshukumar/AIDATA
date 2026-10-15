#!/usr/bin/env python3
"""Provenance audit: which files in a repository are byte-identical copies of popular upstream repos.

Method of record (see arena-session-3b2d329a/audit/README.md): compare git blob SHAs.
A file is an exact copy of an upstream file if its blob SHA equals the blob SHA of some file in the
upstream repository's default branch. Byte-identity is proof; similarity of names or look is not.

  python3 arena-session-3b2d329a/artifacts/audit_upstream_clones.py /tmp/py \
      --target Adarshukumar/Python --out arena-session-3b2d329a/audit/python-repo

Inputs:
  <clone>            a git clone (blobless is fine: only trees are read here)
  --target           the repository being audited (used in the report)
  --map              optional JSON file {"folder": "owner/repo"}; default is the built-in map below

Requires the GitHub CLI (`gh`) with read access to the public repositories listed.

Outputs (in --out):
  files.csv          one row per file: path, folder, blob sha, status (exact | modified | added_or_renamed
                     | no_upstream_checked), matched upstream, same path?, upstream path
  summary.csv        one row per folder: files, exact matches, share, upstream, stars, default branch, truncated?
  unmatched.txt      files that did not match their folder's upstream (for manual review)
  README.md          human-readable report
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Folder in the audited repository -> upstream repository the folder is believed to copy.
# Each mapping is a hypothesis, confirmed or rejected by the blob-SHA match below.
DEFAULT_MAP = {
    "TheAlgorithms-Python": "TheAlgorithms/Python",
    "algorithms": "keon/algorithms",
    "interactive-coding-challenges": "donnemartin/interactive-coding-challenges",
    "pytudes": "norvig/pytudes",
    "tiny-python-projects": "kyclark/tiny_python_projects",
    "30-Days-Of-Python": "Asabeneh/30-Days-Of-Python",
    "python-cheatsheet": "gto76/python-cheatsheet",
    "wtf-python": "satwikkansal/wtfpython",
    "python-mini-projects": "Python-World/python-mini-projects",
    "project-based-learning": "practical-tutorials/project-based-learning",
    "build-your-own-x": "codecrafters-io/build-your-own-x",
    "flasky": "miguelgrinberg/flasky",
    "CoreySchafer-code-snippets": "CoreyMSchafer/code_snippets",
    "PythonDataScienceHandbook": "jakevdp/PythonDataScienceHandbook",
    "pydata-book": "wesm/pydata-book",
    "micrograd": "karpathy/micrograd",
    "nn-zero-to-hero": "karpathy/nn-zero-to-hero",
    "homemade-machine-learning": "trekhleb/homemade-machine-learning",
    "nlp-tutorial": "graykode/nlp-tutorial",
    "ml-book-3rd-edition": "rasbt/python-machine-learning-book-3rd-edition",
    "fastbook": "fastai/fastbook",
    "dive-into-deep-learning": "d2l-ai/d2l-en",
    "spinningup": "openai/spinningup",
    "awesome-python": "vinta/awesome-python",
    "awesome-for-beginners": "MunGell/awesome-for-beginners",
    "learn-python": "trekhleb/learn-python",
    "Python-Learning": "",       # the owner's own lessons per README: expected to match nothing
}


def gh_json(args: list[str]) -> object:
    proc = subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"gh api {' '.join(args)} failed: {proc.stderr.strip()[:300]}")
    return json.loads(proc.stdout)


def list_files(clone: Path) -> list[tuple[str, str]]:
    """(path, blob sha) for every blob at HEAD. Uses -z so odd filenames survive."""
    raw = subprocess.run(["git", "-C", str(clone), "ls-tree", "-r", "-z", "HEAD"],
                         capture_output=True, check=True).stdout.decode("utf-8", "surrogateescape")
    out = []
    for rec in raw.split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        mode, kind, sha = meta.split()
        if kind == "blob":
            out.append((path, sha))
    return out


def upstream_index(repo: str) -> dict:
    """Blob SHA -> list of upstream paths, plus repo metadata. Empty index if the repo cannot be read."""
    meta = gh_json([f"repos/{repo}"])
    branch = meta["default_branch"]
    tree = gh_json([f"repos/{repo}/git/trees/{branch}?recursive=1"])
    by_sha: dict[str, list[str]] = defaultdict(list)
    for entry in tree.get("tree", []):
        if entry.get("type") == "blob":
            by_sha[entry["sha"]].append(entry["path"])
    paths = {e["path"] for e in tree.get("tree", []) if e.get("type") == "blob"}
    return {
        "repo": repo,
        "branch": branch,
        "paths": paths,
        "stars": meta.get("stargazers_count", 0),
        "fork": bool(meta.get("fork")),
        "archived": bool(meta.get("archived")),
        "truncated": bool(tree.get("truncated")),
        "by_sha": by_sha,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clone", type=Path)
    ap.add_argument("--target", required=True, help="owner/repo being audited (for the report)")
    ap.add_argument("--map", type=Path, help="JSON file mapping folder -> owner/repo")
    ap.add_argument("--out", type=Path, required=True, help="output folder")
    args = ap.parse_args()

    mapping = json.loads(args.map.read_text()) if args.map else DEFAULT_MAP
    files = list_files(args.clone)
    print(f"audited files: {len(files)}", file=sys.stderr)

    indexes: dict[str, dict] = {}
    for upstream in sorted({v for v in mapping.values() if v}):
        try:
            indexes[upstream] = upstream_index(upstream)
            print(f"  {upstream}: {len(indexes[upstream]['by_sha'])} distinct blobs"
                  f" (stars {indexes[upstream]['stars']}, truncated={indexes[upstream]['truncated']})",
                  file=sys.stderr)
        except RuntimeError as exc:
            print(f"  {upstream}: UNREADABLE ({exc})", file=sys.stderr)
            indexes[upstream] = {"repo": upstream, "error": str(exc), "by_sha": {}}

    rows = []
    for path, sha in files:
        folder = path.split("/", 1)[0] if "/" in path else "(root)"
        expected = mapping.get(folder, "")
        matched, same_path, upstream_path = "", False, ""
        # 1) the folder's own hypothesised upstream first
        candidates = [expected] if expected else []
        # 2) then every other upstream we indexed (catches misfiled or renamed folders)
        candidates += [u for u in indexes if u != expected]
        for up in candidates:
            hits = indexes.get(up, {}).get("by_sha", {}).get(sha)
            if hits:
                matched = up
                rel = path.split("/", 1)[1] if "/" in path else path
                same_path = rel in hits
                upstream_path = next((h for h in hits if h == rel), hits[0])
                break
        rel = path.split("/", 1)[1] if "/" in path else path
        if matched:
            status = "exact"
        elif expected and rel in indexes.get(expected, {}).get("paths", set()):
            status = "modified"          # same path exists upstream, different bytes
        elif expected:
            status = "added_or_renamed"  # no file at this path upstream, and no blob match anywhere
        else:
            status = "no_upstream_checked"
        rows.append({"path": path, "folder": folder, "blob_sha": sha, "expected_upstream": expected,
                     "status": status, "matched_upstream": matched,
                     "matched_expected": bool(matched) and matched == expected,
                     "same_relative_path": same_path, "upstream_path": upstream_path})

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "files.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    per_folder: dict[str, dict] = {}
    for r in rows:
        f = per_folder.setdefault(r["folder"], {"files": 0, "exact": 0, "expected": r["expected_upstream"]})
        f["files"] += 1
        f["exact"] += 1 if r["matched_upstream"] else 0
    with (args.out / "summary.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["folder", "files", "exact_matches", "share", "expected_upstream", "upstream_stars",
                    "upstream_default_branch", "upstream_truncated", "upstream_error"])
        for folder, f in sorted(per_folder.items(), key=lambda kv: -kv[1]["files"]):
            up = indexes.get(f["expected"], {})
            w.writerow([folder, f["files"], f["exact"], f"{f['exact'] / f['files']:.1%}", f["expected"],
                        up.get("stars", ""), up.get("branch", ""), up.get("truncated", ""), up.get("error", "")])

    unmatched = [r["path"] for r in rows if not r["matched_upstream"]]
    if unmatched:
        pass
    (args.out / "unmatched.txt").write_text("\n".join(unmatched) + "\n", encoding="utf-8")

    total = len(rows)
    exact = sum(1 for r in rows if r["matched_upstream"])
    print(f"exact matches: {exact}/{total} ({exact / total:.1%}); unmatched: {len(unmatched)}", file=sys.stderr)
    print(json.dumps({"target": args.target, "files": total, "exact": exact, "unmatched": len(unmatched),
                      "upstreams": {k: {"stars": v.get("stars"), "branch": v.get("branch"),
                                         "truncated": v.get("truncated"), "error": v.get("error")}
                                    for k, v in indexes.items()}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
