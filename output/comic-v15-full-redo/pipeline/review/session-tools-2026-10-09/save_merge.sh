# Save a finished selection workflow's output to review-sheets and fold it into the chapter's decisions.
# Usage: bash save_merge.sh TASK_ID CH ROUND   (ROUND 1: save_first_round.py; ROUND 2+: merge_round.py from round N-1)
set -e
T=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/tasks
S=/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad
P=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
export PYTHONDONTWRITEBYTECODE=1
cd /Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo
ID=$1; CH=$2; R=$3; OUT=review-sheets/SELECT-ZONES-ch$CH-r$R-2026-10-08.json
[ -e $OUT ] && { echo "$OUT exists"; exit 1; }
cp $T/$ID.output $OUT
$P -c "
import json,sys;d=json.load(open('$OUT'));r=d['result']
f=[z['kind'] for z in r['zones'] if not z.get('result')]
print('failed pages', r['selections'][0].get('failedPages'), '| empty zone results', f)"
if [ $R = 1 ]; then $P $S/save_first_round.py $OUT ch$CH
else
  Q=$((R-1)); FP=$( [ $Q = 1 ] && echo FACES-v1.json || echo FACES-v$Q.json ); KP=$( [ $Q = 1 ] && echo KEEP-c1.json || echo KEEP-c$Q.json )
  $P pipeline/review/session-tools-2026-10-04/merge_round.py $OUT ch$CH LEAN-SELECTION-drawn-r$Q.json LEAN-SELECTION-drawn-r$R.json $FP FACES-v$R.json $KP KEEP-c$R.json
fi
Z=chapters/ch$CH/review; if [ $R = 1 ]; then $P $S/norm_versions.py $Z/KEEP-c1.json $Z/FACES-v1.json; else $P $S/norm_versions.py $Z/KEEP-c$R.json $Z/FACES-v$R.json; fi
