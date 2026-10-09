"""Diagnostic: the planner's verdict for panels at given slot sizes. Args: ch C tag dec 'pid:w:h,pid:w:h,...'"""
import sys, json
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
from types import SimpleNamespace
ch, C, tag, dec, asks = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5].split(',')
rc.UNPAINTED = True
out = rc.package(ch, None); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), 1.0, script)
probe = rc.SlotProbe(script, inputs, fd)
for ask in asks:
    pid, w, h = ask.split(':'); w, h = float(w), float(h)
    panel = probe.panels[pid]; frame = probe.frames[pid]
    row = {'id': pid, 'path': frame['path'], 'width': frame['width'], 'height': frame['height']}
    if pid in probe.keep: row['keep'] = [[a*frame['width'], b*frame['height'], cc*frame['width'], d*frame['height']] for a, b, cc, d in probe.keep[pid]]
    tails = rc.parse_tails(probe.tails[pid], panel['copy'], frame['width'], frame['height'])
    faces = rc.parse_faces([{'x': a, 'y': b, 'r': r} for a, b, r in inputs['faces'].get(pid, [])], frame['width'], frame['height'])
    slot = {'id': pid, 'rect_pt': [c.ART_X_PT, c.ART_Y_PT, w, h]}
    try:
        plan = rc.drawn_geometry(Path(frame['path']), panel['copy'], slot, tails, faces, keep=row.get('keep'))
        found = dict(row); found.update({'visible_rect': plan['visible_rect'], 'reserves': plan['reserves']})
        m = c.copy_fit_measurements([found], script, {'pages': {str(panel['page']): [slot]}}, SimpleNamespace(B=SimpleNamespace(measure=c.measure)), reject_failures=False)
        verdict = 'placed; fits ' + str([x['fits'] for x in m]) + ' visible ' + str([round(v) for v in plan['visible_rect']])
    except Exception as e:
        verdict = f'{type(e).__name__}: {str(e)[:300]}'
    print(f'{pid} {w:.1f}x{h:.1f} faces={len(inputs["faces"].get(pid, []))} keep={len(probe.keep.get(pid, []))}: {verdict}')
