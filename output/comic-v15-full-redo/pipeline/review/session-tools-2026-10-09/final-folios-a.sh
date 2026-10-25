# Final folios (folios.py, 2026-10-09): ch25 lettering rebuild (no-crossing tails), folio-only builds of ch22, ch26, ch27.
cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501 PYTHONDONTWRITEBYTECODE=1
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
runb 25 ch25-split2 u1-b chapters/ch25-split2/LAYOUT-solved-s1.json 363 r2 LEAN-SELECTION-drawn-split-r1.json FACES-s1.json KEEP-s1.json "--unpainted --no-backup"
fb() { pk=""; [ "$2" != "ch$1" ] && pk="--package-dir chapters/$2"; echo "== $2 folio build $6 at $5"
  $P pipeline/run_chapter.py build --chapter $1 $pk --manifest chapters/$2/SELECTION-INPUT-$3.json --layout chapters/$2/$4 --first-folio $5 --revision $6 2>&1 | grep -v "OMP\|^((" | tail -6; }
fb 22 ch22-split s1-b LAYOUT-solved-s1.json 292 r2
fb 26 ch26-split s1-b LAYOUT-solved-s1.json 377 r2
fb 27 ch27 s2-b LAYOUT-solved-s2.json 390 r2
echo FINAL-FOLIOS-A-DONE
