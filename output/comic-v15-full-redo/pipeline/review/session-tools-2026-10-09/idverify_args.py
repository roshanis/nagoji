"""Identity-fix verification input: for each finished identity batch, pair the audited frame with the new candidate.
Usage: idverify_args.py OUT_DIR BATCH [BATCH ...]  -> writes OUT_DIR/group-NNN.json (at most 6 panels, one package each)
and prints the workflow args JSON. Never overwrites."""
import json, sys, glob
from pathlib import Path
sys.path.insert(0, 'pipeline')
import script_pipeline as sp
V = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
S = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad')
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
audit = json.loads((V / 'review-sheets' / 'IDENTITY-AUDIT-2026-10-08.json').read_text())['result']
conf = {(c['package'], c['id'].split()[0]): c for c in audit['confirmed']}
chunk_items = {}
for f in glob.glob(str(S / 'audit' / 'chunk-*.json')):
    ch = json.loads(Path(f).read_text())
    for it in ch['items']: chunk_items[(ch['package'], it['id'])] = it
copy_cache = {}
def copy_of(chapter, pid):
    if chapter not in copy_cache:
        sc = sp.parse_script(V / 'scripts' / f'CHAPTER-{chapter:02d}-SCRIPT.md')
        copy_cache[chapter] = {p['id']: '; '.join(f'{i}: {c["speaker"]}' for i, c in enumerate(p['copy'])) for pg in sc['pages'].values() for p in pg['panels']}
    return copy_cache[chapter].get(pid, '')
groups = {}
for n in sys.argv[2:]:
    jobs = json.loads((V / 'review-sheets' / f'LEAN-BATCH-{n}.json').read_text())
    log = {x['id']: x for x in json.loads((V / 'review-sheets' / f'GENERATION-LOG-LEAN-BATCH-{n}.json').read_text().strip().removesuffix('\\n'))}
    for j in jobs:
        pkg = j['package'].split('/')[-1]; g = log.get(j['id'])
        if not g or g['status'] != 'captured': print('not captured', n, pkg, j['id'], file=sys.stderr); continue
        new_v = Path(g['candidate_record']).stem.split('-')[-1]
        it = chunk_items[(pkg, j['id'])]; c = conf[(pkg, j['id'])]
        old_v = Path(j['edit_source']).stem.split('-')[-1] if j['mode'] == 'edit' else it['version']
        pdir = V / 'chapters' / pkg
        groups.setdefault(pkg, []).append({'id': j['id'], 'chapter': j['chapter'], 'mode': j['mode'], 'batch': n,
            'old_version': old_v, 'new_version': new_v,
            'old_frame': str(pdir / 'frames' / f"{j['id']}-{old_v}.png"), 'new_frame': str(pdir / 'frames' / f"{j['id']}-{new_v}.png"),
            'cast': it['cast'], 'sheets': it['sheets'], 'fault': c['reason'], 'correction': c['correction'],
            'lettering': copy_of(j['chapter'], j['id'])})
args, k = [], len(list(out.glob('group-*.json')))
for pkg, items in sorted(groups.items()):
    for i in range(0, len(items), 6):
        k += 1; part = items[i:i + 6]
        p = out / f'group-{k:03d}.json'
        p.open('x').write(json.dumps({'package': pkg, 'chapter': part[0]['chapter'], 'items': part}, indent=1))
        args.append({'n': k, 'package': pkg, 'chapter': part[0]['chapter'], 'count': len(part), 'file': str(p)})
print(json.dumps({'groups': args}))
