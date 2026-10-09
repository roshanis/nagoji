"""First folio of every V15 chapter from the final page counts (each chapter's live script, which the final packages
were built from), and which chapters' latest builds start on the wrong folio.
Usage (from output/comic-v15-full-redo): folios.py FINAL.json   (FINAL.json: {"1": "ch01-v2:r15", ...} package:revision
of the build to check; a chapter without one is only counted)"""
import json, re, sys
from pathlib import Path
final = json.loads(Path(sys.argv[1]).read_text())
folio, rows = 1, []
for ch in range(1, 29):
    pages = len(re.findall(r'^## PAGE \d+', Path(f'scripts/CHAPTER-{ch:02d}-SCRIPT.md').read_text(), re.M))
    built = None
    if str(ch) in final:
        pkg, rev = final[str(ch)].split(':')
        comp = json.loads((Path('chapters') / pkg / f'review/COMPOSITION-{rev}.json').read_text())
        built = min(p['folio'] for p in comp['placements'])
        nb = len({p['page'] for p in comp['placements']})
        if nb != pages: print(f'ch{ch}: build has {nb} pages, script {pages}')
    rows.append((ch, folio, pages, built))
    folio += pages
for ch, f, n, b in rows:
    print(f'ch{ch:02d} first_folio {f:3d} pages {n:2d}' + ('' if b is None else ('  ok' if b == f else f'  BUILT AT {b}: rebuild')))
print('last folio', folio - 1)
