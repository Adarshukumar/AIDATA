#!/usr/bin/env bash
# Step 3b: explain the files whose blob exists in NO upstream object database.
#
# Hypothesis (verified here): the target repo was committed from a working tree where
# git normalised CRLF line endings (core.autocrlf=true on Windows), so files that upstream
# stores with CRLF appear in the target with LF. Content is otherwise byte-identical.
#
# For every not-found probe result:
#   his blob   <- GET /repos/Adarshukumar/Python/git/blobs/<sha>   (base64, decoded)
#   upstream   <- git show HEAD:<rel_path>  from the local partial clone
# verdicts: COPY_LINE_ENDINGS  (identical after stripping CR)
#           UNKNOWN            (still different -> manual review)
#
# Output: /tmp/audit/out/lineendings.tsv   <target_path>\t<verdict>\t<detail>
set -uo pipefail

CLONES=/tmp/audit/clones
OUT=/tmp/audit/out/lineendings.tsv
PROBES=/tmp/audit/out/probe_results.tsv

clone_dir() { # repo -> local clone dir name
  case "$1" in
    asabeneh/30-Days-Of-Python) echo 30-Days-Of-Python ;;
    TheAlgorithms/Python) echo TheAlgorithms-Python ;;
    keon/algorithms) echo algorithms ;;
    CoreyMSchafer/code_snippets) echo CoreySchafer-code-snippets ;;
    jakevdp/PythonDataScienceHandbook) echo PythonDataScienceHandbook ;;
    d2l-ai/d2l-en) echo dive-into-deep-learning ;;
    fastai/fastbook) echo fastbook ;;
    miguelgrinberg/flasky) echo flasky ;;
    trekhleb/homemade-machine-learning) echo homemade-machine-learning ;;
    donnemartin/interactive-coding-challenges) echo interactive-coding-challenges ;;
    trekhleb/learn-python) echo learn-python ;;
    karpathy/micrograd) echo micrograd ;;
    rasbt/python-machine-learning-book-3rd-edition) echo ml-book-3rd-edition ;;
    graykode/nlp-tutorial) echo nlp-tutorial ;;
    karpathy/nn-zero-to-hero) echo nn-zero-to-hero ;;
    practical-tutorials/project-based-learning) echo project-based-learning ;;
    wesm/pydata-book) echo pydata-book ;;
    gto76/python-cheatsheet) echo python-cheatsheet ;;
    Python-World/python-mini-projects) echo python-mini-projects ;;
    norvig/pytudes) echo pytudes ;;
    openai/spinningup) echo spinningup ;;
    kyclark/tiny_python_projects) echo tiny-python-projects ;;
    satwikkansal/wtfpython) echo wtf-python ;;
    MunGell/awesome-for-beginners) echo awesome-for-beginners ;;
    vinta/awesome-python) echo awesome-python ;;
    codecrafters-io/build-your-own-x) echo build-your-own-x ;;
    *) echo "" ;;
  esac
}

: > "$OUT"
awk -F'\t' '$2==0{print $1"\t"$3"\t"$4}' "$PROBES" | while IFS=$'\t' read -r sha repo path; do
  [ -z "${sha:-}" ] && continue
  dir=$(clone_dir "$repo")
  folder=${path%%/*}
  rel=${path#"$folder"/}

  his=$(gh api "repos/Adarshukumar/Python/git/blobs/$sha" --jq .content 2>/dev/null | base64 -d 2>/dev/null)
  up=$(git -C "$CLONES/$dir.git" show "HEAD:$rel" 2>/dev/null)

  if [ -z "${his:-}" ] || [ -z "${up:-}" ]; then
    printf "%s\tUNKNOWN\tcould not fetch one side\n" "$path" >> "$OUT"
    continue
  fi
  if [ "$(printf '%s' "$his" | tr -d '\r')" = "$(printf '%s' "$up" | tr -d '\r')" ]; then
    printf "%s\tCOPY_LINE_ENDINGS\tupstream CRLF -> his LF, content otherwise identical\n" "$path" >> "$OUT"
  else
    printf "%s\tUNKNOWN\tcontent differs beyond line endings\n" "$path" >> "$OUT"
  fi
done

echo "verdicts:"
awk -F'\t' '{print $2}' "$OUT" | sort | uniq -c
echo "wrote $OUT"
