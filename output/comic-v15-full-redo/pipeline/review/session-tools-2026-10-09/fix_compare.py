"""Before and after crops of a region-edit batch: for every entry in GENERATION-LOG-LEAN-BATCH-<n>.json, the edited
region (padded) from the edit source and from the newest captured version, side by side, into one sheet.
Usage: fix_compare.py PKG BATCH_NUMBER OUT.png [WIDTH]"""
import json, os, sys
from PIL import Image
pkg, n, out = sys.argv[1:4]; width = int(sys.argv[4]) if len(sys.argv) > 4 else 500
log = json.load(open(f'review-sheets/GENERATION-LOG-LEAN-BATCH-{n}.json'))
batch = {b['id']: b for b in json.load(open(f'review-sheets/LEAN-BATCH-{n}.json'))}
def boxes(rc):
    if not rc: return []
    if isinstance(rc[0], (int, float)): return [rc]
    out = []
    for c in rc:
        if isinstance(c, dict):
            c = next(v for k, v in c.items() if isinstance(v, list) and len(v) == 4 and all(isinstance(x, (int, float)) for x in v))
        out.append(c)
    return out
rows = []
for e in log:
    pid = e['id']; src = batch[pid]['edit_source']
    vs = sorted(f for f in os.listdir(f'chapters/{pkg}/frames') if f.startswith(pid + '-v') and not f.endswith('2x.png'))
    a = Image.open(src).convert('RGB'); b = Image.open(f'chapters/{pkg}/frames/{vs[-1]}').convert('RGB')
    for x0, y0, x1, y1 in boxes(e.get('region_crops')):
        pad = 30; box = (max(0, x0 - pad), max(0, y0 - pad), min(a.width, x1 + pad), min(a.height, y1 + pad))
        ca, cb = a.crop(box), b.crop(box); s = width / max(ca.width, ca.height)
        ca = ca.resize((int(ca.width * s), int(ca.height * s))); cb = cb.resize(ca.size)
        row = Image.new('RGB', (ca.width * 2 + 10, ca.height), 'white'); row.paste(ca, (0, 0)); row.paste(cb, (ca.width + 10, 0)); rows.append(row)
    print(pid, os.path.basename(src), '->', vs[-1])
W = max(r.width for r in rows); H = sum(r.height + 12 for r in rows); sheet = Image.new('RGB', (W, H), 'white'); y = 0
for r in rows: sheet.paste(r, (0, y)); y += r.height + 12
sheet.save(out); print(sheet.size)
