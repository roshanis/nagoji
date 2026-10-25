"""Merge a chapter's round-N selection workflow output into new merged decisions, faces and keep files (never overwrites)."""
import json, re, sys
from pathlib import Path
wf_out, C, dec_in, dec_out, f_in, f_out, k_in, k_out = sys.argv[1:9]
out = json.load(open(wf_out))['result']
rev = Path('chapters') / C / 'review'
pid = lambda i: (lambda m: f'page-{int(m[1]):02d}-panel-{int(m[2]):02d}' if m else i)(re.fullmatch(r'(\d+)\.(\d+)', i))
new = {d['id']: d for d in out['selections'][0]['decisions'] if d['pick']}
m = json.loads((rev / dec_in).read_text())
changed = []
for d in m['decisions']:
    n = new.get(d['id'])
    if n: changed.append((d['id'], d['pick'], n['pick'])); d.clear(); d.update(n)
known = {d['id'] for d in m['decisions']}
for d in out['selections'][0]['decisions']:     # a panel first drawn after round 1 (no earlier decision) joins here
    if d['id'] not in known: m['decisions'].append(d); changed.append((d['id'], None, d['pick']))
m['decisions'].sort(key=lambda d: d['id'])
m['round'] = dec_out[len('LEAN-SELECTION-'):-5]
(rev / dec_out).open('x').write(json.dumps(m, indent=1))
z = {x['kind']: x['result'] for x in out['zones'] if x}
f = json.loads((rev / f_in).read_text()); have = {(p['id'], p['version']) for p in f['panels']}
for p in (z.get('faces') or {}).get('panels', []):
    if (pid(p['id']), p['version']) not in have: f['panels'].append({'id': pid(p['id']), 'version': p['version'], 'faces': p['faces']})
(rev / f_out).open('x').write(json.dumps(f, indent=1))
k = json.loads((rev / k_in).read_text()); have = {(p['id'], p['version']) for p in k['panels']}
for p in (z.get('keep') or {}).get('panels', []):
    if (pid(p['id']), p['version']) not in have: k['panels'].append(dict(p, id=pid(p['id'])))
(rev / k_out).open('x').write(json.dumps(k, indent=1))
picks = {d['id']: d['pick'] for d in m['decisions']}
fk = {(p['id'], p['version']) for p in f['panels']}; kk = {(p['id'], p['version']) for p in k['panels']}
print(C, 'changed', len(changed), '| picked', sum(1 for v in picks.values() if v), 'of', len(picks),
      '| no pick', [i for i, v in picks.items() if not v],
      '| picks without faces', [i for i, v in picks.items() if v and (i, v) not in fk], '| without keep', [i for i, v in picks.items() if v and (i, v) not in kk])
