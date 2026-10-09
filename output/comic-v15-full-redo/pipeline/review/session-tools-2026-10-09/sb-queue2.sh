cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
L=/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/review/solve-logs-2026-10-09; mkdir -p $L
run() { ch=$1; tag=$2; dec=$3; faces=$4; keep=$5; folio=$6; bash $S/solve_build.sh $ch ch$ch $tag $dec $faces $keep /tmp/claude-501/cache-ch$ch-$tag $folio r1 > $L/sb-ch$ch-$tag.log 2>&1; echo "ch$ch $tag exit $?: $(grep -E 'has no rows|layout ok' $L/sb-ch$ch-$tag.log | head -1 | cut -c1-60)"; }
case $1 in
A) run 17 s2 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 204; run 21 s2 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 256; run 24 s2 LEAN-SELECTION-drawn-r6.json FACES-v6.json KEEP-c6.json 296;;
B) run 23 s2 LEAN-SELECTION-drawn-r8.json FACES-v8.json KEEP-c8.json 278; run 26 s2 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 339; run 28 s1 LEAN-SELECTION-drawn-r4.json FACES-v4.json KEEP-c4.json 359;;
C) run 19 s2 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 227; run 22 s2 LEAN-SELECTION-drawn-r7.json FACES-v7.json KEEP-c7.json 265; run 27 s1 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 350;;
esac
echo QUEUE-$1-DONE
