import sys, json, math, time
from pathlib import Path
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
import run_chapter as r, reserves as rv, compositor as c
mode = sys.argv[1]
orig_tw = rv.tail_wedge
if mode == 'allshort':
    rv.tail_wedge = lambda box, ratio, target, bounds, scale=1.0, head=None, short=False: orig_tw(box, ratio, target, bounds, scale, head, True)
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
    return panel, frame, tails, faces
golden = json.loads((Path(P) / 'golden_ch04_drawn_planner.json').read_text())
same = diff = 0; t0=time.time(); report=[]
for name, layout in golden['layouts'].items():
    geom = c.geometry_for_script(script, layout)
    for stem, before in golden['placements'][name].items():
        panel, frame, tails, faces = inputs(stem)
        slot = next(p for p in geom['pages'][str(panel['page'])] if p['id'] == panel['id'])
        plan = r.drawn_geometry(frame, panel['copy'], slot, tails, faces)
        for reserve in plan['reserves']:
            reserve.pop('tail_head', None); reserve.pop('tail_short', None)
        got = {'visible_rect': plan['visible_rect'], 'reserves': plan['reserves']}
        if got == before: same += 1
        else:
            diff += 1; report.append((name, stem, plan['short_tail'], [ (a['rect'], b['rect']) for a,b in zip(got['reserves'], before['reserves']) if a['rect']!=b['rect']], got['visible_rect']==before['visible_rect']))
print(mode, 'same', same, 'diff', diff, round(time.time()-t0), 's')
for x in report: print(x)
