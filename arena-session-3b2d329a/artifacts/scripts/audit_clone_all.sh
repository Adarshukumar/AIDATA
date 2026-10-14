#!/usr/bin/env bash
# API-free provenance audit of Adarshukumar/Python.
#
# A git blob SHA is a content hash. Partial clones (--filter=blob:none) fetch commits and
# trees but NOT file contents, so we get every path→blob-sha mapping (HEAD and full
# history) for ~kilobytes, with no GitHub API calls and no rate limit.
#
# Outputs (scratch): /tmp/audit/clones/*.git, /tmp/audit/out/{his,up}/<name>.tsv
set -uo pipefail

CLONES=/tmp/audit/clones
OUT=/tmp/audit/out
mkdir -p "$CLONES" "$OUT/his" "$OUT/up"

clone() { # repo, name
  local repo="$1"
  local name="$2"
  local dir="$CLONES/$name.git"
  if [ ! -d "$dir" ]; then
    git clone -q --filter=blob:none --bare "https://github.com/$repo.git" "$dir" 2>/dev/null \
      || { echo "CLONE FAILED: $repo"; return 1; }
  fi
  # HEAD paths
  git -C "$dir" ls-tree -r HEAD 2>/dev/null | awk '{print $3"\t"$4}' | sort > "$OUT/head__$name.tsv"
  # every blob that ever existed in the repo (full history), with sha only
  git -C "$dir" rev-list --objects --all 2>/dev/null | awk 'NF==2{print $1}' | sort -u > "$OUT/history__$name.tsv"
  printf "%-46s head=%-6s history=%s\n" "$repo" "$(wc -l < "$OUT/head__$name.tsv")" "$(wc -l < "$OUT/history__$name.tsv")"
}

echo "=== target ==="
clone Adarshukumar/Python target

echo "=== upstreams ==="
clone asabeneh/30-Days-Of-Python                30-Days-Of-Python
clone TheAlgorithms/Python                      TheAlgorithms-Python
clone keon/algorithms                           algorithms
clone CoreyMSchafer/code_snippets               CoreySchafer-code-snippets
clone jakevdp/PythonDataScienceHandbook         PythonDataScienceHandbook
clone d2l-ai/d2l-en                             dive-into-deep-learning
clone fastai/fastbook                           fastbook
clone miguelgrinberg/flasky                     flasky
clone trekhleb/homemade-machine-learning        homemade-machine-learning
clone donnemartin/interactive-coding-challenges interactive-coding-challenges
clone trekhleb/learn-python                     learn-python
clone karpathy/micrograd                        micrograd
clone rasbt/python-machine-learning-book-3rd-edition ml-book-3rd-edition
clone graykode/nlp-tutorial                     nlp-tutorial
clone karpathy/nn-zero-to-hero                  nn-zero-to-hero
clone practical-tutorials/project-based-learning project-based-learning
clone wesm/pydata-book                          pydata-book
clone gto76/python-cheatsheet                   python-cheatsheet
clone Python-World/python-mini-projects         python-mini-projects
clone norvig/pytudes                            pytudes
clone openai/spinningup                         spinningup
clone kyclark/tiny_python_projects              tiny-python-projects
clone satwikkansal/wtfpython                    wtf-python
clone MunGell/awesome-for-beginners             awesome-for-beginners
clone vinta/awesome-python                      awesome-python
clone codecrafters-io/build-your-own-x          build-your-own-x
# NOTE: rasbt/machine-learning-book removed - replaced by 3rd-edition repo above

echo "=== disk ==="
du -sh "$CLONES" 2>/dev/null
