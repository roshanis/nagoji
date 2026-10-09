cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
set +e
D=LEAN-SELECTION-drawn-split-r2.json
( runb 5 ch05-split2 s2-b chapters/ch05-split2/LAYOUT-solved-s1.json 32 r4 $D FACES-s2.json KEEP-s2.json "--unpainted --no-backup" > /tmp/claude-501/build-ch05-r4.log 2>&1
  runb 10 ch10-split2 s2c-b chapters/ch10-split2/LAYOUT-solved-s1c.json 96 r2 $D FACES-s2.json KEEP-s2.json "--unpainted --no-backup" > /tmp/claude-501/build-ch10-r2.log 2>&1 ) &
( runb 6 ch06-split s2-b chapters/ch06-split/LAYOUT-solved-s1.json 42 r8 $D FACES-s2.json KEEP-s2.json "--unpainted --no-backup" > /tmp/claude-501/build-ch06-r8.log 2>&1
  runb 11 ch11-split2 s2c-b chapters/ch11-split2/LAYOUT-solved-s1c.json 109 r3 $D FACES-s2.json KEEP-s2.json "--unpainted --no-backup" > /tmp/claude-501/build-ch11-r3.log 2>&1 ) &
wait
echo ALL-DONE
