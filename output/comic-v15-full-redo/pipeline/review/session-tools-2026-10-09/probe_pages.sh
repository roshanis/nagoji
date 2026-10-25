cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501 PYTHONDONTWRITEBYTECODE=1
P=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
run() { REFINE=1 $P $S/solve_bars.py $1 chapters/$2 $3 chapters/$2/review/$4 $5 /tmp/claude-501/probe-$2 0.34 5 > /dev/null 2>&1; echo "ch$1 p$5 $?"; }
run 7 ch07 s5 LEAN-SELECTION-drawn-merged-r3.json 5 & run 7 ch07 s5 LEAN-SELECTION-drawn-merged-r3.json 7 & run 7 ch07 s5 LEAN-SELECTION-drawn-merged-r3.json 8 &
run 14 ch14-split s1 LEAN-SELECTION-drawn-split-r1.json 6 & run 14 ch14-split s1 LEAN-SELECTION-drawn-split-r1.json 7 &
run 16 ch16-split s1 LEAN-SELECTION-drawn-split-r1.json 9 & run 16 ch16-split s1 LEAN-SELECTION-drawn-split-r1.json 13 & run 16 ch16-split s1 LEAN-SELECTION-drawn-split-r1.json 16 &
run 25 ch25-split2 s1 LEAN-SELECTION-drawn-split-r1.json 11 & run 25 ch25-split2 s1 LEAN-SELECTION-drawn-split-r1.json 12 &
wait; echo PROBES-DONE
