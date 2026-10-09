"""Split selection args (make_select_args.py or round2_args.py output) into one text file per page, for the
file-driven selection workflow (v15-select-zones-file.js). Panels with no candidates are left out.
Usage: select_pages.py ARGS.json OUT_DIR  -> prints the workflow args JSON (chapter, pagesDir, pages, framesRoot)."""
import json, sys
from pathlib import Path
a = json.load(open(sys.argv[1])); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=False)
ch = a['chapter']; sheets = {s['key']: s['path'] for s in a['sheets']}
pages = []
for pg in a['pages']:
    lines, keys = [], set()
    for n, cast, versions in pg['panels']:
        if not versions: continue
        pid = f"page-{pg['page']:02d}-panel-{n}"
        keys |= {c for c in cast if c in sheets}
        frames = ' '.join(f"{v}={a['framesRoot']}{pid}-{v}.png" for v in versions)
        lines.append(f"{pid} (script {pg['page']}.{int(n)}); cast: [{', '.join(cast)}]; contact sheet: {a['sheetsRoot']}{pid}.png; "
                     f"candidates: {', '.join(versions)}; frames: {frames}; lettering lines (copy_index: speaker): {a['copy'].get(pid) or 'none'}")
    if not lines: continue
    sheet_lines = [f'{k}: {sheets[k]}' for k in sorted(keys)] or ['(no named principals on this page)']
    (out / f"page-{pg['page']:02d}.txt").write_text('CHARACTER SHEETS (Read the ones for each panel\'s cast):\n' + '\n'.join(sheet_lines)
                                                  + '\n\nPANELS:\n' + '\n'.join(lines) + '\n')
    pages.append({'page': pg['page'], 'panels': len(lines)})
print(json.dumps({'chapter': ch, 'pagesDir': str(out), 'framesRoot': a['framesRoot'], 'pages': pages}))
