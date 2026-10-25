"""Apply a page split made by split_pages.py: back up and replace the chapter's script, art direction and cast
overrides; prepare the split package; import every picked and backup frame from the old package under its new id
(import-frame keeps provenance); re-key the old package's newest decisions, faces and keep files into split-r1, FACES-s1
and KEEP-s1; write IMPORT-MAP and the id map. Never overwrites.
Usage (from output/comic-v15-full-redo): apply_split.py CH OLD_PKG NEW_PKG SPLIT_DIR TAG [--skip-scripts]
(--skip-scripts: the renumbered scripts are already installed, for a re-run into a new package.)"""
import copy, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
S = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad')
PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
sys.path.insert(0, str(S)); from apply_identity_latest import latest
ch, old, new, sdir, tag = int(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]), sys.argv[5]
C = f'{ch:02d}'
O, N = Path('chapters') / old, Path('chapters') / new
if N.exists(): sys.exit(f'{N} exists')
idmap = json.loads((sdir / 'idmap.json').read_text())
skip = '--skip-scripts' in sys.argv
# 0. the old package must keep the script it was prepared from (import-frame reads its lettering from SCRIPT-SOURCE.md
# once the live script has changed)
job = json.loads((O / 'IMAGEGEN-JOBS.json').read_text()); src_md = O / 'SCRIPT-SOURCE.md'
if not src_md.exists():
    cands = [Path('scripts') / f'CHAPTER-{C}-SCRIPT.md'] + sorted(Path('scripts').glob(f'CHAPTER-{C}-SCRIPT.md.backup*'))
    match = next((f for f in cands if hashlib.sha256(f.read_bytes()).hexdigest() == job['script']['sha256']), None)
    if match is None: sys.exit('no script copy matches the old package recorded sha256')
    with open(src_md, 'xb') as f: f.write(match.read_bytes())
    print('wrote', src_md, 'from', match)
# 1. scripts: back up, then install the renumbered files
for name in ([] if skip else (f'CHAPTER-{C}-SCRIPT.md', f'CHAPTER-{C}-ART-DIRECTION.json', f'CHAPTER-{C}-CAST-OVERRIDES.json')):
    src, dst = sdir / name, Path('scripts') / name
    if not src.exists(): continue
    bak = Path('scripts') / f'{name}.backup-pre-{tag}'
    if bak.exists(): sys.exit(f'{bak} exists')
    shutil.copyfile(dst, bak); shutil.copyfile(src, dst); print('installed', name, '(backup', bak.name + ')')
if not (O / 'review' / f'SPLIT-IDMAP-{tag}.json').exists(): shutil.copyfile(sdir / 'idmap.json', O / 'review' / f'SPLIT-IDMAP-{tag}.json')
# 2. prepare the split package
cmd = [PY, 'pipeline/run_chapter.py', 'prepare', '--chapter', str(ch), '--package-dir', str(N), '--allow-draft']
for flag, name in (('--cast-overrides', f'CHAPTER-{C}-CAST-OVERRIDES.json'), ('--art-direction', f'CHAPTER-{C}-ART-DIRECTION.json')):
    if (Path('scripts') / name).exists(): cmd += [flag, f'scripts/{name}']
r = subprocess.run(cmd, capture_output=True, text=True, env=ENV)
if r.returncode: sys.exit('prepare failed: ' + (r.stderr or r.stdout)[-800:])
print('prepared', N)
# 3. import picks and backups
d_in, f_in, k_in = latest(old)[:3]
d = json.loads((O / 'review' / d_in).read_text())
vmap, fails = {}, 0
for x in d['decisions']:
    tid = idmap[x['id']]
    for role in ('pick', 'backup'):
        v = x.get(role)
        if not v or (x['id'], v) in vmap: continue
        r = subprocess.run([PY, 'pipeline/run_chapter.py', 'import-frame', '--chapter', str(ch), '--package-dir', str(N), '--from-package', str(O),
                            '--source', f"{x['id']}-{v}", '--frame-id', tid], capture_output=True, text=True, env=ENV)
        if r.returncode:
            fails += 1; print('FAIL', x['id'], v, (r.stderr or r.stdout).strip().splitlines()[-1][:200]); continue
        rec = json.loads(r.stdout); vmap[(x['id'], v)] = (tid, os.path.basename(rec['path'])[:-4].rsplit('-', 1)[1])
with open(N / f'IMPORT-MAP-{old}-to-{new}.json', 'x') as f:
    json.dump({f'{k[0]}-{k[1]}': f'{v[0]}-{v[1]}' for k, v in vmap.items()}, f, indent=1)
print('imported', len(vmap), 'fails', fails)
# 4. re-key decisions, faces, keep
(N / 'review').mkdir(exist_ok=True)
for x in d['decisions']:
    oldid = x['id']
    for role in ('pick', 'backup'):
        if x.get(role):
            if (oldid, x[role]) in vmap: x[role] = vmap[(oldid, x[role])][1]
            else: x[role] = None
    x['id'] = idmap[oldid]
d['decisions'].sort(key=lambda x: x['id'])
d['round'] = 'split-r1'; d['about_split'] = f'{old} {d_in} re-keyed for the {tag} page split (see review/SPLIT-IDMAP-{tag}.json in {old}); versions renumbered by import-frame.'
with open(N / 'review' / 'LEAN-SELECTION-drawn-split-r1.json', 'x') as f: json.dump(d, f, indent=1, ensure_ascii=False)
for fn, out in ((f_in, 'FACES-s1.json'), (k_in, 'KEEP-s1.json')):
    g = json.loads((O / 'review' / fn).read_text()); kept = []
    for p in g['panels']:
        k = (p['id'], p['version'])
        if k in vmap: q = copy.deepcopy(p); q['id'], q['version'] = vmap[k]; kept.append(q)
    g['panels'] = kept
    with open(N / 'review' / out, 'x') as f: json.dump(g, f, indent=1, ensure_ascii=False)
    print(out, len(kept), 'from', fn)
picks = {(x['id'], x['pick']) for x in d['decisions'] if x.get('pick')}
F = {(p['id'], p['version']) for p in json.loads((N / 'review' / 'FACES-s1.json').read_text())['panels']}
K = {(p['id'], p['version']) for p in json.loads((N / 'review' / 'KEEP-s1.json').read_text())['panels']}
print('decisions from', d_in, '| picks', len(picks), 'missing faces', len(picks - F), 'missing keep', len(picks - K))
