"""Fast page layout under the keep tolerance: every grouping of the page's panels into rows of one or two (reading
order), each panel's lowest placing height at full and half width (STEP pt scan, probe answers cached on disk), the
feasible groupings within the page budget (story height minus the gutters), and for the best of them (row heights
closest to the art's natural heights) slack spread toward those natural heights and every panel verified at its
final height. Writes OUT_DIR/page-NN.json with the rows. Does not replace fit-layout's ranking; it is the fallback for
pages fit-layout leaves unverified or cannot finish inside the time limit.
Usage: solve_page.py CH PKGDIR TAG DECISIONS PAGE OUT_DIR KEEP_MAX STEP"""
import sys, os, json, math, itertools
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
ch, pkg, tag, dec, page, out_dir, kmax, step = sys.argv[1:9]
kmax = float(kmax) if kmax != 'none' else None; step = int(step)
rc.UNPAINTED = True
out = rc.package(int(ch), Path(pkg)); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
C = Path(pkg).name; fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), rc.FACE_SCALE, script)
probe = rc.SlotProbe(script, inputs, fd, keep_max=kmax)
od = Path(out_dir); od.mkdir(parents=True, exist_ok=True)
cache = od / f'page-{int(page):02d}-probe-cache.jsonl'
if cache.exists():
    for line in cache.read_text().splitlines():
        try:
            k, v = json.loads(line); probe.cache[tuple(k)] = v
        except ValueError:
            pass
log = cache.open('a')
def ok(pid, w, h):
    if not probe.probed(pid): return True
    key = (pid, round(w, 3), round(float(h), 3)); fresh = key not in probe.cache
    v = probe.fits(pid, w, float(h))
    if fresh: log.write(json.dumps([list(key), v]) + '\n'); log.flush()
    return v
FULL, HALF = c.ART_WIDTH_PT, (c.ART_WIDTH_PT - c.GAP_PT) / 2
pg = script['pages'].get(int(page)) or script['pages'][str(page)]
ids = [p['id'] for p in pg['panels']]
frames = inputs['frames']
natural = {pid: (FULL * frames[pid]['height'] / frames[pid]['width'], HALF * frames[pid]['height'] / frames[pid]['width']) for pid in ids}
REFINE = os.environ.get('REFINE') == '1'                          # then search 1 pt steps below each coarse minimum
def lowest(pid, w):
    h = next((h for h in range(60, 421, step) if ok(pid, w, h)), None)
    if h is not None and REFINE and h > 60:
        h = next((x for x in range(max(60, h - step + 1), h) if ok(pid, w, x)), h)
    return h
mins = {pid: (lowest(pid, FULL), lowest(pid, HALF)) for pid in ids}
def groupings(k):
    if k == 0: yield []; return
    for size in (1, 2):
        if size <= k:
            for rest in groupings(k - size): yield [size] + rest
cands = []
for g in groupings(len(ids)):
    groups, i = [], 0
    for size in g: groups.append(ids[i:i + size]); i += size
    wi = [0 if len(gr) == 1 else 1 for gr in groups]
    need = [max(mins[p][w] for p in gr) if all(mins[p][w] is not None for p in gr) else None for gr, w in zip(groups, wi)]
    budget = c.STORY_HEIGHT_PT - c.GAP_PT * (len(groups) - 1)
    if None in need or sum(need) > budget: continue
    nat = [max(natural[p][w] for p in gr) for gr, w in zip(groups, wi)]
    cands.append((sum(abs(math.log(max(n, 1) / nd)) for n, nd in zip(need, nat)), g, groups, wi, need, nat, budget))
result = {'page': str(page), 'mins': mins, 'feasible': [c_[1] for c_ in cands], 'rows': None}
for score, g, groups, wi, need, nat, budget in sorted(cands, key=lambda c_: c_[0]):
    slack = budget - sum(need)
    gap = [max(0.0, n - nd) for nd, n in zip(need, nat)]               # room each row has below its natural height
    allocs = [[slack * share * (x / sum(gap)) if sum(gap) else slack * share / len(need) for x in gap] for share in (1.0, 0.6, 0.3)]
    allocs += [[slack / len(need)] * len(need)]                        # placement is not monotone in height:
    allocs += [[slack if j == k else 0.0 for j in range(len(need))] for k in range(len(need))]   # try other spreads too
    for add in allocs:
        hs = [round(nd + a, 1) for nd, a in zip(need, add)]
        hs[-1] = round(budget - sum(hs[:-1]), 1)
        if hs[-1] < need[-1]: continue
        if all(ok(p, FULL if w == 0 else HALF, hs[k]) for k, (gr, w) in enumerate(zip(groups, wi)) for p in gr):
            result['rows'] = [hs[k] if len(gr) == 1 else [hs[k], hs[k]] for k, gr in enumerate(groups)]
            result['grouping'] = g; break
    if result['rows']: break
(od / f'page-{int(page):02d}.json').write_text(json.dumps(result))
print(json.dumps({k: result[k] for k in ('page', 'rows', 'grouping') if k in result}), flush=True)
