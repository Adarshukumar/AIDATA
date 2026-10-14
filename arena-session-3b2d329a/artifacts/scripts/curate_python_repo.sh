#!/usr/bin/env bash
# Curate Adarshukumar/Python — runs the attribution cleanup as a pull request.
#
# WHAT IT DOES
#   1. clones the repo fresh, creates branch `arena/attribution-cleanup`
#   2. removes 10 folders: the 4 with no license upstream (can't be redistributed) and the
#      6 with extremely popular upstreams (linked from CREDITS.md instead)
#   3. installs the new README.md + CREDITS.md (from this folder, or from GitHub raw)
#   4. commits, pushes, and opens a pull request
#
# RESULT: 9,007 files -> 5,772 files, with full attribution for everything kept.
#
# USAGE (needs write access to Adarshukumar/Python — `gh auth status` must show it):
#   bash curate_python_repo.sh
#
set -euo pipefail

REPO="Adarshukumar/Python"
BRANCH="arena/attribution-cleanup"
WORK="${WORK:-/tmp/px-cleanup}"

# where the new README/CREDITS live: prefer a local AIDATA checkout, else GitHub raw
LOCAL_CURATION="$(cd "$(dirname "$0")/../curation" 2>/dev/null && pwd || echo "")"
RAW_BASE="https://raw.githubusercontent.com/Adarshukumar/AIDATA/arena/3b2d329a-aidata/arena-session-3b2d329a/artifacts/curation"

REMOVE=(
  "30-Days-Of-Python"
  "TheAlgorithms-Python"
  "PythonDataScienceHandbook"
  "interactive-coding-challenges"
  "project-based-learning"
  "python-cheatsheet"
  "wtf-python"
  "awesome-for-beginners"
  "awesome-python"
  "build-your-own-x"
)

echo "==> clone"
rm -rf "$WORK"
git clone -q --filter=blob:none "https://github.com/$REPO.git" "$WORK"
cd "$WORK"
git checkout -q -b "$BRANCH"

echo "==> remove ${#REMOVE[@]} folders"
git rm -r -q --ignore-unmatch "${REMOVE[@]}"

echo "==> install README.md + CREDITS.md"
if [ -n "$LOCAL_CURATION" ] && [ -f "$LOCAL_CURATION/CREDITS.md" ]; then
  cp "$LOCAL_CURATION/CREDITS.md" "$LOCAL_CURATION/README.md" .
else
  curl -fsSL "$RAW_BASE/CREDITS.md" -o CREDITS.md
  curl -fsSL "$RAW_BASE/README.md"  -o README.md
fi

echo "==> commit"
git add -A
git commit -q -m "Curate the collection: remove unlicensed & very popular copies, add full CREDITS.md

Removed folders with no license upstream (redistribution not permitted):
  30-Days-Of-Python, awesome-for-beginners, build-your-own-x, python-cheatsheet
Removed extremely popular upstreams (use the original, linked in CREDITS.md):
  TheAlgorithms-Python (225k*), awesome-python (327k*), project-based-learning (287k*),
  PythonDataScienceHandbook (50k*), interactive-coding-challenges (32k*), wtf-python (37k*)
Added: CREDITS.md (folder -> upstream -> license -> authors) and an honest README.
Every kept folder retains its upstream LICENSE."

echo "==> push"
git push -q -u origin "$BRANCH"
echo "pushed $BRANCH"

echo "==> open PR"
gh pr create --repo "$REPO" --base main --head "$BRANCH" \
  --title "Curate collection: remove unlicensed/popular copies + add CREDITS.md" \
  --body-file "$LOCAL_CURATION/PR_BODY_cleanup.md" 2>/dev/null \
  || gh pr create --repo "$REPO" --base main --head "$BRANCH" \
       --title "Curate collection: remove unlicensed/popular copies + add CREDITS.md" \
       --body "Removes 10 folders (4 unlicensed, 6 very popular) and adds CREDITS.md with full attribution. See arena-session-3b2d329a/logs/0010 for details."

echo "done. review the PR on GitHub."
