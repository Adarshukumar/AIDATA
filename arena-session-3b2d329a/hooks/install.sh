#!/usr/bin/env bash
# Install the always-on memory hooks into .git/hooks/ of this repository.
#
#   bash arena-session-3b2d329a/hooks/install.sh
#
# Installs a pre-commit hook that appends every commit to
# arena-session-3b2d329a/logs/auto-commit-log.md and — when the commit did not already
# touch the memory folder — stages that log so the entry rides along with the next commit.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HOOK_SRC="$REPO_ROOT/arena-session-3b2d329a/hooks/pre_commit_log.py"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -f "$HOOK_SRC" ]; then
  echo "error: $HOOK_SRC not found" >&2
  exit 1
fi

cat > "$HOOK_DST" <<EOF
#!/usr/bin/env bash
# Managed by arena-session-3b2d329a — do not edit by hand.
set -euo pipefail
python3 "$HOOK_SRC"
git add arena-session-3b2d329a/logs/auto-commit-log.md >/dev/null 2>&1 || true
EOF

chmod +x "$HOOK_DST"
echo "installed: .git/hooks/pre-commit → logs every commit to logs/auto-commit-log.md"
