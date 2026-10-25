# Final folio-only builds after ch21 grew to 13 pages (2026-10-09): ch22 294, ch23 309, ch24 331, ch25 365, ch26 379,
# ch27 392, ch28 401. Each uses its final b-pass manifest and solved layout; new revision.
cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501 PYTHONDONTWRITEBYTECODE=1
P=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
fb() { pk=""; [ "$2" != "ch$1" ] && pk="--package-dir chapters/$2"; echo "== $2 folio build $6 at $5"
  $P pipeline/run_chapter.py build --chapter $1 $pk --manifest chapters/$2/SELECTION-INPUT-$3.json --layout chapters/$2/$4 --first-folio $5 --revision $6 2>&1 | grep -v "OMP\|^((" | grep -E "minimum_ppi|rror" ; }
fb 22 ch22-split  v2-b LAYOUT-solved-s1.json 294 r4
fb 23 ch23-split  v2-b LAYOUT-solved-s1.json 309 r4
fb 23 ch23-split  v2-b LAYOUT-solved-s1.json 309 r4
fb 28 ch28-split  v2-b LAYOUT-solved-s1.json 401 r4
echo FINAL-FOLIOS-B2-DONE
