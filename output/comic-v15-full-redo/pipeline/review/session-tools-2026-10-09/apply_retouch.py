"""Capture hand retouches as new candidate versions, record them in review-sheets/HAND-RETOUCH-2026-10-08.json and make
each the pick (zones carried from the source version, which must be the current pick) in one new round per package.
Usage (from output/comic-v15-full-redo): apply_retouch.py ITEMS.json
ITEMS.json: [{"package", "chapter", "id", "source", "file", "what"}]  (prompt: the newest prompts/<id>-fix*.txt, else <id>.txt)"""
import json, subprocess, sys, hashlib, re
from pathlib import Path
S = Path('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad')
PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
ENV = {'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'}
sys.path.insert(0, str(S)); from apply_identity_latest import latest
items = json.load(open(sys.argv[1]))
rec_path = Path('review-sheets/HAND-RETOUCH-2026-10-08.json'); rec = json.loads(rec_path.read_text())
by_pkg = {}
for it in items:
    pdir = Path('chapters') / it['package']
    cur = {d['id']: d['pick'] for d in json.loads((pdir / 'review' / latest(it['package'])[0]).read_text())['decisions']}
    if cur.get(it['id']) != it['source']:
        print('SKIP', it['package'], it['id'], 'source', it['source'], 'is not the current pick', cur.get(it['id'])); continue
    fixes = sorted(pdir.glob(f"prompts/{it['id']}-fix*.txt"), key=lambda p: p.stat().st_mtime)
    prompt = (fixes[-1] if fixes else pdir / 'prompts' / f"{it['id']}.txt").resolve()
    before = {p.name for p in (pdir / 'frames').glob(f"{it['id']}-v*.png")}
    r = subprocess.run([PY, 'pipeline/run_chapter.py', 'capture', '--chapter', str(it['chapter']), '--package-dir', str(pdir),
                        '--frame-id', it['id'], '--generated', it['file'], '--prompt', str(prompt)], capture_output=True, text=True, env=ENV)
    new = sorted({p.name for p in (pdir / 'frames').glob(f"{it['id']}-v*.png")} - before)
    if r.returncode or len(new) != 1: print('CAPTURE FAILED', it['package'], it['id'], r.stderr[-300:]); continue
    v = re.search(r'-(v\d+)\.png$', new[0])[1]
    sha = hashlib.sha256((pdir / 'frames' / new[0]).read_bytes()).hexdigest()
    rec['frames'].append({'package': it['package'], 'id': it['id'], 'version': v, 'source': it['source'], 'what': it['what'], 'sha256': sha})
    by_pkg.setdefault(it['package'], {})[it['id']] = v
    print('captured', it['package'], it['id'], v)
rec_path.write_text(json.dumps(rec, indent=1))
for pkg, picks in by_pkg.items():
    d_in, f_in, k_in, d_out, f_out, k_out = latest(pkg)
    ch = S / f'retouch-changes-{pkg}-{d_out[:-5]}.json'
    ch.open('x').write(json.dumps({'picks': picks, 'note': 'Hand retouches (HAND-RETOUCH-2026-10-08.json) of the current picks; composition unchanged, zones carried.'}))
    r = subprocess.run([PY, str(S / 'apply_picks.py'), pkg, d_in, d_out, f_in, f_out, k_in, k_out, str(ch)], capture_output=True, text=True, env=ENV)
    print(r.stdout.strip() or r.stderr.strip()[-400:])
