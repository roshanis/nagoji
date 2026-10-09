"""Write a new decisions round with accepted fix versions and corrected tail targets, plus FACES and KEEP files that
carry each new version's zones over from the version it was edited from (region edits keep the composition).
Never overwrites. Usage: apply_picks.py PKG DEC_IN DEC_OUT FACES_IN FACES_OUT KEEP_IN KEEP_OUT CHANGES.json
CHANGES.json: {"picks": {"page-03-panel-04": "v03", ...}, "tails": {"page-11-panel-02": [{"copy_index":0,"x":..,"y":..}, ...]},
               "note": "..."}"""
import json, copy, sys
from pathlib import Path
pkg, dec_in, dec_out, f_in, f_out, k_in, k_out, changes = sys.argv[1:9]
R = Path('chapters') / pkg / 'review'
ch = json.loads(Path(changes).read_text())
d = json.loads((R / dec_in).read_text())
old = {}
for x in d['decisions']:
    if x['id'] in ch.get('picks', {}):
        old[x['id']] = x['pick']
        x['backup'], x['backup_tails'], x['backup_faces'] = x['pick'], x.get('tails', []), x.get('faces', [])
        x['pick'] = ch['picks'][x['id']]
    if x['id'] in ch.get('tails', {}):
        x['tails'] = [{'copy_index': t['copy_index'], 'x': t['x'], 'y': t['y']} for t in ch['tails'][x['id']]]
assert set(old) == set(ch.get('picks', {})), set(ch.get('picks', {})) - set(old)
d['round'] = dec_out[len('LEAN-SELECTION-drawn-'):-5]
d['about_' + d['round']] = ch.get('note', '')
(R / dec_out).open('x').write(json.dumps(d, indent=1, ensure_ascii=False))
for fi, fo in ((f_in, f_out), (k_in, k_out)):
    g = json.loads((R / fi).read_text()); have = {(p['id'], p['version']) for p in g['panels']}
    add = []
    for pid, v_old in old.items():
        src = [p for p in g['panels'] if p['id'] == pid and p['version'] == v_old]
        assert src, (fi, pid, v_old)
        if (pid, ch['picks'][pid]) not in have:
            q = copy.deepcopy(src[0]); q['version'] = ch['picks'][pid]; add.append(q)
    g['panels'] += add
    (R / fo).open('x').write(json.dumps(g, indent=1, ensure_ascii=False))
print(pkg, dec_out, 'picks', ch.get('picks', {}), 'tails', list(ch.get('tails', {})))
