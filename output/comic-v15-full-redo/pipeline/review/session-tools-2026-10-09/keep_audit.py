"""Audit a built chapter: for each panel, the share of each keep zone's visible part that its placed boxes cover
(the planner's KEEP_OVERLAP_MAX is 0.10). Usage: keep_audit.py PKGDIR GEOMETRY_DIR"""
import sys, json
from pathlib import Path
pkg, gdir = Path(sys.argv[1]), Path(sys.argv[2])
bad = []
for drawn in sorted(gdir.glob('*-drawn.json')):
    stem = drawn.name[:-len('-drawn.json')]
    kf = gdir / f'{stem}-keep.json'
    if not kf.exists(): continue
    d = json.loads(drawn.read_text()); keep = json.loads(kf.read_text())
    from PIL import Image
    with Image.open(pkg / 'frames' / f'{stem}.png') as im: W, H = im.size
    vx0, vy0, vx1, vy1 = d['visible_rect']
    for zi, z in enumerate(keep):
        zx0, zy0, zx1, zy1 = z['x0'] * W, z['y0'] * H, z['x1'] * W, z['y1'] * H
        zx0, zy0, zx1, zy1 = max(zx0, vx0), max(zy0, vy0), min(zx1, vx1), min(zy1, vy1)
        if zx1 <= zx0 or zy1 <= zy0: continue
        area = (zx1 - zx0) * (zy1 - zy0)
        for ri, r in enumerate(d['reserves']):
            bx0, by0, bx1, by1 = r['rect']
            ix, iy = max(0, min(bx1, zx1) - max(bx0, zx0)), max(0, min(by1, zy1) - max(by0, zy0))
            share = ix * iy / area
            if share >= 0.10: bad.append((stem, zi, ri, round(share, 2)))
print(len(bad), 'keep-zone overlaps >= 10%')
for b in bad: print('  ', b)
