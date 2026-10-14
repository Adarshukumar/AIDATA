#!/usr/bin/env python3
"""Step 2 of the provenance audit: local classification (no API calls).

Reads the trees produced by audit_clone_heads.sh
(`/tmp/audit/out/head__<name>.tsv`, lines `<blob_sha>\t<path>`) and classifies every file
of the target repo. Only files that cannot be classified from HEAD trees alone are left
as "NEEDS_PROBE" — they are resolved in step 3 with the GitHub API.

Classification (same definitions as the deliverable):
  ORIGINAL          the author's own files (root files + Python-Learning/)
  COPY_IDENTICAL    same relative path *and* same blob SHA as upstream HEAD
  NEEDS_PROBE_OLD   same path, different SHA  -> maybe an earlier upstream revision
  NEEDS_PROBE_GONE  path absent from upstream HEAD -> maybe removed upstream, maybe his
  UNKNOWN_FOLDER    top-level folder has no known upstream

Outputs:
  /tmp/audit/out/classified.csv     all 9,007 rows, preliminary classes
  /tmp/audit/out/need_probe.tsv     `<blob_sha>\t<upstream_repo>\t<target_path>`
  stdout: counts
"""
from __future__ import annotations

import csv
from pathlib import Path

OUT = Path("/tmp/audit/out")

UPSTREAM = {
    "30-Days-Of-Python": ("asabeneh/30-Days-Of-Python", "30-Days-Of-Python"),
    "TheAlgorithms-Python": ("TheAlgorithms/Python", "TheAlgorithms-Python"),
    "algorithms": ("keon/algorithms", "algorithms"),
    "CoreySchafer-code-snippets": ("CoreyMSchafer/code_snippets", "CoreySchafer-code-snippets"),
    "PythonDataScienceHandbook": ("jakevdp/PythonDataScienceHandbook", "PythonDataScienceHandbook"),
    "dive-into-deep-learning": ("d2l-ai/d2l-en", "dive-into-deep-learning"),
    "fastbook": ("fastai/fastbook", "fastbook"),
    "flasky": ("miguelgrinberg/flasky", "flasky"),
    "homemade-machine-learning": ("trekhleb/homemade-machine-learning", "homemade-machine-learning"),
    "interactive-coding-challenges": ("donnemartin/interactive-coding-challenges", "interactive-coding-challenges"),
    "learn-python": ("trekhleb/learn-python", "learn-python"),
    "micrograd": ("karpathy/micrograd", "micrograd"),
    "ml-book-3rd-edition": ("rasbt/python-machine-learning-book-3rd-edition", "ml-book-3rd-edition"),
    "nlp-tutorial": ("graykode/nlp-tutorial", "nlp-tutorial"),
    "nn-zero-to-hero": ("karpathy/nn-zero-to-hero", "nn-zero-to-hero"),
    "project-based-learning": ("practical-tutorials/project-based-learning", "project-based-learning"),
    "pydata-book": ("wesm/pydata-book", "pydata-book"),
    "python-cheatsheet": ("gto76/python-cheatsheet", "python-cheatsheet"),
    "python-mini-projects": ("Python-World/python-mini-projects", "python-mini-projects"),
    "pytudes": ("norvig/pytudes", "pytudes"),
    "spinningup": ("openai/spinningup", "spinningup"),
    "tiny-python-projects": ("kyclark/tiny_python_projects", "tiny-python-projects"),
    "wtf-python": ("satwikkansal/wtfpython", "wtf-python"),
    "awesome-for-beginners": ("MunGell/awesome-for-beginners", "awesome-for-beginners"),
    "awesome-python": ("vinta/awesome-python", "awesome-python"),
    "build-your-own-x": ("codecrafters-io/build-your-own-x", "build-your-own-x"),
}
OWN_FOLDERS = {"Python-Learning"}


def read_tsv(path: Path) -> dict[str, str]:
    """sha<TAB>path lines -> {path: sha}"""
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or "\t" not in line:
                continue
            sha, p = line.split("\t", 1)
            out[p] = sha
    return out


def main() -> int:
    his = read_tsv(OUT / "head__target.tsv")
    ups = {name: read_tsv(OUT / f"head__{name}.tsv") for _, name in UPSTREAM.values()}

    rows, need_probe = [], []
    for path, sha in sorted(his.items()):
        folder, _, rel = path.partition("/")
        row = {"path": path, "folder": folder or "(root)", "blob_sha": sha,
               "classification": "", "upstream_repo": "", "rel_path": rel}

        if "/" not in path or folder in OWN_FOLDERS:
            row["classification"] = "ORIGINAL"
        elif folder not in UPSTREAM:
            row["classification"] = "UNKNOWN_FOLDER"
        else:
            repo, name = UPSTREAM[folder]
            row["upstream_repo"] = repo
            utree = ups[name]
            if rel in utree:
                if utree[rel] == sha:
                    row["classification"] = "COPY_IDENTICAL"
                else:
                    row["classification"] = "NEEDS_PROBE_OLD"
                    need_probe.append((sha, repo, path))
            else:
                row["classification"] = "NEEDS_PROBE_GONE"
                need_probe.append((sha, repo, path))
        rows.append(row)

    with (OUT / "classified.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["path", "folder", "blob_sha", "classification",
                                           "upstream_repo", "rel_path"])
        w.writeheader()
        w.writerows(rows)

    seen = set()
    with (OUT / "need_probe.tsv").open("w", encoding="utf-8") as fh:
        for sha, repo, path in need_probe:
            key = (sha, repo)
            if key in seen:
                continue
            seen.add(key)
            fh.write(f"{sha}\t{repo}\t{path}\n")

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1
    for k in sorted(counts):
        print(f"  {k:22s} {counts[k]}")
    print(f"  total                  {len(rows)}")
    print(f"  unique blobs to probe  {len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
