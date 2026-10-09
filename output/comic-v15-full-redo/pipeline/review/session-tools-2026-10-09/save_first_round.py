"""Save a chapter's first-round select-and-zones workflow output as LEAN-SELECTION-drawn-r1.json, FACES-v1.json and
KEEP-c1.json in chapters/<pkg>/review (never overwrites), plus REJECTED-r1.json: the panels with no acceptable
candidate and the reviewer's correction for each, ready for a v2 fix batch (build_v2_fix_batch.py, mode "generate").
Usage: save_first_round.py WORKFLOW_OUTPUT PKG"""
import json, re, sys
from pathlib import Path
wf_out, pkg = sys.argv[1:3]
out = json.load(open(wf_out))['result']
rev = Path('chapters') / pkg / 'review'; rev.mkdir(parents=True, exist_ok=True)
pid = lambda i: (lambda m: f'page-{int(m[1]):02d}-panel-{int(m[2]):02d}' if m else i)(re.fullmatch(r'(\d+)\.(\d+)', i))
sel = out['selections'][0]
decisions = sel['decisions']
missing = [d['id'] for d in decisions if not d['pick']]
(rev / 'LEAN-SELECTION-drawn-r1.json').open('x').write(json.dumps({'chapter': sel['chapter'], 'round': 'drawn-r1', 'missing': missing, 'decisions': decisions}, indent=1, ensure_ascii=False))
z = {x['kind']: x['result'] for x in out['zones'] if x}
faces = [{'id': pid(p['id']), 'version': p['version'], 'faces': p['faces']} for p in (z.get('faces') or {}).get('panels', [])]
keep = [dict(p, id=pid(p['id'])) for p in (z.get('keep') or {}).get('panels', [])]
(rev / 'FACES-v1.json').open('x').write(json.dumps({'chapter': str(sel['chapter']), 'panels': faces}, indent=1, ensure_ascii=False))
(rev / 'KEEP-c1.json').open('x').write(json.dumps({'chapter': str(sel['chapter']), 'panels': keep}, indent=1, ensure_ascii=False))
rejected = [{'id': d['id'], 'mode': 'generate', 'correction': d['correction'], 'issues': d['issues']} for d in decisions if not d['pick']]
(rev / 'REJECTED-r1.json').open('x').write(json.dumps({'fixes': rejected}, indent=1, ensure_ascii=False))
picks = {d['id'] for d in decisions if d['pick']}
print(pkg, len(decisions), 'panels;', len(picks), 'picked;', len(missing), 'rejected;', len(faces), 'face sets;', len(keep), 'keep sets;',
      'picks without faces', len(picks - {f['id'] for f in faces}), 'without keep', len(picks - {k['id'] for k in keep}))
