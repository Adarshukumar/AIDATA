#!/usr/bin/env bash
# Claude Code-style Stop hook: end-of-turn checkpoint warning.
# Exit 0 always (a Stop hook that blocks must be deliberate; this one just warns).
cd "$(dirname "$0")/.."

dirty=$(git -C .. status --short -- arena-session-3b2d329a | wc -l | tr -d ' ')
if [ "$dirty" != "0" ]; then
  echo "WARNING: $dirty uncommitted file(s) in arena-session-3b2d329a/ — memory is not safe yet." >&2
  git -C .. status --short -- arena-session-3b2d329a >&2
fi
exit 0
