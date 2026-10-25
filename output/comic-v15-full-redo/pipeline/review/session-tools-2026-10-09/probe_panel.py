"""Probe whether one panel places at given slot sizes with optional zone relaxations.
Usage (from output/comic-v15-full-redo): probe_panel.py CH PKG PANEL_ID VERSION FACES.json KEEP.json MIN_R KEEP_DROP W:H [W:H ...]
MIN_R: drop faces with r below it (0 keeps all); KEEP_DROP: comma list of keep indexes to drop (or -)."""
import json, sys
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc
ch, pkg, pid, ver, ff, kf, min_r, kd = sys.argv[1:9]
sizes = [tuple(map(float, s.split(':'))) for s in sys.argv[9:]]
P = Path('chapters') / pkg
script = rc.lettered_script(Path(f'scripts/CHAPTER-{int(ch):02d}-SCRIPT.md'))
panel = {p['id']: p for page in script['pages'].values() for p in page['panels']}[pid]
frame = P / 'frames' / f'{pid}-{ver}.png'
from PIL import Image
W, H = Image.open(frame).size
faces = next(p['faces'] for p in json.loads((P / 'review' / ff).read_text())['panels'] if p['id'] == pid and p['version'] == ver)
keep = next(p['keep'] for p in json.loads((P / 'review' / kf).read_text())['panels'] if p.get('id') == pid and p.get('version') == ver)
faces = [f for f in faces if f['r'] >= float(min_r)]
drop = set() if kd == '-' else {int(x) for x in kd.split(',')}
keep = [k for i, k in enumerate(keep) if i not in drop]
row = {'id': pid, 'path': str(frame), 'width': W, 'height': H, 'keep': rc.parse_keep(keep, W, H)}
fz = rc.parse_faces(faces, W, H)
tails = [None] * len(panel['copy'])
for w, h in sizes:
    slot = {'id': pid, 'rect_pt': [36, 56.25, w, h]}
    print(f'{w}x{h}: faces {len(faces)} keep {len(keep)} ->', rc.drawn_fits(row, panel, slot, tails, fz, script, keep_max=0.34))
    try:
        plan = rc.drawn_geometry(frame, panel['copy'], slot, tails, fz, keep=row['keep'])
        print('   plan ok; keep coverage', [round(x, 2) for x in rc.keep_coverage([r['rect'] for r in plan['reserves']], row['keep'], plan['visible_rect'])])
    except rc.AutoGeometryError as e:
        print('   ', str(e)[:400])
