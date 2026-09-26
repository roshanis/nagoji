#!/usr/bin/env python3
"""Generate the Chapter 1 map (Malabar Coast, c. 1738) as an antique-style SVG.

Usage:
    python3 images/map_source/make_map.py            # writes images/map_source/map_malabar.svg
    node images/map_source/render_map.js             # renders images/map_malabar.png and .jpg

Fonts: IM Fell English (SIL Open Font License), fetched from Google Fonts into
images/map_source/fonts/ and embedded in the SVG as base64.
"""

import base64
import math
import os
import random
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT_SVG = os.path.join(HERE, "map_malabar.svg")

FONTS = {
    "Fell": ("fell.woff2", "normal",
             "https://fonts.gstatic.com/s/imfellenglish/v14/Ktk1ALSLW8zDe0rthJysWrnLsAzHEKOY.woff2"),
    "FellItalic": ("fell_it.woff2", "italic",
                   "https://fonts.gstatic.com/s/imfellenglish/v14/Ktk3ALSLW8zDe0rthJysWrnLsAzHFZOafYs.woff2"),
    "FellSC": ("fell_sc.woff2", "normal",
               "https://fonts.gstatic.com/s/imfellenglishsc/v16/a8IENpD3CDX-4zrWfr1VY879qFF05pZ7PIIP.woff2"),
}

# ---------------------------------------------------------------- canvas
W, H = 1500, 2000
X0, Y0, X1, Y1 = 90, 90, 1410, 1910          # neatline (map area)
LAT_TOP = 20.6
KY = 140.0                                   # px per degree latitude
KX = KY * math.cos(math.radians(14))         # px per degree longitude
LON_LEFT = 71.0

INK = "#3a2716"
PAPER = "#efe0bc"
LAND = "#e3cc98"

# ---------------------------------------------------------------- geography (lat, lon)
COAST = [
    (21.6, 72.6), (20.9, 72.9), (20.4, 72.83), (20.0, 72.73), (19.6, 72.73),
    (19.35, 72.78), (19.2, 72.8), (18.95, 72.82), (18.8, 72.92), (18.64, 72.87),
    (18.3, 72.95), (18.0, 73.02), (17.7, 73.1), (17.3, 73.2), (17.0, 73.27),
    (16.6, 73.33), (16.3, 73.4), (16.05, 73.47), (15.8, 73.63), (15.5, 73.8),
    (15.3, 73.9), (15.0, 74.02), (14.8, 74.12), (14.5, 74.35), (14.2, 74.45),
    (13.95, 74.55), (13.6, 74.68), (13.34, 74.7), (12.9, 74.82), (12.5, 74.98),
    (12.1, 75.17), (11.87, 75.35), (11.6, 75.58), (11.25, 75.77), (10.9, 75.88),
    (10.55, 76.02), (10.2, 76.18), (9.97, 76.24), (9.7, 76.3), (9.49, 76.32),
    (9.25, 76.42), (9.1, 76.47), (8.95, 76.54), (8.88, 76.57), (8.75, 76.68),
    (8.64, 76.77), (8.5, 76.9), (8.38, 76.98), (8.28, 77.1), (8.2, 77.2),
    (8.17, 77.27), (8.12, 77.36), (8.09, 77.46), (8.07, 77.55), (8.12, 77.65),
    (8.2, 77.78), (8.35, 77.98), (8.5, 78.12), (8.78, 78.15), (9.0, 78.3),
    (9.12, 78.5), (9.2, 78.85), (9.26, 79.1), (9.28, 79.3), (9.36, 79.08),
    (9.5, 78.95), (9.8, 79.1), (10.1, 79.25), (10.28, 79.4), (10.3, 79.85),
    (10.6, 79.85), (10.8, 79.85), (11.1, 79.85), (11.5, 79.77), (11.93, 79.83),
    (12.2, 79.98), (12.6, 80.2), (13.08, 80.29), (13.5, 80.3), (14.0, 80.15),
    (14.5, 80.12), (15.0, 80.05), (15.5, 80.2), (15.8, 80.7), (15.9, 81.2),
    (16.3, 81.7), (17.0, 82.3), (21.6, 83.5),
]

CEYLON = [
    (9.55, 79.9), (9.7, 79.95), (9.8, 80.1), (9.83, 80.25), (9.6, 80.55),
    (9.2, 80.8), (8.7, 81.15), (8.5, 81.25), (7.9, 81.6), (7.3, 81.85),
    (6.5, 81.7), (6.0, 80.8), (6.1, 80.1), (7.0, 79.85), (7.6, 79.8),
    (8.1, 79.75), (8.6, 79.95), (8.9, 79.92), (9.1, 79.8), (9.3, 79.9),
]

ADAMS_BRIDGE = [(9.26, 79.35), (9.2, 79.5), (9.13, 79.65), (9.08, 79.8)]

GHATS = [
    [(20.6, 73.6), (20.0, 73.62), (19.5, 73.6), (19.0, 73.62), (18.5, 73.55),
     (18.0, 73.65), (17.5, 73.75), (17.0, 73.8), (16.5, 73.95), (16.0, 74.05),
     (15.5, 74.25), (15.0, 74.45), (14.5, 74.8), (14.0, 75.05), (13.5, 75.25),
     (13.0, 75.5), (12.5, 75.7), (12.0, 75.9), (11.6, 76.3), (11.4, 76.7)],
    [(10.55, 76.8), (10.3, 77.05), (10.05, 77.15), (9.8, 77.2), (9.55, 77.22),
     (9.3, 77.2), (9.0, 77.18), (8.75, 77.22), (8.55, 77.3), (8.4, 77.45)],
]

RIVERS = [
    # Godavari, rising near Nashik
    [(19.93, 73.53), (20.0, 73.79), (19.8, 74.4), (19.6, 75.0), (19.3, 76.0),
     (19.1, 77.0), (18.9, 78.0), (18.8, 79.0), (18.3, 80.3), (17.8, 81.2)],
    # Krishna
    [(17.95, 73.66), (17.3, 74.2), (16.85, 74.57), (16.5, 75.3), (16.25, 76.1),
     (16.2, 77.0), (16.1, 77.6), (15.9, 78.2), (16.1, 78.8), (16.5, 79.5),
     (16.5, 80.6), (15.9, 81.1)],
    # Kaveri
    [(12.4, 75.6), (12.42, 76.7), (12.25, 77.3), (12.12, 77.77), (11.8, 77.8),
     (11.35, 77.75), (11.1, 78.1), (10.9, 78.5), (10.85, 78.7), (10.95, 79.2),
     (11.14, 79.85)],
    # Vaigai, through Madurai
    [(10.05, 77.35), (10.0, 77.7), (9.93, 78.12), (9.7, 78.5), (9.4, 78.9)],
]


# ---------------------------------------------------------------- helpers
def proj_main(lat, lon):
    return X0 + (lon - LON_LEFT) * KX, Y0 + (LAT_TOP - lat) * KY


def make_proj(x0, y0, lat_top, lon_left, ky):
    kx = ky * math.cos(math.radians(8.6))
    return lambda lat, lon: (x0 + (lon - lon_left) * kx, y0 + (lat_top - lat) * ky)


def roughen(pts, step=0.08, amp=0.012, seed=7):
    """Subdivide a lat/lon line and add small deterministic wobble, in degrees."""
    rnd = random.Random(seed)
    out = []
    for (a, b), (c, d) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(c - a, d - b) / step))
        for i in range(n):
            t = i / n
            la, lo = a + (c - a) * t, b + (d - b) * t
            if i:
                la += rnd.uniform(-amp, amp)
                lo += rnd.uniform(-amp, amp)
            out.append((la, lo))
    out.append(pts[-1])
    return out


def smooth_path(xy, closed=False):
    """Catmull-Rom spline through points, as SVG cubic Beziers."""
    if closed:
        p = [xy[-1]] + xy + [xy[0], xy[1]]
    else:
        p = [xy[0]] + xy + [xy[-1]]
    d = [f"M{p[1][0]:.1f},{p[1][1]:.1f}"]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    if closed:
        d.append("Z")
    return " ".join(d)


def land_path(proj):
    pts = [proj(*ll) for ll in roughen(COAST, seed=3)]
    return smooth_path(pts, closed=True)


def ceylon_path(proj):
    pts = [proj(*ll) for ll in roughen(CEYLON + [CEYLON[0]], seed=5)]
    return smooth_path(pts[:-1], closed=True)


def esc(s):
    return s.replace("&", "&amp;")


def text(x, y, s, size, family="Fell", anchor="start", spacing=0, rotate=0,
         opacity=1.0, weight=None, fill=INK):
    tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}"{ls}{op}{tr}>{esc(s)}</text>')


def halo_text(*args, **kw):
    """Label with a soft parchment halo so it reads over hatching and rivers."""
    t = text(*args, **kw)
    halo = t.replace("<text ", f'<text stroke="{PAPER}" stroke-width="5" stroke-linejoin="round" opacity="0.85" ', 1)
    return halo + t


def town(x, y, r=5):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 0.36:.1f}" fill="{INK}"/>')


def fort(x, y, s=1.0):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s})" fill="{PAPER}" stroke="{INK}" stroke-width="1.3">'
            '<path d="M-6,5 L-6,-3 L-4.5,-3 L-4.5,-6 L-2,-6 L-2,-3 L2,-3 L2,-6 L4.5,-6 L4.5,-3 L6,-3 L6,5 Z"/>'
            '<path d="M-1.6,5 L-1.6,1.2 Q0,-0.8 1.6,1.2 L1.6,5" fill="none"/></g>')


def swords(x, y, s=1.0):
    blade = ('<path d="M-11,-11 L9,9" stroke-width="1.7"/>'
             '<path d="M5,11 L11,5" stroke-width="1.7"/>')
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s})" stroke="{INK}" fill="none" stroke-linecap="round">'
            f'{blade}<g transform="scale(-1 1)">{blade}</g></g>')


def peaks(proj, ridge, spacing, size, seed):
    """Hachured mountain glyphs along a ridge line, two loose rows."""
    rnd = random.Random(seed)
    xy = [proj(*ll) for ll in ridge]
    out = []
    carry = 0.0
    for (ax, ay), (bx, by) in zip(xy, xy[1:]):
        seg = math.hypot(bx - ax, by - ay)
        t = carry
        while t < seg:
            f = t / seg
            px, py = ax + (bx - ax) * f, ay + (by - ay) * f
            for row in (0, 1):
                sz = size * rnd.uniform(0.75, 1.15) * (0.8 if row else 1)
                ox = rnd.uniform(-2, 2) + (size * 0.9 if row else 0)
                oy = rnd.uniform(-2, 2) + (size * 0.35 if row else 0)
                out.append(peak(px + ox, py + oy, sz))
            t += spacing * rnd.uniform(0.85, 1.15)
        carry = t - seg
    return "".join(out)


def peak(x, y, s):
    h, w = s, s * 0.9
    lines = [f'<path d="M{x - w:.1f},{y + h * 0.35:.1f} L{x:.1f},{y - h * 0.65:.1f} L{x + w:.1f},{y + h * 0.35:.1f}" '
             f'fill="{LAND}" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"/>']
    for k in range(1, 4):
        f = k / 4
        sx = x + w * f * 0.55
        sy = y - h * 0.65 + (h * f)
        lines.append(f'<path d="M{sx:.1f},{sy:.1f} L{sx + w * 0.28:.1f},{y + h * 0.3:.1f}" '
                     f'stroke="{INK}" stroke-width="0.7" opacity="0.8"/>')
    return "".join(lines)


def rivers(proj, width):
    out = []
    for i, r in enumerate(RIVERS):
        pts = [proj(*ll) for ll in roughen(r, step=0.15, amp=0.03, seed=20 + i)]
        out.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{INK}" stroke-width="{width}" '
                   f'opacity="0.55" stroke-linecap="round"/>')
    return "".join(out)


def waterlines(mask_id, paths, rings):
    """Concentric shore lines: rings of stroke drawn through a mask outside the land."""
    m = [f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
         f'<rect width="{W}" height="{H}" fill="black"/>']
    for k, w in reversed(list(enumerate(rings))):
        shade = int(255 * (1 - k / (len(rings) + 1.5)))
        for d in paths:
            m.append(f'<path d="{d}" fill="none" stroke="rgb({shade},{shade},{shade})" stroke-width="{w + 1.5}"/>')
        for d in paths:
            m.append(f'<path d="{d}" fill="none" stroke="black" stroke-width="{w}"/>')
    for d in paths:
        m.append(f'<path d="{d}" fill="black"/>')
    m.append("</mask>")
    return "".join(m)


def tint_band(paths, clip_id, width):
    """Hand-colouring along the inside of the coast, as on engraved maps."""
    clip = "".join(f'<path d="{d}"/>' for d in paths)
    band = "".join(f'<path d="{d}" fill="none" stroke="#a9773a" stroke-width="{width}" filter="url(#blur3)"/>' for d in paths)
    return f'<clipPath id="{clip_id}">{clip}</clipPath><g clip-path="url(#{clip_id})" opacity="0.32">{band}</g>'


def compass(cx, cy, r):
    out = [f'<g transform="translate({cx} {cy})">',
           f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="1.2"/>',
           f'<circle r="{r - 6}" fill="none" stroke="{INK}" stroke-width="0.6"/>',
           f'<circle r="{r * 0.34:.1f}" fill="none" stroke="{INK}" stroke-width="0.8"/>']
    for i in range(32):
        a = math.radians(i * 11.25)
        r0 = r - 6
        r1 = r - (14 if i % 2 else 20)
        out.append(f'<line x1="{r0 * math.sin(a):.1f}" y1="{-r0 * math.cos(a):.1f}" '
                   f'x2="{r1 * math.sin(a):.1f}" y2="{-r1 * math.cos(a):.1f}" stroke="{INK}" stroke-width="0.6"/>')
    for i in range(16):
        a = math.radians(i * 22.5)
        length = r * (0.95 if i % 4 == 0 else 0.7 if i % 2 == 0 else 0.48)
        half = math.radians(9 if i % 4 == 0 else 8 if i % 2 == 0 else 7)
        base = r * 0.12
        tip = (length * math.sin(a), -length * math.cos(a))
        lft = (base * math.sin(a - half * 4), -base * math.cos(a - half * 4))
        rgt = (base * math.sin(a + half * 4), -base * math.cos(a + half * 4))
        z = (0, 0)
        order = 0 if i % 4 == 0 else 1 if i % 2 == 0 else 2
        out.append(f'<path d="M{z[0]},{z[1]} L{lft[0]:.1f},{lft[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} Z" '
                   f'fill="{INK}" stroke="{INK}" stroke-width="0.6" opacity="{1 if order < 2 else 0.85}"/>')
        out.append(f'<path d="M{z[0]},{z[1]} L{rgt[0]:.1f},{rgt[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} Z" '
                   f'fill="{PAPER}" stroke="{INK}" stroke-width="0.6"/>')
    out.append(f'<circle r="4" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    # fleur-de-lis style north marker
    out.append(f'<g transform="translate(0 {-r - 16})" fill="{INK}">'
               '<path d="M0,-18 C5,-10 5,-4 0,2 C-5,-4 -5,-10 0,-18 Z"/>'
               '<path d="M-2,0 C-10,-2 -14,-10 -9,-14 C-8,-8 -5,-5 -1,-3 Z"/>'
               '<path d="M2,0 C10,-2 14,-10 9,-14 C8,-8 5,-5 1,-3 Z"/>'
               '<rect x="-7" y="1" width="14" height="2.4"/></g>')
    out.append("</g>")
    return "".join(out)


def ship(x, y, s=1.0, flip=False):
    fx = -1 if flip else 1
    return (f'<g transform="translate({x} {y}) scale({s * fx} {s})" stroke="{INK}" stroke-linejoin="round">'
            f'<path d="M-44,-2 Q-38,14 -20,16 L26,16 Q40,12 48,-4 L30,0 L-30,0 Z" fill="{LAND}" stroke-width="1.3"/>'
            '<path d="M-36,6 L40,6" stroke-width="0.6" fill="none"/>'
            '<path d="M-24,0 L-24,-44 M4,0 L4,-60 M28,0 L28,-38 M48,-4 L66,-16" stroke-width="1.3" fill="none"/>'
            f'<path d="M-35,-40 Q-24,-34 -13,-40 L-12,-20 Q-24,-14 -36,-20 Z" fill="{PAPER}" stroke-width="1"/>'
            f'<path d="M-9,-56 Q4,-50 17,-56 L18,-32 Q4,-26 -10,-32 Z" fill="{PAPER}" stroke-width="1"/>'
            f'<path d="M-11,-28 Q4,-21 19,-28 L20,-6 Q4,0 -12,-6 Z" fill="{PAPER}" stroke-width="1"/>'
            f'<path d="M19,-34 Q28,-30 37,-34 L38,-14 Q28,-10 18,-14 Z" fill="{PAPER}" stroke-width="1"/>'
            f'<path d="M4,-60 L18,-65 L4,-68 Z" fill="{INK}" stroke-width="0.6"/>'
            '<path d="M-60,22 Q-50,18 -40,22 T-20,22 M20,22 Q30,18 40,22 T60,22" fill="none" stroke-width="0.7"/>'
            '</g>')


def neatline():
    out = [f'<rect x="{X0 - 30}" y="{Y0 - 30}" width="{X1 - X0 + 60}" height="{Y1 - Y0 + 60}" fill="none" stroke="{INK}" stroke-width="2.4"/>',
           f'<rect x="{X0 - 22}" y="{Y0 - 22}" width="{X1 - X0 + 44}" height="{Y1 - Y0 + 44}" fill="none" stroke="{INK}" stroke-width="0.8"/>',
           f'<rect x="{X0 - 12}" y="{Y0 - 12}" width="{X1 - X0 + 24}" height="{Y1 - Y0 + 24}" fill="none" stroke="{INK}" stroke-width="0.8"/>',
           f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" fill="none" stroke="{INK}" stroke-width="1.4"/>']
    # alternating degree bars between the inner lines
    lon = math.floor(LON_LEFT)
    k = 0
    while True:
        xa, _ = proj_main(0, lon)
        xb, _ = proj_main(0, lon + 0.5)
        if xa >= X1:
            break
        xa, xb = max(xa, X0), min(xb, X1)
        if k % 2 == 0 and xb > xa:
            for yy in (Y0 - 12, Y1):
                out.append(f'<rect x="{xa:.1f}" y="{yy}" width="{xb - xa:.1f}" height="12" fill="{INK}" opacity="0.85"/>')
        lon += 0.5
        k += 1
    lat = math.ceil(LAT_TOP * 2) / 2
    k = 0
    while True:
        _, ya = proj_main(lat, 0)
        _, yb = proj_main(lat - 0.5, 0)
        if ya >= Y1:
            break
        ya, yb = max(ya, Y0), min(yb, Y1)
        if k % 2 == 0 and yb > ya:
            for xx in (X0 - 12, X1):
                out.append(f'<rect x="{xx}" y="{ya:.1f}" width="12" height="{yb - ya:.1f}" fill="{INK}" opacity="0.85"/>')
        lat -= 0.5
        k += 1
    for lon in range(72, 81, 2):
        x, _ = proj_main(0, lon)
        out.append(text(x, Y0 - 42, f"{lon}°", 20, "Fell", "middle"))
        out.append(text(x, Y1 + 56, f"{lon}°", 20, "Fell", "middle"))
    for lat in range(8, 21, 2):
        _, y = proj_main(lat, 0)
        out.append(text(X0 - 48, y + 7, f"{lat}°", 20, "Fell", "middle", rotate=-90))
        out.append(text(X1 + 48, y + 7, f"{lat}°", 20, "Fell", "middle", rotate=90))
    return "".join(out)


def graticule(proj, lat_range, lon_range, opacity=0.22):
    out = []
    for lon in lon_range:
        xa, ya = proj(30, lon)
        xb, yb = proj(0, lon)
        out.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{INK}" stroke-width="0.6" opacity="{opacity}"/>')
    for lat in lat_range:
        xa, ya = proj(lat, 60)
        xb, yb = proj(lat, 90)
        out.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{INK}" stroke-width="0.6" opacity="{opacity}"/>')
    return "".join(out)


def rhumb_lines(cx, cy):
    out = []
    for i in range(16):
        a = math.radians(i * 22.5)
        x2, y2 = cx + 2400 * math.sin(a), cy - 2400 * math.cos(a)
        dash = "" if i % 2 == 0 else ' stroke-dasharray="6 6"'
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="0.5" opacity="0.28"{dash}/>')
    return "".join(out)


def font_face():
    os.makedirs(FONT_DIR, exist_ok=True)
    css = []
    for fam, (fname, style, url) in FONTS.items():
        path = os.path.join(FONT_DIR, fname)
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
        with open(path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        css.append(f"@font-face{{font-family:'{fam}';font-style:{style};"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "".join(css)


# ---------------------------------------------------------------- build
def build():
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    s.append(f"<defs><style>{font_face()}</style>")
    s.append('<radialGradient id="paper" cx="50%" cy="45%" r="75%">'
             '<stop offset="0" stop-color="#f3e6c6"/><stop offset="0.7" stop-color="#e9d6ad"/>'
             '<stop offset="1" stop-color="#cfb27c"/></radialGradient>')
    s.append('<filter id="grain" x="0" y="0" width="100%" height="100%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4"/>'
             '<feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.24  0 0 0 0 0.1  0 0 0 0.22 0"/></filter>')
    s.append('<filter id="mottle" x="0" y="0" width="100%" height="100%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.006" numOctaves="4" seed="11"/>'
             '<feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.3  0 0 0 0 0.12  0 0 0 0.55 -0.18"/></filter>')
    s.append('<filter id="blur3"><feGaussianBlur stdDeviation="3"/></filter>')
    s.append('<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>')
    s.append(f'<clipPath id="mapclip"><rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}"/></clipPath>')

    # inset geometry
    IX0, IY0, IX1, IY1 = 110, 1440, 700, 1890
    ITITLE = 50
    iproj = make_proj(IX0, IY0 + ITITLE, 9.3, 76.2, (IY1 - IY0 - ITITLE) / 1.35)
    s.append(f'<clipPath id="insetclip"><rect x="{IX0}" y="{IY0 + ITITLE}" width="{IX1 - IX0}" height="{IY1 - IY0 - ITITLE}"/></clipPath>')

    main_land, main_ceylon = land_path(proj_main), ceylon_path(proj_main)
    in_land, in_ceylon = land_path(iproj), ceylon_path(iproj)
    s.append(waterlines("wl_main", [main_land, main_ceylon], [7, 15, 24, 34, 46]))
    s.append(waterlines("wl_inset", [in_land], [8, 18, 30, 44]))
    s.append("</defs>")

    # paper
    s.append(f'<rect width="{W}" height="{H}" fill="url(#paper)"/>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#mottle)"/>')
    rnd = random.Random(42)
    for _ in range(14):
        cx, cy = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.uniform(20, 70)
        s.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#9a6b32" opacity="{rnd.uniform(0.04, 0.09):.2f}" filter="url(#blur8)"/>')
        s.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * 0.92:.0f}" fill="none" stroke="#8a5a26" stroke-width="2" opacity="{rnd.uniform(0.05, 0.1):.2f}" filter="url(#blur8)"/>')

    # ---- main map
    s.append('<g clip-path="url(#mapclip)">')
    rose = (250, 1010)
    s.append(rhumb_lines(*rose))
    s.append(graticule(proj_main, range(8, 22, 2), range(72, 82, 2)))
    s.append(f'<rect width="{W}" height="{H}" fill="{INK}" mask="url(#wl_main)" opacity="0.7"/>')
    s.append(f'<path d="{main_land}" fill="{LAND}" opacity="0.9"/>')
    s.append(f'<path d="{main_ceylon}" fill="{LAND}" opacity="0.9"/>')
    s.append(tint_band([main_land, main_ceylon], "tint_main", 16))
    s.append(graticule(proj_main, range(8, 22, 2), range(72, 82, 2), 0.14))
    s.append(rivers(proj_main, 1.3))
    for i, ridge in enumerate(GHATS):
        s.append(peaks(proj_main, ridge, 17, 11, 100 + i))
    s.append(f'<path d="{main_land}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<path d="{main_ceylon}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    for la, lo in roughen(ADAMS_BRIDGE, step=0.03, amp=0.01, seed=9):
        x, y = proj_main(la, lo)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.3" fill="{INK}" opacity="0.7"/>')

    # regions and seas
    s.append(text(905, 790, "DECCAN", 44, "FellSC", "middle", spacing=12, opacity=0.72))
    s.append(text(1080, 1075, "CARNATIC", 34, "FellSC", "middle", spacing=9, opacity=0.72))
    s.append(text(418, 560, "KONKAN", 26, "FellSC", "middle", spacing=9, rotate=79, opacity=0.72))
    s.append(text(340, 1185, "THE ARABIAN", 34, "FellItalic", "middle", spacing=7, opacity=0.8))
    s.append(text(340, 1232, "SEA", 34, "FellItalic", "middle", spacing=7, opacity=0.8))
    s.append(text(1386, 960, "BAY OF BENGAL", 22, "FellItalic", "middle", spacing=3, rotate=90, opacity=0.8))
    s.append(text(1350, 1870, "CEYLON", 22, "FellSC", "middle", spacing=3, opacity=0.8))

    # inset extent on main map
    bx0, by0 = proj_main(9.3, 76.2)
    bx1, by1 = proj_main(7.95, 78.22)
    s.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}" fill="none" '
             f'stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4" opacity="0.8"/>')
    s.append(halo_text(bx0, by0 - 12, "TRAVANCORE", 24, "FellSC", "start", spacing=3))

    # places
    P = []
    def place(lat, lon, label, dx, dy, anchor="start", size=26, kind="town", family="Fell"):
        x, y = proj_main(lat, lon)
        P.append(fort(x, y, 1.3) if kind == "fort" else town(x, y))
        P.append(halo_text(x + dx, y + dy, label, size, family, anchor))
    place(20.0, 73.79, "Nashik", 12, 8)
    place(18.52, 73.86, "Pune", 12, 8)
    place(19.35, 72.8, "Vasai", -14, 8, "end", kind="fort")
    place(15.49, 73.83, "Goa", -16, 10, "end", size=34, kind="fort")
    place(12.9, 79.33, "Arcot", -12, 8, "end")
    place(9.93, 78.12, "Madurai", 12, 8)
    cx, cy = proj_main(8.17, 77.27)
    P.append(swords(cx - 2, cy + 14, 0.7))
    s.extend(P)
    s.append("</g>")

    # compass and ships sit above the waterlines
    s.append(compass(*rose, 88))
    s.append(ship(300, 690, 0.95))
    s.append(ship(560, 1360, 0.8, flip=True))

    # ---- title cartouche
    tx0, ty0, tx1, ty1 = 860, 125, 1380, 420
    s.append(f'<rect x="{tx0}" y="{ty0}" width="{tx1 - tx0}" height="{ty1 - ty0}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="{tx0 + 9}" y="{ty0 + 9}" width="{tx1 - tx0 - 18}" height="{ty1 - ty0 - 18}" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    for (cx, cy, sx, sy) in [(tx0, ty0, 1, 1), (tx1, ty0, -1, 1), (tx0, ty1, 1, -1), (tx1, ty1, -1, -1)]:
        s.append(f'<g transform="translate({cx} {cy}) scale({sx} {sy})" fill="none" stroke="{INK}" stroke-width="1.1">'
                 '<path d="M9,34 C9,18 18,9 34,9"/><path d="M16,40 C18,24 24,18 40,16"/>'
                 f'<circle cx="22" cy="22" r="3.2" fill="{INK}"/></g>')
    mx = (tx0 + tx1) / 2
    s.append(text(mx, ty0 + 62, "A MAP OF THE", 28, "FellSC", "middle", spacing=6))
    s.append(text(mx, ty0 + 128, "MALABAR COAST", 50, "FellSC", "middle", spacing=3))
    s.append(f'<path d="M{mx - 150},{ty0 + 150} Q{mx},{ty0 + 136} {mx + 150},{ty0 + 150}" fill="none" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<path d="M{mx - 6},{ty0 + 143} L{mx},{ty0 + 137} L{mx + 6},{ty0 + 143} L{mx},{ty0 + 149} Z" fill="{INK}"/>')
    s.append(text(mx, ty0 + 188, "with the Konkan, the Deccan, the Carnatic", 23, "FellItalic", "middle"))
    s.append(text(mx, ty0 + 218, "and the Kingdom of Travancore", 23, "FellItalic", "middle"))
    s.append(text(mx, ty0 + 262, "MDCCXXXVIII", 24, "FellSC", "middle", spacing=5))

    # scale of miles
    sx0, sy0 = 930, 470
    mile_px = KY / 69.0
    length = 100 * mile_px
    s.append(text(sx0 + length / 2, sy0 - 14, "A Scale of English Miles", 20, "FellItalic", "middle"))
    for i in range(4):
        x = sx0 + i * length / 4
        fill = INK if i % 2 == 0 else PAPER
        s.append(f'<rect x="{x:.1f}" y="{sy0}" width="{length / 4:.1f}" height="7" fill="{fill}" stroke="{INK}" stroke-width="0.9"/>')
    for i, v in enumerate([0, 25, 50, 75, 100]):
        s.append(text(sx0 + i * length / 4, sy0 + 28, str(v), 17, "Fell", "middle"))

    # ---- inset: Travancore
    s.append(f'<rect x="{IX0 - 8}" y="{IY0 - 8}" width="{IX1 - IX0 + 16}" height="{IY1 - IY0 + 16}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="{IX0}" y="{IY0}" width="{IX1 - IX0}" height="{IY1 - IY0}" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>')
    s.append(text((IX0 + IX1) / 2, IY0 + 34, "THE KINGDOM OF TRAVANCORE", 25, "FellSC", "middle", spacing=3))
    s.append(f'<line x1="{IX0}" y1="{IY0 + ITITLE}" x2="{IX1}" y2="{IY0 + ITITLE}" stroke="{INK}" stroke-width="0.9"/>')
    s.append('<g clip-path="url(#insetclip)">')
    s.append(graticule(iproj, [8.5, 9.0], [76.5, 77.0, 77.5]))
    s.append(f'<rect width="{W}" height="{H}" fill="{INK}" mask="url(#wl_inset)" opacity="0.7"/>')
    s.append(f'<path d="{in_land}" fill="{LAND}" opacity="0.9"/>')
    s.append(tint_band([in_land], "tint_inset", 22))
    s.append(rivers(iproj, 1.6))
    s.append(peaks(iproj, GHATS[1][4:], 24, 15, 300))
    s.append(f'<path d="{in_land}" fill="none" stroke="{INK}" stroke-width="2"/>')

    def iplace(lat, lon, label, dx, dy, anchor="start", size=23, kind="town", family="Fell"):
        x, y = iproj(lat, lon)
        out = fort(x, y, 1.4) if kind == "fort" else town(x, y, 5.5)
        return out + halo_text(x + dx, y + dy, label, size, family, anchor)
    s.append(iplace(9.17, 76.52, "Kayamkulam", 12, 8))
    s.append(iplace(9.03, 76.56, "Velinadu", 12, 8, family="FellItalic"))
    s.append(iplace(8.88, 76.60, "Kollam", -12, 8, "end"))
    s.append(iplace(8.70, 76.82, "Attingal", 12, 8))
    s.append(iplace(8.50, 76.95, "Thiruvananthapuram", -12, 8, "end", size=21))
    s.append(iplace(8.25, 77.34, "Padmanabhapuram", 12, 12))
    s.append(iplace(8.29, 77.28, "Udayagiri Fort", -14, -6, "end", kind="fort"))
    x, y = iproj(8.17, 77.27)
    s.append(swords(x - 30, y + 4))
    s.append(halo_text(x - 48, y + 12, "Colachel", 24, "Fell", "end"))
    s.append(halo_text(x - 48, y + 36, "1741", 19, "FellItalic", "end"))
    s.append(iplace(8.08, 77.55, "Kanyakumari", 0, 32, "middle"))
    s.append(halo_text(IX1 - 14, IY0 + ITITLE + 34, "to Madurai", 20, "FellItalic", "end"))
    x, y = IX1 - 40, IY0 + ITITLE + 48
    s.append(f'<path d="M{x - 20},{y} L{x + 20},{y} M{x + 12},{y - 5} L{x + 20},{y} L{x + 12},{y + 5}" stroke="{INK}" stroke-width="1.1" fill="none"/>')
    s.append(text(IX0 + 75, IY1 - 34, "Arabian Sea", 22, "FellItalic", "middle", opacity=0.8))
    s.append("</g>")

    s.append(neatline())

    # fold creases and fine grain over everything
    s.append(f'<line x1="{W / 2}" y1="0" x2="{W / 2}" y2="{H}" stroke="#7a5a30" stroke-width="3" opacity="0.08"/>')
    s.append(f'<line x1="0" y1="{H / 2}" x2="{W}" y2="{H / 2}" stroke="#7a5a30" stroke-width="3" opacity="0.08"/>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')
    s.append("</svg>")

    with open(OUT_SVG, "w") as fh:
        fh.write("".join(s))
    print(f"wrote {OUT_SVG}")


if __name__ == "__main__":
    build()
