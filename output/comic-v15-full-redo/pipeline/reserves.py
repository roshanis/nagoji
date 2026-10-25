#!/usr/bin/env python3
"""Find the blank outlined text areas in a generated V15 frame and turn them into reserves.

Each image prompt asks the generator to "Reserve exactly N blank outlined text area(s),
one per copy chunk". A reserve is therefore a near-white caption box or speech balloon
enclosed by a darker outline. detect_reserves() locates those shapes, takes the largest
axis-aligned rectangle inside each one, insets it, and returns geometry in the format
that `run_chapter.py select` records. The build later requires every glyph to sit on
light native pixels, so a rectangle is only ever taken from pixels that are light.

Only numpy and Pillow are needed. The `style` field is never written here; it is set by
hand for the one unreadable-speech panel.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

INSET_PX = 6                # inset of the returned rectangle from the largest blank rectangle
LIGHT_CHANNEL_MIN = 215     # every channel above this: near-white
RECT_LIGHT_MEAN = 195       # rectangle pixels must also clear the build's mean RGB > 190 audit
MIN_AREA_FRACTION = 0.0055  # regions smaller than this share of the image are noise or bright scenery (0.3 to 0.46%); real boxes are 1.4% or more
OPEN_SIZE = 5               # morphological opening removes specks and hairlines
RING_WIDTH = 5              # how far outside a region the outline is searched for
DARK_MAX = 130              # a ring pixel at or below this brightest channel counts as outline ink
COARSE = 4                  # the largest-rectangle search runs on a grid this many pixels coarse
EXACT_BELOW = 40000         # masks with fewer pixels than this are searched pixel-exact
MAX_INSET_PX = 8            # a larger inset could empty the smallest rectangle that is accepted
MIN_RECT_SIDE = 2 * INSET_PX + 8   # a blank area narrower than this cannot hold lettering
PAD_WHITE = 235             # edge rows and columns at least PAD_SHARE this white are letterbox padding
PAD_SHARE = .995
MARGIN_SHARE = .9           # a thin edge band at least this near-white is a margin, though not 99.5 percent clean
MARGIN_MAX = .03            # ... if it is no deeper than this share of the frame
MARGIN_EDGE = .5            # ... and ends sharply: the next row or column is less than this near-white
MARGIN_PALE = 215           # ... where near-white for a margin is every channel above this (cream paper counts)
PAD_BLACK = 10              # edge rows and columns at least PAD_SHARE this black (every channel below) are padding too
PAD_SAFETY_PX = 2           # extra pixels trimmed past padding, to lose its anti-aliased seam
MIN_RECT_FILL = .40         # blank rectangle / region area: boxes are near 1, ellipses about .64, blobs less
MIN_OUTLINE = .15           # share of the band outside the region that is dark ink
COVER_PX = 8                # a drawn box covers a painted region's bounding box plus this margin
BOX_GAP_PX = 4              # drawn boxes keep at least this much clear space between them
TARGET_GUARD = .08          # boxes keep this share of the frame's shorter side away from a tail target
TAIL_MARGIN_PX = 12         # a box stays at least this far from a tail target, so its tail is visible
EDGE_PX = 3                 # a tail target this close to the visible frame's edge, or beyond it, is off frame
PARTIAL_MIN_SHARE = .10     # a painted region is worth covering only if this share of it can still be covered
CORNER_SLACK_PX = 1         # a painted pixel must lie this far inside a rounded corner, for anti-aliasing
CORNER_CLEAR = 1 - math.sqrt(.5)   # a rounded corner takes this share of its radius from its text area's corner
FACE_MARGIN_PX = 4          # a box stays at least this far from a face zone
BODY_HALF_WIDTH = 2         # a face zone stands for a figure: its body is this many face radii either side of the face,
BODY_DEPTH = 8              # ... from the face's bottom down to this many radii below its centre (a tail tip there is theirs)
OVERLAP_MAX = .5            # a lower-ranked region sharing more than this with a chosen one is a duplicate
TOP_WEIGHT = .35            # a quiet window's cost rises by this much from the top of the frame to the bottom
TOP_RETRY = (1.5, 4.0)      # when placement fails, retry with these stronger top preferences, in turn
REPAIR_ROUNDS = 4           # then re-place this many times, each barring the box that stopped a later chunk from its spot
MIN_KEEP = .45               # a cover crop keeps at least this share of the art's height (or width)
WEDGE_HALF_MIN_PT = 2.5     # a tail's wedge is at least this wide either side of its centre (see compositor._tail_plan)
WEDGE_HALF_MAX_PT = 6.0     # and at most this
WEDGE_HALF_SHARE = .18      # in between, this share of the balloon's shorter side
WEDGE_EDGE_PT = 2.0         # the compositor holds a tail's mouth point this far inside the panel
TAIL_EDGE_PT = .5           # the compositor takes a mouth point this near the panel edge, or beyond it, as off panel
WEDGE_MIN_PT = 8.0          # a tail is at least this long (compositor.TAIL_MIN_PT) and stops short of the mouth by 12
WEDGE_GAP_MIN_PT = 4.0      # percent of the way, between these bounds (compositor.TAIL_GAP_MIN_PT and TAIL_GAP_MAX_PT)
WEDGE_GAP_MAX_PT = 12.0
WEDGE_HEAD_GAP_PT = 3.0     # a tail to a known head stops this far outside the head's circle (compositor.TAIL_HEAD_GAP_PT)
WEDGE_SHORT_REACH = .6      # the legacy short tail, the fallback of a chunk the long one cannot place (compositor.TAIL_SHORT_REACH and
WEDGE_SHORT_MAX_PT = 28.0   # TAIL_SHORT_MAX_PT): it runs this share of the way to the mouth, within WEDGE_MIN_PT and this, 90 percent at most
TAIL_MAX_SHARE = .35        # a free balloon's tail is kept within this share of the visible frame's diagonal, where it can be
TAIL_NEAR_SHARE = .06       # tail lengths within this share of the diagonal count as alike: quietness breaks the tie
WEDGE_STROKE_PT = .8        # the compositor's stroke (compositor.DRAW_STROKE_PT): an off-frame voice's tail needs WEDGE_MIN_PT plus this of room
KEEP_OVERLAP_MAX = .10      # a box that keeps off the keep zones may still cover less than this share of one
RULES = ('cross', 'face', 'tip', 'order')   # the placement rules of a chunk: tails clear of balloons, clear of faces, tips at the speaker, reading order
SAME_SPEAKER_PX = 2.0       # tail targets this close are one speaker's, whose tails may cross (place_boxes `uncross`)


class ReserveError(ValueError):
    """Fewer blank outlined areas were found than the panel has copy chunks."""

    def __init__(self, count, found, regions):
        self.count, self.found, self.regions = count, found, regions
        detail = '; '.join(
            f"bbox {r['bbox']} area {r['area']} rect {r['rect']} outline {r['outline']:.2f} score {r['score']:.2f}"
            for r in regions) or 'no candidate regions'
        super().__init__(f'expected {count} blank reserve(s), found {found}: {detail}')


class PlacementError(ValueError):
    """Drawn boxes cannot be placed in the frame without overlapping or leaving it; `chunk` is the one that failed."""

    def __init__(self, message, chunk=None, blocker=None):
        super().__init__(message)
        self.chunk = chunk
        self.blocker = blocker          # (earlier chunk, its box) when that box is what stops this chunk, else None


def _box_sum(mask, size):
    """Sum of a size x size window around every pixel (zero padded), via an integral image."""
    pad = size // 2
    padded = np.pad(mask.astype(np.int32), pad)
    integral = np.zeros((padded.shape[0] + 1, padded.shape[1] + 1), np.int32)
    integral[1:, 1:] = padded.cumsum(0).cumsum(1)
    h, w = mask.shape
    return (integral[size:size + h, size:size + w] - integral[:h, size:size + w]
            - integral[size:size + h, :w] + integral[:h, :w])


def _opening(mask, size):
    eroded = _box_sum(mask, size) == size * size
    return _box_sum(eroded, size) > 0


def _label(mask):
    """Label 4-connected True regions. Returns (labels, count); background is 0."""
    h, w = mask.shape
    padded = np.zeros((h, w + 2), np.int8)
    padded[:, 1:-1] = mask
    edges = np.diff(padded, axis=1)
    rows_s, cols_s = np.nonzero(edges == 1)
    rows_e, cols_e = np.nonzero(edges == -1)
    n = len(rows_s)
    if n == 0:
        return np.zeros((h, w), np.int32), 0
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    bounds = np.searchsorted(rows_s, np.arange(h + 1)).tolist()
    starts, ends = cols_s.tolist(), cols_e.tolist()
    for y in range(1, h):
        i, i_end = bounds[y - 1], bounds[y]
        j, j_end = bounds[y], bounds[y + 1]
        while i < i_end and j < j_end:
            if starts[i] < ends[j] and starts[j] < ends[i]:
                a, b = find(i), find(j)
                if a != b:
                    parent[b] = a
            if ends[i] < ends[j]:
                i += 1
            else:
                j += 1
    roots = np.array([find(i) for i in range(n)])
    _, run_label = np.unique(roots, return_inverse=True)
    run_label = run_label.astype(np.int32) + 1
    diff = np.zeros((h, w + 1), np.int32)
    diff[rows_s, cols_s] += run_label
    diff[rows_e, cols_e] -= run_label
    return np.cumsum(diff, axis=1)[:, :w], int(run_label.max())


def _fill_holes(region):
    """Fill background pockets that do not connect to the region's outside."""
    padded = np.pad(~region, 1, constant_values=True)
    labels, count = _label(padded)
    if count == 0:
        return region
    outside = labels[0, 0]
    return region | ((labels[1:-1, 1:-1] != outside) & (labels[1:-1, 1:-1] > 0))


def largest_rectangle(mask):
    """Largest all-True axis-aligned rectangle as (x0, y0, x1, y1) half-open, or None.

    Runs on a coarse grid (a coarse cell is True only if every pixel in it is), then grows
    each side pixel by pixel while the new row or column is entirely True.
    """
    mask = np.asarray(mask, bool)
    h, w = mask.shape
    if mask.size < EXACT_BELOW:
        return _largest_rectangle_exact(mask)
    ch, cw = h // COARSE, w // COARSE
    if ch and cw:
        cells = mask[:ch * COARSE, :cw * COARSE].reshape(ch, COARSE, cw, COARSE).all(axis=(1, 3))
    else:
        cells = np.zeros((0, 0), bool)
    best, area = None, 0
    if cells.size:
        heights = np.zeros(cw, np.int32)
        for y in range(ch):
            heights = np.where(cells[y], heights + 1, 0)
            stack = []   # (start, height)
            for x in range(cw + 1):
                current = int(heights[x]) if x < cw else 0
                start = x
                while stack and stack[-1][1] >= current:
                    s, hh = stack.pop()
                    if hh * (x - s) > area:
                        area = hh * (x - s)
                        best = (s, y - hh + 1, x, y + 1)
                    start = s
                stack.append((start, current))
        if best is not None:
            best = [best[0] * COARSE, best[1] * COARSE, best[2] * COARSE, best[3] * COARSE]
    if best is None:
        # No coarse cell fits: search pixel-exact.
        return _largest_rectangle_exact(mask)
    x0, y0, x1, y1 = best
    grown = True
    while grown:
        grown = False
        if x0 > 0 and mask[y0:y1, x0 - 1].all():
            x0 -= 1; grown = True
        if x1 < w and mask[y0:y1, x1].all():
            x1 += 1; grown = True
        if y0 > 0 and mask[y0 - 1, x0:x1].all():
            y0 -= 1; grown = True
        if y1 < h and mask[y1, x0:x1].all():
            y1 += 1; grown = True
    return (x0, y0, x1, y1)


def _largest_rectangle_exact(mask):
    h, w = mask.shape
    heights = np.zeros(w, np.int32)
    best, area = None, 0
    for y in range(h):
        heights = np.where(mask[y], heights + 1, 0)
        stack = []
        for x in range(w + 1):
            current = int(heights[x]) if x < w else 0
            start = x
            while stack and stack[-1][1] >= current:
                s, hh = stack.pop()
                if hh * (x - s) > area:
                    area = hh * (x - s)
                    best = (s, y - hh + 1, x, y + 1)
                start = s
            stack.append((start, current))
    return None if best is None else tuple(int(v) for v in best)


def reading_order(rects):
    """Indices of [x0, y0, x1, y1] rects in reading order.

    Rows run top to bottom; a rect joins a row when it overlaps the row's first rect
    vertically by more than half of the smaller height. Within a row: left to right.
    """
    order = sorted(range(len(rects)), key=lambda i: (rects[i][1], rects[i][0]))
    rows = []
    for i in order:
        x0, y0, x1, y1 = rects[i]
        for row in rows:
            ax0, ay0, ax1, ay1 = rects[row[0]]
            overlap = min(y1, ay1) - max(y0, ay0)
            if overlap > .5 * min(y1 - y0, ay1 - ay0):
                row.append(i)
                break
        else:
            rows.append([i])
    return [i for row in rows for i in sorted(row, key=lambda k: rects[k][0])]


def _regions(rgb):
    """Candidate blank regions with their measurements, before ranking."""
    h, w, _ = rgb.shape
    light = rgb.min(axis=2) > LIGHT_CHANNEL_MIN
    light = _opening(light, OPEN_SIZE)
    labels, count = _label(light)
    if count == 0:
        return []
    areas = np.bincount(labels.ravel(), minlength=count + 1)
    minimum = MIN_AREA_FRACTION * h * w
    mean = rgb.astype(np.float32).mean(axis=2)
    brightest = rgb.max(axis=2)
    regions = []
    ys, xs = np.nonzero(labels)
    order = np.argsort(labels[ys, xs], kind='stable')
    ys, xs, ids = ys[order], xs[order], labels[ys, xs][order]
    edges = np.searchsorted(ids, np.arange(count + 2))
    for label in range(1, count + 1):
        if areas[label] < minimum:
            continue
        sl = slice(edges[label], edges[label + 1])
        ry, rx = ys[sl], xs[sl]
        y0, y1, x0, x1 = int(ry.min()), int(ry.max()) + 1, int(rx.min()), int(rx.max()) + 1
        crop = labels[y0:y1, x0:x1] == label
        filled = _fill_holes(crop)
        blank = filled & (mean[y0:y1, x0:x1] > RECT_LIGHT_MEAN)
        rect = largest_rectangle(blank)
        # Outline: how much of the band just outside the region is dark ink.
        py0, py1, px0, px1 = max(0, y0 - RING_WIDTH), min(h, y1 + RING_WIDTH), max(0, x0 - RING_WIDTH), min(w, x1 + RING_WIDTH)
        canvas = np.zeros((py1 - py0, px1 - px0), bool)
        canvas[y0 - py0:y1 - py0, x0 - px0:x1 - px0] = filled
        ring = _box_sum(canvas, 2 * RING_WIDTH + 1) > 0
        ring &= ~canvas
        dark = brightest[py0:py1, px0:px1] <= DARK_MAX
        outline = float((ring & dark).sum() / max(1, ring.sum()))
        area = int(filled.sum())
        rect_area = 0 if rect is None else (rect[2] - rect[0]) * (rect[3] - rect[1])
        regions.append({
            'bbox': [x0, y0, x1, y1], 'area': area, 'solidity': area / ((x1 - x0) * (y1 - y0)),
            'rect_local': rect, 'rect_area': rect_area, 'rect_fill': rect_area / area if area else 0.0,
            'outline': outline, 'offset': (x0, y0), 'filled': filled})
    return regions


def _score(region):
    return region['rect_fill'] * region['outline']


def art_bounds(rgb):
    """The frame's [x0, y0, x1, y1] without its white or black letterbox or border padding.

    The generator often pads art with near-white bars or a thin white margin, and now and then
    with flat black bars. Edge rows and columns that are at least 99.5 percent near-white, or
    99.5 percent flat black, are padding (dark art is textured, so it never is). So is a thin band
    at the edge that is at least 90 percent near-white or pale paper (soft specks or a faint line in a white
    margin, or a cream border), no deeper than 3 percent of the frame and ending sharply; a pale sky fades in
    and runs deeper. A
    further two pixels are trimmed to lose the anti-aliased seam. A frame without padding is
    returned whole, so its bounds are [0, 0, W, H].
    """
    h, w, _ = rgb.shape
    white = rgb.min(axis=2) > PAD_WHITE
    black = rgb.max(axis=2) < PAD_BLACK
    rows = (white.mean(axis=1) >= PAD_SHARE) | (black.mean(axis=1) >= PAD_SHARE)
    cols = (white.mean(axis=0) >= PAD_SHARE) | (black.mean(axis=0) >= PAD_SHARE)

    def lead(flags):
        n = 0
        while n < len(flags) and flags[n]:
            n += 1
        return n

    def margin(shares):
        """A thin, slightly noisy near-white band at the edge that ends sharply: its depth, or 0.

        The band ends at the first row or column, within MARGIN_MAX of the frame, that is less than MARGIN_EDGE
        near-white; everything before it must average at least MARGIN_SHARE (a faint line inside the margin is allowed).
        """
        limit = int(MARGIN_MAX * len(shares))
        edge = next((n for n in range(1, limit) if shares[n] < MARGIN_EDGE), None)
        return edge if edge is not None and shares[:edge].mean() >= MARGIN_SHARE else 0

    pale = rgb.min(axis=2) > MARGIN_PALE
    row_white, col_white = pale.mean(axis=1), pale.mean(axis=0)
    top, bottom = max(lead(rows), margin(row_white)), max(lead(rows[::-1]), margin(row_white[::-1]))
    left, right = max(lead(cols), margin(col_white)), max(lead(cols[::-1]), margin(col_white[::-1]))
    if top + bottom >= h or left + right >= w:
        return [0, 0, w, h]     # a blank frame is not padding around art
    trim = lambda n: n + PAD_SAFETY_PX if n else 0
    return [trim(left), trim(top), w - trim(right), h - trim(bottom)]


def cover_crop(visible, slot_aspect, keep=(), min_keep=MIN_KEEP):
    """The [x0, y0, x1, y1] part of the art to show so that it fills a slot of `slot_aspect` (width / height).

    `visible` is the art rectangle (see art_bounds). The art is cropped on one axis only: its height when the
    slot is wider than it, its width when the slot is taller, to the size that gives the slot's aspect. The
    crop never keeps less than `min_keep` of that axis, nor less than the span of the `keep` rectangles
    ([x0, y0, x1, y1] in source pixels, each clipped to the art; one that ends up empty is ignored), and is
    placed so that it holds them all, as close to centred on their span (or on the art when there are none)
    as the art allows. Its edges are rounded outward, so a keep rectangle is always whole inside it. Art within
    2 percent of the slot's aspect (as compositor.fit_clip_contain has it) is returned as it is. The result may
    still differ from the slot's aspect when `min_keep` or the keep span stopped the crop: the compositor then
    fits what is left inside the slot, with bars.
    """
    x0, y0, x1, y1 = [int(v) for v in visible]
    if abs((x1 - x0) / (y1 - y0) / slot_aspect - 1.0) <= .02:
        return [x0, y0, x1, y1]
    wide = slot_aspect > (x1 - x0) / (y1 - y0)                    # the slot is wider than the art: crop the height
    axis = 1 if wide else 0
    lo, hi = (y0, y1) if wide else (x0, x1)
    target = (x1 - x0) / slot_aspect if wide else (y1 - y0) * slot_aspect
    clipped = [[max(k[0], x0), max(k[1], y0), min(k[2], x1), min(k[3], y1)] for k in keep]
    spans = [(k[axis], k[axis + 2]) for k in clipped if k[2] > k[0] and k[3] > k[1]]
    if spans:
        first, last = min(s[0] for s in spans), max(s[1] for s in spans)
    else:
        first = last = (lo + hi) / 2                              # nothing to keep: centre on the art
    used = min(hi - lo, max(target, min_keep * (hi - lo), last - first))
    start = (first + last) / 2 - used / 2
    start = min(max(start, lo, last - used), hi - used, first)    # still inside the art, and still holding the span
    a, b = min(math.floor(start), math.floor(first)), max(math.ceil(start + used), math.ceil(last))
    a, b = max(a, lo), min(b, hi)
    return [x0, a, x1, b] if wide else [a, y0, b, y1]


def _overlap(a, b):
    """Shared area as a fraction of the smaller rectangle."""
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    smaller = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return ix * iy / smaller if smaller else 0.0


def _shapes(rgb, bounds):
    """Blank outlined shapes in the visible art, best first, nested duplicates removed."""
    ox, oy = bounds[0], bounds[1]
    regions = []
    for r in _regions(rgb[bounds[1]:bounds[3], bounds[0]:bounds[2]]):
        rect = r['rect_local']
        if rect is None or rect[2] - rect[0] < MIN_RECT_SIDE or rect[3] - rect[1] < MIN_RECT_SIDE:
            continue
        if r['rect_fill'] < MIN_RECT_FILL or r['outline'] < MIN_OUTLINE:
            continue     # not a compact, outlined blank shape: art highlight, cloth, foam
        rx, ry = r['offset']
        r['score'] = _score(r)
        r['rect'] = [ox + rx + rect[0], oy + ry + rect[1], ox + rx + rect[2], oy + ry + rect[3]]
        r['bbox'] = [ox + rx, oy + ry, ox + r['bbox'][2], oy + r['bbox'][3]]
        regions.append(r)
    chosen = []
    for r in sorted(regions, key=lambda r: r['score'], reverse=True):
        # Double-outlined shapes give nested regions with the same blank rectangle.
        if all(_overlap(r['rect'], c['rect']) <= OVERLAP_MAX for c in chosen):
            chosen.append(r)
    return chosen


def find_regions(image_path, count):
    """The best `count` painted blank shapes of a frame, in reading order; never raises for a shortage.

    Returns {"size": [W, H], "visible_rect": [...], "regions": [{"bbox": [...], "rect": [...],
    "score": s, "painted": {...}}]}. bbox is the shape's bounding box and rect its largest blank
    rectangle. "painted" holds the region's painted pixels for corner-aware covering: "origin"
    [x, y], "mask" (a boolean array, the region's hole-filled interior grown by its outline
    width and clipped to the frame) and "edge" (an N x 2 array of the mask's boundary pixel
    centres). It holds arrays, so it is not JSON.
    """
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    with Image.open(image_path) as image:
        rgb = np.asarray(image.convert('RGB'))
    h, w, _ = rgb.shape
    bounds = art_bounds(rgb)
    chosen = _shapes(rgb, bounds)[:count] if count else []
    order = reading_order([r['rect'] for r in chosen])
    return {'size': [w, h], 'visible_rect': bounds,
            'regions': [{'bbox': chosen[i]['bbox'], 'rect': chosen[i]['rect'], 'score': float(chosen[i]['score']),
                         'painted': _painted(chosen[i], bounds)} for i in order]}


def _painted(region, bounds):
    """A region's painted pixels: its interior grown by the outline width, clipped to the visible frame."""
    grown = _box_sum(np.pad(region['filled'], RING_WIDTH), 2 * RING_WIDTH + 1) > 0
    x0 = bounds[0] + region['offset'][0] - RING_WIDTH
    y0 = bounds[1] + region['offset'][1] - RING_WIDTH
    left, top = max(bounds[0] - x0, 0), max(bounds[1] - y0, 0)
    right, bottom = min(bounds[2] - x0, grown.shape[1]), min(bounds[3] - y0, grown.shape[0])
    grown, x0, y0 = grown[top:bottom, left:right], x0 + left, y0 + top
    inner = (_box_sum(np.pad(grown, 1), 3) == 9)[1:-1, 1:-1]
    ys, xs = np.nonzero(grown & ~inner)
    return {'origin': [int(x0), int(y0)], 'mask': grown,
            'edge': np.stack([xs + x0 + .5, ys + y0 + .5], axis=1)}


def painted_hidden(painted, box, ratio):
    """True when a rounded rectangle (corner radius `ratio` of its shorter side) hides every painted pixel.

    The painted region is filled and convex-enough that its boundary is what matters, so only
    the boundary pixels are tested. A pixel in a corner must lie inside the corner's arc.
    """
    points = painted['edge']
    if not len(points):
        return True
    x0, y0, x1, y1 = box
    radius = ratio * min(x1 - x0, y1 - y0)
    dx = np.minimum(points[:, 0] - x0, x1 - points[:, 0])
    dy = np.minimum(points[:, 1] - y0, y1 - points[:, 1])
    if (dx < 0).any() or (dy < 0).any():
        return False
    corner = (dx < radius) & (dy < radius)
    return bool(((radius - dx[corner]) ** 2 + (radius - dy[corner]) ** 2 <= (radius - CORNER_SLACK_PX) ** 2).all())


def _clip_rect(rect, bounds):
    return [max(rect[0], bounds[0]), max(rect[1], bounds[1]), min(rect[2], bounds[2]), min(rect[3], bounds[3])]


def _apart(a, b, gap):
    """True when two rectangles keep at least `gap` pixels between them."""
    return a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1]


def on_frame_edge(point, bounds, tolerance=EDGE_PX):
    """True for a tail target on or beyond the visible frame's edge: its speaker is off frame."""
    return (point[0] <= bounds[0] + tolerance or point[0] >= bounds[2] - tolerance
            or point[1] <= bounds[1] + tolerance or point[1] >= bounds[3] - tolerance)


def speaker_head(target, faces):
    """The head circle (x, y, r) a tail target sits in, as the placement step picks it (run_chapter._tail_head): the
    nearest-centre face zone holding it, else the nearest implied head zone ("head of chunk ..."), else None."""
    if target is None or not faces:
        return None
    for implied in (False, True):
        held = [f for f in faces if str(f[3]).startswith('head of chunk') == implied
                and math.hypot(target[0] - f[0], target[1] - f[1]) <= f[2]]
        if held:
            x, y, r, _ = min(held, key=lambda f: math.hypot(target[0] - f[0], target[1] - f[1]))
            return (round(x), round(y), round(r, 1))
    return None


def _head_entry(base, target, head):
    """Distance along the ray from `base` toward `target` to where it first enters the head circle, or None
    (compositor._head_entry)."""
    hx, hy, hr = head
    dx, dy = target[0] - base[0], target[1] - base[1]
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    ox, oy = base[0] - hx, base[1] - hy
    b, c = ox * ux + oy * uy, ox * ox + oy * oy - hr * hr
    if c <= 0:
        return None
    disc = b * b - c
    if disc < 0 or b >= 0:
        return None
    return -b - math.sqrt(disc)


def _off_panel(target, bounds, scale=1.0):
    """True for a tail target the compositor takes as a speaker off the panel (compositor.EDGE_TOLERANCE_PT): its tail runs to
    the border, whichever length rule a tail follows."""
    tol = TAIL_EDGE_PT / scale
    return not (bounds[0] + tol < target[0] < bounds[2] - tol and bounds[1] + tol < target[1] < bounds[3] - tol)


def tail_wedge(box, ratio, target, bounds, scale=1.0, head=None, short=False):
    """Where a balloon's tail runs, in pixels: ((base x, base y), (mouth x, mouth y), half the wedge's base width, wedge length), or None.

    This is the compositor's own rule (compositor._tail_plan) in source pixels. The wedge leaves the edge of `box`
    nearest the speaker's mouth (the top or bottom edge when the mouth is farther above or below than beside), its base
    centred on the mouth's line but kept on the edge's straight part, clear of the corners (radius `ratio` of the shorter
    side), and as wide as the compositor draws it (`scale` is points per source pixel). It tapers to a tip that stops
    short of the mouth, by the compositor's length rule: just outside `head`, the speaker's head circle (x, y, r) when it
    is known (see speaker_head), else 12 percent of the way short within 4 to 12 pt. With `short` it is the legacy short
    tail instead, which ignores `head`: WEDGE_SHORT_REACH of the way, within WEDGE_MIN_PT and WEDGE_SHORT_MAX_PT, 90 percent at
    most (a chunk place_boxes could place only so, see its "short_tail"). The mouth is first held 2 pt inside `bounds`, the
    panel. None when the mouth is inside the box: an off-frame speaker touching the box draws no tail.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    inset = WEDGE_EDGE_PT / scale
    tx, ty = min(max(target[0], bounds[0] + inset), bounds[2] - inset), min(max(target[1], bounds[1] + inset), bounds[3] - inset)
    dx, dy = max(x0 - tx, 0.0, tx - x1), max(y0 - ty, 0.0, ty - y1)
    if dx == 0 and dy == 0:
        return None
    half = max(WEDGE_HALF_MIN_PT, min(WEDGE_HALF_MAX_PT, WEDGE_HALF_SHARE * min(w, h) * scale)) / scale
    radius = ratio * min(w, h)
    if dy >= dx:         # the tail leaves through the top or bottom edge
        low, high, along, edge = x0, x1, tx, (y0 if ty < y0 else y1)
    else:                # through the left or right edge
        low, high, along, edge = y0, y1, ty, (x0 if tx < x0 else x1)
    lo, hi = low + radius + half, high - radius - half
    base = min(max(along, lo), hi) if lo <= hi else (low + high) / 2
    point = (base, edge) if dy >= dx else (edge, base)
    distance = math.hypot(tx - point[0], ty - point[1])
    if short:
        length = min(min(max(WEDGE_SHORT_REACH * distance, WEDGE_MIN_PT / scale), WEDGE_SHORT_MAX_PT / scale), .9 * distance)
    else:
        entry = _head_entry(point, (tx, ty), head) if head is not None else None
        gap = min(max(.12 * distance, WEDGE_GAP_MIN_PT / scale), WEDGE_GAP_MAX_PT / scale)
        length = distance - gap if entry is None else entry - WEDGE_HEAD_GAP_PT / scale
        length = min(max(length, WEDGE_MIN_PT / scale), max(.9 * distance, distance - WEDGE_GAP_MAX_PT / scale))
    if _off_panel(target, bounds, scale):
        length = distance          # the compositor runs a tail to an off-panel speaker all the way to the border
    return point, (tx, ty), half, length


def _tail_parts(wedge):
    """A tail's path as (the wedge's triangle, its tip, the mouth): the triangle is drawn, the line on from its tip is read."""
    (bx, by), (tx, ty), half, length = wedge
    distance = math.hypot(tx - bx, ty - by)
    ux, uy = (tx - bx) / distance, (ty - by) / distance
    tip = (bx + ux * length, by + uy * length)
    return [(bx - half * uy, by + half * ux), (bx + half * uy, by - half * ux), tip], tip, (tx, ty)


def _polygon_meets_rect(polygon, rect):
    """True when a convex polygon and an axis-aligned rectangle touch (separating axis test)."""
    corners = [(rect[0], rect[1]), (rect[2], rect[1]), (rect[0], rect[3]), (rect[2], rect[3])]
    axes = [(1.0, 0.0), (0.0, 1.0)] + [(a[1] - b[1], b[0] - a[0]) for a, b in zip(polygon, polygon[1:] + polygon[:1])]
    for ax, ay in axes:
        mine = [px * ax + py * ay for px, py in polygon]
        theirs = [px * ax + py * ay for px, py in corners]
        if max(mine) < min(theirs) or min(mine) > max(theirs):
            return False
    return True


def _segment_meets_rect(a, b, rect):
    """True when the segment a to b touches the rectangle (Liang-Barsky clipping)."""
    lo, hi = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - rect[0]), (dx, rect[2] - a[0]), (-dy, a[1] - rect[1]), (dy, rect[3] - a[1])):
        if p == 0:
            if q < 0:
                return False
        elif p < 0:
            lo = max(lo, q / p)
        else:
            hi = min(hi, q / p)
    return lo <= hi


def _segment_gap(point, a, b):
    """Distance from a point to the segment a to b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    share = 0.0 if dx == dy == 0 else min(max(((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / (dx * dx + dy * dy), 0.0), 1.0)
    return math.hypot(point[0] - a[0] - share * dx, point[1] - a[1] - share * dy)


def tail_crosses(wedge, rect):
    """True when a tail's path touches a rectangle: the wedge as drawn (see tail_wedge), or the line on from its tip to the mouth.

    Near the base the wedge is as wide as it is drawn, so it, and not just its centre line, stays clear of the rectangle.
    """
    triangle, tip, mouth = _tail_parts(wedge)
    return _polygon_meets_rect(triangle, rect) or _segment_meets_rect(tip, mouth, rect)


def tails_cross(first, second):
    """True when two tails cross each other: each is the straight line from its wedge's base to its mouth (see tail_wedge).

    A drawn tail and the line read on from its tip lie on that line. Lines that only touch, share an end or run parallel
    do not cross.
    """
    (a, b), (c, d) = first[:2], second[:2]
    side = lambda p, q, r: (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return side(a, b, c) * side(a, b, d) < 0 and side(c, d, a) * side(c, d, b) < 0


def crossed_tails(result, targets, rounded, faces, scale=None):
    """(i, j) pairs of balloons in a place_boxes result whose tails, as the compositor draws them, cross each other, for
    different speakers (targets more than SAME_SPEAKER_PX apart)."""
    pts = 1.0 if scale is None else scale
    bounds, boxes = result['visible_rect'], result['boxes']
    wedges = [tail_wedge(boxes[i], result['corner'][i], t, bounds, pts, speaker_head(t, faces or []), result['short_tail'][i])
              if t is not None and rounded is not None and rounded[i] is not None else None for i, t in enumerate(targets or [])]
    return [(i, j) for i in range(len(wedges)) for j in range(i + 1, len(wedges))
            if wedges[i] is not None and wedges[j] is not None
            and math.hypot(targets[i][0] - targets[j][0], targets[i][1] - targets[j][1]) > SAME_SPEAKER_PX
            and tails_cross(wedges[i], wedges[j])]


def tail_meets_face(wedge, face):
    """True when a tail's path (see tail_crosses) enters a face zone, a circle (x, y, radius, name)."""
    triangle, tip, mouth = _tail_parts(wedge)
    centre, radius = (face[0], face[1]), face[2]
    sides = list(zip(triangle, triangle[1:] + triangle[:1]))
    inside = all((b[0] - a[0]) * (centre[1] - a[1]) - (b[1] - a[1]) * (centre[0] - a[0]) >= 0 for a, b in sides) or \
        all((b[0] - a[0]) * (centre[1] - a[1]) - (b[1] - a[1]) * (centre[0] - a[0]) <= 0 for a, b in sides)
    return inside or min(_segment_gap(centre, a, b) for a, b in sides + [(tip, mouth)]) < radius


def _tail_lengths(x0, y0, w, h, ratio, target, bounds, scale):
    """Tail length, wedge base to mouth, of boxes w x h with top left corners x0, y0 (arrays), as tail_wedge places it."""
    inset = WEDGE_EDGE_PT / scale
    tx, ty = min(max(target[0], bounds[0] + inset), bounds[2] - inset), min(max(target[1], bounds[1] + inset), bounds[3] - inset)
    x1, y1 = x0 + w, y0 + h
    dx, dy = np.maximum(np.maximum(x0 - tx, tx - x1), 0.0), np.maximum(np.maximum(y0 - ty, ty - y1), 0.0)
    half = max(WEDGE_HALF_MIN_PT, min(WEDGE_HALF_MAX_PT, WEDGE_HALF_SHARE * min(w, h) * scale)) / scale
    reach = ratio * min(w, h) + half
    base_x = np.where(w >= 2 * reach, np.minimum(np.maximum(tx, x0 + reach), x1 - reach), (x0 + x1) / 2)
    base_y = np.where(h >= 2 * reach, np.minimum(np.maximum(ty, y0 + reach), y1 - reach), (y0 + y1) / 2)
    vertical = dy >= dx                                 # the tail leaves through the top or bottom edge
    end_x, end_y = np.where(vertical, base_x, np.where(tx < x0, x0, x1)), np.where(vertical, np.where(ty < y0, y0, y1), base_y)
    return np.hypot(tx - end_x, ty - end_y)


READ_ROW_SHARE = .25         # tops within this share of the shorter box's height are level: a row, read left to right
LEFT_BELOW_SHARE = .1        # a later box at the left must start below the earlier one, overlapping it by at most this share
LENIENT_ROW_SHARE = .4       # the fallback rule, used only when no placement meets the strict one: tops this level are a row,
LENIENT_LEVEL_SHARE = 2 / 3  # ... and so is a later box starting lower by less than this share of the shorter box's height,
LENIENT_BAND_SHARE = .5      # ... or with at least this share of the shorter box's height inside the earlier box's band


def _reads_after(first, second, strict=True):
    """True when box `second`, of a later chunk, may read after box `first`, as a reader takes them.

    Tops within READ_ROW_SHARE of the shorter box's height are level, and a level later box must lie to the right (by
    centre). Otherwise a later box must start lower: to the right it may still overlap the earlier box's height, but
    to the left it must start below the earlier box (by at least its bottom, less LEFT_BELOW_SHARE of the shorter
    height), since a box at the left inside another's band is read first by some readers and second by others. The
    planner places boxes as high as the rule allows, so these are bounds a placement can sit on and still read right.

    With strict=False, the fallback for panels with no strictly ordered placement: tops within LENIENT_ROW_SHARE, or a
    later box starting lower by less than LENIENT_LEVEL_SHARE of the shorter height, or starting lower with at least
    LENIENT_BAND_SHARE of the shorter height inside the earlier box's band (a short box beside a tall one), are level
    (later to the right); otherwise the later box must start lower, wherever it sits.
    """
    short = min(first[3] - first[1], second[3] - second[1])
    dy = second[1] - first[1]
    right = second[0] + second[2] > first[0] + first[2]
    if not strict:
        band = min(first[3], second[3]) - max(first[1], second[1])        # the shared height of the two boxes
        if abs(dy) <= LENIENT_ROW_SHARE * short or 0 <= dy < LENIENT_LEVEL_SHARE * short or (dy >= 0 and band >= LENIENT_BAND_SHARE * short):
            return right
        return dy > 0
    if abs(dy) <= READ_ROW_SHARE * short:
        return right
    if dy < 0:
        return False
    return right or second[1] >= first[3] - LEFT_BELOW_SHARE * short


def _on_body(point, face):
    """True when a point lies on the body below a face zone (see BODY_HALF_WIDTH and BODY_DEPTH)."""
    x, y, r = face[0], face[1], face[2]
    return x - BODY_HALF_WIDTH * r <= point[0] <= x + BODY_HALF_WIDTH * r and y + r <= point[1] <= y + BODY_DEPTH * r


def _rule_message(i, culprit, placed, tried):
    """Why chunk i cannot be placed, when lifting one placement rule is what lets it: culprit is (rule, who)."""
    kind, who = culprit
    clear = 'every position that holds its text and clears everything else'
    if kind == 'tail':
        label = 'balloon' if placed[who] is not None else 'balloon (over its painted region)'
        return (f"chunk {i}: its tail would cross chunk {who}'s {label}: {clear} runs the tail from its balloon to "
                f"its speaker's mouth through it; {tried}")
    if kind == 'box':
        return (f"chunk {i}: its box would cross chunk {who}'s tail: {clear} lies across the tail from chunk {who}'s "
                f"balloon to its speaker's mouth; {tried}")
    if kind == 'face':
        return (f"chunk {i}: its tail would cross a face ({who}): {clear} runs the tail from its balloon to its "
                f"speaker's mouth across {who}; {tried}")
    if kind == 'tip':
        return (f"chunk {i}: its tail tip would point at another figure ({who}): {clear} ends the drawn tail nearer {who} "
                f"than its own speaker, or on {who}'s body, so a reader would credit the balloon to {who}; {tried}")
    if kind == 'uncross':
        return (f"chunk {i}: its tail would cross chunk {who}'s tail: {clear} runs the two tails across each other; {tried}")
    return (f"chunk {i}: its box would read before chunk {who}'s, against the script order: {clear} is above it, "
            f"or left of it on the same line; {tried}")


def _near(box, point, margin):
    """True when a point is inside a box or closer to it than `margin` pixels."""
    return box[0] - margin < point[0] < box[2] + margin and box[1] - margin < point[1] < box[3] + margin


def _trim_cover(cover, keepouts, margin):
    """The largest part of a cover that keeps every keep-out point clear; (cover or None, was it cut)."""
    cut = False
    original = (cover[2] - cover[0]) * (cover[3] - cover[1])
    for x, y in keepouts:
        if cover is None or not _near(cover, (x, y), margin):
            continue
        cut = True
        parts = [[cover[0], cover[1], x - margin, cover[3]], [x + margin, cover[1], cover[2], cover[3]],
                 [cover[0], cover[1], cover[2], y - margin], [cover[0], y + margin, cover[2], cover[3]]]
        parts = [q for q in parts if q[2] > q[0] and q[3] > q[1]]
        cover = max(parts, key=lambda q: (q[2] - q[0]) * (q[3] - q[1])) if parts else None
    if cover is not None and (cover[2] - cover[0]) * (cover[3] - cover[1]) < PARTIAL_MIN_SHARE * original:
        cover = None
    return cover, cut


def face_gap(box, ratio, face):
    """Distance from a face zone's edge to a box, in pixels; negative where they overlap.

    `face` is (x, y, radius, name). The box is taken as drawn: a rounded rectangle whose corner
    radius is `ratio` of its shorter side (a balloon), or a plain rectangle when `ratio` is None
    (a caption), so a face tucked beside a rounded corner is not counted as touched.
    """
    cx, cy, radius = face[0], face[1], face[2]
    x0, y0, x1, y1 = box
    corner = (ratio or 0) * min(x1 - x0, y1 - y0)
    qx = abs(cx - (x0 + x1) / 2) - ((x1 - x0) / 2 - corner)
    qy = abs(cy - (y0 + y1) / 2) - ((y1 - y0) / 2 - corner)
    return math.hypot(max(qx, 0.0), max(qy, 0.0)) + min(max(qx, qy), 0.0) - corner - radius


def _faces_clear(box, ratio, faces, margin):
    return all(face_gap(box, ratio, f) >= margin for f in faces)


def _nearest_face(box, ratio, faces):
    """(gap, name) of the face closest to a box, or None."""
    return min(((face_gap(box, ratio, f), f[3]) for f in faces), default=None)


def _painted_gap(painted, face):
    """Distance from a face zone's edge to a region's painted pixels; negative if the zone reaches them."""
    cx, cy, radius = face[0], face[1], face[2]
    ox, oy = painted['origin']
    mask = painted['mask']
    ix, iy = int(math.floor(cx - ox)), int(math.floor(cy - oy))
    if 0 <= iy < mask.shape[0] and 0 <= ix < mask.shape[1] and mask[iy, ix]:
        return -radius
    edge = painted['edge']
    if not len(edge):
        return float('inf')
    return float(np.hypot(edge[:, 0] - cx, edge[:, 1] - cy).min()) - radius


def _touching(bbox, bounds, touch):
    """Which frame edges (left, top, right, bottom) a painted region touches or is within `touch` px of."""
    return [bbox[0] - bounds[0] <= touch, bbox[1] - bounds[1] <= touch,
            bounds[2] - bbox[2] <= touch, bounds[3] - bbox[3] <= touch]


def _extended(bounds, flags, ratio, width, height):
    """The frame grown, on the flagged edges, by how far a rounded box may run past it.

    The text area and its padding (the box inset by the corner clearance, CORNER_CLEAR of the
    radius) must stay inside the frame, so a box may overhang a flagged edge by that clearance.
    """
    clear = CORNER_CLEAR * ratio * min(width, height)
    return [bounds[0] - (clear if flags[0] else 0), bounds[1] - (clear if flags[1] else 0),
            bounds[2] + (clear if flags[2] else 0), bounds[3] + (clear if flags[3] else 0)]


def _keep_zones(keep, bounds):
    """The keep zones ([x0, y0, x1, y1] source pixels) as (index in the list, the part inside the visible frame); empty parts are dropped."""
    zones = []
    for index, zone in enumerate(keep or []):
        clipped = _clip_rect(list(zone), bounds)
        if clipped[2] > clipped[0] and clipped[3] > clipped[1]:
            zones.append((index, clipped))
    return zones


def _covered_share(x0, y0, x1, y1, zone):
    """The share of a keep zone [x0, y0, x1, y1] that the rectangle x0, y0, x1, y1 covers; the rectangle's values may be arrays."""
    ix = np.maximum(np.minimum(x1, zone[2]) - np.maximum(x0, zone[0]), 0)
    iy = np.maximum(np.minimum(y1, zone[3]) - np.maximum(y0, zone[1]), 0)
    return ix * iy / ((zone[2] - zone[0]) * (zone[3] - zone[1]))


def _keep_hits(box, zones):
    """The indexes of the keep zones (see _keep_zones) that a box covers by KEEP_OVERLAP_MAX of the zone or more."""
    return [index for index, zone in zones if _covered_share(box[0], box[1], box[2], box[3], zone) >= KEEP_OVERLAP_MAX]


def _edge_sides(target, bounds):
    """Which frame edges (left, top, right, bottom) a tail target is on, or beyond: the edges its off-frame speaker is past."""
    return [target[0] <= bounds[0] + EDGE_PX, target[1] <= bounds[1] + EDGE_PX,
            target[0] >= bounds[2] - EDGE_PX, target[1] >= bounds[3] - EDGE_PX]


def _edge_clear(box, bounds, room):
    """True when a box keeps `room` px (left, top, right, bottom; 0 where nothing is asked) from the frame's edges."""
    gaps = (box[0] - bounds[0], box[1] - bounds[1], bounds[2] - box[2], bounds[3] - box[3])
    return all(ask == 0 or gap >= ask - 1e-9 for ask, gap in zip(room, gaps))


def _region_box(cover, width, height, bounds, obstacles, keepouts, margin, own, faces=(), face_margin=0,
                accept=None, bleed=None, shape=None, need=None, allow=None):
    """A box of at least width x height that covers a painted region, clear of obstacles and keep-out points.

    First choice is centred on the region. When that swallows the speaker's mouth (`own`) the box
    is grown away from it: the side nearest the mouth stays at the region's edge and the box
    extends the other way, along the vector from the mouth through the region's centre, then
    the two perpendicular ways. Failing those, any position that covers the region, stays
    inside the frame and clears everything is used, nearest the centred one. None if there is none.
    `accept`, if given, is a further test a box must pass. `bleed`, if given, is (flags, ratio):
    the box may then run past the flagged frame edges (see _extended), preferring to stay inside.
    A box also stays `face_margin` px clear of every face zone in `faces`, measured to its shape
    (`shape` is the corner ratio of a balloon, or None for a rectangle). `need`, if given, is
    need(height_px, corner ratio) -> the width in px a balloon of that height needs to keep the
    text width its wrap was sized for: a box made taller by the region it covers has more corner
    clearance, so it is widened to that width (plus a pixel), and everything else here is checked on the
    widened box. A box that already has the width it needs is left exactly as it was. `allow`, if given, is
    allow(box, corner ratio) -> True when the placement rules hold for the box (see place_boxes: tails clear of
    balloons and faces, reading order).
    """
    bw, bh = max(width, cover[2] - cover[0]), max(height, cover[3] - cover[1])
    if need is not None:
        wanted = need(bh, shape)
        if wanted > bw:
            bw = wanted + 1         # widened: one pixel to spare, as the option sizes carry
    reach = _extended(bounds, bleed[0], bleed[1], bw, bh) if bleed else bounds
    lo_x, hi_x = math.ceil(max(reach[0], cover[2] - bw)), math.floor(min(cover[0], reach[2] - bw))   # x0 keeping the cover
    lo_y, hi_y = math.ceil(max(reach[1], cover[3] - bh)), math.floor(min(cover[1], reach[3] - bh))
    if lo_x > hi_x or lo_y > hi_y:
        return None
    clamp = lambda v, lo, hi: min(max(v, lo), hi)
    cx, cy = (cover[0] + cover[2]) / 2, (cover[1] + cover[3]) / 2
    inside_x = (max(bounds[0], cover[2] - bw), min(cover[0], bounds[2] - bw))
    inside_y = (max(bounds[1], cover[3] - bh), min(cover[1], bounds[3] - bh))
    mid_x = clamp(round(cx - bw / 2), *(inside_x if inside_x[0] <= inside_x[1] else (lo_x, hi_x)))
    mid_y = clamp(round(cy - bh / 2), *(inside_y if inside_y[0] <= inside_y[1] else (lo_y, hi_y)))

    def box_at(x0, y0):
        return [x0, y0, x0 + bw, y0 + bh]

    refused = []                 # set when `allow` turned away a box that was clear in every other way

    def clear(x0, y0):
        box = box_at(x0, y0)
        if not (all(_apart(box, o, BOX_GAP_PX) for o in obstacles) and not any(_near(box, t, margin) for t in keepouts)
                and _faces_clear(box, shape, faces, face_margin) and (accept is None or accept(box))):
            return False
        if allow is not None and not allow(box, shape):
            refused.append(True)
            return False
        return True

    tries = [(mid_x, mid_y)]
    if own is not None:
        vx, vy = cx - own[0], cy - own[1]
        away_x, other_x = (lo_x, hi_x) if vx < 0 else (hi_x, lo_x)       # extend left / right
        away_y, other_y = (lo_y, hi_y) if vy < 0 else (hi_y, lo_y)       # extend up / down
        if abs(vx) >= abs(vy):
            tries += [(away_x, mid_y), (mid_x, away_y), (mid_x, other_y)]
        else:
            tries += [(mid_x, away_y), (away_x, mid_y), (other_x, mid_y)]
        tries += [(away_x, away_y)]
    for x0, y0 in tries:
        if clear(x0, y0):
            return box_at(x0, y0)
    xs, ys = {lo_x, hi_x, mid_x}, {lo_y, hi_y, mid_y}
    for o in obstacles:
        xs |= {o[2] + BOX_GAP_PX, o[0] - BOX_GAP_PX - bw}
        ys |= {o[3] + BOX_GAP_PX, o[1] - BOX_GAP_PX - bh}
    for tx, ty in keepouts:
        xs |= {math.ceil(tx + margin), math.floor(tx - margin - bw)}
        ys |= {math.ceil(ty + margin), math.floor(ty - margin - bh)}
    for face in faces:
        reach = face[2] + face_margin
        xs |= {math.ceil(face[0] + reach), math.floor(face[0] - reach - bw)}
        ys |= {math.ceil(face[1] + reach), math.floor(face[1] - reach - bh)}
    spots = sorted(((x, y) for x in xs if lo_x <= x <= hi_x for y in ys if lo_y <= y <= hi_y),
                   key=lambda q: abs(q[0] - mid_x) + abs(q[1] - mid_y))
    found = next((box_at(x0, y0) for x0, y0 in spots if clear(x0, y0)), None)
    if found is not None or not refused:
        return found
    # A tail path is a slanted strip, not an edge to sit against: look along the whole range of positions too.
    tried = set(spots)
    grid = sorted(((x, y) for x in {round(lo_x + (hi_x - lo_x) * k / 12) for k in range(13)}
                   for y in {round(lo_y + (hi_y - lo_y) * k / 12) for k in range(13)} if (x, y) not in tried),
                  key=lambda q: abs(q[0] - mid_x) + abs(q[1] - mid_y))
    return next((box_at(x0, y0) for x0, y0 in grid if clear(x0, y0)), None)


def _grow_to_hide(cover, width, height, same, painted, ratios, flags, need=None, allow=None):
    """(box, ratio): the smallest box over a rounded balloon that hides `painted`, or (None, None).

    Tries the box as sized, then a larger one: the box grows evenly on every side, by the least
    amount, until every painted pixel lies inside its rounded corners. Growth is measured from
    the box as it would be drawn, which is at least as large as the painted region. For each
    corner ratio from the full radius down to the minimum this is found separately, and the
    smaller box wins (the larger radius on a tie). With `flags`, the box may also run past the
    flagged edges.
    """
    bounds = same[0]
    bw, bh = max(width, cover[2] - cover[0]), max(height, cover[3] - cover[1])

    def attempt(grow, ratio):
        return _region_box(cover, bw + 2 * grow, bh + 2 * grow, *same,
                           accept=lambda box: painted_hidden(painted, box, ratio),
                           bleed=None if flags is None else (flags, ratio), shape=ratio, need=need, allow=allow)

    for ratio in ratios:
        box = attempt(0, ratio)
        if box is not None:
            return box, ratio
    room = int(CORNER_CLEAR * ratios[0] * min(bounds[2] - bounds[0], bounds[3] - bounds[1])) if flags else 0
    most = min(bounds[2] - bounds[0] - bw, bounds[3] - bounds[1] - bh) // 2 + room    # the most it can grow
    best = None
    for ratio in ratios:
        # Growth is not monotone (a larger box may swallow a tail point), so look upward for the first
        # growth that works, then bisect only between it and the last one that did not.
        failed, grow, high = 0, 1, None
        while most >= 1:
            trial = min(grow, most)
            if attempt(trial, ratio) is not None:
                high = trial
                break
            failed = trial
            if trial >= most:
                break
            grow *= 2
        if high is None:
            continue
        low = failed + 1
        while low < high:
            middle = (low + high) // 2
            if attempt(middle, ratio) is not None:
                high = middle
            else:
                low = middle + 1
        box = attempt(low, ratio)
        area = (box[2] - box[0]) * (box[3] - box[1])
        if best is None or area < best[0]:
            best = (area, box, ratio)
    return (best[1], best[2]) if best else (None, None)


def _trim_bleed(box, ratio, cover, same, painted, flags, allow=None):
    """Slide a box that runs past a frame edge back inside by as much as still hides the painted region."""
    bounds, obstacles, keepouts, margin, own, faces, face_margin = same

    def valid(b):
        reach = _extended(bounds, flags, ratio, b[2] - b[0], b[3] - b[1])
        return (b[0] >= reach[0] and b[1] >= reach[1] and b[2] <= reach[2] and b[3] <= reach[3]
                and b[0] <= cover[0] and b[1] <= cover[1] and b[2] >= cover[2] and b[3] >= cover[3]
                and all(_apart(b, o, BOX_GAP_PX) for o in obstacles)
                and not any(_near(b, t, margin) for t in keepouts) and _faces_clear(b, ratio, faces, face_margin)
                and (allow is None or allow(b, ratio)) and painted_hidden(painted, b, ratio))

    for _ in range(2):
        for axis in (0, 1):
            low, high = bounds[axis] - box[axis], box[axis + 2] - bounds[axis + 2]      # overhang past each edge
            if low > 0 and high <= 0:
                step, amount = 1, low
            elif high > 0 and low <= 0:
                step, amount = -1, high
            else:
                continue

            def moved(k, box=box, axis=axis, step=step):
                b = list(box)
                b[axis] += step * k
                b[axis + 2] += step * k
                return b

            lo, hi = 0, amount
            while lo < hi:
                middle = (lo + hi + 1) // 2
                if valid(moved(middle)):
                    lo = middle
                else:
                    hi = middle - 1
            box = moved(lo)
    return box


def _rounded_region_box(cover, width, height, bounds, obstacles, keepouts, margin, own, painted, ratios, flags=None,
                        faces=(), face_margin=0, need=None, allow=None):
    """A box over a rounded balloon that hides a painted region's corners: (box, corner ratio, blocked).

    First inside the frame (see _grow_to_hide). Only if that cannot hide the corners, and the
    painted region touches a frame edge (`flags`, see _touching), the box may run off those
    edges, by no more than the text area and its padding allow, and then by no more than needed
    (see _trim_bleed). `blocked` is True when a box without the corner rule exists but no
    rounded one does.
    """
    same = (bounds, obstacles, keepouts, margin, own, faces, face_margin)
    if _region_box(cover, width, height, *same, shape=ratios[0], need=need, allow=allow) is None:
        return None, None, False
    box, ratio = _grow_to_hide(cover, width, height, same, painted, ratios, None, need, allow)
    if box is not None:
        return box, ratio, False
    if flags is not None and any(flags):
        box, ratio = _grow_to_hide(cover, width, height, same, painted, ratios, flags, need, allow)
        if box is not None:
            return _trim_bleed(box, ratio, cover, same, painted, flags, allow), ratio, False
    return None, None, True


def _edge_integral(image_path, bounds):
    """Integral image of local edge strength (luminance gradient), for fast window sums."""
    with Image.open(image_path) as image:
        lum = np.asarray(image.convert('L'), dtype=np.float64)
    edge = np.abs(np.diff(lum, axis=1, prepend=lum[:, :1])) + np.abs(np.diff(lum, axis=0, prepend=lum[:1]))
    integral = np.zeros((edge.shape[0] + 1, edge.shape[1] + 1))
    integral[1:, 1:] = edge.cumsum(0).cumsum(1)
    x0, y0, x1, y1 = bounds
    mean = (integral[y1, x1] - integral[y0, x1] - integral[y1, x0] + integral[y0, x0]) / max(1, (x1 - x0) * (y1 - y0))
    return integral, mean


def _quiet_window(integral, mean, bounds, size, obstacles, targets, previous, faces=(), face_margin=0, accept=None,
                  lead=None, keeps=(), room=None, top=TOP_WEIGHT, inside=None):
    """Best clear window of `size`: low edge density, high in the frame (by `top`), in reading order, off the targets.

    `accept`, if given, is a further test on a window ([x0, y0, x1, y1]); the best one that passes is returned.
    `keeps`, if given, are keep zones as _keep_zones has them: a window covering KEEP_OVERLAP_MAX of one or more is not
    valid. `room`, if given, is (left, top, right, bottom) px a window must keep from those frame edges (0: no demand).
    `lead`, if given, is (mouth, corner ratio, scale) of a balloon whose speaker is in the frame: windows are then
    ranked by tail length first (see place_boxes) and by the cost above only within a step of TAIL_NEAR_SHARE.
    """
    x0, y0, x1, y1 = bounds
    w, h = size
    step = max(4, min(w, h) // 8)
    xs, ys = np.arange(x0, x1 - w + 1, step), np.arange(y0, y1 - h + 1, step)
    if inside is not None:
        # Seed each zone independently, including its last fitting integer position.
        # Filtering only the frame grid would miss narrow or off-grid blank bands.
        axes = [[], []]
        for a, b, c, d in inside:
            lo_x, lo_y = math.ceil(max(x0, a)), math.ceil(max(y0, b))
            hi_x, hi_y = math.floor(min(x1, c) - w), math.floor(min(y1, d) - h)
            if lo_x <= hi_x and lo_y <= hi_y:
                for axis, lo, hi in ((0, lo_x, hi_x), (1, lo_y, hi_y)):
                    axes[axis].extend(range(lo, hi + 1, step))
                    axes[axis].append(hi)
        xs, ys = (np.array(sorted(set(axis)), dtype=int) for axis in axes)
    if not len(xs) or not len(ys):
        return None
    X, Y = xs[None, :], ys[:, None]
    sums = integral[Y + h, X + w] - integral[Y, X + w] - integral[Y + h, X] + integral[Y, X]
    cost = sums / (w * h) / (mean + 1e-6)
    cost = cost + top * ((Y + h / 2 - y0) / (y1 - y0))                      # prefer the top of the frame
    invalid = np.zeros(cost.shape, bool)
    if inside is not None:
        held = np.zeros(cost.shape, bool)
        for a, b, c, d in inside:
            held |= (X >= a) & (Y >= b) & (X + w <= c) & (Y + h <= d)
        invalid |= ~held
    for o in obstacles:
        invalid |= (X + w > o[0] - BOX_GAP_PX) & (X < o[2] + BOX_GAP_PX) & (Y + h > o[1] - BOX_GAP_PX) & (Y < o[3] + BOX_GAP_PX)
    guard = TARGET_GUARD * min(x1 - x0, y1 - y0)
    for tx, ty in targets:
        nearest = np.hypot(np.maximum(np.maximum(X - tx, tx - (X + w)), 0), np.maximum(np.maximum(Y - ty, ty - (Y + h)), 0))
        invalid |= nearest < guard
    for face in faces:
        nearest = np.hypot(np.maximum(np.maximum(X - face[0], face[0] - (X + w)), 0),
                           np.maximum(np.maximum(Y - face[1], face[1] - (Y + h)), 0))
        invalid |= nearest < face[2] + face_margin
    for _, zone in keeps:
        invalid |= _covered_share(X, Y, X + w, Y + h, zone) >= KEEP_OVERLAP_MAX
    if room is not None:
        for ask, off in zip(room, (X - x0, Y - y0, x1 - (X + w), y1 - (Y + h))):
            if ask:
                invalid |= off < ask - 1e-9
    if previous is not None:                                                # keep reading order
        pcx, pcy, ph = (previous[0] + previous[2]) / 2, (previous[1] + previous[3]) / 2, previous[3] - previous[1]
        cx, cy = X + w / 2, Y + h / 2
        half = .5 * max(h, ph)
        cost = cost + 1.5 * ((cy < pcy - half) | ((np.abs(cy - pcy) <= half) & (cx < pcx)))
    cost = np.where(invalid, np.inf, cost)
    if not np.isfinite(cost).any():
        return None
    flat = cost.ravel()

    def window(index):
        row, col = np.unravel_index(index, cost.shape)
        return [int(xs[col]), int(ys[row]), int(xs[col]) + w, int(ys[row]) + h]

    if lead is None:
        order, first = None, int(np.argmin(flat))
    else:
        diagonal = math.hypot(x1 - x0, y1 - y0)
        length = np.broadcast_to(_tail_lengths(X, Y, w, h, lead[1], lead[0], bounds, lead[2]), cost.shape).ravel()
        over = length > TAIL_MAX_SHARE * diagonal          # long tails come last, shortest first, only if nothing else is valid
        order = np.lexsort((flat, np.where(over, length, np.floor(length / (TAIL_NEAR_SHARE * diagonal))), over,
                            ~np.isfinite(flat)))
        first = int(order[0])
    if accept is None or accept(window(first)):
        return window(first)
    for index in (np.argsort(flat, kind='stable') if order is None else order):      # the next best windows, in order
        if not np.isfinite(flat[index]):
            break
        if index != first and accept(window(int(index))):
            return window(int(index))
    return None


def _cause(sizes, cover, bounds, neighbours, keepouts, margin, corner_blocked=False, min_ratio=None):
    """Why no option of a chunk could be placed, in words: the smallest box against what it must avoid."""
    fits = [z for z in sizes if z[0] <= bounds[2] - bounds[0] and z[1] <= bounds[3] - bounds[1]]
    if not sizes:
        return 'it has no size options'
    if not fits:
        w, h = min(sizes, key=lambda z: z[0] * z[1])
        return f'even its smallest box, {w} x {h} px, is larger than the visible frame'
    w, h = min(fits, key=lambda z: z[0] * z[1])
    if cover is None:
        return f'no clear area of {w} x {h} px remains in the frame'
    bw, bh = max(w, cover[2] - cover[0]), max(h, cover[3] - cover[1])
    lo_x, hi_x = max(bounds[0], cover[2] - bw), min(cover[0], bounds[2] - bw)
    lo_y, hi_y = max(bounds[1], cover[3] - bh), min(cover[1], bounds[3] - bh)
    causes = []
    if corner_blocked:
        causes.append(f"the corners of its painted region cannot be hidden: a balloon keeps a corner radius of at least "
                      f"{min_ratio:.0%} of its shorter side, may run off a frame edge only where its region touches it, "
                      f"and cannot grow into its neighbours")
    for j, rect, kind in neighbours:
        if not _apart(cover, rect, BOX_GAP_PX):
            causes.append(f"its painted region is within {BOX_GAP_PX} px of chunk {j}'s {kind}, so their boxes would overlap")

    def blocked(lo, hi, size, spans):
        """True when the forbidden intervals leave no position for a box's low edge between lo and hi."""
        pieces = [(lo, hi)]
        for a, b in spans:
            pieces = [q for p, r in pieces for q in ([(p, min(r, a))] if p <= a else []) + ([(max(p, b), r)] if r >= b else [])]
        return not pieces

    # A neighbour blocks one axis when every position overlaps it on the other axis; all blockers of an axis together.
    in_y = [(j, rect, kind) for j, rect, kind in neighbours if lo_y > rect[1] - BOX_GAP_PX - bh and hi_y < rect[3] + BOX_GAP_PX]
    in_x = [(j, rect, kind) for j, rect, kind in neighbours if lo_x > rect[0] - BOX_GAP_PX - bw and hi_x < rect[2] + BOX_GAP_PX]
    for blockers, lo, hi, size, at in ((in_y, lo_x, hi_x, bw, 0), (in_x, lo_y, hi_y, bh, 1)):
        if blockers and blocked(lo, hi, size, [(r[at] - BOX_GAP_PX - size, r[at + 2] + BOX_GAP_PX) for _, r, _ in blockers]):
            names = ' or '.join(f"chunk {j}'s {kind}" for j, _, kind in blockers)
            causes.append(f"even its smallest box, {bw} x {bh} px, would always overlap {names}")
            break
    for j, (tx, ty) in keepouts:
        if lo_x > tx - margin - bw and hi_x < tx + margin and lo_y > ty - margin - bh and hi_y < ty + margin:
            causes.append(f"any box that covers its painted region and holds the text, at least {bw} x {bh} px, is within "
                          f"{margin} px of the tail point of chunk {j} at ({round(tx)}, {round(ty)})")
    return '; '.join(causes) or f'its smallest box, {bw} x {bh} px, cannot avoid every neighbour and tail point at once'


def place_boxes(image_path, found, options, targets=None, *, tail_margin=TAIL_MARGIN_PX, rounded=None, bleed=None,
                faces=None, face_margin=FACE_MARGIN_PX, widen=None, scale=None, keep=None, uncross=False, inside=None):
    """Place one drawn box per chunk, none overlapping, all inside the visible frame.

    `found` is find_regions() output. options[i] lists the (width, height) pixel sizes that
    would hold chunk i's text, most preferred first. targets[i] is chunk i's tail target
    (x, y), the speaker's mouth, or None.

    `inside[i]` is None or a list of source-pixel rectangles. Its whole box must fit
    in one rectangle, on every search and retry. An empty list permits no placement.
    Matching soft `keep` rectangles are ignored for that chunk only.

    A chunk whose reading-order position has a painted region gets a box that covers its
    bounding box plus 8 px, so no painted outline shows. A box never covers a tail target
    (its own or another chunk's) or comes within `tail_margin` px of one: when the box centred
    on its region would, it is grown away from the target (see _region_box). If a painted
    region itself contains a target, the largest part of it that keeps the target clear is
    covered instead and the chunk is reported in "partial". A target on or beyond the visible
    frame's edge belongs to an off-frame speaker and never blocks anything. A chunk with no
    painted region goes in the clearest window (see below). Options are tried in order, narrower
    wraps last, until one can be placed; PlacementError names the chunk when none can.

    rounded[i] is None for a chunk drawn as a rectangle (a caption) or (ratio, minimum ratio)
    for a balloon whose corners have radius `ratio` of its shorter side. A rounded box over a
    painted region must hide every painted pixel, corners included: it grows, or its radius is
    reduced toward the minimum, whichever keeps it smaller (see _rounded_region_box). A region
    that is only partly covered is not held to this.

    `bleed` is a distance in pixels, or None. When a painted region touches or is within that
    distance of a frame edge, and only then, a rounded box that cannot hide its corners inside the
    frame may run past that edge, by at most the corner clearance and no more than needed, because
    the panel clips it there. A caption (rounded None) never does.

    `faces` lists face zones as (x, y, radius, name) in pixels. No box, as drawn (its rounded shape
    and any bleed included), comes within `face_margin` px of one. A painted region that itself
    reaches a face cannot be covered without covering it, and a box that every option would push
    onto a face cannot be placed; both raise PlacementError saying the box "would cover a face" and
    naming the chunk and the face. The quiet-window search avoids faces too.

    `widen[i][k]`, if given, is None or need(height_px, corner ratio) -> px for option k of chunk i.
    A balloon's text area is inset by its padding plus a corner clearance that grows with its shorter
    side, so a box that must cover a painted region taller than the option is (or that grows to hide
    the region's corners) has a narrower text area than the wrap was sized for and the copy would
    re-wrap. Such a box is widened to need(its height, its corner ratio), and every check (frame,
    neighbours, tail points, faces, hidden corners) is made on the widened box. A `need` that asks for
    no more than the box already has changes nothing.

    A tail is read as pointing at whoever it reaches, so a balloon with a tail (rounded and a target)
    is placed to be read correctly. `scale` is points per source pixel and sizes the tail's wedge (see
    tail_wedge; 1 when omitted). (1) The tail's path, from the balloon's wedge base to the mouth, is the wedge
    as drawn (as wide as its base where it starts, tapering to its tip) and the line on from the tip (see
    tail_crosses). It never crosses another chunk's balloon (a later chunk's painted region stands for its
    balloon), and no box lies across another chunk's tail path; off-frame targets run to the edge. (2) When the
    speaker is in the frame, the path never enters a face zone other than the speaker's own (the zone nearest
    the mouth, and any that holds the mouth or overlaps that zone). (3) Readers credit a balloon to whoever its
    drawn tail's tip lands nearest, and the tip often stops well short of the mouth: when the speaker is in the
    frame (and faces are known), the tip of the wedge (see _tail_parts) is never nearer to another face zone than to
    the speaker's own zones (the ones rule 2 spares), each measured to the zone's edge and 0 inside it, and it never
    lands on another figure's body (see _on_body) unless it is on the speaker's own as well. (4) Boxes read in
    script order, by their tops: box j, after box i for i < j, lies to its right (by centre) where their tops are level
    (within READ_ROW_SHARE of the shorter box's height), and otherwise starts lower than it (see _reads_after). Each is a test a position must pass, so the other positions and
    narrower wraps are tried; PlacementError names the chunk and the tail, face or chunk it cannot be placed
    clear of. (5) A balloon with a painted region stays where it covers it. One
    without goes as near its speaker (or, for a voice off frame, its point on the edge) as it validly can: candidate windows
    are ranked by tail length (wedge base to mouth) in steps of TAIL_NEAR_SHARE of the frame's diagonal,
    and quietness only breaks ties within a step. A tail longer than TAIL_MAX_SHARE of the diagonal is
    accepted only when no position within that limit is valid, and then the shortest valid one is taken. If the
    chunks cannot all be placed that way, nearness is given up only where needed (the rules above still hold): for the
    failing chunk, then for it and one earlier chunk at a time (the nearest first), then for every chunk; the first
    failure is reported if all of that fails too.

    The tail in rules (1) to (3) is the one the compositor draws when it knows the speaker's head: it runs to just outside
    the head (see tail_wedge and speaker_head), so it is long. A chunk that no position (of any size option, with or without
    the soft wishes below) lets through under that tail is tried again with the legacy short tail (tail_wedge with `short`:
    60 percent of the way, 28 pt at most) and, if that places it, is listed in "short_tail"; the compositor then draws that
    tail too (a reserve's "tail_short", see run_chapter.drawn_geometry). Every later chunk is checked against the tail
    each earlier chunk was placed with. If the greedy order still strands a chunk, the last resort is the planner as it was
    before tails knew heads (every balloon with the short tail, all the passes above), and then each balloon's long tail goes
    back wherever it reads right in that layout, the boxes staying where they are (a "pins" pass of _place_boxes). Where neither
    places the panel it fails as it did, the error explaining the long tails.

    Two more wishes are soft: a chunk is placed to meet them when any position (of any size option) does, and
    without them, as before, when none does. (a) A balloon whose target is on the frame's edge (an off-frame voice)
    keeps WEDGE_MIN_PT plus WEDGE_STROKE_PT (points, so `scale` converts) between its box and that edge, so the
    compositor draws a tail and not a clipped stub; "edge_voice_no_tail" lists the chunks that could not (they touch the
    edge, or sit too near it, and their tail is missing or only a stub). (b) `keep`, if given, lists keep zones, [x0, y0, x1, y1] in
    source pixels (story-critical art, see run_chapter.parse_keep); a box covering KEEP_OVERLAP_MAX (a tenth) or
    more of the visible part of any of them is not valid, and "keep_overlaps" maps each chunk that could not keep off them to the indexes
    of the zones it covers that much. When both cannot be had, the keep zones win: the balloon gives up its tail room first.

    With `uncross`, two speakers' tails are not left crossing each other where the search can keep them apart: when the
    layout above has such an X (see crossed_tails), the whole search runs again with one more rule, that a balloon's tail
    never crosses an earlier balloon's tail unless both point at one speaker (as rule (1), and an earlier chunk is moved
    when a later one cannot keep clear of its tail). That layout is taken only if it covers no keep zone the first did
    not and leaves no more off-frame voices without tail room; otherwise, or when there is none, the first layout stands.
    A layout with no crossing tails is returned exactly as without `uncross`.

    Returns {"visible_rect", "boxes": [[x0, y0, x1, y1]], "painted": [bool], "partial": [bool],
    "corner": [ratio or None], "bleed": [[left, top, right, bottom] px past the frame],
    "face_clearance": [(px to the nearest face, its name) or None], "choice": [option index],
    "keep_overlaps": {chunk: [keep index]}, "edge_voice_no_tail": [chunk], "short_tail": [bool]} (the last, one per chunk:
    True where only the short tail placed it).
    """
    if inside is not None and len(inside) != len(options):
        raise ValueError('inside must have one entry per chunk')
    kwargs = dict(tail_margin=tail_margin, rounded=rounded, bleed=bleed, faces=faces, face_margin=face_margin,
                  widen=widen, scale=scale, keep=keep, inside=inside)
    plain = _place_all(image_path, found, options, targets, kwargs)
    if not uncross or not crossed_tails(plain, targets, rounded, faces, scale):
        return plain
    try:
        apart = _place_all(image_path, found, options, targets, dict(kwargs, uncross=True))
    except PlacementError:
        return plain
    worse = any(not set(zones) <= set(plain['keep_overlaps'].get(i, [])) for i, zones in apart['keep_overlaps'].items()) \
        or not set(apart['edge_voice_no_tail']) <= set(plain['edge_voice_no_tail'])
    return plain if worse or crossed_tails(apart, targets, rounded, faces, scale) else apart


def _place_all(image_path, found, options, targets, kwargs):
    """place_boxes' whole search (see there) with one set of rules: kwargs as place_boxes builds them, with "uncross"."""
    scale, rounded = kwargs['scale'], kwargs['rounded']
    try:
        return _cascade(image_path, found, options, targets, kwargs)[0]
    except PlacementError as error:
        # Last resort: the planner as it was before tails knew heads, every balloon with the short tail. The greedy order
        # that lets each chunk have the tail it can may still strand a later one, which the short tails never did.
        pts = 1.0 if scale is None else scale
        if not any(rounded is not None and rounded[i] is not None and t is not None and not _off_panel(t, found['visible_rect'], pts)
                   for i, t in enumerate(targets or [])):
            raise
        try:
            legacy, strict = _cascade(image_path, found, options, targets, dict(kwargs, legacy=True))
        except PlacementError:
            raise error from None
    # The long tail goes back on every chunk whose long tail reads right in that layout, one chunk at a time in script order.
    pins = list(zip(legacy['boxes'], legacy['corner'], legacy['choice']))
    try:
        return _place_boxes(image_path, found, options, targets, near=[True] * len(options), **dict(kwargs, strict=strict, pins=pins))
    except PlacementError:
        return legacy


def _cascade(image_path, found, options, targets, kwargs):
    """place_boxes' search: (the result, whether the strict reading order placed it), or the first PlacementError."""
    # Placement is greedy: an early chunk can take the quiet bottom of the frame and leave the later ones no place that
    # reads after it, so each reading-order rule is tried at the usual top preference and then at stronger ones. The
    # strict rule comes first; the lenient one only when nothing meets it. The lenient default's error is reported.
    first_error, blocked = None, []
    for strict in (True, False):
        for top in (TOP_WEIGHT,) + TOP_RETRY:
            try:
                return _place_relaxed(image_path, found, options, targets, dict(kwargs, top=top, strict=strict)), strict
            except PlacementError as error:
                if not strict and top == TOP_WEIGHT:
                    first_error = error
                blocked.append(error)
    # Greedy placement never revisits a chunk: when a later chunk is stopped by an earlier chunk's box, re-place with
    # that box barred from the spot it took, for a few rounds. A panel that placed above is placed exactly as before.
    for strict in (True, False):
        avoid, error = {}, next((e for e in blocked if e.blocker is not None), None)
        for _ in range(REPAIR_ROUNDS):
            if error is None or error.blocker is None:
                break
            who, rect = error.blocker
            avoid = {**avoid, who: avoid.get(who, []) + [list(rect)]}
            error = None
            for top in (TOP_WEIGHT,) + TOP_RETRY:
                try:
                    return _place_relaxed(image_path, found, options, targets, dict(kwargs, top=top, strict=strict, avoid=avoid)), strict
                except PlacementError as failure:
                    if error is None or (failure.blocker is not None and error.blocker is None):
                        error = failure
    raise first_error from None


def _place_relaxed(image_path, found, options, targets, kwargs):
    """place_boxes at one top preference: every chunk near its speaker first, then nearness given up where needed."""
    count, rounded = len(options), kwargs['rounded']
    try:
        return _place_boxes(image_path, found, options, targets, near=[True] * count, **kwargs)
    except PlacementError as error:
        free = [i for i in range(count) if i >= len(found['regions']) and targets is not None and rounded is not None
                and rounded[i] is not None and targets[i] is not None]
        if not free or (error.chunk is not None and error.chunk < free[0]):
            raise                       # no chunk is ranked by proximity, or the failure came before the first one
        # Give up nearness only where it is needed: the failing chunk first, then with it one earlier chunk at a
        # time (the nearest first), and only then every chunk (quietness alone, as a single pass did before).
        failing = error.chunk if error.chunk in free else None
        tries = []
        if failing is not None:
            tries.append({failing})
            tries += [{failing, j} for j in reversed(free) if j < failing]
        tries.append(set(free))
        for relaxed in tries:
            try:
                return _place_boxes(image_path, found, options, targets, near=[i not in relaxed for i in range(count)],
                                    **kwargs)
            except PlacementError:
                continue
        raise error from None


def _place_boxes(image_path, found, options, targets, tail_margin, rounded, bleed, faces, face_margin, widen, scale, keep, near,
                 top=TOP_WEIGHT, strict=True, avoid=None, legacy=False, pins=None, uncross=False, inside=None):
    """One placement pass of place_boxes; near[i] ranks free balloon i's windows by tail length before quietness.

    With `legacy` every balloon gets the short tail and none is tried with the long one. With `pins`, a (box, corner ratio,
    size option) per chunk, nothing is searched: each chunk is checked at its pinned place, long tail first, and is placed
    there or the pass fails. With `uncross` a balloon's tail may not cross an earlier balloon's tail either (see place_boxes).
    """
    faces = list(faces or [])
    rules = RULES + (('uncross',) if uncross else ())
    bounds = found['visible_rect']
    regions = found['regions']
    targets = list(targets) if targets is not None else [None] * len(options)
    pts = 1.0 if scale is None else scale
    zones = _keep_zones(keep, bounds)
    tail_room = (WEDGE_MIN_PT + WEDGE_STROKE_PT) / pts                                  # what an off-frame voice's tail needs, in px
    rooms = [None] * len(options)                                                      # per chunk: the room it asks of the edges it is beyond
    aimed = [(j, t) for j, t in enumerate(targets) if t is not None and not on_frame_edge(t, bounds)]
    aims = [t for _, t in aimed]                                                       # keep-out points
    covers, partial = [], []       # what each chunk's box must hide: its painted region plus a margin
    for i in range(len(options)):
        cover, cut = None, False
        if i < len(regions):
            x0, y0, x1, y1 = regions[i]['bbox']
            cover, cut = _trim_cover(_clip_rect([x0 - COVER_PX, y0 - COVER_PX, x1 + COVER_PX, y1 + COVER_PX], bounds),
                                     aims, tail_margin)
        covers.append(cover)
        partial.append(cut)
    for i in range(min(len(options), len(regions))):
        for face in faces:
            if _painted_gap(regions[i]['painted'], face) < face_margin:
                raise PlacementError(f"chunk {i}: its box would cover a face ({face[3]}): the painted region it must "
                                     f"hide reaches {face[3]}", i)
    painted = [i < len(regions) for i in range(len(options))]
    placed, choice = [None] * len(options), [None] * len(options)
    shorts = [False] * len(options)                    # per chunk: placed with the legacy short tail (see place_boxes), not the long one
    corner = [None if rounded is None or rounded[i] is None else rounded[i][0] for i in range(len(options))]
    edge = None
    for i, sizes in enumerate(options):
        inside_zones = None if inside is None else inside[i]
        # A hard write constraint takes priority over its own soft keep rectangle.
        chunk_zones = zones if inside_zones is None else [(j, z) for j, z in zones if not any(list(z) == list(h) for h in inside_zones)]
        # Earlier chunks are placed; later chunks with a painted region keep their cover clear.
        neighbours = [(j, placed[j] if placed[j] is not None else covers[j],
                       'box' if placed[j] is not None else 'painted region')
                      for j in range(len(options)) if j != i and (placed[j] is not None or covers[j] is not None)]
        obstacles = [rect for _, rect, _ in neighbours] + list((avoid or {}).get(i, ()))   # spots a repair has barred
        own = targets[i] if targets[i] is not None and not on_frame_edge(targets[i], bounds) else None
        ratios = None if rounded is None or rounded[i] is None else (rounded[i][0], rounded[i][1])
        balloon = ratios is not None and targets[i] is not None          # a speech balloon with a tail
        # What this chunk's placement must respect so its tail reads correctly and the balloons read in order.
        wedges = [(j, w) for j in range(len(options)) if j != i and placed[j] is not None and rounded is not None
                  and rounded[j] is not None and targets[j] is not None
                  for w in [tail_wedge(placed[j], corner[j], targets[j], bounds, pts, speaker_head(targets[j], faces), shorts[j])]
                  if w is not None]
        theirs, ours = [], []          # the face zones this chunk's tail must not enter (not its speaker's), and its speaker's
        if own is not None and balloon and faces:
            dist = lambda f: math.hypot(own[0] - f[0], own[1] - f[1]) - f[2]
            nearest = min(faces, key=dist)      # the speaker's zone, and any that holds the mouth or overlaps it
            theirs = [f for f in faces if f is not nearest and dist(f) > 0
                      and math.hypot(f[0] - nearest[0], f[1] - nearest[1]) >= f[2] + nearest[2]]
            ours = [f for f in faces if f not in theirs]
        elif balloon and faces and targets[i] is not None:
            theirs = list(faces)                # an off-frame voice: its tail runs to the edge, and no face is its speaker's
        before = [(j, placed[j]) for j in range(i) if placed[j] is not None]      # the boxes that read before this one

        def breach(box, ratio, kinds=rules, short=False):
            """The first placement rule (of `kinds`) that `box` breaks, as (kind, who), or None; `short`: with the short tail."""
            if inside_zones is not None and not any(a <= box[0] and b <= box[1] and box[2] <= c and box[3] <= d
                                            for a, b, c, d in inside_zones):
                return 'inside', i
            mine = None
            if balloon and ('cross' in kinds or 'face' in kinds or 'tip' in kinds):
                mine = tail_wedge(box, ratios[0] if ratio is None else ratio, targets[i], bounds, pts, speaker_head(targets[i], faces), short)
            if 'cross' in kinds:
                if mine is not None:
                    for j, rect, _ in neighbours:
                        if tail_crosses(mine, rect):
                            return 'tail', j
                for j, wedge in wedges:
                    if tail_crosses(wedge, box):
                        return 'box', j
            if 'face' in kinds and mine is not None:
                for f in theirs:
                    if tail_meets_face(mine, f):
                        return 'face', f[3]
            if 'tip' in kinds and mine is not None and own is not None and theirs:
                tip = _tail_parts(mine)[1]
                reach = lambda f: max(0.0, math.hypot(tip[0] - f[0], tip[1] - f[1]) - f[2])
                held = min(reach(f) for f in ours)
                for f in theirs:
                    if reach(f) < held:
                        return 'tip', f[3]
                # A tip on another figure's body reads as theirs too, however near the speaker's face it is.
                if not any(_on_body(tip, f) for f in ours):
                    for f in theirs:
                        if _on_body(tip, f):
                            return 'tip', f[3]
            if 'uncross' in kinds and mine is not None:
                for j, wedge in wedges:
                    if math.hypot(targets[j][0] - targets[i][0], targets[j][1] - targets[i][1]) > SAME_SPEAKER_PX \
                            and tails_cross(mine, wedge):
                        return 'uncross', j
            if 'order' in kinds:
                for j, rect in before:
                    if not _reads_after(rect, box, strict):
                        return 'order', j
            return None

        governed = bool(wedges or theirs or before or balloon or inside_zones is not None)
        lead = (targets[i], ratios[0], pts) if near[i] and balloon else None   # an off-frame voice goes near its edge point too
        corner_blocked = False
        blocker = None                 # the face an unconstrained box for this chunk would have covered
        previous = next((placed[j] for j in range(i - 1, -1, -1) if placed[j] is not None), None)

        voice = balloon and on_frame_edge(targets[i], bounds)        # a balloon for a speaker off frame: its tail needs room
        if voice:
            rooms[i] = tuple(tail_room if beyond else 0.0 for beyond in _edge_sides(targets[i], bounds))
        wishes = tuple(name for name, asked in (('keep', bool(chunk_zones)), ('edge', voice)) if asked)   # the soft ones, most wanted first
        levels = [wishes]              # tried in turn: all wishes, then all but one, then none (as the planner always did)
        for dropped in ('edge', 'keep'):
            fewer = tuple(name for name in wishes if name != dropped)
            if fewer not in levels:
                levels.append(fewer)
        if () not in levels:
            levels.append(())

        def solve(width, height, need, active, kinds=rules, soft=(), short=False):
            allow = (lambda b, q: breach(b, q, kinds, short) is None) if governed and (kinds or inside_zones is not None) else None
            keeps, clear = (chunk_zones if 'keep' in soft else ()), (rooms[i] if 'edge' in soft else None)
            if covers[i] is not None and (keeps or clear):
                hard = allow
                allow = lambda b, q: ((hard is None or hard(b, q)) and not _keep_hits(b, keeps)
                                      and (clear is None or _edge_clear(b, bounds, clear)))
            if covers[i] is not None and ratios is not None and not partial[i]:
                flags = _touching(regions[i]['bbox'], bounds, bleed) if bleed is not None else None
                return _rounded_region_box(covers[i], width, height, bounds, obstacles, aims, tail_margin, own,
                                           regions[i]['painted'], ratios, flags, active, face_margin, need, allow)
            if covers[i] is not None:
                return (_region_box(covers[i], width, height, bounds, obstacles, aims, tail_margin, own,
                                    active, face_margin, need=need, allow=allow), None, False)
            return (_quiet_window(edge[0], edge[1], bounds, (width, height), obstacles, aims, previous,
                                  active, face_margin, None if allow is None else (lambda b: allow(b, None)), lead,
                                  keeps, clear, top, inside=inside_zones), None, False)

        # The long tail first. Only a chunk no position of which (any size, with or without the soft wishes) the long tail
        # lets through is tried again with the legacy short one; an off-panel voice's tail runs to the border either way.
        tails = (((True,) if legacy else (False, True)) if balloon and not _off_panel(targets[i], bounds, pts) else (False,))
        if pins is not None:                # a layout to check, not to search: the chunk stays where it was, with the tail it can have
            box, ratio, k = pins[i]
            short = next((model for model in tails if breach(box, ratio, rules, model) is None), None)
            if short is None:
                raise PlacementError(f'chunk {i}: its tail does not read right in the layout it was to keep', i)
            placed[i], choice[i], shorts[i] = box, k, short
            if ratio is not None:
                corner[i] = ratio
            continue
        for short in tails:
            for soft in levels:
                for k, (width, height) in enumerate(sizes):
                    if width > bounds[2] - bounds[0] or height > bounds[3] - bounds[1]:
                        continue
                    need = widen[i][k] if widen is not None and widen[i] is not None and k < len(widen[i]) else None
                    if covers[i] is None and edge is None:
                        edge = _edge_integral(image_path, bounds)
                    box, ratio, blocked = solve(width, height, need, faces, rules, soft, short)
                    if not soft and short == legacy:     # only the first tail's placement without wishes explains a failure
                        corner_blocked = corner_blocked or blocked
                        if box is None and faces and blocker is None:
                            free, free_ratio, _ = solve(width, height, need, (), rules, (), legacy)
                            if free is not None:
                                blocker = _nearest_face(free, free_ratio if free_ratio is not None else (ratios[0] if ratios else None), faces)
                    if box is not None:
                        if ratio is not None:
                            corner[i] = ratio
                        placed[i], choice[i], shorts[i] = box, k, short
                        break
                if placed[i] is not None:
                    break
            if placed[i] is not None:
                break
        if placed[i] is None:
            tried = f'{len(sizes)} size(s) tried, from {sizes[0][0]} x {sizes[0][1]} down to {sizes[-1][0]} x {sizes[-1][1]} px' \
                if sizes else 'no sizes to try'
            if governed:
                # Which rule is it? Lift each in turn, for the first option that fits the frame.
                first = next(((k, z) for k, z in enumerate(sizes) if z[0] <= bounds[2] - bounds[0] and z[1] <= bounds[3] - bounds[1]), None)
                culprit = None
                # One rule at a time, then each with the tip rule: a tail across a face ends at it too, so the face rule
                # alone (or the tip rule alone) does not free a position.
                lifts = [(kind,) for kind in rules] + [(kind, 'tip') for kind in rules if kind != 'tip']
                for lifted in (lifts if first is not None else ()):
                    (width, height), need = first[1], (widen[i][first[0]] if widen is not None and widen[i] is not None
                                                        and first[0] < len(widen[i]) else None)
                    free, free_ratio, _ = solve(width, height, need, faces, tuple(r for r in rules if r not in lifted), (), legacy)
                    if free is not None:
                        culprit = breach(free, free_ratio, lifted, legacy)
                        if culprit is not None:
                            break
                if culprit is not None:
                    who = culprit[1]
                    stop = (who, placed[who]) if isinstance(who, int) and 0 <= who < len(placed) and placed[who] is not None else None
                    raise PlacementError(_rule_message(i, culprit, placed, tried), i, stop)
            if blocker is not None:
                raise PlacementError(f'chunk {i}: its box would cover a face ({blocker[1]}): every position that holds its '
                                     f'text and hides its painted region reaches {blocker[1]}; {tried}', i)
            if inside_zones is not None:
                raise PlacementError(f'chunk {i}: its box cannot fit wholly inside one write zone; {tried}', i)
            raise PlacementError(f'chunk {i}: its box cannot be placed ('
                                 + _cause(sizes, covers[i], bounds, neighbours, aimed, tail_margin, corner_blocked,
                                          ratios[1] if ratios else None) + f'; {tried})', i)
    clearance = [_nearest_face(b, corner[i] if rounded is not None and rounded[i] is not None else None, faces)
                 for i, b in enumerate(placed)]
    overlaps = {i: hits for i, b in enumerate(placed)
                for hits in [_keep_hits(b, [(j, z) for j, z in zones
                    if inside is None or inside[i] is None or not any(list(z) == list(h) for h in inside[i])])] if hits}
    return {'visible_rect': bounds, 'boxes': placed, 'painted': painted, 'partial': partial, 'corner': corner,
            'face_clearance': clearance,
            'bleed': [[max(0, bounds[0] - b[0]), max(0, bounds[1] - b[1]), max(0, b[2] - bounds[2]), max(0, b[3] - bounds[3])]
                      for b in placed], 'choice': choice, 'keep_overlaps': overlaps,
            'edge_voice_no_tail': [i for i, room in enumerate(rooms) if room is not None and not _edge_clear(placed[i], bounds, room)],
            'short_tail': shorts}


def detect_reserves(image_path, count, speakers, *, inset=INSET_PX):
    """Geometry for `count` blank outlined reserves found in a frame, in reading order.

    Each rectangle is the largest blank rectangle in its shape, inset by `inset` pixels
    (6 by default; 0 to 8 allowed, for a shape that is a few points short at 6).

    Returns {"visible_rect": [x0, y0, x1, y1], "reserves": [{"kind", "rect", "copy_indices"}]}
    in top-left source pixels. visible_rect is [0, 0, W, H] unless the frame carries white
    letterbox padding, which is excluded from it and from the search. Raises ReserveError
    when fewer than `count` qualify. count 0 returns no reserves.
    """
    speakers = list(speakers)
    if len(speakers) != count:
        raise ValueError(f'{count} reserve(s) need {count} speaker(s), got {len(speakers)}')
    if not isinstance(inset, int) or isinstance(inset, bool) or not 0 <= inset <= MAX_INSET_PX:
        raise ValueError(f'inset must be a whole number of pixels from 0 to {MAX_INSET_PX}: {inset!r}')
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    with Image.open(image_path) as image:
        rgb = np.asarray(image.convert('RGB'))
    bounds = art_bounds(rgb)
    result = {'visible_rect': bounds, 'reserves': []}
    if count == 0:
        return result
    chosen = _shapes(rgb, bounds)
    if len(chosen) < count:
        raise ReserveError(count, len(chosen), chosen)
    chosen = chosen[:count]
    for index, i in enumerate(reading_order([r['rect'] for r in chosen])):
        x0, y0, x1, y1 = chosen[i]['rect']
        rect = [x0 + inset, y0 + inset, x1 - inset, y1 - inset]
        kind = 'caption' if speakers[index].strip().upper().startswith('CAPTION') else 'speech'
        result['reserves'].append({'kind': kind, 'rect': [int(v) for v in rect], 'copy_indices': [index]})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--speakers', default='', help='comma separated speaker labels, one per reserve')
    parser.add_argument('--inset', type=int, default=INSET_PX, help='pixels to inset each rectangle (0 to 8)')
    args = parser.parse_args(argv)
    speakers = [s.strip() for s in args.speakers.split(',') if s.strip()]
    try:
        print(json.dumps(detect_reserves(args.image, len(speakers), speakers, inset=args.inset), indent=2))
    except (ReserveError, ValueError, FileNotFoundError) as error:
        sys.exit(f'reserves: {error}')


if __name__ == '__main__':
    main()
