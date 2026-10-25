"""Assemble fit_pages.py results into a layout and report exactly as run_chapter.structure_fit / fit_layout_command do.
Usage: fit_merge.py CH PKGDIR MANIFEST DECISIONS FACES_DIR LAYOUT_IN OUT_DIR LAYOUT_OUT REPORT_OUT"""
import sys, json
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, layout_fit as lf, compositor as c
ch, pkg, manifest, dec, faces_dir, layout_in, out_dir, layout_out, report_out = sys.argv[1:10]
rc.UNPAINTED = True
out = rc.package(int(ch), Path(pkg)); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
inputs = rc.fit_inputs(out, Path(manifest), Path(dec), Path(faces_dir), rc.FACE_SCALE, script)
page_rows, pages, probed, calls = {}, {}, {}, 0
for p in script['pages']:
    d = json.loads((Path(out_dir) / f'page-{int(p):02d}.json').read_text())
    page_rows[str(p)], pages[str(p)] = d['rows'], d['report']; calls += d['calls']
    for k0, k1, v in d['probed']: probed[(k0, tuple(k1))] = v
fitted = lf.assemble_structures(page_rows, pages, lf.MARGIN, lf.PROBE_TOP)
chosen = [probed[(page_no, tuple(page['structure']['chosen']))] for page_no, page in fitted['report']['pages'].items()]
merged = {'step_pt': rc.PROBE_STEP_PT, 'planner_calls': calls, 'rounds': max((f['rounds'] for f in chosen), default=0),
          'floors': {}, 'pins': {}, 'verified': {}, 'unplaceable': [], 'off_grid': [], 'unprobed': []}
for f in chosen:
    for k in ('floors', 'pins', 'verified'): merged[k].update(f[k])
    for k in ('unplaceable', 'off_grid', 'unprobed'): merged[k] += f[k]
for k in ('unplaceable', 'off_grid', 'unprobed'): merged[k].sort()
fitted['report']['probe'] = merged
source = {'layout': layout_in, 'layout_sha256': c.sha256(Path(layout_in)), 'manifest': manifest, 'margin': lf.MARGIN,
          'face_scale': rc.FACE_SCALE, 'structures': True, 'chunked': 'scratchpad fit_pages.py + fit_merge.py (run_chapter._structure_page per page)'}
import os
if os.environ.get('KEEP_MAX'): source['keep_max'] = float(os.environ['KEEP_MAX'])
if os.environ.get('MIXED'): source['pages_from'] = os.environ['MIXED']
lo = Path(layout_out)
if lo.exists(): raise SystemExit(f'layout file already exists: {lo}')
rc.write_json(lo, {'page_rows': fitted['page_rows'], 'fitted_from': source})
Path(report_out).write_text(json.dumps({'layout_out': str(lo), **fitted['report'], 'face_scale': rc.FACE_SCALE, 'sources': inputs['sources'],
    'faces': sorted(inputs['faces']), 'painted': sorted(inputs['painted']), 'keep': sorted(inputs['keep'])}, indent=1, default=str))
print('merged', len(page_rows), 'pages; planner calls', calls, '| unplaceable', merged['unplaceable'] or 'none')
