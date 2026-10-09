"""Diagnostic + proposal: for one page and one row grouping, the exact (1 pt) lowest height each row places all its
panels at, then a slack-distributed set of heights verified panel by panel. Optional face drops: 'pid:i;j'."""
import sys, json, os
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, compositor as c
rc.UNPAINTED = True
ch, C, tag, dec, page, grouping = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], [int(x) for x in sys.argv[6].split(',')]
drops = dict((d.split(':')[0], [int(i) for i in d.split(':')[1].split(';')]) for d in sys.argv[7].split(',')) if len(sys.argv) > 7 and sys.argv[7] else {}
out = rc.package(ch, Path(f'chapters/{C}')); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
layout = json.loads(Path(os.environ.get('LAYOUT_FILE') or f'chapters/{C}/LAYOUT-fitted-{tag}.json').read_text())
fd = f'chapters/{C}/review/geometry-{tag}-a'
inputs = rc.fit_inputs(out, Path(f'chapters/{C}/SELECTION-INPUT-{tag}-a.json'), Path(dec), Path(fd), 1.0, script)
for pid, idx in drops.items():
    inputs['faces'][pid] = [f for i, f in enumerate(inputs['faces'].get(pid, [])) if i not in idx]
probe = rc.SlotProbe(script, inputs, fd)
pg = script['pages'].get(int(page)) or script['pages'][str(page)]
ids = [p['id'] for p in pg['panels']]
rows = layout['page_rows'][str(page)]; budget = sum(r[0] if isinstance(r, list) else r for r in rows)
FULL, HALF = c.ART_WIDTH_PT, (c.ART_WIDTH_PT - c.GAP_PT) / 2
groups, i = [], 0
for size in grouping: groups.append(ids[i:i + size]); i += size
budget = c.STORY_HEIGHT_PT - c.GAP_PT * (len(groups) - 1)          # rows plus a gutter between each fill the story height
def ok(pid, w, h): return (not probe.probed(pid)) or probe.fits(pid, w, h)
mins = []
for g in groups:
    w = FULL if len(g) == 1 else HALF
    h = next((h for h in range(60, 421) if all(ok(p, w, float(h)) for p in g)), None)
    mins.append(h)
print(f'{C} page {page} grouping {grouping} drops {drops}: row minimums {mins} total {sum(m or 9999 for m in mins)} budget {budget:.1f}')
if None in mins or sum(mins) > budget:
    print('   NOT FEASIBLE'); sys.exit()
slack = budget - sum(mins); heights = [m + slack * m / sum(mins) for m in mins]
for attempt in range(40):
    bad = [k for k, g in enumerate(groups) if not all(ok(p, FULL if len(g) == 1 else HALF, round(heights[k], 1)) for p in g)]
    if not bad: break
    # pull a failing row back towards its proven minimum, giving the difference to the others
    for k in bad:
        give = heights[k] - mins[k]; heights[k] = float(mins[k])
        others = [j for j in range(len(groups)) if j != k]
        for j in others: heights[j] += give / len(others)
heights = [round(h, 1) for h in heights]; heights[-1] = round(budget - sum(heights[:-1]), 1)
verified = {p: ok(p, FULL if len(g) == 1 else HALF, heights[k]) for k, g in enumerate(groups) for p in g}
entry = [heights[k] if len(g) == 1 else [heights[k], heights[k]] for k, g in enumerate(groups)]
print('   proposed rows', entry, 'sum', round(sum(heights), 1), 'verified', all(verified.values()), verified)
