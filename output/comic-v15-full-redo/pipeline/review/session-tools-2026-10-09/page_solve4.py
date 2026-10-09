"""Diagnostic + proposal for a page fit-layout left unverified: each panel's lowest placing height at full and half width
(1 pt scan, seeded from the chunked fit's probe cache), then the fitter's candidate structures in its own rank order,
each checked against the page's real budget (story height minus the gutters) and, if it fits, given verified heights.
Usage: page_solve.py CH PKGDIR TAG DECISIONS PAGE FIT_REPORT CACHE_JSONL"""
import sys, json, os
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
ch, pkg, tag, dec, page, report, cache = sys.argv[1:8]
rc.UNPAINTED = True
out = rc.package(int(ch), Path(pkg)); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
C = Path(pkg).name
fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), rc.FACE_SCALE, script)
DROPS = json.loads(os.environ.get('DROPS', '{}'))         # {panel id: [face indices]} background faces a balloon may cover
for pid, idx in DROPS.items():
    inputs['faces'][pid] = [f for i, f in enumerate(inputs['faces'].get(pid, [])) if i not in idx]
STEP = int(os.environ.get('STEP', '1'))
KEEP_MAX = float(os.environ['KEEP_MAX']) if os.environ.get('KEEP_MAX') else None
probe = rc.SlotProbe(script, inputs, fd, keep_max=KEEP_MAX)
if Path(cache).exists() and not DROPS:
    for line in Path(cache).read_text().splitlines():
        try:
            k, v = json.loads(line); probe.cache[tuple(k)] = v
        except ValueError:
            pass
FULL, HALF = c.ART_WIDTH_PT, (c.ART_WIDTH_PT - c.GAP_PT) / 2
pg = script['pages'].get(int(page)) or script['pages'][str(page)]
ids = [p['id'] for p in pg['panels']]
ok = lambda pid, w, h: (not probe.probed(pid)) or probe.fits(pid, w, float(h))
def lowest(pid, w):
    return next((h for h in range(60, 421, STEP) if ok(pid, w, h)), None)
mins = {pid: (lowest(pid, FULL), lowest(pid, HALF)) for pid in ids}
print(f'{C} page {page} minimums (full, half):', {p[-8:]: m for p, m in mins.items()})
alts = json.loads(Path(report).read_text())['pages'][str(page)]['structure']['alternatives']
for alt in alts:
    g = alt['structure']; groups, i = [], 0
    for size in g: groups.append(ids[i:i + size]); i += size
    need = [max((mins[p][0 if len(gr) == 1 else 1] for p in gr), default=0) if all(mins[p][0 if len(gr) == 1 else 1] is not None for p in gr) else None for gr in groups]
    budget = c.STORY_HEIGHT_PT - c.GAP_PT * (len(groups) - 1)
    if None in need or sum(need) > budget:
        print('  ', g, 'needs', need, 'budget', budget, 'NOT FEASIBLE'); continue
    slack = budget - sum(need)
    for share in (1.0, 0.5, 0.0):                      # spread the slack in proportion, then half of it, then none
        hs = [n + slack * share * n / sum(need) for n in need]; hs[-1] = budget - sum(hs[:-1])
        hs = [round(h, 1) for h in hs]; hs[-1] = round(budget - sum(hs[:-1]), 1)
        verified = all(ok(p, FULL if len(gr) == 1 else HALF, hs[k]) for k, gr in enumerate(groups) for p in gr)
        if verified:
            entry = [hs[k] if len(gr) == 1 else [hs[k], hs[k]] for k, gr in enumerate(groups)]
            print('  ', g, 'FEASIBLE: needs', need, 'budget', budget, 'rows', entry, '| fitter fill', alt['min_fill'], alt['mean_fill'])
            break
    else:
        print('  ', g, 'needs', need, 'budget', budget, 'fits on minimums but no slack spread verified')
