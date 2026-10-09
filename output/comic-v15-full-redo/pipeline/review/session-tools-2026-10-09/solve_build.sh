# Whole V15 chapter pass for one package: first pass (lean_assemble, tag TAG-a), every page through solve_bars.py
# (keep_max 0.34, 1 pt refinement, eight pages at a time, probe answers cached in CACHE_DIR), the solved layout
# (LAYOUT-solved-TAG.json; stops if any page has no rows), the b-pass and build (run-b-only.sh), then the keep and bars
# audits. Run from output/comic-v15-full-redo with bash.
# Usage: bash solve_build.sh CH PKG TAG DECISIONS FACES KEEP CACHE_DIR FOLIO REV
set -e
CH=$1; PKG=$2; TAG=$3; DEC=$4; FACES=$5; KEEP=$6; CACHE=$7; FOLIO=$8; REV=$9
export TMPDIR=/tmp/claude-501 PYTHONDONTWRITEBYTECODE=1
P=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
R=chapters/$PKG/review
echo "== $PKG first pass $TAG-a"
$P $S/lean_assemble.py --chapter $CH --package chapters/$PKG --decisions $R/$DEC --tag $TAG-a --no-backup --draw \
  --faces-file $R/$FACES --face-scale 1.0 --keep-file $R/$KEEP --unpainted > $TMPDIR/$PKG-$TAG-a.json
grep -E '"selected"|"regenerate"' $TMPDIR/$PKG-$TAG-a.json
NP=$(grep -c "^## PAGE" scripts/CHAPTER-$(printf %02d $CH)-SCRIPT.md)
echo "== $PKG solve $NP pages"
mkdir -p $CACHE
for pg in $(seq 1 $NP); do
  REFINE=1 $P $S/solve_bars.py $CH chapters/$PKG $TAG $R/$DEC $pg $CACHE 0.34 5 > /dev/null 2>&1 &
  [ $((pg % 8)) -eq 0 ] && wait
done
wait
$P - <<EOF
import json, sys
rows, fills = {}, {}
for p in range(1, $NP + 1):
    d = json.load(open(f'$CACHE/page-{p:02d}.json'))
    if not d['rows']: sys.exit(f'page {p} has no rows')
    rows[str(p)] = d['rows']; fills[str(p)] = d['fill']
for k, v in rows.items():
    t = sum(r[0] if isinstance(r, list) else r for r in v)
    assert abs(t + 2 * (len(v) - 1) - 523.5) < 0.05, (k, t)
out = {'page_rows': rows, 'fitted_from': {'solver': 'scratchpad solve_bars.py: every grouping into rows of one or two, planner-verified at the final heights with keep_max 0.34, and each slot kept inside the shapes its cover crop can reach (worst-panel fill per page in page_fill)',
       'package': 'chapters/$PKG', 'manifest': 'chapters/$PKG/SELECTION-INPUT-$TAG-a.json', 'decisions': '$R/$DEC', 'faces': '$R/$FACES', 'keep': '$R/$KEEP', 'keep_max': 0.34, 'step_pt': 5, 'page_fill': fills}}
open('chapters/$PKG/LAYOUT-solved-$TAG.json', 'x').write(json.dumps(out, indent=1))
print('layout ok; fills', fills)
EOF
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
runb $CH $PKG $TAG-b chapters/$PKG/LAYOUT-solved-$TAG.json $FOLIO $REV $DEC $FACES $KEEP "--unpainted --no-backup"
$P $S/keep_audit.py chapters/$PKG $R/geometry-$TAG-b
$P $S/bars_audit.py $CH chapters/$PKG $R/geometry-$TAG-b chapters/$PKG/LAYOUT-solved-$TAG.json 0.9
echo "== $PKG done"
