import json, sys
from pathlib import Path
pkg, tag, dec, fit = sys.argv[1:5]
picks = {d['id']: d['pick'] for d in json.load(open(f'chapters/{pkg}/review/{dec}'))['decisions']}
rows = json.load(open(f'chapters/{pkg}/SELECTION-INPUT-{tag}.json'))['frames']
back = [(r['id'], Path(r['path']).stem[len(r['id']) + 1:], picks.get(r['id'])) for r in rows if Path(r['path']).stem[len(r['id']) + 1:].replace('-2x', '') != picks.get(r['id'])]
print('backups used:', back or 'none')
f = json.load(open(fit))
print('fit statuses', f['statuses'], 'structure', f.get('structure_search', {}).get('pages_changed'))
low = [(pid, p.get('fill_after'), p.get('ratio_after')) for pg in f['pages'].values() for pid, p in pg['panels'].items() if (p.get('fill_after') or 1) < .97 or (p.get('ratio_after') or 9) < 1.5]
print('low fill or ratio:', low or 'none')
pr = f.get('probe') or {}
print('probe unplaceable:', pr.get('unplaceable') or 'none', '| unprobed:', pr.get('unprobed') or 'none')
