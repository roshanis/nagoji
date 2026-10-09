"""Diagnostic: per panel, the lowest full- and half-width row height the planner places; then every grouping of the
page into rows of one or two (reading order) whose minimum heights fit the page's art height."""
import sys, json, itertools
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
rc.UNPAINTED = True
ch, C, tag, dec, pages = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], [int(x) for x in sys.argv[5].split(',')]
out = rc.package(ch, None); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
layout = json.loads(Path(f'chapters/{C}/LAYOUT-fitted-{tag}.json').read_text())
fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), 1.0, script)
probe = rc.SlotProbe(script, inputs, fd)
GAP = c.GAP_PT
FULL, HALF = c.ART_WIDTH_PT, (c.ART_WIDTH_PT - GAP) / 2
def lowest(pid, w):
    if not probe.probed(pid): return 60.0 if not probe.panels[pid]['copy'] else None
    return probe.first_fit(pid, w, 60.0, 420.0, 5.0)
for pg in pages:
    ids = [p['id'] for p in (script['pages'].get(pg) or script['pages'][str(pg)])['panels']]
    rows = layout['page_rows'][str(pg)]
    budget = sum(r[0] if isinstance(r, list) else r for r in rows)
    mins = {pid: (lowest(pid, FULL), lowest(pid, HALF)) for pid in ids}
    print(f'== {C} page {pg}: fitted rows {rows} (sum {budget:.1f})')
    for pid in ids: print(f'   {pid}: full {mins[pid][0]}  half {mins[pid][1]}  copy {[len(x["text"]) for x in probe.panels[pid]["copy"]]}')
    n = len(ids); found = []
    for cuts in itertools.product([1, 2], repeat=n):
        if sum(cuts) != n: continue
        pass
    def groupings(k):
        if k == 0: yield []; return
        for size in (1, 2):
            if size <= k:
                for rest in groupings(k - size): yield [size] + rest
    for g in groupings(n):
        i = 0; total = 0; ok = True; desc = []
        for size in g:
            members = ids[i:i + size]; i += size
            need = [mins[m][0 if size == 1 else 1] for m in members]
            if any(x is None for x in need): ok = False; break
            total += max(need); desc.append(max(need))
        if ok: found.append((total, g, desc))
    found.sort()
    print('   feasible groupings (row sizes, min heights, total vs budget):', [(g, d, t) for t, g, d in found if t <= budget + 0.1][:5] or 'NONE')
    print('   closest:', [(g, d, t) for t, g, d in found[:3]])
