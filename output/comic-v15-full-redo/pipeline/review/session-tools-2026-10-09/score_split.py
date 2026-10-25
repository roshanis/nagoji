"""Score candidate page splits from solve_bars page files: each half's minimum height and fill (its panels' tallest crops at
full width against the 523.5 pt story height; 1.0 fills the page, lower leaves bars).
Usage: score_split.py CACHE_DIR P:K [P:K ...]"""
import json, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from suggest_splits import need, reach, BUDGET
for spec in sys.argv[2:]:
    p, k = map(int, spec.split(':'))
    j = json.load(open(f'{sys.argv[1]}/page-{p:02d}.json'))
    ids = sorted(j['mins']); mins = {x: tuple(v) for x, v in j['mins'].items()}; ar = j['aspect_range']
    a, b = ids[:k - 1], ids[k - 1:]
    na, nb = need(a, mins), need(b, mins)
    fa, fb = min(1, reach(a, ar) / BUDGET), min(1, reach(b, ar) / BUDGET)
    print(f"{spec}: halves {len(a)}+{len(b)} panels, need {na} and {nb} pt, fill {fa:.2f} and {fb:.2f}, page fill now {j.get('fill')}")
