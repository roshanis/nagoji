"""Final V15 status report for the author: the build table (from each chapter's final build records), what changed on
2026-10-09, and what is left for the author. Writes Markdown and a rendered HTML copy, and a JSON of the table.
Usage (from output/comic-v15-full-redo): final_report.py FINAL.json OUT_STEM
FINAL.json: {"1": "ch01-v2:r15:d9t-b", ...}  package:revision:b-pass tag of each chapter's final build"""
import html, json, math, re, sys
from pathlib import Path
sys.path.insert(0, 'pipeline')
import reserves as rv, compositor as c

final, stem = json.loads(Path(sys.argv[1]).read_text()), Path(sys.argv[2])


def crossings(pkg, rev, btag):
    p = Path('chapters') / pkg
    frames = {f['id']: f for f in json.loads((p / f'SELECTION-INPUT-{btag}.json').read_text())['frames']}
    places = {x['frame_id']: x for x in json.loads((p / f'review/COMPOSITION-{rev}.json').read_text())['placements']}
    hits = []
    for pid, fr in sorted(frames.items()):
        sp = [r for r in fr['reserves'] if r.get('draw') == 'speech' and r.get('tail')]
        scale = places[pid]['matrix'][0] / fr['width']
        w = [rv.tail_wedge(r['rect'], r.get('corner', c.BALLOON_RADIUS_RATIO), r['tail'], fr['visible_rect'], scale,
                           tuple(r['tail_head']) if r.get('tail_head') else None, bool(r.get('tail_short'))) for r in sp]
        if any(w[i] and w[j] and math.dist(sp[i]['tail'], sp[j]['tail']) > rv.SAME_SPEAKER_PX and rv.tails_cross(w[i], w[j])
               for i in range(len(sp)) for j in range(i + 1, len(sp))):
            hits.append(f"{int(pid[5:7])}.{int(pid[-2:])}")
    return hits


rows, problems = [], []
for ch in range(1, 29):
    pkg, rev, btag = final[str(ch)].split(':')
    p = Path('chapters') / pkg
    dpi = json.loads((p / f'review/DPI-REPORT-{rev}.json').read_text())
    comp = json.loads((p / f'review/COMPOSITION-{rev}.json').read_text())
    folios = sorted({x['folio'] for x in comp['placements']})
    pages = len(re.findall(r'^## PAGE \d+', Path(f'scripts/CHAPTER-{ch:02d}-SCRIPT.md').read_text(), re.M))
    pdf = Path(dpi['pdf_path'])
    row = {'chapter': ch, 'package': pkg, 'revision': rev, 'pages': dpi['page_count'], 'script_pages': pages,
           'first_folio': folios[0], 'last_folio': folios[0] + dpi['page_count'] - 1, 'images': dpi['placed_image_count'],
           'min_ppi': round(dpi['minimum_effective_ppi'], 1), 'pdf': str(pdf.relative_to(Path.cwd())) if pdf.is_absolute() else str(pdf),
           'crossing_tails': crossings(pkg, rev, btag)}
    rows.append(row)
for a, b in zip(rows, rows[1:]):
    if b['first_folio'] != a['last_folio'] + 1: problems.append(f"ch{b['chapter']} starts at {b['first_folio']}, not {a['last_folio'] + 1}")
for r in rows:
    if r['pages'] != r['script_pages']: problems.append(f"ch{r['chapter']}: {r['pages']} pages built, script has {r['script_pages']}")
    if r['min_ppi'] < 300: problems.append(f"ch{r['chapter']}: minimum {r['min_ppi']} PPI")
Path(f'{stem}.json').write_text(json.dumps({'chapters': rows, 'problems': problems}, indent=1))

md = Path(f'{stem}-body.md').read_text()
table = ['| Ch | Pages | Folios | Images | Min PPI | Crossing tails left | PDF |', '|---|---|---|---|---|---|---|']
for r in rows:
    table.append(f"| {r['chapter']} | {r['pages']} | {r['first_folio']} to {r['last_folio']} | {r['images']} | {r['min_ppi']} | "
                 f"{', '.join(r['crossing_tails']) or 'none'} | `{r['pdf']}` |")
total_pages = sum(r['pages'] for r in rows)
md = md.replace('{{TABLE}}', '\n'.join(table)).replace('{{TOTAL_PAGES}}', str(total_pages)) \
       .replace('{{TOTAL_IMAGES}}', str(sum(r['images'] for r in rows))) \
       .replace('{{MIN_PPI}}', str(min(r['min_ppi'] for r in rows))) \
       .replace('{{CROSSINGS}}', str(sum(len(r['crossing_tails']) for r in rows))) \
       .replace('{{PROBLEMS}}', '; '.join(problems) or 'all pass. Folios run on without a gap, every chapter has its script\'s page count, and every image is at 300 PPI or more')
Path(f'{stem}.md').write_text(md)


def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)


out, i, lines = [], 0, md.splitlines()
while i < len(lines):
    l = lines[i]
    if l.startswith('|'):
        block = []
        while i < len(lines) and lines[i].startswith('|'):
            block.append([x.strip() for x in lines[i].strip('|').split('|')]); i += 1
        out.append('<div class="tw"><table><thead><tr>' + ''.join(f'<th>{inline(x)}</th>' for x in block[0]) + '</tr></thead><tbody>'
                   + ''.join('<tr>' + ''.join(f'<td>{inline(x)}</td>' for x in r) + '</tr>' for r in block[2:]) + '</tbody></table></div>')
        continue
    if l.startswith('- '):
        items = []
        while i < len(lines) and lines[i].startswith('- '):
            items.append(lines[i][2:]); i += 1
        out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'); continue
    m = re.match(r'^(#{1,3}) (.*)$', l)
    if m: out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>')
    elif l.strip(): out.append(f'<p>{inline(l)}</p>')
    i += 1
title = re.match(r'^# (.*)$', md, re.M)[1]
css = (':root{--bg:#faf7f0;--fg:#1d1b17;--muted:#6b645a;--card:#fff;--line:#ddd5c7;--accent:#9a4a1f}'
       '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#171513;--fg:#ece6da;--muted:#a59d90;--card:#211e1a;--line:#3a352e;--accent:#e08a5a}}'
       ':root[data-theme="dark"]{--bg:#171513;--fg:#ece6da;--muted:#a59d90;--card:#211e1a;--line:#3a352e;--accent:#e08a5a}'
       'body{background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif;margin:0;padding:24px 16px}main{max-width:980px;margin:0 auto}'
       'h1{font-size:1.7em}h2{color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:4px;margin-top:1.8em}h3{margin-top:1.4em}'
       'li{margin:.35em 0}code{font-size:.85em;word-break:break-all}.tw{overflow-x:auto}table{border-collapse:collapse;font-size:.88em;width:100%}'
       'th,td{border:1px solid var(--line);padding:4px 7px;text-align:left;vertical-align:top}th{background:var(--card)}')
Path(f'{stem}.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
                                f'content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{css}</style></head>'
                                f'<body><main>{"".join(out)}</main></body></html>')
print('pages', total_pages, '| problems:', problems or 'none')
