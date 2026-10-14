#!/usr/bin/env bash
# v2 (fixed) — API-free HEAD-tree extraction for the provenance audit.
#
# v1 failure (see logs/0004): it also ran `git rev-list --objects --all` to collect the
# full-history blob set. In a blobless partial clone (--filter=blob:none) that command
# triggers one lazy fetch per missing blob; on a 9,007-file repo it ran 28+ minutes and
# was still going, downloading small packs one after another.
#
# v2 therefore collects ONLY `git ls-tree -r HEAD` (trees are present locally, so this is
# instant and offline). The "does this blob exist in upstream history" question is
# answered later with the GitHub API (`GET /repos/{o}/{r}/git/blobs/{sha}`) for the small
# set of differing files (~210), instead of walking history.
#
# Output: /tmp/audit/out/head__<name>.tsv   lines: <blob_sha>\t<path>
set -uo pipefail

CLONES=/tmp/audit/clones
OUT=/tmp/audit/out
mkdir -p "$CLONES" "$OUT"

head_tree() { # repo, name
  local repo="$1"
  local name="$2"
  local dir="$CLONES/$name.git"
  if [ ! -d "$dir" ]; then
    git clone -q --filter=blob:none --bare "https://github.com/$repo.git" "$dir" 2>/dev/null \
      || { echo "  CLONE FAILED: $repo"; return 1; }
  fi
  # -z: never C-quote paths (git's default quotepath wraps the one Cyrillic path in the
  # 30-Days-Of-Python repo in quotes with octal escapes, which broke folder matching).
  git -C "$dir" ls-tree -r -z HEAD 2>/dev/null | tr '\0' '\n' \
    | awk -F'\t' '$1 ~ / blob /{split($1,a," "); print a[3]"\t"$2}' \
    | sort > "$OUT/head__$name.tsv"
  printf "  %-48s %6s blobs\n" "$repo" "$(wc -l < "$OUT/head__$name.tsv")"
}

echo "=== target (his repo) ==="
head_tree Adarshukumar/Python target

echo "=== upstreams ==="
head_tree asabeneh/30-Days-Of-Python                   30-Days-Of-Python
head_tree TheAlgorithms/Python                         TheAlgorithms-Python
head_tree keon/algorithms                              algorithms
head_tree CoreyMSchafer/code_snippets                  CoreySchafer-code-snippets
head_tree jakevdp/PythonDataScienceHandbook            PythonDataScienceHandbook
head_tree d2l-ai/d2l-en                                 dive-into-deep-learning
head_tree fastai/fastbook                              fastbook
head_tree miguelgrinberg/flasky                        flasky
head_tree trekhleb/homemade-machine-learning           homemade-machine-learning
head_tree donnemartin/interactive-coding-challenges    interactive-coding-challenges
head_tree trekhleb/learn-python                        learn-python
head_tree karpathy/micrograd                           micrograd
head_tree rasbt/python-machine-learning-book-3rd-edition ml-book-3rd-edition
head_tree graykode/nlp-tutorial                        nlp-tutorial
head_tree karpathy/nn-zero-to-hero                     nn-zero-to-hero
head_tree practical-tutorials/project-based-learning   project-based-learning
head_tree wesm/pydata-book                             pydata-book
head_tree gto76/python-cheatsheet                      python-cheatsheet
head_tree Python-World/python-mini-projects            python-mini-projects
head_tree norvig/pytudes                               pytudes
head_tree openai/spinningup                            spinningup
head_tree kyclark/tiny_python_projects                 tiny-python-projects
head_tree satwikkansal/wtfpython                       wtf-python
head_tree MunGell/awesome-for-beginners                awesome-for-beginners
head_tree vinta/awesome-python                         awesome-python
head_tree codecrafters-io/build-your-own-x             build-your-own-x

echo "=== disk used by clone cache ==="
du -sh "$CLONES"
