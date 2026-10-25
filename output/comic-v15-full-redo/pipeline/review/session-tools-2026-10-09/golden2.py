import sys, json, math, time
from pathlib import Path
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
import run_chapter as r, reserves as rv, compositor as c
package = r.V15 / 'chapters' / 'ch04'
job = json.loads((package / 'IMAGEGEN-JOBS.json').read_text())
script = job['script']
geometry_dir = package / 'review' / 'geometry-drawn-r4'
panels = {p['id']: p for page in script['pages'].values() for p in page['panels']}
def inputs(stem):
    from PIL import Image
    panel_id = stem.rsplit('-v', 1)[0]
    record = json.loads((package / 'candidates' / f'{stem}.json').read_text())
    frame = r.frame_file(record, package)
    with Image.open(frame) as image: width, height = image.size
    panel = panels[panel_id]
    tails = r.parse_tails(json.loads((geometry_dir / f'{stem}-tails.json').read_text()), panel['copy'], width, height)
    raw = json.loads((geometry_dir / f'{stem}-faces.json').read_text())
    faces = r.parse_faces([dict(face, r=face['r'] * .55) for face in raw], width, height)
    return panel, frame, {'id': panel_id, 'path': str(frame), 'width': width, 'height': height}, tails, faces
golden = json.loads((Path(P) / 'golden_ch04_drawn_planner.json').read_text())
out = {}; fitfail = []
for name, layout in golden['layouts'].items():
    geom = c.geometry_for_script(script, layout)
    out[name] = {}
    for stem in golden['placements'][name]:
        panel, frame, row, tails, faces = inputs(stem)
        slot = next(p for p in geom['pages'][str(panel['page'])] if p['id'] == panel['id'])
        plan = r.drawn_geometry(frame, panel['copy'], slot, tails, faces)
        out[name][stem] = {'visible_rect': plan['visible_rect'], 'reserves': plan['reserves']}
        fits = r.drawn_fits(row, panel, slot, tails, faces, script)
        if not fits: fitfail.append((name, stem))
        if plan['short_tail']: print('short', name, stem, plan['short_tail'])
print('fit failures', fitfail)
json.dump(out, open(sys.argv[1], 'w'))
print({k: len(v) for k, v in out.items()})
