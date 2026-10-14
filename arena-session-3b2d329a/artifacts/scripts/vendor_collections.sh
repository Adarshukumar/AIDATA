#!/usr/bin/env bash
# Vendor two curated collections into Adarshukumar/Python WITH attribution.
#
# Adds, as two new folders:
#   Python-Mini-Projects-Community/   <- ndleah/python-mini-project            (MIT, 131 projects)
#   All-In-One-Python-Projects/       <- king04aman/All-In-One-Python-Projects (MIT,  65 projects)
#
# Each keeps its upstream LICENSE file and gets a row in CREDITS.md. Junk is stripped
# (__pycache__, *.pyc, .DS_Store, .github, oversized blobs > 20 MB).
#
# USAGE (needs write access to Adarshukumar/Python):
#   bash vendor_collections.sh
#
set -euo pipefail

REPO="Adarshukumar/Python"
BRANCH="arena/vendor-collections"
WORK="${WORK:-/tmp/px-vendor}"
TMP="${TMP:-/tmp/vendor-src}"
MAX_MB=20

COLLECTIONS=(
  "ndleah/python-mini-project|Python-Mini-Projects-Community"
  "king04aman/All-In-One-Python-Projects|All-In-One-Python-Projects"
)

echo "==> clone target"
rm -rf "$WORK"; git clone -q --filter=blob:none "https://github.com/$REPO.git" "$WORK"
cd "$WORK"; git checkout -q -b "$BRANCH"

for entry in "${COLLECTIONS[@]}"; do
  src="${entry%%|*}"; dest="${entry##*|}"
  echo "==> $src -> $dest/"
  rm -rf "$TMP/$dest"
  git clone -q --depth 1 "https://github.com/$src.git" "$TMP/$dest"
  rm -rf "$TMP/$dest/.git" "$TMP/$dest/.github"

  # strip junk + oversized files
  find "$TMP/$dest" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
  find "$TMP/$dest" -type f \( -name '*.pyc' -o -name '.DS_Store' \) -delete 2>/dev/null || true
  find "$TMP/$dest" -type f -size +${MAX_MB}M -print -delete 2>/dev/null || true

  mkdir -p "$dest"
  cp -R "$TMP/$dest/." "$dest/"
  cat > "$dest/SOURCE.md" <<EOF
# Source

This folder is a **copy of an open-source project**, not my own work.

- Upstream: https://github.com/$src
- License: MIT (see \`LICENSE\` in this folder)
- Vendored: $(date -u +%Y-%m-%d)
- Attribution: see [/CREDITS.md](../CREDITS.md) at the repository root
EOF
done

echo "==> append rows to CREDITS.md"
python3 - <<'PY'
from pathlib import Path
p = Path("CREDITS.md")
if p.exists():
    text = p.read_text()
    rows = (
        "| `Python-Mini-Projects-Community` | [ndleah/python-mini-project](https://github.com/ndleah/python-mini-project) | MIT | [@ndleah](https://github.com/ndleah) + 100 contributors |\n"
        "| `All-In-One-Python-Projects` | [king04aman/All-In-One-Python-Projects](https://github.com/king04aman/All-In-One-Python-Projects) | MIT | [@king04aman](https://github.com/king04aman) + contributors |\n"
    )
    marker = "## Removed from this repository"
    if marker in text and "ndleah/python-mini-project" not in text:
        text = text.replace(marker, rows + "\n" + marker)
        p.write_text(text)
        print("CREDITS.md updated")
    else:
        print("CREDITS.md unchanged (already updated?)")
else:
    print("WARNING: no CREDITS.md found — run curate_python_repo.sh first")
PY

echo "==> commit + push + PR"
git add -A
git commit -q -m "Vendor two community Python collections with full attribution

- Python-Mini-Projects-Community/ <- ndleah/python-mini-project (MIT, 131 projects)
- All-In-One-Python-Projects/     <- king04aman/All-In-One-Python-Projects (MIT, 65 projects)
Both keep their LICENSE, get a SOURCE.md and a row in CREDITS.md.
Stripped __pycache__/.DS_Store/.github and files over ${MAX_MB} MB."
git push -q -u origin "$BRANCH"
gh pr create --repo "$REPO" --base main --head "$BRANCH" \
  --title "Add two community collections (fully credited)" \
  --body "Vendors ndleah/python-mini-project (MIT, 131 projects) and king04aman/All-In-One-Python-Projects (MIT, 65 projects). Both keep their upstream LICENSE, get a SOURCE.md, and are listed in CREDITS.md. Junk files stripped."
echo "done."
