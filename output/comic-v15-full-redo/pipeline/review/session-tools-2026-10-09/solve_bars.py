"""Fast page layout under the keep tolerance: every grouping of the page's panels into rows of one or two (reading
order), each panel's lowest placing height at full and half width (STEP pt scan, probe answers cached on disk), the
feasible groupings within the page budget (story height minus the gutters), and for the best of them (row heights
closest to the art's natural heights) slack spread toward those natural heights and every panel verified at its
final height. Writes OUT_DIR/page-NN.json with the rows. Does not replace fit-layout's ranking; it is the fallback for
pages fit-layout leaves unverified or cannot finish inside the time limit.
This version also keeps every panel's slot inside the shapes its cover crop can reach (reserves.cover_crop never keeps
less than MIN_KEEP of an axis nor less than the span of the faces, heads, tails and keep zones), so the compositor
draws no bars: the art fills at least FILL of its slot. FILL steps down from 0.98 until a layout verifies, so the
worst panel's fill is as high as the page allows (0.01 is the plain solve); the FILL used is recorded. Separate cache name from solve_page.py (the answers are the same, the file is shared).
Usage: solve_bars.py CH PKGDIR TAG DECISIONS PAGE OUT_DIR KEEP_MAX STEP"""
import sys, os, json, math, itertools
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c, reserves as rv, layout_fit as lf
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
panels_by_id = {p['id']: p for p in pg['panels']}
def aspect_range(pid):
    # the slot shapes (width / height) the planner's cover crop can reach, as drawn_geometry computes its crop
    fr = frames[pid]; W, H = fr['width'], fr['height']; copy = panels_by_id[pid].get('copy') or []
    found = rv.find_regions(Path(fr['path']), 0); art = found['visible_rect']
    faces = rc.parse_faces([{'x': x, 'y': y, 'r': r} for x, y, r in inputs['faces'].get(pid, [])], W, H)
    keep = [[x0 * W, y0 * H, x1 * W, y1 * H] for x0, y0, x1, y1 in (inputs.get('keep') or {}).get(pid, [])]
    if copy and probe.probed(pid):
        tails = rc.parse_tails(probe.tails[pid], copy, W, H)
        hold = rc._crop_keep(faces, rc.head_zones(tails, faces, art, H), tails, [], art, keep)
    else:
        hold = rc._crop_keep(faces, [], [], [], art, keep)
    x0, y0, x1, y1 = art; aw, ah = x1 - x0, y1 - y0
    cl = [[max(k[0], x0), max(k[1], y0), min(k[2], x1), min(k[3], y1)] for k in hold]
    cl = [k for k in cl if k[2] > k[0] and k[3] > k[1]]
    span_x = (max(k[2] for k in cl) - min(k[0] for k in cl)) if cl else 0
    span_y = (max(k[3] for k in cl) - min(k[1] for k in cl)) if cl else 0
    return max(rv.MIN_KEEP * aw, span_x) / ah, aw / max(rv.MIN_KEEP * ah, span_y)
arange = {pid: aspect_range(pid) for pid in ids}
cues = {p['id']: lf.layout_cues(p) for p in pg['panels']}          # script layout cues, as fit-layout reads them:
solo = {pid for pid, cue in cues.items() if cue['solo']}            # alone in its row ("full width", strip, tier)
cue_floor = {pid: lf.cue_floor_pt(cue['min_share']) for pid, cue in cues.items() if cue['min_share']}   # size cue floors
def hbounds(pid, w, fill):
    amin, amax = arange[pid]
    return w * fill / amax, w / (amin * fill)          # heights whose slot shape the crop reaches within FILL
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
result = {'page': str(page), 'mins': mins, 'aspect_range': arange, 'solo': sorted(solo), 'cue_floor': cue_floor, 'rows': None}
for RELAX in ('none', 'size floors', 'size floors and solo'):        # cues first; relaxed only if the page cannot hold them
    use_solo = RELAX != 'size floors and solo'; use_floor = RELAX == 'none'
    for FILL in (.98, .95, .9, .85, .8, .75, .7, .65, .6, .55, .5, .45, .4, .35, .3, 0.01):   # the worst panel's fill, raised as far as the page allows
        cands = []
        for g in groupings(len(ids)):
            groups, i = [], 0
            for size in g: groups.append(ids[i:i + size]); i += size
            wi = [0 if len(gr) == 1 else 1 for gr in groups]
            if any(mins[p][w] is None for gr, w in zip(groups, wi) for p in gr): continue
            if use_solo and any(len(gr) > 1 and any(p in solo for p in gr) for gr in groups): continue
            ws = [FULL if w == 0 else HALF for w in wi]
            lo = [max(max(mins[p][w] for p in gr), max(hbounds(p, W, FILL)[0] for p in gr), max((cue_floor.get(p, 0) if use_floor else 0) for p in gr)) for gr, w, W in zip(groups, wi, ws)]
            hi = [min(hbounds(p, W, FILL)[1] for p in gr) for gr, W in zip(groups, ws)]
            budget = c.STORY_HEIGHT_PT - c.GAP_PT * (len(groups) - 1)
            if any(l > h for l, h in zip(lo, hi)) or sum(lo) > budget or sum(hi) < budget: continue
            nat = [min(max(max(natural[p][w] for p in gr), l), h) for gr, w, l, h in zip(groups, wi, lo, hi)]
            cands.append((sum(abs(math.log(max(n, 1) / l)) for n, l in zip(nat, lo)), g, groups, wi, lo, hi, nat, budget))
        result.setdefault('feasible', {})[str(FILL)] = [c_[1] for c_ in cands]
        for score, g, groups, wi, lo, hi, nat, budget in sorted(cands, key=lambda c_: c_[0]):
            allocs = []
            # toward natural heights first, then up to each row's ceiling; several spreads (placement is not monotone)
            for share in (1.0, 0.6, 0.3, 0.0):
                hs = [l + share * (n - l) for l, n in zip(lo, nat)]
                room = budget - sum(hs)
                if room < 0:
                    scale = (budget - sum(lo)) / max(sum(h - l for h, l in zip(hs, lo)), 1e-9); hs = [l + (h - l) * scale for h, l in zip(hs, lo)]; room = 0
                cap = [h_ - x for h_, x in zip(hi, hs)]
                hs = [x + room * (cp / sum(cap)) if sum(cap) else x for x, cp in zip(hs, cap)]
                allocs.append(hs)
            slack = budget - sum(lo)                                # and each row's floor with the slack in one row or spread evenly
            for k in range(len(lo)):
                hs = list(lo); hs[k] = min(hi[k], lo[k] + slack); allocs.append(hs)
            allocs.append([min(h_, l + slack / len(lo)) for l, h_ in zip(lo, hi)])
            for hs in allocs:
                hs = [round(x, 1) for x in hs]; hs[-1] = round(budget - sum(hs[:-1]), 1)
                if any(x < l - .05 or x > h + .05 for x, l, h in zip(hs, lo, hi)): continue
                if all(ok(p, FULL if w == 0 else HALF, hs[k]) for k, (gr, w) in enumerate(zip(groups, wi)) for p in gr):
                    result['rows'] = [hs[k] if len(gr) == 1 else [hs[k], hs[k]] for k, gr in enumerate(groups)]
                    result['grouping'] = g; result['fill'] = FILL; result['relaxed'] = RELAX; break
            if result['rows']: break
        if result['rows']: break
    if result['rows']: break
(od / f'page-{int(page):02d}.json').write_text(json.dumps(result))
print(json.dumps({k: result[k] for k in ('page', 'rows', 'grouping', 'fill', 'relaxed') if k in result}), flush=True)
