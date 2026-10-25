"""Mirror the art inside one ruled panel of a model sheet left to right (the border and the label below it stay put).
Finds the panel's thin dark border nearest a hint box. Never overwrites.
Usage: flip_panel.py IN.png OUT.png X0 Y0 X1 Y1   (hint box in pixels, roughly the panel's border)"""
import sys
import numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; hx0, hy0, hx1, hy1 = map(int, sys.argv[3:7])
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int); L = a.mean(axis=2)
def line(axis, lo, hi, span):
    # the row/col in [lo, hi] whose pixels across `span` are darkest on average (a ruled border)
    best = None
    for v in range(lo, hi + 1):
        seg = L[v, span[0]:span[1]] if axis == 'row' else L[span[0]:span[1], v]
        s = seg.mean()
        if best is None or s < best[0]: best = (s, v)
    return best[1]
pad = 14
top = line('row', hy0 - pad, hy0 + pad, (hx0 + 30, hx1 - 30)); bot = line('row', hy1 - pad, hy1 + pad, (hx0 + 30, hx1 - 30))
lft = line('col', hx0 - pad, hx0 + pad, (hy0 + 30, hy1 - 30)); rgt = line('col', hx1 - pad, hx1 + pad, (hy0 + 30, hy1 - 30))
inner = (lft + 3, top + 3, rgt - 2, bot - 2)
print('border', (lft, top, rgt, bot), 'inner', inner)
b = a.copy(); x0, y0, x1, y1 = inner
b[y0:y1, x0:x1] = a[y0:y1, x0:x1][:, ::-1]
Image.fromarray(b.astype('uint8')).save(out) if not __import__('os').path.exists(out) else sys.exit('exists: ' + out)
