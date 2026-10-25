"""Preview geometry JSON files on their frames: balloon rects, a line from each rect's nearest edge point to its tail target,
numbered. Usage: geom_preview.py OUT.png FRAME.png GEOM.json [FRAME.png GEOM.json ...]"""
import json, sys
from PIL import Image, ImageDraw, ImageFont
out, pairs = sys.argv[1], list(zip(sys.argv[2::2], sys.argv[3::2]))
COL = [(230, 20, 20), (20, 110, 230), (0, 160, 60), (220, 120, 0)]
tiles = []
for fp, gp in pairs:
    im = Image.open(fp).convert('RGB'); g = json.load(open(gp)); d = ImageDraw.Draw(im)
    v = g['visible_rect']
    n = 0
    for r in g['reserves']:
        x0, y0, x1, y1 = r['rect']
        if r['kind'] == 'speech':
            col = COL[n % 4]; n += 1
            d.rounded_rectangle((x0, y0, x1, y1), 30, fill='white', outline=col, width=6)
            if r.get('tail'):
                tx, ty = r['tail']; bx, by = min(max(tx, x0), x1), min(max(ty, y0), y1)
                d.line((bx, by, tx, ty), fill=col, width=8); d.ellipse((tx - 14, ty - 14, tx + 14, ty + 14), outline=col, width=6)
            d.text((x0 + 20, y0 + 10), str(n), fill=col, font=ImageFont.load_default(size=60))
        else:
            d.rectangle((x0, y0, x1, y1), fill='white', outline='black', width=4)
    im = im.crop(v); im.thumbnail((760, 760)); t = Image.new('RGB', (760, im.height + 26), 'white'); t.paste(im, (0, 26))
    ImageDraw.Draw(t).text((4, 2), gp.split('/')[-1], fill='black', font=ImageFont.load_default(size=18)); tiles.append(t)
W = 2 * 770 + 10; rows = [tiles[i:i + 2] for i in range(0, len(tiles), 2)]
sheet = Image.new('RGB', (W, sum(max(t.height for t in r) for r in rows) + 10 * (len(rows) + 1)), (80, 80, 80)); y = 10
for r in rows:
    for i, t in enumerate(r): sheet.paste(t, (10 + i * 770, y))
    y += max(t.height for t in r) + 10
sheet.save(out)
