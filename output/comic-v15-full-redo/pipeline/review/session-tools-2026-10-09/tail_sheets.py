"""Tail check sheets for one built V15 chapter: every panel with drawn speech, cut from the page render, with each
speech balloon numbered and its tail point ringed, and under it the speaker, the line and the panel's visible cast.
A reviewer reads the sheets to confirm every tail lands on the named speaker (and the speaker is drawn as that person).
Also writes INDEX.json (one entry per balloon) for the review.
Usage (from output/comic-v15-full-redo): tail_sheets.py CH PKG REV BTAG OUT_DIR
  PKG: chapters/<PKG>; REV: render revision (r15); BTAG: the b-pass input tag of that build (d9t-b)"""
import json, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'pipeline')
from script_pipeline import parse_script

ch, pkg, rev, btag, out = int(sys.argv[1]), Path('chapters') / sys.argv[2], sys.argv[3], sys.argv[4], Path(sys.argv[5])
out.mkdir(parents=True, exist_ok=True)
PAGE_H, K = 666.0, 300 / 72
TILE_W, COLS, ROWS = 760, 2, 3
COLOURS = [(230, 20, 20), (20, 110, 230), (0, 160, 60), (220, 120, 0), (170, 0, 200), (0, 170, 170)]
font = lambda n: ImageFont.load_default(size=n)

script = parse_script(Path(f'scripts/CHAPTER-{ch:02d}-SCRIPT.md'))
panels = {p['id']: p for pg in script['pages'] for p in pg['panels']} if isinstance(script.get('pages'), list) else \
         {p['id']: p for pg in script['pages'].values() for p in pg['panels']} if isinstance(script.get('pages'), dict) else \
         {p['id']: p for p in script['panels']}
cast_path = Path(f'scripts/CHAPTER-{ch:02d}-CAST-OVERRIDES.json')
cast = json.loads(cast_path.read_text()) if cast_path.exists() else {}
frames = {f['id']: f for f in json.loads((pkg / f'SELECTION-INPUT-{btag}.json').read_text())['frames']}
places = {p['frame_id']: p for p in json.loads((pkg / f'review/COMPOSITION-{rev}.json').read_text())['placements']}
if set(frames) != set(panels) or set(places) != set(panels):
    sys.exit(f'panel ids differ: script {len(panels)}, input {len(frames)}, composition {len(places)}')


def to_px(pt):                       # page point (y up) -> render pixel
    return pt[0] * K, (PAGE_H - pt[1]) * K


def src_to_px(x, y, fr, pl):
    a, _, _, d, e, f = pl['matrix']
    return to_px((e + a * x / fr['width'], f + d * (1 - y / fr['height'])))


import os
ONLY = set(filter(None, os.environ.get('ONLY', '').split(',')))      # optional: just these panel ids (page-02-panel-03,...)
tiles, index, renders = [], [], {}
for pid in sorted(panels):
    if ONLY and pid not in ONLY: continue
    fr, pl, copy = frames[pid], places[pid], panels[pid]['copy']
    speech = [r for r in fr['reserves'] if r.get('kind') == 'speech' or r.get('draw') == 'speech']
    if not speech: continue
    page = pl['page']
    if page not in renders: renders[page] = Image.open(pkg / f'renders/{rev}/page-{page:02d}.png').convert('RGB')
    x, y, w, h = pl['clip_xywh_pt']
    X0, Y0 = to_px((x, y + h)); X1, Y1 = to_px((x + w, y))
    crop = renders[page].crop((int(X0) - 6, int(Y0) - 6, int(X1) + 6, int(Y1) + 6)).copy()
    s = TILE_W / crop.width
    crop = crop.resize((TILE_W, max(1, round(crop.height * s))), Image.LANCZOS)
    dr = ImageDraw.Draw(crop)
    lines = []
    for n, r in enumerate(speech, 1):
        col = COLOURS[(n - 1) % len(COLOURS)]
        speakers = [copy[i]['speaker'] for i in r['copy_indices']]
        texts = [copy[i]['text'] for i in r['copy_indices']]
        bx, by = src_to_px(r['rect'][0], r['rect'][1], fr, pl)
        bx, by = (bx - X0 + 6) * s, (by - Y0 + 6) * s
        bx, by = max(0, bx - 38), max(0, by - 4)          # badge just left of the balloon, clear of its first letters
        dr.rounded_rectangle((bx, by, bx + 34, by + 30), 6, fill=col, outline='white', width=2)
        dr.text((bx + 9, by + 2), str(n), fill='white', font=font(24))
        tail = r.get('tail')
        where = 'no tail (tailless box)'
        if tail:
            tx, ty = src_to_px(tail[0], tail[1], fr, pl); tx, ty = (tx - X0 + 6) * s, (ty - Y0 + 6) * s
            dr.ellipse((tx - 11, ty - 11, tx + 11, ty + 11), outline=col, width=4)
            dr.text((tx + 13, ty - 12), str(n), fill=col, font=font(22), stroke_width=2, stroke_fill='white')
            edge = tail[0] <= 1 or tail[1] <= 1 or tail[0] >= fr['width'] - 1 or tail[1] >= fr['height'] - 1
            where = 'tail to the panel edge (off-panel speaker)' if edge else 'tail ringed'
        line = f"{n}. {' / '.join(speakers)}: {' '.join(texts)}"
        lines.append((col, line[:110] + ('...' if len(line) > 110 else '')))
        index.append({'panel': pid, 'balloon': n, 'speakers': speakers, 'text': ' '.join(texts), 'tail': where,
                      'cast': cast.get(pid)})
    head = f"{pid.replace('page-', 'p').replace('-panel-', '.')}  (book page {page})   cast: {', '.join(cast.get(pid) or ['(none listed)'])}"
    pad = 30 + 26 * len(lines) + 8
    tile = Image.new('RGB', (TILE_W, crop.height + pad), 'white')
    tile.paste(crop, (0, pad))
    td = ImageDraw.Draw(tile)
    td.text((6, 4), head, fill='black', font=font(20))
    for k, (col, line) in enumerate(lines):
        td.text((6, 30 + 26 * k), line, fill=col, font=font(19))
    tiles.append((pid, tile))

sheets = []
for i in range(0, len(tiles), COLS * ROWS):
    group = tiles[i:i + COLS * ROWS]
    rows = [group[j:j + COLS] for j in range(0, len(group), COLS)]
    heights = [max(t.height for _, t in r) for r in rows]
    sheet = Image.new('RGB', (COLS * TILE_W + (COLS + 1) * 12, sum(heights) + (len(rows) + 1) * 12), (90, 90, 90))
    yy = 12
    for r, hgt in zip(rows, heights):
        for c, (_, t) in enumerate(r): sheet.paste(t, (12 + c * (TILE_W + 12), yy))
        yy += hgt + 12
    name = out / f'ch{ch:02d}-tails-{len(sheets) + 1:02d}.png'
    sheet.save(name); sheets.append({'sheet': str(name.resolve()), 'panels': [p for p, _ in group]})
(out / f'ch{ch:02d}-INDEX.json').write_text(json.dumps({'chapter': ch, 'package': str(pkg), 'rev': rev, 'sheets': sheets,
                                                       'balloons': index}, indent=1))
print(f'ch{ch}: {len(tiles)} panels, {len(index)} balloons, {len(sheets)} sheets')
