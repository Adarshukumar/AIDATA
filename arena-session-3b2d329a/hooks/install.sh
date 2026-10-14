#!/usr/bin/env bash
# Install the always-on memory hook into .git/hooks/ (local to this clone).
set -euo pipefail
SESSION_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(git -C "$SESSION_DIR" rev-parse --show-toplevel)"
SRC="$SESSION_DIR/hooks/pre_commit_log.py"
DST="$REPO/.git/hooks/pre-commit"
REL="${SESSION_DIR#"$REPO"/}"

[ -f "$SRC" ] || { echo "error: $SRC not found" >&2; exit 1; }
cat > "$DST" <<HOOK
#!/usr/bin/env bash
# Managed by $REL — do not edit by hand.
set -euo pipefail
python3 "$SRC"
git add "$REL/logs/auto-commit-log.md" >/dev/null 2>&1 || true
HOOK
chmod +x "$DST"
echo "installed: .git/hooks/pre-commit → logs every commit to $REL/logs/auto-commit-log.md"
