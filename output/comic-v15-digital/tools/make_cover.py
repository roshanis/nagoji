"""Provisional screen-edition cover: title type over the ch11 page 21 ridge frame."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

frame_path, font_path, serif_path, out = sys.argv[1:5]
W, H = 1600, 2311
bg = (20, 14, 10)
cover = Image.new("RGB", (W, H), bg)
frame = Image.open(frame_path).convert("RGB")
fw = W
fh = round(frame.size[1] * fw / frame.size[0])
frame = frame.resize((fw, fh), Image.LANCZOS)
top = 700
# fade the frame's top and bottom edges into the background
mask = Image.new("L", (fw, fh), 255)
d = ImageDraw.Draw(mask)
fade = 220
for y in range(fade):
    a = round(255 * y / fade)
    d.line([(0, y), (fw, y)], fill=a)
    d.line([(0, fh - 1 - y), (fw, fh - 1 - y)], fill=a)
cover.paste(frame, (0, top), mask)

draw = ImageDraw.Draw(cover)
gold = (214, 172, 104)
cream = (240, 228, 205)

def centred(text, font, y, fill):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)

title = ImageFont.truetype(font_path, 150)
small = ImageFont.truetype(font_path, 52)
author = ImageFont.truetype(font_path, 72)
serif = ImageFont.truetype(serif_path, 46)
centred("BLOOD AND THRONES  ·  BOOK ONE", small, 200, gold)
centred("HORSE OF THE", title, 330, cream)
centred("SERVANT", title, 500, cream)
centred("A Graphic Novel", serif, 1880, gold)
centred("RV MENON", author, 2050, cream)
cover.save(out, "JPEG", quality=90, optimize=True, progressive=True, subsampling=0)
