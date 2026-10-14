#!/usr/bin/env bash
# Install the always-on memory hook into .git/hooks/ (local to this clone).
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$REPO/arena-session-3b2d329a/hooks/pre_commit_log.py"
DST="$REPO/.git/hooks/pre-commit"

[ -f "$SRC" ] || { echo "error: $SRC not found" >&2; exit 1; }
cat > "$DST" <<HOOK
#!/usr/bin/env bash
# Managed by arena-session-3b2d329a — do not edit by hand.
set -euo pipefail
python3 "$SRC"
git add arena-session-3b2d329a/logs/auto-commit-log.md >/dev/null 2>&1 || true
HOOK
chmod +x "$DST"
echo "installed: .git/hooks/pre-commit → logs every commit to logs/auto-commit-log.md"
