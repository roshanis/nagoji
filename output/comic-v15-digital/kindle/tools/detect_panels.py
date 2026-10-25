"""Find the bordered panels on each V15 screen page (cream background, black-bordered panels)."""
import sys, json, glob, os
import numpy as np
from PIL import Image

def bg_mask(a):
    # cream page colour, sampled from the margin
    ref = np.median(a[5:40, 5:40].reshape(-1, 3), axis=0)
    d = np.abs(a.astype(int) - ref).sum(axis=2)
    return d > 40  # True where not page background

def runs(v, minlen):
    out, start = [], None
    for i, x in enumerate(list(v) + [False]):
        if x and start is None: start = i
        if not x and start is not None:
            if i - start >= minlen: out.append((start, i))
            start = None
    return out

def split(bg, dark, box, W, H, depth=0):
    """Split a merged block at a cream gutter edged by black panel borders."""
    x0, y0, x1, y1 = box
    if depth > 6: return [box]
    for axis in (0, 1):  # 0: vertical gutters, 1: horizontal gutters
        sub, dk = bg[y0:y1, x0:x1], dark[y0:y1, x0:x1]
        frac, dfrac = sub.mean(axis=axis), dk.mean(axis=axis)
        n = len(frac)
        minpart = 0.12 * W if axis == 0 else 0.06 * H
        best = None
        for s, e in runs(frac > 0.5, 2):
            if e - s > 40 or s < minpart or n - e < minpart: continue
            left = dfrac[max(0, s - 8):s].max(initial=0)
            right = dfrac[e:e + 8].max(initial=0)
            if left < 0.5 or right < 0.5: continue
            score = frac[s:e].mean()
            if best is None or score > best[0]: best = (score, s, e)
        if best:
            _, s, e = best
            if axis == 0:
                a, b = [x0, y0, x0 + s, y1], [x0 + e, y0, x1, y1]
            else:
                a, b = [x0, y0, x1, y0 + s], [x0, y0 + e, x1, y1]
            return split(bg, dark, a, W, H, depth + 1) + split(bg, dark, b, W, H, depth + 1)
    return [box]

def detect(path):
    from scipy import ndimage
    a = np.asarray(Image.open(path).convert('RGB'))
    h, w, _ = a.shape
    bg = ~bg_mask(a)
    dark = a.astype(int).sum(axis=2) < 200
    lab, n = ndimage.label(bg)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(edge))
    lab2, n2 = ndimage.label(~outside)
    panels = []
    for sl in ndimage.find_objects(lab2):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (x1 - x0) * (y1 - y0) < 0.02 * w * h: continue
        if y1 < h * 0.07: continue  # running title
        panels.extend(split(bg, dark, [int(x0), int(y0), int(x1), int(y1)], w, h))
    panels.sort(key=lambda p: (p[1] // 40, p[0]))
    return w, h, panels

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    res = {}
    for f in sorted(glob.glob(os.path.join(src, 'ch*-p*.jpg'))):
        w, h, p = detect(f)
        res[os.path.basename(f)[:-4]] = {'w': w, 'h': h, 'panels': p}
    json.dump(res, open(out, 'w'), indent=0)
    print(len(res))
