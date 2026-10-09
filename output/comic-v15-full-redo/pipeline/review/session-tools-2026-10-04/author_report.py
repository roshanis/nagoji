"""Author report for the V15 chapters: decisions, accepted faults with panel crops, and script/continuity flags.

Usage: python author_report.py OUT_DIR CH=PACKAGE:REVISION ...   (e.g. 1=ch01-v2:r14 2=ch02:r4)
Writes OUT_DIR/AUTHOR-REPORT.md (crops linked from OUT_DIR/crops/) and OUT_DIR/AUTHOR-REPORT.html (crops embedded).
Never overwrites: OUT_DIR must not exist.
"""
import base64, html, io, json, re, sys
from pathlib import Path
from PIL import Image

V = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
PAGE_PT = (441.0, 666.0)
out = Path(sys.argv[1])
builds = {int(k): tuple(v.split(':')) for k, v in (a.split('=') for a in sys.argv[2:])}
out.mkdir(parents=True)
(out / 'crops').mkdir()

faults = json.loads((V / 'review-sheets/AUTHOR-LIST-accepted-faults-2026-10-01.json').read_text())
flags = json.loads((V / 'review-sheets/AUTHOR-FLAGS-ch05-08-2026-10-01.json').read_text())
flags = flags['flags'] if isinstance(flags, dict) else flags


def panels_of(text):
    """Panel ids named in a free-form id: page-02-panel-01, 2.1, '03-05' after a page-panel id."""
    ids = [(int(p), int(n)) for p, n in re.findall(r'page-(\d+)-panel-(\d+)', text)]
    ids += [(int(p), int(n)) for p, n in re.findall(r'(?<![\d.-])(\d{1,2})\.(\d{1,2})(?![\d.])', text)]
    ids += [(int(p), int(n)) for p, n in re.findall(r'(?<=, )(\d\d)-(\d\d)', text)]
    seen, res = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i); res.append(i)
    return res


def page_of(text):
    m = re.search(r'page (\d+)', text)
    return int(m.group(1)) if m else None


def crop(chapter, page, panel=None):
    """A JPEG crop of a panel (or a whole page) from the chapter's latest render, or None."""
    if chapter not in builds:
        return None
    package, rev = builds[chapter]
    render = V / 'chapters' / package / 'renders' / rev / f'page-{page:02d}.png'
    if not render.exists():
        return None
    im = Image.open(render).convert('RGB')
    if panel is not None:
        dpi = json.loads((V / 'chapters' / package / 'review' / f'DPI-REPORT-{rev}.json').read_text())
        pid = f'page-{page:02d}-panel-{panel:02d}'
        rect = next((x['clip_xywh_pt'] for x in dpi['images'] if x['frame_id'] == pid), None)
        if rect is None:
            return None
        s = im.width / PAGE_PT[0]
        x, y, w, h = rect
        box = (int(x * s) - 8, int((PAGE_PT[1] - y - h) * s) - 8, int((x + w) * s) + 8, int((PAGE_PT[1] - y) * s) + 8)
        im = im.crop(box)
    im.thumbnail((900, 900))
    name = f'ch{chapter:02d}-p{page:02d}' + (f'-{panel:02d}' if panel is not None else '') + '.jpg'
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=82)
    (out / 'crops' / name).write_bytes(buf.getvalue())
    return name, base64.b64encode(buf.getvalue()).decode()


md, body = [], []
def both(m, h): md.append(m); body.append(h)

both('# Horse of the Servant V15: author decisions and accepted faults\n',
     '<h1>Horse of the Servant V15</h1><p class="sub">Author decisions and accepted faults, chapters 1 to 8</p>')
builds_line = ', '.join(f'ch{c} {p} {r}' for c, (p, r) in sorted(builds.items()))
both(f'Builds shown: {builds_line}.\n', f'<p class="meta">Builds shown: {html.escape(builds_line)}.</p>')

def shots_for(x):
    shots = [crop(x['chapter'], p, n) for p, n in panels_of(x['id'])[:3]]
    if not any(shots) and page_of(x['id']):
        shots = [crop(x['chapter'], page_of(x['id']))]
    return [s for s in shots if s]


both('\n## Decisions waiting on you\n', '<h2>Decisions waiting on you</h2>')
decisions = list(faults.get('pending_decisions', []))
for d in decisions:
    both(f'- {d}', f"<div class='item'><p>{html.escape(d)}</p></div>")
for x in [x for x in faults['items'] if 'question' in x['kind'] or 'decision' in x['kind']]:
    decisions.append(x['id'])
    both(f"- **Chapter {x['chapter']}, {x['id']}**: {x['fault']}",
         f"<div class='item'><p><b>Chapter {x['chapter']}, {html.escape(x['id'])}</b></p><p>{html.escape(x['fault'])}</p>")
    for s in shots_for(x):
        md.append(f'  ![](crops/{s[0]})')
        body.append(f"<img alt='{s[0]}' src='data:image/jpeg;base64,{s[1]}'>")
    body.append('</div>')

both('\n## Accepted faults, by chapter\n',
     '<h2>Accepted faults, by chapter</h2><p>Each used its correction attempts or sits in art you approved. '
     'For each: accept it, or ask for a regeneration on a later pass.</p>')
for chapter in sorted({x['chapter'] for x in faults['items']}):
    items = [x for x in faults['items'] if x['chapter'] == chapter and 'question' not in x['kind'] and 'decision' not in x['kind']]
    if not items:
        continue
    both(f'\n### Chapter {chapter}\n', f'<h3>Chapter {chapter}</h3>')
    for x in items:
        both(f"- **{x['id']}** ({x['kind']}): {x['fault']}",
             f"<div class='item'><p><b>{html.escape(x['id'])}</b> <span class='kind'>{html.escape(x['kind'])}</span></p>"
             f"<p>{html.escape(x['fault'])}</p>")
        for s in shots_for(x):
            md.append(f'  ![](crops/{s[0]})')
            body.append(f"<img alt='{s[0]}' src='data:image/jpeg;base64,{s[1]}'>")
        body.append('</div>')

both('\n## Script and continuity flags (chapters 5 to 8, from the prompt audit)\n',
     '<h2>Script and continuity flags</h2><p>From the chapter 5 to 8 prompt audit: script or CONTINUITY.md wording '
     'for you to align. The art was worked around them.</p>')
for chapter in sorted({f['chapter'] for f in flags}):
    both(f'\n### Chapter {chapter}\n', f'<h3>Chapter {chapter}</h3><ul>')
    for f in [f for f in flags if f['chapter'] == chapter]:
        md.append(f"- **{f['id']}**: {f['flag']}")
        body.append(f"<li><b>{html.escape(f['id'])}</b>: {html.escape(f['flag'])}</li>")
    body.append('</ul>')

(out / 'AUTHOR-REPORT.md').write_text('\n'.join(md) + '\n')
css = """
:root{--bg:#faf7f0;--fg:#1d1b17;--muted:#6b645a;--card:#fff;--line:#e3dccd;--accent:#8a3b12}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#171513;--fg:#ece6da;--muted:#a59d90;--card:#211e1a;--line:#3a352e;--accent:#e08a5a}}
:root[data-theme="dark"]{--bg:#171513;--fg:#ece6da;--muted:#a59d90;--card:#211e1a;--line:#3a352e;--accent:#e08a5a}
body{background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif;margin:0;padding:24px 16px}
main{max-width:860px;margin:0 auto}h1{margin:0}h2{color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:4px;margin-top:2em}
.sub,.meta,.kind{color:var(--muted)}.kind{font-size:.85em;margin-left:.5em}
.item{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:12px 0}
.item p{margin:.3em 0}img{max-width:100%;height:auto;display:block;margin:8px 0;border:1px solid var(--line)}
li{margin:.4em 0}
"""
(out / 'AUTHOR-REPORT.html').write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>V15 Author Decisions</title><style>{css}</style></head><body><main>' + '\n'.join(body) + '</main></body></html>\n')
print('wrote', out, len(faults['items']), 'faults,', len(flags), 'flags,', len(decisions), 'decisions,',
      len(list((out / 'crops').iterdir())), 'crops')
