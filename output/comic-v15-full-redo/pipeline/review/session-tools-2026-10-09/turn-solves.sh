cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
L=pipeline/review/solve-logs-2026-10-09
run() { bash $S/solve_build.sh $1 $2 s1 LEAN-SELECTION-drawn-split-r1.json FACES-s1.json KEEP-s1.json /tmp/claude-501/cache-$3-s1 $4 r1 > $L/sb-$2-s1.log 2>&1; echo "$2 exit $?: $(grep -E 'has no rows|minimum_ppi' $L/sb-$2-s1.log | head -1 | cut -c1-80)"; }
run 7 ch07-turn ch07turn 54 &
run 14 ch14-split2 ch14split2 165 &
run 16 ch16-split3 ch16split3 195 &
run 24 ch24-split2 ch24split2 331 &
run 25 ch25-split3 ch25split3 365 &
wait; echo TURN-SOLVES-DONE
