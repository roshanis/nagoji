"""For given stems of a chapter: place with the live pipeline under several body-zone sizes; print each speech tail's tip
and which face's body (if any, other than the speaker's) it lands on. argv: C ch layout geo_dir stems..."""
import json, math, sys
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as r, compositor as c, reserves as rv
r.UNPAINTED = True
from PIL import Image
C, ch, layout_file, geo_dir = sys.argv[1:5]
V = Path('.').resolve(); package = V / 'chapters' / C
job = json.loads((package / 'IMAGEGEN-JOBS.json').read_text()); script = job['script']
panels = {p['id']: p for page in script['pages'].values() for p in page['panels']}
geo = c.geometry_for_script(script, json.loads(Path(layout_file).read_text())['page_rows'])
for stem in sys.argv[5:]:
    pid = stem.rsplit('-v', 1)[0]
    record = json.loads((package / 'candidates' / f'{stem}.json').read_text())
    frame = r.frame_file(record, package)
    with Image.open(frame) as im: W, H = im.size
    panel = panels[pid]; g = Path(geo_dir)
    tails = r.parse_tails(json.loads((g / f'{stem}-tails.json').read_text()), panel['copy'], W, H)
    faces = r.parse_faces(json.loads((g / f'{stem}-faces.json').read_text()), W, H)
    keep = r.parse_keep(json.loads((g / f'{stem}-keep.json').read_text()), W, H)
    slot = next(p for p in geo['pages'][str(panel['page'])] if p['id'] == pid)
    for depth, half in ((8, 2), (12, 3), (14, 3)):
        rv.BODY_DEPTH, rv.BODY_HALF_WIDTH = depth, half
        try:
            plan = r.drawn_geometry(frame, panel['copy'], slot, tails, faces, keep=keep)
        except Exception as e:
            print(stem, depth, half, 'FAIL', str(e)[:200]); continue
        out = []
        for res in plan['reserves']:
            if res.get('draw') != 'speech' or not res.get('tail'): continue
            t = res['tail']; i = res['copy_indices'][0]
            w = rv.tail_wedge(res['rect'], .45, t, plan['visible_rect'], 1.0)
            out.append((i, res['rect'], 'mouth', [round(v) for v in t]))
        print(stem, depth, half, 'OK', out)
