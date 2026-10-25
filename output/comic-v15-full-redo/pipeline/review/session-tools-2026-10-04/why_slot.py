"""Diagnostic: for panels the b-pass could not place, the planner's error at the fitted slot and the heights that work."""
import sys, json
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
from types import SimpleNamespace
ch, C, tag, dec, ids = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5].split(',')
rc.UNPAINTED = True
out = rc.package(ch, None)
job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
layout = json.loads(Path(f'chapters/{C}/LAYOUT-fitted-{tag}.json').read_text())
geo = c.geometry_for_script(script, layout['page_rows'])
slots = {s['id']: s for pg in geo['pages'].values() for s in pg}
fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), 1.0, script)
probe = rc.SlotProbe(script, inputs, fd)
for pid in ids:
    slot = slots[pid]; x, y, w, h = slot['rect_pt']
    panel = probe.panels[pid]; frame = probe.frames[pid]
    print('==', pid, frame['path'].split('/')[-1], f'slot {w:.1f}x{h:.1f}', 'probed' if probe.probed(pid) else 'NOT PROBED (no tails file)',
          [ch_['speaker'] for ch_ in panel['copy']], [len(ch_['text']) for ch_ in panel['copy']])
    if not probe.probed(pid):
        print('   tails file missing in', fd); continue
    row = {'id': pid, 'path': frame['path'], 'width': frame['width'], 'height': frame['height']}
    if pid in probe.keep: row['keep'] = [[a*frame['width'], b*frame['height'], cc*frame['width'], d*frame['height']] for a, b, cc, d in probe.keep[pid]]
    tails = rc.parse_tails(probe.tails[pid], panel['copy'], frame['width'], frame['height'])
    faces = rc.parse_faces([{'x': a, 'y': b, 'r': r} for a, b, r in inputs['faces'].get(pid, [])], frame['width'], frame['height'])
    try:
        rc.drawn_geometry(Path(frame['path']), panel['copy'], {'id': pid, 'rect_pt': [c.ART_X_PT, c.ART_Y_PT, w, h]}, tails, faces, keep=row.get('keep'))
        print('   planner places it at the fitted slot; fits:', probe.fits(pid, w, h))
    except Exception as e:
        print('   at slot:', str(e)[:330])
    ok = [hh for hh in range(int(h) - 60, int(h) + 121, 5) if hh > 40 and probe.fits(pid, w, float(hh))]
    print('   heights that work at this width (step 5):', ok[:20])
