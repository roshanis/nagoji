"""Book imposition plan: which side each chapter opens on, the blank left-hand pages that put it there, and every
chapter's first folio, chosen so the scripts' marked page turns land. A "*Page turn.*" after page P wants P on a right-hand
(odd) page; "Pages A and B face each other" wants A on a left-hand (even) page. Chapter 1 opens on folio 1. Each chapter
opens on the side that satisfies most of its own markers (ties keep the side it would fall on anyway); a blank left-hand
page goes before a chapter whose natural side is the wrong one. Chapters without markers take whatever side they fall on.
Writes OUT.json {chapters: [{chapter, pages, first_folio, side, blank_before, markers, landing}], blanks: [folio], last_folio}.
Usage (from output/comic-v15-full-redo): imposition.py OUT.json"""
import json, re, sys
from pathlib import Path


def markers(ch):
    page, out = None, []
    for line in Path(f'scripts/CHAPTER-{ch:02d}-SCRIPT.md').read_text().splitlines():
        m = re.match(r'^## PAGE (\d+)', line)
        if m: page = int(m[1]); continue
        if page and re.fullmatch(r'\*Page turn\.\*', line.strip()): out.append(('turn after', page, 1))
        f = re.search(r'Pages (\d+) and (\d+) face each other', line)
        if f and page: out.append(('faces', int(f[1]), 0))
    return out          # (kind, page, wanted parity of that page's folio)


def pages(ch):
    return len(re.findall(r'^## PAGE \d+', Path(f'scripts/CHAPTER-{ch:02d}-SCRIPT.md').read_text(), re.M))


folio, rows, blanks = 1, [], []
for ch in range(1, 29):
    ms = markers(ch)
    score = lambda first: sum((first + p - 1) % 2 == want for _, p, want in ms)
    blank = False
    if ch > 1 and ms and score(folio + 1) > score(folio):
        blanks.append(folio); folio += 1; blank = True
    rows.append({'chapter': ch, 'pages': pages(ch), 'first_folio': folio, 'side': 'right' if folio % 2 else 'left',
                 'blank_before': blank, 'markers': [f'{k} {p}' for k, p, _ in ms],
                 'landing': sum((folio + p - 1) % 2 == w for _, p, w in ms)})
    folio += pages(ch)
plan = {'chapters': rows, 'blanks': blanks, 'last_folio': folio - 1,
        'markers': sum(len(r['markers']) for r in rows), 'landing': sum(r['landing'] for r in rows)}
Path(sys.argv[1]).write_text(json.dumps(plan, indent=1))
for r in rows:
    print(f"ch{r['chapter']:02d} {r['pages']:2d} pages, opens {r['side']:5s} at {r['first_folio']:3d}" + (' after a blank' if r['blank_before'] else '')
          + (f"  turns landing {r['landing']}/{len(r['markers'])}" if r['markers'] else ''))
print('blank pages at', blanks, '| last folio', folio - 1, '| markers landing', plan['landing'], 'of', plan['markers'])
