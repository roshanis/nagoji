# Lettering rebuilds (no-crossing tails; ch16 Varma redraw 13.3; ch20 priest tail 14.3) at the final folios, and folio-only
# builds of ch15 and ch19 (their b-pass geometry already has the new rules). Folios from folios.py (2026-10-09).
cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501 PYTHONDONTWRITEBYTECODE=1
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
X="--unpainted --no-backup"
runb 16 ch16-split  u1-b chapters/ch16-split/LAYOUT-solved-s1.json  195 r2 LEAN-SELECTION-drawn-split-r2.json FACES-s2.json KEEP-s2.json "$X"
runb 18 ch18-split  u1-b chapters/ch18-split/LAYOUT-solved-s1.json  234 r2 LEAN-SELECTION-drawn-split-r1.json FACES-s1.json KEEP-s1.json "$X"
runb 20 ch20-split2 u1-b chapters/ch20-split2/LAYOUT-solved-s2.json 262 r2 LEAN-SELECTION-drawn-split-r2.json FACES-s2.json KEEP-s2.json "$X"
for x in "15 ch15-split s1-b LAYOUT-solved-s1.json 177" "19 ch19 s3-b LAYOUT-solved-s3.json 250"; do set -- $x
  pk=""; [ "$2" != "ch$1" ] && pk="--package-dir chapters/$2"
  echo "== $2 folio build r2"
  $P pipeline/run_chapter.py build --chapter $1 $pk --manifest chapters/$2/SELECTION-INPUT-$3.json --layout chapters/$2/$4 --first-folio $5 --revision r2 2>&1 | grep -v "OMP\|^((" | tail -6
done
echo REBUILD-16-20-DONE
