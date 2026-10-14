#!/usr/bin/env bash
# Claude Code-style SessionStart hook: load memory into a fresh session's context.
# Prints the live state and the newest log entry, then exits 0.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== SESSION_STATE.md ==="
cat SESSION_STATE.md

echo
echo "=== newest log entry ==="
newest=$(ls logs/ | grep -E '^[0-9]{4}-' | sort | tail -1 || true)
if [ -n "${newest:-}" ]; then
  echo "--- logs/$newest ---"
  cat "logs/$newest"
else
  echo "(no log entries yet)"
fi

echo
echo "=== uncommitted memory changes ==="
git -C .. status --short -- arena-session-3b2d329a || true
