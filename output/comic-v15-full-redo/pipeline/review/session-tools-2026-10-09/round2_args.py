"""Round-2 selection args: only the panels in the given regeneration batches, and only the candidates captured after
each batch file was written. Usage: round2_args.py FULL_ARGS.json OUT.json BATCH_NUMBER [BATCH_NUMBER ...]
(FULL_ARGS.json is make_select_args.py output for the chapter, with sheetsRoot pointing at the new round's sheets.)"""
import json, sys
from pathlib import Path
V = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
full, out, batches = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3:]
want = {}
for n in batches:
    b = V / 'review-sheets' / f'LEAN-BATCH-{n}.json'; t = b.stat().st_mtime
    for j in json.loads(b.read_text()):
        if j['package'].split('/')[-1] != Path(full['framesRoot'].rstrip('/')).parent.name: continue
        pkg = V / 'chapters' / j['package'].split('/')[-1]
        vs = sorted(p.stem.split('-')[-1] for p in (pkg / 'candidates').glob(j['id'] + '-v*.json') if p.stat().st_mtime > t)
        want[j['id']] = vs
pages = []
for pg in full['pages']:
    panels = []
    for n, cast, versions in pg['panels']:
        pid = f"page-{pg['page']:02d}-panel-{n}"
        if pid in want and want[pid]: panels.append([n, cast, want[pid][::-1]])
    if panels: pages.append({'page': pg['page'], 'panels': panels})
full['pages'] = pages
json.dump(full, open(out, 'w'))
print(out, len(want), 'regenerated panels;', sum(len(p['panels']) for p in pages), 'with new candidates; none yet:', [k for k, v in want.items() if not v])
