# Lettering-only rebuild of ch5-13 with the no-crossing tails rule (reserves.place_boxes uncross, 2026-10-09), the ch6 11.5
# face fix and the Varma redraws (ch10 12.5, ch11 3.5, 4.5, 17.2). Same layouts and folios as the last builds; new b tag u1-b.
cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
export TMPDIR=/tmp/claude-501
source pipeline/review/session-tools-2026-10-04/run-b-only.sh
X="--unpainted --no-backup"
runb 5  ch05-split2 u1-b chapters/ch05-split2/LAYOUT-solved-s1.json  32  r6  LEAN-SELECTION-drawn-split-r5.json FACES-s5.json KEEP-s5.json "$X"
runb 6  ch06-split  u1-b chapters/ch06-split/LAYOUT-solved-s1.json   42  r10 LEAN-SELECTION-drawn-split-r4.json FACES-s4.json KEEP-s4.json "$X"
runb 8  ch08-split  u1-b chapters/ch08-split/LAYOUT-solved-s1c.json  66  r7  LEAN-SELECTION-drawn-split-r4.json FACES-s4.json KEEP-s4.json "$X"
runb 10 ch10-split2 u1-b chapters/ch10-split2/LAYOUT-solved-s1c.json 96  r4  LEAN-SELECTION-drawn-split-r3.json FACES-s3.json KEEP-s3.json "$X"
runb 11 ch11-split2 u1-b chapters/ch11-split2/LAYOUT-solved-s1c.json 109 r5  LEAN-SELECTION-drawn-split-r4.json FACES-s4.json KEEP-s4.json "$X"
runb 12 ch12-split2 u1-b chapters/ch12-split2/LAYOUT-solved-s2c.json 133 r8  LEAN-SELECTION-drawn-split-r5.json FACES-s5.json KEEP-s5.json "$X"
runb 13 ch13-split  u1-b chapters/ch13-split/LAYOUT-solved-s1.json   144 r2  LEAN-SELECTION-drawn-split-r1.json FACES-s1.json KEEP-s1.json "$X"
echo REBUILD-5-13-DONE
