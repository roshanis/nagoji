# Lettering rebuilds after the second Varma redraws (LEAN-BATCH-196 to 199), at the final folios.
cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501 PYTHONDONTWRITEBYTECODE=1
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
X="--unpainted --no-backup"
runb 15 ch15-split v2-b chapters/ch15-split/LAYOUT-solved-s1.json 177 r3 LEAN-SELECTION-drawn-split-r2.json FACES-s2.json KEEP-s2.json "$X"
runb 22 ch22-split v2-b chapters/ch22-split/LAYOUT-solved-s1.json 292 r3 LEAN-SELECTION-drawn-split-r2.json FACES-s2.json KEEP-s2.json "$X"
runb 23 ch23-split v2-b chapters/ch23-split/LAYOUT-solved-s1.json 307 r3 LEAN-SELECTION-drawn-split-r2.json FACES-s2.json KEEP-s2.json "$X"
runb 28 ch28-split v2-b chapters/ch28-split/LAYOUT-solved-s1.json 399 r3 LEAN-SELECTION-drawn-split-r2.json FACES-s2.json KEEP-s2.json "$X"
echo REBUILD-VARMA2-DONE
