cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
set +e
( runb 1 ch01-v2 d9t-b chapters/ch01-v2/LAYOUT-fitted-d9.json 1 r15 LEAN-SELECTION-drawn-merged-d4.json FACES-v4.json KEEP-c4.json "" > /tmp/claude-501/build-ch01-r15.log 2>&1
  runb 3 ch03 s12t-b chapters/ch03/LAYOUT-fitted-s12.json 16 r11 LEAN-SELECTION-drawn-merged-r16.json FACES-v2f.json KEEP-c11.json "" > /tmp/claude-501/build-ch03-r11.log 2>&1 ) &
( runb 2 ch02 d6t-b chapters/ch02/LAYOUT-fitted-d6.json 10 r5 LEAN-SELECTION-drawn-merged-d5.json FACES-v7.json KEEP-c8.json "" > /tmp/claude-501/build-ch02-r5.log 2>&1
  runb 4 ch04 s13t-b chapters/ch04/LAYOUT-fitted-s13.json 26 r15 LEAN-SELECTION-drawn-merged-r15.json FACES-v2h.json KEEP-c14.json "--style=page-06-panel-02:0=unreadable" > /tmp/claude-501/build-ch04-r15.log 2>&1 ) &
wait
echo ALL-DONE
