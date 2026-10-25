"""Kindle cover (1600 x 2560) from a V15 frame, with title type. Usage: frame mode out [cx]
mode 'crop': portrait crop of a wide frame centred on cx (fraction of width).
mode 'band': the whole frame across the middle, fading into dark above and below."""
import sys
from PIL import Image, ImageDraw, ImageFont

FONTS = sys.argv[5] if len(sys.argv) > 5 else '.'
frame_path, mode, out = sys.argv[1:4]
cx = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
W, H = 1600, 2560
dark = (18, 12, 8)
frame = Image.open(frame_path).convert('RGB')
cover = Image.new('RGB', (W, H), dark)
if mode == 'crop':
    # the picture fills the lower part of the cover; the title sits on dark above it
    top = 640
    ph = H - top
    fw, fh = frame.size
    cw = round(fh * W / ph)
    x0 = min(max(0, round(cx * fw - cw / 2)), fw - cw)
    pic = frame.crop((x0, 0, x0 + cw, fh)).resize((W, ph), Image.LANCZOS)
    m = Image.new('L', (W, ph), 255); d = ImageDraw.Draw(m)
    for y in range(220):
        d.line([(0, y), (W, y)], fill=round(255 * y / 220))
    cover.paste(pic, (0, top), m)
    shade = Image.new('RGB', (W, H), dark)
    m2 = Image.new('L', (W, H), 0); d2 = ImageDraw.Draw(m2)
    for y in range(H - 900, H):
        d2.line([(0, y), (W, y)], fill=min(245, round(245 * (y - (H - 900)) / 600)))
    cover = Image.composite(shade, cover, m2)
else:
    fh = round(frame.size[1] * W / frame.size[0])
    fr = frame.resize((W, fh), Image.LANCZOS)
    top = (H - fh) // 2 + 60
    m = Image.new('L', (W, fh), 255); d = ImageDraw.Draw(m)
    fade = 260
    for y in range(fade):
        a = round(255 * y / fade)
        d.line([(0, y), (W, y)], fill=a); d.line([(0, fh - 1 - y), (W, fh - 1 - y)], fill=a)
    cover.paste(fr, (0, top), m)

draw = ImageDraw.Draw(cover)
gold, cream = (220, 178, 108), (244, 233, 210)
def centred(text, font, y, fill, stroke=False):
    w = draw.textlength(text, font=font)
    x = (W - w) / 2
    if stroke:
        draw.text((x, y), text, font=font, fill=fill, stroke_width=3, stroke_fill=dark)
    else:
        draw.text((x + 4, y + 5), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=fill)
cin = FONTS + '/cinzel-700.woff'
ital = FONTS + '/eb-garamond-400-italic.woff'
centred('BLOOD AND THRONES  ·  BOOK ONE', ImageFont.truetype(cin, 58), 150, gold)
centred('HORSE OF THE', ImageFont.truetype(cin, 158), 270, cream)
centred('SERVANT', ImageFont.truetype(cin, 210), 450, cream)
centred('A Graphic Novel', ImageFont.truetype(ital, 88), H - 470, (238, 206, 150), stroke=True)
centred('RV MENON', ImageFont.truetype(cin, 120), H - 310, cream, stroke=True)
cover.save(out, 'JPEG', quality=92, optimize=True, progressive=False, subsampling=0)
print(out, cover.size)
