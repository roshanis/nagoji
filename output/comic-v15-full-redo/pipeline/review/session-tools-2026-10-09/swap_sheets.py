"""Point existing packages' jobs at the author-approved span sheets (concepts/APPROVED-SHEETS.json entries with
"character" and "spans") in place of the V13 nagoji-v2.png / varma-v1.png, panel by panel; rehash. Backs up each
IMAGEGEN-JOBS.json once (never overwrites a backup). Prompts are not touched.
Usage: swap_sheets.py PACKAGE_DIR [PACKAGE_DIR ...]   (run from output/comic-v15-full-redo)"""
import json, hashlib, re, sys, shutil
from pathlib import Path
V = Path.cwd(); APPROVED = V / 'concepts' / 'APPROVED-SHEETS.json'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def point(s, end):
    parts = [int(x) for x in s.split('.')]
    return tuple(parts + ([99] if end else [1]) * (3 - len(parts)))
entries = [(e['character'], (V / 'concepts' / e['file']).resolve(), [(point(a, False), point(b, True)) for a, b in e['spans']])
           for e in json.loads(APPROVED.read_text()).values() if e.get('spans')]
for c, f, _ in entries:
    assert sha(f) == next(e['sha256'] for e in json.loads(APPROVED.read_text()).values() if e.get('spans') and (V / 'concepts' / e['file']).resolve() == f), f
V13 = {'nagoji-v2.png': 'nagoji', 'varma-v1.png': 'varma'}
def resolve(character, pos):
    hits = [f for c, f, spans in entries if c == character and any(a <= pos <= b for a, b in spans)]
    assert len(hits) <= 1, (character, pos, hits); return hits[0] if hits else None
for pkg in map(Path, sys.argv[1:]):
    jf = pkg / 'IMAGEGEN-JOBS.json'; bak = pkg / 'IMAGEGEN-JOBS.backup-pre-sheets-2026-10-08.json'
    if not bak.exists(): shutil.copy2(jf, bak)
    d = json.loads(jf.read_text()); ch = int(d['chapter']); changed = 0
    for j in d['jobs']:
        m = re.match(r'page-(\d+)-panel-(\d+)', j['id']); pos = (ch, int(m[1]), int(m[2]))
        refs = []
        for r in j.get('reference_images', []):
            who = V13.get(Path(r).name); new = resolve(who, pos) if who else None
            refs.append(str(new) if new else r); changed += bool(new)
        if refs != j.get('reference_images', []):
            j['reference_images'] = refs; j['reference_image_sha256'] = {r: sha(r) for r in refs}
            if 'image_gen' in j and 'args' in j['image_gen']: j['image_gen']['args']['referenced_image_paths'] = refs
    jf.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
    print(pkg.name, 'references switched:', changed)
