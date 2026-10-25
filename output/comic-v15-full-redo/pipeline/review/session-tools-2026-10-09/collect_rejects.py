"""Collect panels rejected in a selection round into a fixes file for build_v2_fix_batch.py (mode "generate").
Usage: collect_rejects.py SELECT_ZONES.json CH OUT_FIXES.json
Only panels the round rejected (pick null) are taken, each with the reviewer's correction; panels that later rounds
picked are skipped by checking the chapter's newest LEAN-SELECTION-drawn-rN.json."""
import json, sys, glob, re
from pathlib import Path
sz, ch, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
r = json.load(open(sz))['result']
rev = Path(f'chapters/ch{ch:02d}/review')
newest = max(rev.glob('LEAN-SELECTION-drawn-r*.json'), key=lambda p: int(re.search(r'-r(\d+)\.json$', p.name)[1]))
picked = {d['id'] for d in json.loads(newest.read_text())['decisions'] if d['pick']}
fixes = [{'id': d['id'], 'mode': 'generate', 'correction': d['correction'], 'issues': d['issues']}
         for d in r['selections'][0]['decisions'] if not d['pick'] and d['id'] not in picked]
for f in fixes:
    for dash in ('—', '–'): f['correction'] = f['correction'].replace(dash, ', ')
    assert f['correction'].strip(), f['id']
json.dump({'fixes': fixes}, open(out, 'x'), indent=1, ensure_ascii=False)
print(f'ch{ch}', newest.name, len(fixes), 'to regenerate:', [f['id'] for f in fixes])
