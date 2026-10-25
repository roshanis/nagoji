"""Apply accepted identity-fix EDITS from a v15-identity-verify result: one new decisions/faces/keep round per package,
via apply_picks.py (an edit keeps its source frame's composition, so its zones and tails carry over).
Usage (from output/comic-v15-full-redo): apply_identity.py VERIFY_RESULT.json VERIFY_ARGS.json (the idverify_args.py output)
Prints what it applied and what still needs work (retry, keep_old, accepted regenerations). Never overwrites."""
import json, re, subprocess, sys, glob
from pathlib import Path
S = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad')
PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
res = json.load(open(sys.argv[1])); res = res.get('result', res)
groups = {}
for f in [g['file'] for g in json.load(open(sys.argv[2]))['groups']]:   # this round's groups only
    g = json.load(open(f))
    for it in g['items']: groups[(g['package'], it['id'], it['new_version'])] = it

def latest(pkg):
    R = Path('chapters') / pkg / 'review'
    names = [p.name for p in R.glob('LEAN-SELECTION-drawn-*.json')]
    for kind, dpat, fpat, kpat in (('split', r'LEAN-SELECTION-drawn-split-r(\d+)\.json', 'FACES-s{}.json', 'KEEP-s{}.json'),
                                    ('merged', r'LEAN-SELECTION-drawn-merged-r(\d+)\.json', None, None),
                                    ('plain', r'LEAN-SELECTION-drawn-r(\d+)\.json', 'FACES-v{}.json', 'KEEP-c{}.json')):
        ns = sorted(int(m.group(1)) for n in names for m in [re.fullmatch(dpat, n)] if m)
        if not ns: continue
        n = ns[-1]
        if kind == 'merged':           # ch07: merged-r3 with FACES-v4 and KEEP-c5
            fn = max(int(m.group(1)) for p in R.glob('FACES-v*.json') for m in [re.fullmatch(r'FACES-v(\d+)\.json', p.name)] if m)
            kn = max(int(m.group(1)) for p in R.glob('KEEP-c*.json') for m in [re.fullmatch(r'KEEP-c(\d+)\.json', p.name)] if m)
            return (f'LEAN-SELECTION-drawn-merged-r{n}.json', f'FACES-v{fn}.json', f'KEEP-c{kn}.json',
                    f'LEAN-SELECTION-drawn-merged-r{n + 1}.json', f'FACES-v{fn + 1}.json', f'KEEP-c{kn + 1}.json')
        return (dpat.replace(r'(\d+)', str(n)).replace('\\', ''), fpat.format(n), kpat.format(n),
                dpat.replace(r'(\d+)', str(n + 1)).replace('\\', ''), fpat.format(n + 1), kpat.format(n + 1))
    raise SystemExit(f'{pkg}: no decisions file')

by_pkg, todo = {}, []
for x in res['items']:
    it = groups.get((x['package'], x['id'], next((g[2] for g in groups if g[0] == x['package'] and g[1] == x['id']), None)))
    if it is None: todo.append((x['package'], x['id'], 'no group record')); continue
    if it['mode'] == 'edit' and (x['verdict'] == 'accept_new' or (x['verdict'] == 'retry' and x.get('retry_from') == 'new')):
        by_pkg.setdefault(x['package'], {})[x['id']] = (it['old_version'], it['new_version'], x.get('notes', ''))
    else:
        todo.append((x['package'], x['id'], f"{x['verdict']} ({it['mode']}) new {it['new_version']}"))
    if x['verdict'] == 'retry' and x.get('retry_from') == 'new':
        todo.append((x['package'], x['id'], f"interim pick {it['new_version']}; still: {(x['remaining'] or x['new_faults'])[:90]}"))
for pkg, picks in sorted(by_pkg.items()):
    d_in, f_in, k_in, d_out, f_out, k_out = latest(pkg)
    cur = {d['id']: d['pick'] for d in json.load(open(Path('chapters') / pkg / 'review' / d_in))['decisions']}
    stale = {pid: (old, cur.get(pid)) for pid, (old, new, _) in picks.items() if cur.get(pid) != old}
    ok = {pid: new for pid, (old, new, _) in picks.items() if pid not in stale}
    for pid, (old, now) in stale.items(): todo.append((pkg, pid, f'edit was made from {old} but the current pick is {now}'))
    if not ok: continue
    ch = S / f'idfix-changes-{pkg}-{d_out[:-5]}.json'
    ch.open('x').write(json.dumps({'picks': ok, 'note': 'Identity fixes (2026-10-08 sheets and bible markers): edits of the audited frame accepted by v15-identity-verify. ' +
                                   ' '.join(f'{p}: {picks[p][2]}' for p in ok if picks[p][2])}))
    r = subprocess.run([PY, str(S / 'apply_picks.py'), pkg, d_in, d_out, f_in, f_out, k_in, k_out, str(ch)], capture_output=True, text=True,
                       env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
    print(r.stdout.strip() or r.stderr.strip()[-400:])
print('STILL TO DO:'); [print('  ', *t) for t in todo]
