cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
run() { ch=$1; dec=$2; faces=$3; keep=$4; folio=$5; bash $S/solve_build.sh $ch ch$ch s1 $dec $faces $keep /tmp/claude-501/cache-ch$ch-s1 $folio r1 > /tmp/claude-501/sb-ch$ch.log 2>&1; echo "ch$ch exit $?: $(grep -E 'has no rows|layout ok' /tmp/claude-501/sb-ch$ch.log | head -1 | cut -c1-80)"; }
if [ "$1" = A ]; then
run 13 LEAN-SELECTION-drawn-r6.json FACES-v6.json KEEP-c6.json 144
run 15 LEAN-SELECTION-drawn-r4.json FACES-v4.json KEEP-c4.json 169
run 17 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 204
run 21 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 256
run 24 LEAN-SELECTION-drawn-r6.json FACES-v6.json KEEP-c6.json 296
run 27 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 350
else
run 14 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 159
run 18 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 217
run 23 LEAN-SELECTION-drawn-r8.json FACES-v8.json KEEP-c8.json 278
run 26 LEAN-SELECTION-drawn-r5.json FACES-v5.json KEEP-c5.json 339
run 28 LEAN-SELECTION-drawn-r4.json FACES-v4.json KEEP-c4.json 359
fi
echo QUEUE-$1-DONE
