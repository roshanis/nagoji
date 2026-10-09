"""Which panels of a built layout get bars: the b-pass crop (geometry dir, *-drawn.json "visible_rect") cannot reach
the slot's shape, so the compositor fits the art inside the slot with empty paper beside or above it
(compositor.fit_clip_contain). Prints each such panel with the share of the slot the art fills, worst first.
Usage: bars_audit.py CH PKGDIR GEOMETRY_DIR LAYOUT [MIN_FILL]   (MIN_FILL default 0.98, the compositor's 2 percent)"""
import sys, json
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
ch, pkg, gdir, layout = sys.argv[1:5]
min_fill = float(sys.argv[5]) if len(sys.argv) > 5 else .98
out = rc.package(int(ch), Path(pkg)); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
rows = json.loads(Path(layout).read_text())['page_rows']
FULL, HALF = c.ART_WIDTH_PT, (c.ART_WIDTH_PT - c.GAP_PT) / 2
drawn = {p.name.rsplit('-v', 1)[0]: p for p in Path(gdir).glob('*-drawn.json')}
bad = []
for page, pg in script['pages'].items():
    ids = [p['id'] for p in pg['panels']]; i = 0
    for row in rows[str(page)]:
        group = ids[i:i + (2 if isinstance(row, list) else 1)]; i += len(group)
        h = row[0] if isinstance(row, list) else row; w = HALF if isinstance(row, list) else FULL
        for pid in group:
            f = drawn.get(pid)
            if not f: bad.append((0, page, pid, 'no geometry')); continue
            x0, y0, x1, y1 = json.loads(f.read_text())['visible_rect']
            art, slot = (x1 - x0) / (y1 - y0), w / h
            fill = min(art / slot, slot / art)
            if fill < min_fill:
                bad.append((round(fill, 2), page, pid, 'narrower than its slot' if art < slot else 'shorter than its slot'))
    assert i == len(ids), (page, i, len(ids))
for fill, page, pid, how in sorted(bad):
    print(f'page {page} {pid}: art fills {fill:.0%} of the slot, {how}')
print(len(bad), 'panels with bars')
