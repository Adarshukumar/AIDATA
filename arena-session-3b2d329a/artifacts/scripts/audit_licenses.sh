#!/usr/bin/env bash
# License pass of the provenance audit.
#
# For every upstream: SPDX id from the GitHub API (26 calls) + whether the license text
# survived inside the copied folder of the target repo (checked offline from the local
# partial clone). Output: /tmp/audit/out/licenses.tsv
#   lines: <folder>\t<repo>\t<spdx|NONE>\t<license_file_in_copy: yes|no>\t<files>
set -uo pipefail

CLONES=/tmp/audit/clones
OUT=/tmp/audit/out/licenses.tsv
TARGET="$CLONES/target.git"

PAIRS="
30-Days-Of-Python|asabeneh/30-Days-Of-Python
TheAlgorithms-Python|TheAlgorithms/Python
algorithms|keon/algorithms
CoreySchafer-code-snippets|CoreyMSchafer/code_snippets
PythonDataScienceHandbook|jakevdp/PythonDataScienceHandbook
dive-into-deep-learning|d2l-ai/d2l-en
fastbook|fastai/fastbook
flasky|miguelgrinberg/flasky
homemade-machine-learning|trekhleb/homemade-machine-learning
interactive-coding-challenges|donnemartin/interactive-coding-challenges
learn-python|trekhleb/learn-python
micrograd|karpathy/micrograd
ml-book-3rd-edition|rasbt/python-machine-learning-book-3rd-edition
nlp-tutorial|graykode/nlp-tutorial
nn-zero-to-hero|karpathy/nn-zero-to-hero
project-based-learning|practical-tutorials/project-based-learning
pydata-book|wesm/pydata-book
python-cheatsheet|gto76/python-cheatsheet
python-mini-projects|Python-World/python-mini-projects
pytudes|norvig/pytudes
spinningup|openai/spinningup
tiny-python-projects|kyclark/tiny_python_projects
wtf-python|satwikkansal/wtfpython
awesome-for-beginners|MunGell/awesome-for-beginners
awesome-python|vinta/awesome-python
build-your-own-x|codecrafters-io/build-your-own-x
"

: > "$OUT"
for pair in $PAIRS; do
  folder="${pair%%|*}"; repo="${pair##*|}"
  spdx=$(gh api "repos/$repo" --jq 'if .license then .license.spdx_id else "NONE" end' 2>/dev/null)
  kept=$(git -C "$TARGET" ls-tree -r -z HEAD 2>/dev/null | tr '\0' '\n' \
        | awk -F'\t' -v f="$folder/" 'index($2, f)==1 && tolower($2) ~ /license|licence|copying/ {print; found=1} END{}' \
        | head -1)
  [ -n "$kept" ] && k=yes || k=no
  n=$(git -C "$TARGET" ls-tree -r -z HEAD 2>/dev/null | tr '\0' '\n' \
      | awk -F'\t' -v f="$folder/" 'index($2, f)==1' | wc -l)
  printf "%s\t%s\t%s\t%s\t%s\n" "$folder" "$repo" "${spdx:-NONE}" "$k" "$n" >> "$OUT"
  printf "  %-32s %-46s %-12s license-in-copy=%s\n" "$folder" "$repo" "${spdx:-NONE}" "$k"
done
echo "wrote $OUT"
