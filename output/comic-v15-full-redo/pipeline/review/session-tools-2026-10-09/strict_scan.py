"""For every lettered panel of a chapter: does the planner place it with no keep zone more than KEEP_MAX covered at a
generous slot (full width and half width, 300 pt tall)? Panels that fail both are outpaint candidates.
Usage: strict_scan.py CH PKGDIR TAG DECISIONS KEEP_MAX"""
import sys, json
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
ch, pkg, tag, dec, kmax = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
rc.UNPAINTED = True
out = rc.package(int(ch), Path(pkg)); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
C = Path(pkg).name; fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), rc.FACE_SCALE, script)
probe = rc.SlotProbe(script, inputs, fd, keep_max=kmax)
FULL, HALF = c.ART_WIDTH_PT, (c.ART_WIDTH_PT - c.GAP_PT) / 2
bad = []
for pid in sorted(probe.tails):
    full = probe.fits(pid, FULL, 300.0); half = probe.fits(pid, HALF, 300.0) if not full else None
    if not full and not half: bad.append(pid)
    print(pid, 'full' if full else ('half only' if half else 'NEITHER'), flush=True)
print('OUTPAINT CANDIDATES', C, bad)
