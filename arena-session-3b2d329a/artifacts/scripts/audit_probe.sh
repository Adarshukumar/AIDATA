#!/usr/bin/env bash
# Step 3 of the provenance audit: resolve NEEDS_PROBE files against the upstream object DB.
#
# For each `<blob_sha>\t<upstream_repo>\t<path>` line in /tmp/audit/out/need_probe.tsv:
#   GET /repos/<upstream>/git/blobs/<sha>
#   HTTP 200 -> the blob exists in that upstream repo's history
#               -> the file is an upstream artefact (an earlier revision / removed file)
#               -> COPY_OLD_REV (or COPY_REMOVED_UP when its path is gone from HEAD)
#   HTTP 404 -> no upstream explanation -> UNKNOWN (manual review)
#
# Respects the 5,000-requests/hour core rate limit: checks /rate_limit first and only
# runs when enough quota is left. Output: /tmp/audit/out/probe_results.tsv
#   lines: <sha>\t<exists:1|0>\t<repo>\t<path>
set -uo pipefail

IN=/tmp/audit/out/need_probe.tsv
OUT=/tmp/audit/out/probe_results.tsv
JOBS="${JOBS:-6}"

[ -f "$IN" ] || { echo "missing $IN — run audit_classify.py first" >&2; exit 1; }
need=$(wc -l < "$IN")
left=$(gh api rate_limit --jq '.resources.core.remaining')
echo "blobs to probe: $need   |   API remaining: $left"
if [ "$left" -lt $((need + 50)) ]; then
  reset=$(gh api rate_limit --jq '.resources.core.reset')
  echo "NOT ENOUGH QUOTA. resets at $(date -u -d "@$reset" +%Y-%m-%dT%H:%M:%SZ)" >&2
  exit 2
fi

probe_one() {
  local sha="$1" repo="$2" path="$3"
  if gh api "repos/$repo/git/blobs/$sha" >/dev/null 2>&1; then
    printf "%s\t1\t%s\t%s\n" "$sha" "$repo" "$path"
  else
    printf "%s\t0\t%s\t%s\n" "$sha" "$repo" "$path"
  fi
}
export -f probe_one

: > "$OUT"
# 3 columns, tab separated; last field may be empty -> keep path optional
awk -F'\t' '{print $1"\t"$2"\t"$3}' "$IN" | \
  xargs -P "$JOBS" -d '\n' -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r s r p <<< "{}"; probe_one "$s" "$r" "$p"' >> "$OUT"

echo "probed: $(wc -l < "$OUT")  |  exists: $(awk -F'\t' '$2==1' "$OUT" | wc -l)  |  not-found: $(awk -F'\t' '$2==0' "$OUT" | wc -l)"
