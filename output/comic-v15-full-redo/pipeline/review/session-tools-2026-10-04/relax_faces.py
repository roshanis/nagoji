"""Write a relaxed FACES file: keep named cast and faces of at least MIN_R of the frame height; drop small background faces."""
import json, re, sys
from pathlib import Path
C, src, dst, min_r, words = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
note = sys.argv[6]
rev = Path('chapters') / C / 'review'
f = json.loads((rev / src).read_text())
cast = re.compile(words, re.I)
dropped = kept = 0
for p in f['panels']:
    before = len(p['faces'])
    p['faces'] = [x for x in p['faces'] if x['r'] >= min_r or cast.search(x.get('who', ''))]
    kept += len(p['faces']); dropped += before - len(p['faces'])
f['note'] = (f.get('note', '') + ' ' + note).strip()
(rev / dst).open('x').write(json.dumps(f, indent=1))
print(C, dst, 'kept', kept, 'dropped', dropped)
