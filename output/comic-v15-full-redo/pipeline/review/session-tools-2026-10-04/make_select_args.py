"""Selection args for a whole chapter's first pass: every panel's candidates, cast, copy speakers and the cast's sheets."""
import json, sys, glob
from pathlib import Path
sys.path.insert(0, 'pipeline')
import script_pipeline as s
ch, sheets_dir = int(sys.argv[1]), sys.argv[2]
V = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'); C = f'ch{ch:02d}'
jobs = json.loads((V / 'chapters' / C / 'IMAGEGEN-JOBS.json').read_text())['jobs']
sc = s.parse_script(V / 'scripts' / f'CHAPTER-{ch:02d}-SCRIPT.md')
copy = {p['id']: '; '.join(f'{i}: {c["speaker"]}' for i, c in enumerate(p['copy'])) for pg in sc['pages'].values() for p in pg['panels']}
sheets = {}
pages = {}
for job in jobs:
    for ref in job['reference_images']:
        name = Path(ref).name
        key = next((c for c in job['cast'] if c.split('_')[0] in name.lower() or (c == 'nagoji' and 'nagoji' in name)), name.split('.')[0])
        sheets[key] = ref
    versions = sorted(Path(f).stem.split('-')[-1] for f in glob.glob(str(V / 'chapters' / C / 'candidates' / f"{job['id']}-v*.json")))
    pg, n = job['id'].split('-')[1], job['id'].split('-')[3]
    pages.setdefault(int(pg), []).append([n, [c for c in job['cast'] if c in sheets or True], versions[::-1]])
args = {'chapter': ch, 'sheetsRoot': str(V / 'review-sheets' / sheets_dir) + '/', 'framesRoot': str(V / 'chapters' / C / 'frames') + '/',
        'sheets': [{'key': k, 'path': v} for k, v in sorted(sheets.items())],
        'pages': [{'page': p, 'panels': panels} for p, panels in sorted(pages.items())],
        'copy': copy}
missing = [j['id'] for j in jobs if not glob.glob(str(V / 'chapters' / C / 'candidates' / f"{j['id']}-v*.json"))]
print(json.dumps(args), file=open(sys.argv[3], 'w'))
print(C, len(jobs), 'panels;', sum(len(p) for p in pages.values()), 'with candidates; missing', missing, '| sheets', sorted(sheets))
