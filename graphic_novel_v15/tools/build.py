#!/usr/bin/env python3
"""Build the V15 graphic novel from characters.yaml and script_*.yaml.

Commands:
  check     validate the script and characters (run before anything else)
  docs      write character_bible.md and script_*.md for reading and review
  prompts   write prompts/<script>.jsonl, one Qwen request per panel
  openai    write OpenAI image prompts (JSONL for the API, Markdown for ChatGPT)
  pages     compose lettered pages from art/<panel-id>.png (grey placeholders
            where art is missing) into out/pages/*.png and out/<script>.pdf

Usage:
  python tools/build.py check|docs|prompts|openai|pages [script_ch01-05.yaml]

Lettering is done here, not by the image model, so balloons can never overflow,
go blank or cover a title the way V13 page 136 did: any text that does not fit
stops the build with an error that names the panel.
"""
import json
import math
import re
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"

# Page geometry: 6.125 x 9.25 in trim (same as V13) at 300 dpi.
DPI = 300
PAGE_W, PAGE_H = round(6.125 * DPI), round(9.25 * DPI)
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 96, 110, 150
GUTTER = 30
HEADER_H = 190
BORDER = 6

PAPER = (246, 239, 224)
INK = (22, 20, 18)
CAPTION_FILL = (250, 236, 196)
BALLOON_FILL = (255, 255, 255)

LETTER_PT = 8.0          # standard comic lettering size
MIN_LETTER_PT = 7.0      # never shrink below this; fail instead
MAX_CAPTION_WORDS = 18   # style rule, see style_guide.md
MAX_BALLOON_WORDS = 22

# Output sizes Qwen-Image accepts (width, height).
QWEN_SIZES = [(1664, 928), (1472, 1140), (1328, 1328), (1140, 1472), (928, 1664)]

POSITIONS = {"tl", "tc", "tr", "ml", "mr", "bl", "bc", "br"}
TAILS = {"l", "r", "b", "bl", "br", "tr", "tl"}
KINDS = {"speech", "shout", "whisper", "thought"}


def pt_to_px(pt):
    return round(pt * DPI / 72)


def load(script_name):
    chars = yaml.safe_load((ROOT / "characters.yaml").read_text())
    script = yaml.safe_load((ROOT / script_name).read_text())
    return chars, script


def split_char(ref):
    cid, _, phase = ref.partition(":")
    return cid, phase or None


# ------------------------------------------------------------------ check
def check(chars, script):
    errors, warnings = [], []
    cdefs = chars["characters"]
    palettes = chars["style"]["palettes"]
    seen = set()

    def text_rules(where, text, limit):
        if "\u2014" in text or "\u2013" in text:
            errors.append(f"{where}: dash character not allowed (house style: no em dashes)")
        n = len(text.split())
        if n > limit:
            warnings.append(f"{where}: {n} words (limit {limit})")

    for c in cdefs.values():
        for field in ("prompt", "name"):
            if "\u2014" in str(c.get(field, "")):
                errors.append(f"characters.yaml {c.get('name')}: em dash")

    expected_page = 1
    for page in script["pages"]:
        pn = page["page"]
        if pn != expected_page:
            errors.append(f"page {pn}: expected page {expected_page}")
        expected_page = pn + 1
        slots = sum(len(r) for r in page["layout"])
        if len(page["heights"]) != len(page["layout"]):
            errors.append(f"page {pn}: heights and layout have different row counts")
        if slots != len(page["panels"]):
            errors.append(f"page {pn}: layout has {slots} slots but {len(page['panels'])} panels")
        if page.get("palette") not in palettes:
            errors.append(f"page {pn}: unknown palette {page.get('palette')}")
        if "chapter_open" in page and page["chapter_open"] not in script["chapters"]:
            errors.append(f"page {pn}: chapter_open {page['chapter_open']} not in chapters")
        words_on_page = 0
        for p in page["panels"]:
            pid = p["id"]
            if pid in seen:
                errors.append(f"panel {pid}: duplicate id")
            seen.add(pid)
            if not pid.startswith(f"{pn:02d}-"):
                errors.append(f"panel {pid}: id does not match page {pn}")
            for ref in p.get("chars", []):
                cid, phase = split_char(ref)
                if cid not in cdefs:
                    errors.append(f"panel {pid}: unknown character {cid}")
                elif phase and phase not in cdefs[cid].get("phases", {}):
                    errors.append(f"panel {pid}: {cid} has no phase {phase}")
                elif not phase and cdefs[cid].get("phases"):
                    errors.append(f"panel {pid}: {cid} needs a phase ({', '.join(cdefs[cid]['phases'])})")
            art = p.get("art", "")
            if not art.strip():
                errors.append(f"panel {pid}: no art description")
            if '"' in art:
                warnings.append(f"panel {pid}: quotation marks in art text can make Qwen draw lettering")
            text_rules(f"panel {pid} art", art, 10_000)
            has_words = False
            for c in p.get("captions", []):
                text_rules(f"panel {pid} caption", c["text"], MAX_CAPTION_WORDS)
                if c.get("pos", "tl") not in POSITIONS:
                    errors.append(f"panel {pid}: bad caption pos {c.get('pos')}")
                words_on_page += len(c["text"].split())
                has_words = True
            for b in p.get("balloons", []):
                text_rules(f"panel {pid} balloon", b["text"], MAX_BALLOON_WORDS)
                if b.get("kind", "speech") not in KINDS:
                    errors.append(f"panel {pid}: bad balloon kind {b.get('kind')}")
                if b.get("pos", "tl") not in POSITIONS:
                    errors.append(f"panel {pid}: bad balloon pos {b.get('pos')}")
                if b.get("tail", "b") not in TAILS:
                    errors.append(f"panel {pid}: bad balloon tail {b.get('tail')}")
                if not b["text"].strip():
                    errors.append(f"panel {pid}: empty balloon")
                words_on_page += len(b["text"].split())
                has_words = True
            if not has_words and not p.get("silent"):
                warnings.append(f"panel {pid}: no text; mark silent: true if intended")
        if words_on_page > 90:
            warnings.append(f"page {pn}: {words_on_page} words of lettering (aim for 90 or fewer)")
    return errors, warnings


# ------------------------------------------------------------------ layout
def page_boxes(page):
    top = MARGIN_TOP + (HEADER_H if page.get("chapter_open") else 0)
    avail_h = PAGE_H - top - MARGIN_BOTTOM - GUTTER * (len(page["layout"]) - 1)
    avail_w = PAGE_W - 2 * MARGIN_X
    total_h = sum(page["heights"])
    boxes, y = [], top
    for row, rh in zip(page["layout"], page["heights"]):
        h = round(avail_h * rh / total_h)
        w_avail = avail_w - GUTTER * (len(row) - 1)
        total_w = sum(row)
        x = MARGIN_X
        for i, cw in enumerate(row):
            w = round(w_avail * cw / total_w) if i < len(row) - 1 else MARGIN_X + avail_w - x
            boxes.append((x, y, w, h))
            x += w + GUTTER
        y += h + GUTTER
    return boxes


def qwen_size(w, h):
    ratio = w / h
    return min(QWEN_SIZES, key=lambda s: abs(math.log((s[0] / s[1]) / ratio)))


# ------------------------------------------------------------------ prompts
def build_prompt(chars, page, panel):
    style = chars["style"]
    cdefs = chars["characters"]
    parts = [style["prompt"].strip().rstrip(".") + ".", style["palettes"][page["palette"]] + "."]
    parts.append(f"Shot: {panel.get('shot', 'medium')}.")
    parts.append(panel["art"].strip().rstrip(".") + ".")
    negatives = [style["negative"]]
    refs = []
    for ref in panel.get("chars", []):
        cid, phase = split_char(ref)
        c = cdefs[cid]
        desc = c["prompt"].strip()
        if phase:
            desc += f", wearing: {c['phases'][phase]['wear'].strip()}"
        parts.append(f"Character: {desc}.")
        if c.get("avoid_visual"):
            negatives.append(c["avoid_visual"])
        refs.append(cid)
    parts.append("Leave clear empty space for lettering; no text anywhere in the image.")
    return " ".join(parts), ", ".join(negatives), refs


def cmd_prompts(chars, script, script_name):
    out = ROOT / "prompts" / (Path(script_name).stem + ".jsonl")
    out.parent.mkdir(exist_ok=True)
    lines = []
    for page in script["pages"]:
        for panel, (x, y, w, h) in zip(page["panels"], page_boxes(page)):
            prompt, negative, refs = build_prompt(chars, page, panel)
            qw, qh = qwen_size(w, h)
            lines.append(json.dumps({
                "id": panel["id"], "page": page["page"], "size": f"{qw}*{qh}",
                "panel_px": [w, h], "characters": refs,
                "prompt": prompt, "negative_prompt": negative,
            }, ensure_ascii=False))
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(ROOT)} ({len(lines)} panels)")


# ------------------------------------------------------------------ OpenAI prompts
# OpenAI image models (gpt-image-1) take one natural-language prompt and no negative
# prompt, so exclusions are written into the prompt as an "Avoid" line.
OPENAI_SIZES = [(1536, 1024), (1024, 1024), (1024, 1536)]
AREA = {"t": "top", "m": "middle", "b": "bottom", "l": "left", "c": "centre", "r": "right"}


def openai_size(w, h):
    ratio = w / h
    return min(OPENAI_SIZES, key=lambda s: abs(math.log((s[0] / s[1]) / ratio)))


def char_block(c, phase):
    lines = [f"- {c['prompt'].strip()}."]
    if phase:
        lines.append(f"  Wearing: {c['phases'][phase]['wear'].strip()}.")
    return "\n".join(lines)


def openai_panel_prompt(chars, page, panel, w, h):
    style, cdefs = chars["style"], chars["characters"]
    ow, oh = openai_size(w, h)
    shape = "landscape" if ow > oh else "portrait" if oh > ow else "square"
    out = [f"A single {shape} panel for a historical graphic novel set on the Indian west coast in 1738.",
           f"Style: {style['prompt'].strip().rstrip('.')}.",
           f"Colour: {style['palettes'][page['palette']]}.",
           f"Camera: {panel.get('shot', 'medium')}.",
           f"Scene: {panel['art'].strip().rstrip('.')}."]
    refs = panel.get("chars", [])
    if refs:
        out.append("Characters (if character reference sheets are attached, match them exactly):")
        for ref in refs:
            cid, phase = split_char(ref)
            out.append(char_block(cdefs[cid], phase))
    spots = sorted({AREA[i["pos"][0]] + "-" + AREA[i["pos"][1]]
                    for i in panel.get("captions", []) + panel.get("balloons", [])})
    if spots:
        out.append("Composition: keep the " + " and ".join(spots) + " area of the frame calm and "
                   "uncluttered (sky, wall or shadow, no faces) because lettering will be added there later.")
    avoid = [style["negative"].strip()]
    avoid += [cdefs[split_char(r)[0]]["avoid_visual"] for r in refs if cdefs[split_char(r)[0]].get("avoid_visual")]
    out.append("Do not draw any text, letters, speech bubbles or captions. Avoid: " + "; ".join(avoid) + ".")
    return "\n".join(out), f"{ow}x{oh}"


def openai_sheet_prompt(chars, cid, phase):
    style, c = chars["style"], chars["characters"][cid]
    animal = any(k in c.get("role", "").lower() for k in ("horse", "mare"))
    views = ("side view, three-quarter view and a head close-up" if animal else
             "full-body front view, three-quarter view, profile view and a head close-up")
    out = [f"A character model sheet for a historical graphic novel: {views} of the same "
           f"{'animal' if animal else 'person'}, on plain warm paper, even neutral light, "
           "the design identical in every view.",
           f"Style: {style['prompt'].strip().rstrip('.')}.",
           "Subject:", char_block(c, phase),
           "Do not draw any text or labels. Avoid: " + style["negative"].strip()
           + (f"; {c['avoid_visual']}" if c.get("avoid_visual") else "") + "."]
    return "\n".join(out)


def cmd_openai(chars, script, script_name):
    stem = Path(script_name).stem
    used = []
    for page in script["pages"]:
        for p in page["panels"]:
            for ref in p.get("chars", []):
                if ref not in used:
                    used.append(ref)
    jl, md = [], [
        f"# OpenAI image prompts: {stem}", "",
        f"Generated by `tools/build.py openai` from `characters.yaml` and `{script_name}`. "
        "Edit those files, not this one.", "",
        "## How to use in ChatGPT", "",
        "1. Generate every character sheet below first, in one conversation per character. "
        "Save the one you like best as `refs/<id>.png`.",
        "2. For each panel, start a new conversation, attach the sheets for the characters "
        "named in that panel, then paste the prompt.",
        "3. Save each result as `art/<panel id>.png`, then run `python tools/build.py pages` to "
        "letter the pages. Do not let ChatGPT add the dialogue; the build does that.", "",
        "The API route is `tools/generate_openai.py`, which does steps 1 and 2 automatically.", "",
        "## Character sheets", ""]
    for ref in used:
        cid, phase = split_char(ref)
        prompt = openai_sheet_prompt(chars, cid, phase)
        rid = ref.replace(":", "__")
        jl.append(json.dumps({"kind": "sheet", "id": rid, "size": "1536x1024", "prompt": prompt},
                             ensure_ascii=False))
        md += [f"### Sheet `{rid}` (1536x1024)", "", "```", prompt, "```", ""]
    md += ["## Panels", ""]
    for page in script["pages"]:
        md += [f"### Page {page['page']}", ""]
        for panel, (x, y, w, h) in zip(page["panels"], page_boxes(page)):
            prompt, size = openai_panel_prompt(chars, page, panel, w, h)
            refs = [r.replace(":", "__") for r in panel.get("chars", [])]
            jl.append(json.dumps({"kind": "panel", "id": panel["id"], "page": page["page"],
                                  "size": size, "refs": refs, "prompt": prompt}, ensure_ascii=False))
            attach = ", ".join(f"`{r}`" for r in refs) or "none"
            md += [f"#### Panel {panel['id']} ({size}; attach: {attach})", "", "```", prompt, "```", ""]
    (ROOT / "prompts").mkdir(exist_ok=True)
    (ROOT / "prompts" / f"{stem}.openai.jsonl").write_text("\n".join(jl) + "\n")
    (ROOT / f"openai_prompts_{stem.removeprefix('script_')}.md").write_text("\n".join(md))
    print(f"wrote prompts/{stem}.openai.jsonl and openai_prompts_{stem.removeprefix('script_')}.md "
          f"({len(used)} sheets, {len(jl) - len(used)} panels)")


# ------------------------------------------------------------------ docs
def cmd_docs(chars, script, script_name):
    c = chars["characters"]
    md = ["# Horse of the Servant V15: Character Bible", "",
          "Generated from `characters.yaml` by `tools/build.py docs`. Edit the YAML, not this file.", "",
          "## House style", "", chars["style"]["prompt"].strip(), "",
          "**Never:** " + chars["style"]["negative"].strip(), "", "## Characters", ""]
    for cid, d in c.items():
        md += [f"### {d['name']}", ""]
        if d.get("role"):
            md += [f"*{d['role']}*", ""]
        md += [d["prompt"].strip(), ""]
        if d.get("anchors"):
            md += ["**Recognition anchors (must be visible every time):**", ""]
            md += [f"- {a}" for a in d["anchors"]] + [""]
        if d.get("phases"):
            md += ["**Costume phases:**", ""]
            md += [f"- `{k}` ({v['when']}): {v['wear'].strip()}" for k, v in d["phases"].items()] + [""]
        if d.get("avoid"):
            md += [f"**Corrects V13:** {d['avoid']}", ""]
        if d.get("verify"):
            md += [f"**Verify before drawing:** {d['verify']}", ""]
    (ROOT / "character_bible.md").write_text("\n".join(md))

    s = [f"# {script['book']}, V15 script: {Path(script_name).stem}", "",
         f"Generated from `{script_name}` by `tools/build.py docs`. Edit the YAML, not this file.", ""]
    for page in script["pages"]:
        if page.get("chapter_open"):
            n = page["chapter_open"]
            s += [f"## Chapter {n}: {script['chapters'][n]}", ""]
        s += [f"### Page {page['page']}", "", f"*{page['purpose']}*", ""]
        for p in page["panels"]:
            who = ", ".join(split_char(r)[0] for r in p.get("chars", [])) or "no characters"
            s += [f"**Panel {p['id']}** ({p.get('shot', '')}; {who})", "", f"> {p['art'].strip()}", ""]
            for cap in p.get("captions", []):
                s.append(f"- CAPTION: {cap['text']}")
            for b in p.get("balloons", []):
                s.append(f"- {b.get('kind', 'speech').upper()}: {b['text']}")
            if p.get("silent"):
                s.append("- (silent)")
            s.append("")
    (ROOT / (Path(script_name).stem + ".md")).write_text("\n".join(s))
    print("wrote character_bible.md and", Path(script_name).stem + ".md")


# ------------------------------------------------------------------ lettering
def font(name, px):
    return ImageFont.truetype(str(FONTS / name), px)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def layout_text(draw, text, max_w, bold=True):
    """Return (font, lines, text_w, text_h), shrinking to MIN_LETTER_PT before failing."""
    name = "comic-neue-latin-700-normal.woff" if bold else "comic-neue-latin-400-normal.woff"
    pt = LETTER_PT
    while pt >= MIN_LETTER_PT:
        fnt = font(name, pt_to_px(pt))
        lines = wrap(draw, text.upper(), fnt, max_w)
        widest = max(draw.textlength(l, font=fnt) for l in lines)
        if widest <= max_w:
            lh = round(pt_to_px(pt) * 1.18)
            return fnt, lines, widest, lh * len(lines), lh
        pt -= 0.5
    raise ValueError(f"text will not fit at {MIN_LETTER_PT}pt: {text!r}")


def anchor_xy(pos, box, w, h, pad):
    x0, y0, bw, bh = box
    col = {"l": x0 + pad, "c": x0 + (bw - w) // 2, "r": x0 + bw - pad - w}
    row = {"t": y0 + pad, "m": y0 + (bh - h) // 2, "b": y0 + bh - pad - h}
    r, c = pos[0], pos[1]
    return col[c], row[r]


def overlaps(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def draw_tail(draw, rect, tail, box, kind):
    x0, y0, x1, y1 = rect
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    L = 46
    bx0, by0, bw, bh = box
    if tail in ("b", "bl", "br"):
        base_y = y1 - 4
        bxm = {"b": cx, "bl": x0 + (x1 - x0) // 3, "br": x1 - (x1 - x0) // 3}[tail]
        dx = {"b": 0, "bl": -L // 2, "br": L // 2}[tail]
        tip = (bxm + dx, min(y1 + L, by0 + bh - 8))
        base = [(bxm - 16, base_y), (bxm + 16, base_y)]
    elif tail in ("tl", "tr"):
        base_y = y0 + 4
        bxm = x0 + (x1 - x0) // 3 if tail == "tl" else x1 - (x1 - x0) // 3
        tip = (bxm + (-L // 2 if tail == "tl" else L // 2), max(y0 - L, by0 + 8))
        base = [(bxm - 16, base_y), (bxm + 16, base_y)]
    else:
        base_x = x0 + 4 if tail == "l" else x1 - 4
        tip = (max(x0 - L, bx0 + 8) if tail == "l" else min(x1 + L, bx0 + bw - 8), cy + 18)
        base = [(base_x, cy - 14), (base_x, cy + 14)]
    draw.polygon([base[0], tip, base[1]], fill=BALLOON_FILL, outline=INK)
    width = 5 if kind == "shout" else 3
    draw.line([base[0], tip, base[1]], fill=INK, width=width)
    # Cover the balloon border where the tail joins it.
    draw.line(base, fill=BALLOON_FILL, width=width + 4)


def letter_panel(img, draw, panel, box):
    x0, y0, bw, bh = box
    pad = 22
    placed = []
    items = [("caption", c) for c in panel.get("captions", [])] + \
            [("balloon", b) for b in panel.get("balloons", [])]
    for kind, item in items:
        pos = item.get("pos", "tl")
        max_w = int(min(bw * (0.62 if kind == "balloon" else 0.8), 780))
        fnt, lines, tw, th, lh = layout_text(draw, item["text"], max_w,
                                             bold=(kind == "balloon"))
        ipx, ipy = (30, 22) if kind == "balloon" else (18, 12)
        w, h = int(tw + 2 * ipx), int(th + 2 * ipy)
        if w > bw - 2 * pad or h > bh - 2 * pad:
            raise ValueError(f"panel {panel['id']}: {kind} too large for the panel: {item['text']!r}")
        x, y = anchor_xy(pos, box, w, h, pad)
        rect = [x, y, x + w, y + h]
        # Stack items that share a corner instead of overlapping them.
        for _ in range(8):
            hit = next((r for r in placed if overlaps(rect, r)), None)
            if not hit:
                break
            dy = (hit[3] + 14 - rect[1]) if pos[0] != "b" else (hit[1] - 14 - rect[3])
            rect = [rect[0], rect[1] + dy, rect[2], rect[3] + dy]
        if any(overlaps(rect, r) for r in placed) or rect[1] < y0 or rect[3] > y0 + bh:
            raise ValueError(f"panel {panel['id']}: no room for {kind}: {item['text']!r}")
        placed.append(rect)
        if kind == "caption":
            draw.rectangle(rect, fill=CAPTION_FILL, outline=INK, width=3)
        else:
            k = item.get("kind", "speech")
            width = 5 if k == "shout" else 3
            draw.rounded_rectangle(rect, radius=min(h // 2, 60), fill=BALLOON_FILL,
                                   outline=INK, width=width)
            if k == "whisper":
                # Dashed look: break the outline with paper-coloured gaps.
                for gx in range(rect[0] + 40, rect[2] - 40, 36):
                    draw.line([(gx, rect[1]), (gx + 12, rect[1])], fill=BALLOON_FILL, width=width + 2)
                    draw.line([(gx, rect[3]), (gx + 12, rect[3])], fill=BALLOON_FILL, width=width + 2)
            draw_tail(draw, rect, item.get("tail", "b"), box, k)
        ty = rect[1] + ipy
        for line in lines:
            lw = draw.textlength(line, font=fnt)
            tx = rect[0] + (w - lw) / 2 if kind == "balloon" else rect[0] + ipx
            draw.text((tx, ty), line, font=fnt, fill=INK)
            ty += lh


def placeholder(panel, w, h, qsize):
    img = Image.new("RGB", (w, h), (205, 200, 190))
    d = ImageDraw.Draw(img)
    f = font("comic-neue-latin-400-normal.woff", 30)
    msg = f"ART {panel['id']}  ({qsize[0]}x{qsize[1]})\n" + "\n".join(
        wrap(d, panel["art"].strip(), f, w - 60)[:6])
    d.multiline_text((30, h - 40 - 36 * (msg.count("\n") + 1)), msg, font=f, fill=(95, 90, 82), spacing=6)
    return img


def fit_cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def cmd_pages(chars, script, script_name):
    art_dir = ROOT / "art"
    out_dir = ROOT / "out" / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)
    rendered, missing = [], 0
    for page in script["pages"]:
        img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        draw = ImageDraw.Draw(img)
        if page.get("chapter_open"):
            n = page["chapter_open"]
            y = MARGIN_TOP
            draw.line([(MARGIN_X, y + HEADER_H - 40), (PAGE_W - MARGIN_X, y + HEADER_H - 40)], fill=INK, width=3)
            f1 = font("cinzel-latin-700-normal.woff", pt_to_px(9))
            f2 = font("cinzel-latin-700-normal.woff", pt_to_px(19))
            t1 = f"CHAPTER {n}"
            draw.text(((PAGE_W - draw.textlength(t1, font=f1)) / 2, y), t1, font=f1, fill=INK)
            t2 = script["chapters"][n]
            if draw.textlength(t2, font=f2) > PAGE_W - 2 * MARGIN_X:
                f2 = font("cinzel-latin-700-normal.woff", pt_to_px(15))
            draw.text(((PAGE_W - draw.textlength(t2, font=f2)) / 2, y + 52), t2, font=f2, fill=INK)
        for panel, box in zip(page["panels"], page_boxes(page)):
            x, y, w, h = box
            src = art_dir / f"{panel['id']}.png"
            if src.exists():
                art = fit_cover(Image.open(src).convert("RGB"), w, h)
            else:
                art = placeholder(panel, w, h, qwen_size(w, h))
                missing += 1
            img.paste(art, (x, y))
            letter_panel(img, draw, panel, box)
            draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=BORDER)
        fpn = font("cinzel-latin-700-normal.woff", pt_to_px(8))
        num = str(page["page"])
        draw.text(((PAGE_W - draw.textlength(num, font=fpn)) / 2, PAGE_H - MARGIN_BOTTOM + 55), num, font=fpn, fill=INK)
        path = out_dir / f"page-{page['page']:03d}.png"
        img.save(path, dpi=(DPI, DPI))
        rendered.append(img)
    pdf = ROOT / "out" / (Path(script_name).stem + ".pdf")
    rendered[0].save(pdf, save_all=True, append_images=rendered[1:], resolution=DPI)
    print(f"wrote {len(rendered)} pages to {out_dir.relative_to(ROOT)} and {pdf.relative_to(ROOT)}"
          f" ({missing} panels still placeholder art)")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    script_name = sys.argv[2] if len(sys.argv) > 2 else "script_ch01-05.yaml"
    chars, script = load(script_name)
    errors, warnings = check(chars, script)
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        sys.exit(1)
    if cmd == "check":
        print(f"ok: {len(script['pages'])} pages, "
              f"{sum(len(p['panels']) for p in script['pages'])} panels")
    elif cmd == "docs":
        cmd_docs(chars, script, script_name)
    elif cmd == "prompts":
        cmd_prompts(chars, script, script_name)
    elif cmd == "openai":
        cmd_openai(chars, script, script_name)
    elif cmd == "pages":
        cmd_pages(chars, script, script_name)
    else:
        sys.exit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
