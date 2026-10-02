"""V15 native lettering helpers, derived from the read-only Chapter 1 r3 wrapper.

Preserves the reviewed font metrics, exact-copy mapping and aspect-fit policy.
General chapter assembly and print verification live below these helpers.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
import re
import statistics
import subprocess
from pathlib import Path
from types import SimpleNamespace

PAGE_WIDTH_PT=441.0
PAGE_HEIGHT_PT=666.0
ART_X_PT=36.0
ART_Y_PT=56.25
ART_WIDTH_PT=369.0
TITLE_BAND_PT=30.0
STORY_HEIGHT_PT=523.5
GAP_PT=2.0
DIN_SIZE_PT=8.5
DIN_LEADING_PT=9.52
MIN_INK_MARGIN_PT=1.0
PREFERRED_INK_MARGIN_PT=2.0
LEDGER_INSCRIPTION_SOURCE_RECT=[300.0,560.0,760.0,690.0]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _font_paths():
    return {
        "din": Path("/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"),
        "georgia_bold": Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf"),
        "georgia": Path("/System/Library/Fonts/Supplemental/Georgia.ttf"),
        "georgia_italic": Path("/System/Library/Fonts/Supplemental/Georgia Italic.ttf"),
    }

def _copy_rect_source(rect):
    if not isinstance(rect, list) or len(rect) != 4:
        raise ValueError("copy reserve rect must be four source-pixel values")
    x0, y0, x1, y1 = [float(v) for v in rect]
    if x1 <= x0 or y1 <= y0:
        raise ValueError("copy reserve rect must be half-open [x0,y0,x1,y1]")
    return x0, y0, x1, y1

def _source_to_page(x, y, image_size, measured):
    """Map top-left selected-image pixels through the reviewed V14 matrix."""
    width, height = image_size
    a, _, _, d, e, f = measured["matrix"]
    return e + a * x / width, f + d * (1.0 - y / height)

def _wrap_text(text, font, size, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = word if not line else line + " " + word
        if font.stringWidth(candidate, size) <= width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def _din_ink_metrics(size=DIN_SIZE_PT):
    """Return actual DIN glyph bounds, scaled from the trusted system font."""
    from PIL import ImageFont
    scale = 100
    font = ImageFont.truetype(str(_font_paths()["din"]), int(size * scale))
    def line_bounds(line):
        x0, y0, x1, y1 = font.getbbox(line, anchor="ls")
        # PIL reports y downward from the baseline. Convert to PDF's upward y.
        return (x0 / scale, -y1 / scale, x1 / scale, -y0 / scale)
    return line_bounds

def _measure_copy_block(lines, box_width, box_height, size=DIN_SIZE_PT):
    """Fit lines by actual glyph ink boxes and V14's native leading."""
    line_bounds = _din_ink_metrics(size)
    bounds = [line_bounds(line) for line in lines]
    if not bounds:
        return {"fits": True, "ink_margins_pt": {"left": box_width, "right": box_width,
                "top": box_height, "bottom": box_height}, "tight": False,
                "actual_line_bounds_pt": [], "baselines_pt": []}
    content_width = box_width - 4.0
    max_ink_width = max(b[2] - b[0] for b in bounds)
    top_box = max(b[3] for b in bounds)
    bottom_box = min(b[1] for b in bounds)
    span = (len(lines) - 1) * DIN_LEADING_PT + top_box - bottom_box
    first_baseline = box_height - (box_height - span) / 2.0 - top_box
    baselines = [first_baseline - i * DIN_LEADING_PT for i in range(len(lines))]
    ink_top = baselines[0] + top_box
    ink_bottom = baselines[-1] + bottom_box
    ink_margins = {"left": 2.0, "right": box_width - 2.0 - max_ink_width,
                   "top": box_height - ink_top, "bottom": ink_bottom}
    hard_fit = max_ink_width <= content_width and all(value >= MIN_INK_MARGIN_PT for value in ink_margins.values())
    return {"fits": hard_fit, "ink_margins_pt": ink_margins, "tight": any(value < PREFERRED_INK_MARGIN_PT for value in ink_margins.values()),
            "actual_line_bounds_pt": bounds, "baselines_pt": baselines, "span_pt": span}

def validate_copy_runs(script, rows):
    """Confirm every native copy chunk is represented exactly once in reserves."""
    panels = {p["id"]: p for page in script["pages"].values() for p in page["panels"]}
    report = {"panel_count": len(panels), "copy_chunk_count": 0, "covered_chunk_count": 0, "panels": []}
    for row in rows:
        copy_count = len(panels[row["id"]]["copy"])
        indices = [i for reserve in row.get("reserves", []) for i in reserve.get("copy_indices", [])]
        if sorted(indices) != list(range(copy_count)):
            raise ValueError(f"copy chunks are not represented exactly once in {row['id']}")
        report["copy_chunk_count"] += copy_count
        report["covered_chunk_count"] += len(indices)
        report["panels"].append({"frame_id": row["id"], "copy_chunks": copy_count, "covered_indices": indices})
    return report

def fit_clip_contain(row, panel):
    """Fit a selected visible viewport without distorting or clipping reserves."""
    px, py, pw, ph = panel["rect_pt"]
    vx0, vy0, vx1, vy1 = row["visible_rect"]
    image_aspect = (vx1 - vx0) / (vy1 - vy0)
    target_aspect = pw / ph
    if abs(image_aspect / target_aspect - 1.0) <= 0.02:
        return [px, py, pw, ph], None
    if image_aspect > target_aspect:
        height = pw / image_aspect
        clip = [px, py + (ph - height) / 2.0, pw, height]
    else:
        width = ph * image_aspect
        clip = [px + (pw - width) / 2.0, py, width, ph]
    return clip, {"planned_rect_pt": [px, py, pw, ph], "actual_clip_rect_pt": clip,
                  "visible_aspect": image_aspect, "planned_aspect": target_aspect,
                  "policy": "contain_visible_viewport_centered_inside_planned_slot"}

def copy_fit_measurements(rows, script, geometry, v14, reject_failures=True):
    """Validate and report every ledger reserve before any PDF authoring."""
    panel_by_id = {p["id"]: p for page in geometry["pages"].values() for p in page}
    panels_by_script = {p["id"]: p for page in script["pages"].values() for p in page["panels"]}
    measurements = []
    from reportlab.pdfbase import pdfmetrics
    _register_fonts(); din = pdfmetrics.getFont("Chapter01DIN")
    copy_run_report = validate_copy_runs(script, rows)
    for row in rows:
        panel = panel_by_id[row["id"]]; clip, adaptation = fit_clip_contain(row, panel)
        measured = v14.B.measure([row["width"], row["height"]], row["visible_rect"], clip)
        copy = panels_by_script[row["id"]]["copy"]
        for reserve in row["reserves"]:
            x0, y0, x1, y1 = _copy_rect_source(reserve["rect"])
            left, bottom = _source_to_page(x0, y1, (row["width"], row["height"]), measured)
            right, top = _source_to_page(x1, y0, (row["width"], row["height"]), measured)
            width, height = right - left, top - bottom
            lines = []
            for index in reserve["copy_indices"]:
                lines.extend(_wrap_text(copy[index]["text"], din, 8.5, width - 4.0))
            block = _measure_copy_block(lines, width, height, DIN_SIZE_PT)
            fits = width > 4.0 and block["fits"]
            if not fits and reject_failures:
                raise ValueError(f"copy reserve does not fit {row['id']} indices {reserve['copy_indices']}")
            measurements.append({"frame_id": row["id"], "copy_indices": reserve["copy_indices"],
                                 "rect_pt": [left, bottom, width, height], "lines": lines,
                                 "adaptation": adaptation,
                                 "fits": fits, "fit_issue": None if fits else "reserve height or width is insufficient",
                                 "minimum_clearance_pt": MIN_INK_MARGIN_PT, "target_clearance_pt": PREFERRED_INK_MARGIN_PT,
                                 "ink_margins_pt": block["ink_margins_pt"], "tight_margin": block["tight"],
                                 "leading_pt": DIN_LEADING_PT, "actual_line_bounds_pt": block["actual_line_bounds_pt"],
                                 "baselines_pt": block["baselines_pt"]})
    return measurements

def _register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    paths = _font_paths()
    for path in paths.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    pdfmetrics.registerFont(TTFont("Chapter01DIN", str(paths["din"])))
    pdfmetrics.registerFont(TTFont("Chapter01GeorgiaBold", str(paths["georgia_bold"])))
    pdfmetrics.registerFont(TTFont("Chapter01Georgia", str(paths["georgia"])))
    pdfmetrics.registerFont(TTFont("Chapter01GeorgiaItalic", str(paths["georgia_italic"])))
    return paths

def _draw_sound_symbols(canvas, row, measured):
    """Draw tiny vector sound marks from ledger source coordinates."""
    origin = row.get("sound_origin")
    if not isinstance(origin, list) or len(origin) != 2:
        return
    x, y = _source_to_page(float(origin[0]), float(origin[1]), (row["width"], row["height"]), measured)
    gray = float(row.get("sound_gray", 0.08))
    scale = float(row.get("sound_scale", 0.6))
    if not 0.0 <= gray <= 1.0 or scale <= 0.0:
        raise ValueError(f"invalid sound symbol style for {row['id']}")
    canvas.saveState()
    canvas.setStrokeColorRGB(gray, gray, gray)
    canvas.setFillColorRGB(gray, gray, gray)
    for offset in (0.0, 9.0 * scale):
        cx = x + offset
        cy = y - offset * 0.12
        canvas.circle(cx, cy, 1.9 * scale, stroke=0, fill=1)
        canvas.setLineWidth(0.9 * scale)
        canvas.line(cx + 1.8 * scale, cy + 1.5 * scale, cx + 1.8 * scale, cy + 12.0 * scale)
        canvas.line(cx + 1.8 * scale, cy + 12.0 * scale, cx + 6.5 * scale, cy + 14.0 * scale)
    canvas.restoreState()


def measure(size, visible, clip):
    """Uniform image placement; PPI includes crop and exterior image padding."""
    width, height = size
    vx0, vy0, vx1, vy1 = visible
    if not (width > 0 and height > 0 and 0 <= vx0 < vx1 <= width and 0 <= vy0 < vy1 <= height):
        raise ValueError('Invalid dimensions or visible rectangle')
    x, y, w, h = clip
    if not all(math.isfinite(v) for v in clip) or min(w, h) <= 0:
        raise ValueError('Invalid clip rectangle')
    vw, vh = vx1-vx0, vy1-vy0
    s = max(w/vw, h/vh)
    return {'matrix': [s*width, 0, 0, s*height,
                       x+(w-s*vw)/2-s*vx0, y+(h-s*vh)/2-s*(height-vy1)],
            'clip_xywh_pt': list(clip), 'effective_ppi': 72/s}


def scaled_row(row, width, height):
    result = copy.deepcopy(row)
    sx, sy = width/row['width'], height/row['height']
    def rect(values):
        return [round(v*(sx if i%2 == 0 else sy)) for i,v in enumerate(values)]
    result['width'], result['height'] = width, height
    result['visible_rect'] = rect(row['visible_rect'])
    for reserve in result['reserves']:
        reserve['rect'] = rect(reserve['rect'])
    if row.get('sound_origin'):
        result['sound_origin'] = rect(row['sound_origin'])
    if row.get('ledger_rect'):
        result['ledger_rect'] = rect(row['ledger_rect'])
    if row.get('original_visible_rect'):
        result['original_visible_rect'] = rect(row['original_visible_rect'])
    return result


def geometry_for_script(script, page_rows=None):
    """Arbitrary page count, with explicit row overrides or equal default rows."""
    pages = {}
    for page_no, page in script['pages'].items():
        panel_ids = [p['id'] for p in page['panels']]
        rows = (page_rows or {}).get(str(page_no))
        if rows is None:
            n = len(panel_ids)
            rows = [(STORY_HEIGHT_PT-GAP_PT*(n-1))/n]*n
        expanded = [r if isinstance(r, (list,tuple)) else [r] for r in rows]
        if sum(len(r) for r in expanded) != len(panel_ids):
            raise ValueError(f'Layout panel count differs on page {page_no}')
        if abs(sum(r[0] for r in expanded)+GAP_PT*(len(expanded)-1)-STORY_HEIGHT_PT)>0.01:
            raise ValueError(f'Layout heights do not fill page {page_no}')
        if any(not r or min(r)<=0 or len(set(r))!=1 for r in expanded):
            raise ValueError('Each row must have a positive common height')
        y_top = ART_Y_PT+STORY_HEIGHT_PT
        panels = []
        for row in expanded:
            height=row[0]; width=(ART_WIDTH_PT-GAP_PT*(len(row)-1))/len(row)
            y=y_top-height
            for col in range(len(row)):
                panels.append({'id':panel_ids[len(panels)],
                    'rect_pt':[ART_X_PT+col*(width+GAP_PT),y,width,height]})
            y_top=y-GAP_PT
        pages[str(page_no)]=panels
    return {'page_width_pt':441,'page_height_pt':666,'pages':pages}


def validate_selection(rows, script, chapter_dir):
    from PIL import Image
    expected=[p['id'] for page in script['pages'].values() for p in page['panels']]
    if [r['id'] for r in rows] != expected:
        raise ValueError('Selected frames must cover every scripted panel once, in order')
    seen=set()
    for r in rows:
        path=Path(r['path']).resolve()
        if not path.is_relative_to(chapter_dir.resolve()):
            raise ValueError(f'Selected frame must be copied into chapter: {path}')
        if sha256(path)!=r['sha256'] or r['sha256'] in seen:
            raise ValueError(f'Changed or duplicated frame: {r["id"]}')
        seen.add(r['sha256'])
        with Image.open(path) as im:
            if im.mode!='RGB' or im.size!=(r['width'],r['height']):
                raise ValueError(f'RGB/dimensions mismatch: {r["id"]}')
        if sha256(Path(r['prompt_path']))!=r['prompt_sha256']:
            raise ValueError(f'Prompt hash mismatch: {r["id"]}')
        for ref in r.get('references',[]):
            if sha256(Path(ref['path']))!=ref['sha256']:
                raise ValueError(f'Reference drift: {ref["path"]}')
        if r.get('visual_review') not in ('pass','passed'):
            raise ValueError(f'Frame lacks visual acceptance: {r["id"]}')
    validate_copy_runs(script, rows)


def dpi_gate(rows, geometry, chapter_dir, upscale_python, upscale_script):
    """Upscale only actual placement failures, retaining originals and provenance."""
    from PIL import Image
    panel_map={p['id']:p for pp in geometry['pages'].values() for p in pp}
    selected=[]; actions=[]
    for original in rows:
        row=copy.deepcopy(original)
        panel=panel_map[row['id']]
        for attempt in range(4):
            clip,_=fit_clip_contain(row,panel)
            before=measure([row['width'],row['height']],row['visible_rect'],clip)
            if before['effective_ppi']>=300: break
            if attempt==3: raise ValueError(f'Cannot reach 300 PPI: {row["id"]}')
            source=Path(row['path'])
            dest=chapter_dir/'frames'/f'{source.stem}-2x.png'
            if dest.exists(): raise FileExistsError(dest)
            subprocess.run([str(upscale_python),str(upscale_script),str(source),str(dest)],check=True)
            with Image.open(dest) as im:
                width,height=im.size
                if im.mode!='RGB' or (width,height)!=(row['width']*2,row['height']*2):
                    raise ValueError('Upscaler did not produce exact 2x RGB output')
            action={'frame_id':row['id'],'input_path':str(source),'input_sha256':sha256(source),
                    'output_path':str(dest),'output_sha256':sha256(dest),
                    'before_ppi':before['effective_ppi'],'factor':2,
                    'upscaler_path':str(upscale_script),'upscaler_sha256':sha256(upscale_script)}
            model=upscale_script.with_name('RealESRGAN_x2plus.pth')
            licence=upscale_script.with_name('LICENSE-Real-ESRGAN.txt')
            if model.exists():action['model_sha256']=sha256(model)
            if licence.exists():action['licence_sha256']=sha256(licence)
            row=scaled_row(row,width,height)
            row['path']=str(dest.resolve());row['sha256']=sha256(dest)
            row.setdefault('transforms',[]).append(action)
            actions.append(action)
        selected.append(row)
    return selected,actions


def page_boxes(folio):
    return {'media_box':[0,0,441,666],'bleed_box':[0,0,441,666],
            'trim_box':([9,9,441,657] if folio%2 else [0,9,432,657])}


def compose(rows,script,geometry,output_path,*,first_folio=1,chapter=1):
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, black
    from reportlab.lib.utils import ImageReader
    helper=SimpleNamespace(B=SimpleNamespace(measure=measure))
    measurements=copy_fit_measurements(rows,script,geometry,helper)
    copy_by_frame={}
    for m in measurements:copy_by_frame.setdefault(m['frame_id'],[]).append(m)
    row_map={r['id']:r for r in rows}
    if output_path.exists():raise FileExistsError(output_path)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(output_path),pagesize=(441,666),pageCompression=1,invariant=1)
    c.setTitle(f'Horse of the Servant V15 Chapter {chapter}: {script["title"]}')
    placements=[]
    for index,(page_no,page) in enumerate(script['pages'].items()):
        folio=first_folio+index;boxes=page_boxes(folio)
        c.setBleedBox(boxes['bleed_box']);c.setTrimBox(boxes['trim_box'])
        c.setFillColor(HexColor('#F7F0DE'));c.rect(0,0,441,666,stroke=0,fill=1)
        panels=geometry['pages'][str(page_no)]
        for panel in panels:
            row=row_map[panel['id']];clip,_=fit_clip_contain(row,panel)
            m=measure([row['width'],row['height']],row['visible_rect'],clip)
            if m['effective_ppi']<300:raise ValueError('DPI gate failed before authoring')
            c.saveState();p=c.beginPath();p.rect(*clip);c.clipPath(p,stroke=0,fill=0)
            a,_,_,d,e,f=m['matrix']
            c.drawImage(ImageReader(row['path']),e,f,width=a,height=d,mask='auto')
            c.restoreState();c.setStrokeColor(black);c.setLineWidth(.75);c.rect(*clip,stroke=1,fill=0)
            _draw_sound_symbols(c,row,m)
            if row.get('ledger_inscription'):
                global LEDGER_INSCRIPTION_SOURCE_RECT
                LEDGER_INSCRIPTION_SOURCE_RECT=row.get('ledger_rect',[300,560,760,690])
                _draw_ledger_inscription(c,panel,row,m)
            placements.append({'frame_id':row['id'],'page':index+1,'folio':folio,
                               'image_sha256':row['sha256'],**m})
        c.setFillColor(black);c.setFont('Chapter01GeorgiaBold',14.5)
        title=re.sub(r'^Chapter\s+\d+\s*:\s*','',script['title'],flags=re.I)
        # Wrap a long heading at word boundaries without shrinking native lettering.
        from reportlab.pdfbase import pdfmetrics
        heading=_wrap_text(title,pdfmetrics.getFont('Chapter01GeorgiaBold'),14.5,ART_WIDTH_PT)
        if len(heading)>2:raise ValueError('Chapter title requires a reviewed heading layout')
        for line_no,line in enumerate(heading):
            c.drawCentredString(220.5,ART_Y_PT+STORY_HEIGHT_PT+8+(len(heading)-1-line_no)*15,line)
        c.setFont('Chapter01Georgia',8);c.drawCentredString(220.5,42,str(folio))
        for panel in panels:
            for m in copy_by_frame.get(panel['id'],[]):
                x,y,w,h=m['rect_pt']
                c.setFillColor(black);c.setFont('Chapter01DIN',DIN_SIZE_PT)
                for line,baseline in zip(m['lines'],m['baselines_pt']):
                    c.drawString(x+2,y+baseline,line)
        c.showPage()
    c.save()
    return {'copy_fit_measurements':measurements,'placements':placements}


def verify_page_chunks(text,chunks):
    """Require exact words and punctuation, whitespace-normalised, in order."""
    norm=lambda v:re.sub(r'\s+',' ',v).strip()
    text=norm(text)
    from collections import Counter
    counts=Counter(norm(x) for x in chunks)
    for chunk,count in counts.items():
        if text.count(chunk)!=count:raise ValueError(f'Missing or duplicate script chunk: {chunk}')
    cursor=0
    for chunk in chunks:
        chunk=norm(chunk);found=text.find(chunk,cursor)
        if found<0:raise ValueError(f'Out-of-order script chunk: {chunk}')
        cursor=found+len(chunk)
    return len(chunks)


def verify_pdf(pdf,rows,script,placements,first_folio=1):
    """Audit every embedded placement from PDF transformation matrices."""
    from pypdf import PdfReader
    from PIL import Image
    reader=PdfReader(pdf)
    if len(reader.pages)!=len(script['pages']):raise ValueError('PDF page count differs')
    row_map={r['id']:r for r in rows}
    images=[];chunks=0;fonts=[]
    for i,page in enumerate(reader.pages):
        expected=[r for r in placements if r['page']==i+1]
        info=pdf_image_placements(page,reader)
        if len(info)!=len(expected):raise ValueError('Placed image count differs')
        boxes=page_boxes(first_folio+i)
        for name,attribute in [('media_box','mediabox'),('bleed_box','bleedbox'),('trim_box','trimbox')]:
            if [float(v) for v in getattr(reader.pages[i],attribute)]!=boxes[name]:
                raise ValueError(f'PDF {name} differs')
        for actual,wanted in zip(info,expected):
            a,b,c,d,e,f=actual['transform']
            width_in=math.hypot(a,b)/72;height_in=math.hypot(c,d)/72
            px=actual['width']/width_in;py=actual['height']/height_in
            if min(px,py)<300-0.001:raise ValueError(f'Embedded image below 300 PPI: {wanted["frame_id"]}')
            if abs(min(px,py)-wanted['effective_ppi'])>.01:raise ValueError('PDF transform differs from plan')
            with Image.open(row_map[wanted['frame_id']]['path']) as im:
                if hashlib.sha256(actual['rgb']).hexdigest()!=hashlib.sha256(im.tobytes()).hexdigest():
                    raise ValueError(f'Embedded RGB differs: {wanted["frame_id"]}')
            images.append({'frame_id':wanted['frame_id'],'page':i+1,'xref':actual['xref'],
                'pixels':[actual['width'],actual['height']], 'placed_inches':[width_in,height_in],
                'ppi_x':px,'ppi_y':py,'effective_ppi':min(px,py),
                'clip_xywh_pt':wanted['clip_xywh_pt'],'source_sha256':wanted['image_sha256']})
        text=page.extract_text()
        if chr(0x2014) in text or chr(0x2013) in text:raise ValueError('Dash in PDF lettering')
        scripted_page=list(script['pages'].values())[i]
        chunks+=verify_page_chunks(text,[c['text'] for p in scripted_page['panels'] for c in p['copy']])
        for name,ref in page['/Resources']['/Font'].items():
            font=ref.get_object();descriptor=font.get('/FontDescriptor')
            # ReportLab may register unused Helvetica; require embedding for used fonts.
            from pypdf.generic import ContentStream
            used={str(args[0]) for args,op in ContentStream(page.get_contents(),reader).operations if op==b'Tf'}
            if str(name) not in used:continue
            if descriptor is None:
                # ReportLab emits a harmless initial Helvetica Tf with no associated Tj.
                if str(font.get('/BaseFont'))=='/Helvetica':continue
                raise ValueError(f'Font has no descriptor: {name}')
            descriptor=descriptor.get_object()
            if not any(k in descriptor for k in ('/FontFile','/FontFile2','/FontFile3')):
                raise ValueError(f'Font not embedded: {name}')
            fonts.append(str(font['/BaseFont']))
    values=[r['effective_ppi'] for r in images]
    if len({r['xref'] for r in images})!=len(images):
        raise ValueError('PDF must contain one unique image object per panel')
    return {'status':'pass','pdf_path':str(pdf),'pdf_sha256':sha256(pdf),'page_count':len(reader.pages),
            'placed_image_count':len(images),'minimum_effective_ppi':min(values),
            'median_effective_ppi':statistics.median(values),'required_ppi':300,
            'method':'Embedded pixel dimensions divided by PDF image transform lengths in inches. Crop does not increase PPI.',
            'images':images,'script_chunks_verified':chunks,'embedded_fonts':sorted(set(fonts))}


def render_pdf(pdf,render_dir):
    """Render the final PDF at 300 DPI using Poppler."""
    import shutil
    from pypdf import PdfReader
    from PIL import Image
    render_dir.mkdir(parents=True,exist_ok=True)
    bundled=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm'
    poppler=shutil.which('pdftoppm') or (str(bundled) if bundled.exists() else None)
    if not poppler:raise RuntimeError('Poppler pdftoppm is required')
    doc=PdfReader(pdf);result=[]
    for i,page in enumerate(doc.pages):
        path=render_dir/f'page-{i+1:02d}.png'
        if path.exists():raise FileExistsError(path)
        if poppler:
            subprocess.run([poppler,'-png','-singlefile','-r','300','-f',str(i+1),'-l',str(i+1),str(pdf),str(path.with_suffix(''))],check=True)
        with Image.open(path) as im:
            if im.size!=(1838,2775):raise ValueError(f'Unexpected 300 DPI render size {im.size}')
        result.append({'path':str(path),'sha256':sha256(path),'dpi':300,'renderer':'Poppler' if poppler else 'MuPDF'})
    return result


def pdf_image_placements(page,reader):
    """Read actual CTMs, resolving nested Form XObjects conservatively."""
    from pypdf.generic import ContentStream
    def concat(left,right):
        a,b,c,d,e,f=left;A,B,C,D,E,F=right
        return [a*A+c*B,b*A+d*B,a*C+c*D,b*C+d*D,a*E+c*F+e,b*E+d*F+f]
    found=[]
    def walk(stream,resources,initial,depth=0):
        if depth>10:raise ValueError('Nested PDF form depth exceeded')
        matrix=initial[:];stack=[]
        for args,op in ContentStream(stream,reader).operations:
            if op==b'q':stack.append(matrix[:])
            elif op==b'Q':matrix=stack.pop()
            elif op==b'cm':matrix=concat(matrix,[float(x) for x in args])
            elif op==b'Do':
                ref=resources['/XObject'].raw_get(args[0]);obj=ref.get_object()
                if obj['/Subtype']=='/Image':
                    if obj['/ColorSpace']!='/DeviceRGB' or int(obj['/BitsPerComponent'])!=8:
                        raise ValueError('Expected 8-bit RGB embedded image')
                    found.append({'width':int(obj['/Width']),'height':int(obj['/Height']),
                        'transform':matrix[:],'xref':ref.idnum,'rgb':obj.get_data()})
                elif obj['/Subtype']=='/Form':
                    walk(obj,obj.get('/Resources',resources),concat(matrix,list(obj.get('/Matrix',[1,0,0,1,0,0]))),depth+1)
    walk(page.get_contents(),page['/Resources'],[1,0,0,1,0,0])
    return found

def _draw_ledger_inscription(canvas, panel, row, measured):
    """Add the tiny native ledger entry specified by page 1 panel 2."""
    x0, y0, x1, y1 = LEDGER_INSCRIPTION_SOURCE_RECT
    left, bottom = _source_to_page(x0, y1, (row["width"], row["height"]), measured)
    right, top = _source_to_page(x1, y0, (row["width"], row["height"]), measured)
    canvas.saveState()
    canvas.setFillColorRGB(0.08, 0.06, 0.04)
    canvas.setFont("Chapter01GeorgiaItalic", 6.5)
    canvas.drawString(left, bottom + (top - bottom) * 0.26, "17   prisioneiro marata")
    canvas.restoreState()
