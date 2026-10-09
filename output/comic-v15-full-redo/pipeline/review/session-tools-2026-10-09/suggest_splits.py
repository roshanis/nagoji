"""List a chapter's pages that solve_bars left without rows, and rank each split point K (panels K.. to a new page) by a
height estimate: each half must fit its panels' minimum heights in the story height (523.5 pt, 2 pt gutters, a half-width
panel paired with its neighbour when both allow it) and should reach the story height at the art's tallest crop (fill).
A panel with no placing height at any width is reported separately: no split helps it.
Usage: suggest_splits.py CACHE_DIR [SCRIPT.md]   (with the script: also a RECOMMEND line of split specs that keep every
inset on its host's page, best fill first, then the most balanced halves)"""
import glob, json, re, sys
BUDGET, GAP, FULL = 523.5, 2.0, 369.0


def need(ids, mins):
    """Lowest total height of a run of panels: rows of one, or two neighbours that both allow half width."""
    best = [0.0] + [None] * len(ids)
    for i in range(1, len(ids) + 1):
        a = mins[ids[i - 1]]
        cands = []
        if a[0] is not None and best[i - 1] is not None: cands.append(best[i - 1] + a[0] + (GAP if i > 1 else 0))
        if i >= 2:
            b = mins[ids[i - 2]]
            if a[1] is not None and b[1] is not None and best[i - 2] is not None:
                cands.append(best[i - 2] + max(a[1], b[1]) + (GAP if i > 2 else 0))
        best[i] = min(cands) if cands else None
    return best[-1]


def reach(ids, ar):
    return sum(FULL / ar[p][0] for p in ids) + GAP * (len(ids) - 1)     # tallest full-width crops, all solo


def report(cache_dir):
    for f in sorted(glob.glob(cache_dir + '/page-??.json')):
        j = json.load(open(f))
        if j.get('rows'): continue
        ids = sorted(j['mins']); mins = {k: tuple(v) for k, v in j['mins'].items()}; ar = j['aspect_range']
        dead = [p for p in ids if mins[p][0] is None and mins[p][1] is None]
        print(f"page {j['page']}: needs {need(ids, mins)} pt of {BUDGET}; solo {j['solo']}" + (f"; NO PLACING HEIGHT: {dead}" if dead else ''))
        for k in range(2, len(ids) + 1):
            a, b = ids[:k - 1], ids[k - 1:]
            na, nb = need(a, mins), need(b, mins)
            if na is None or nb is None: continue
            fa, fb = min(1, reach(a, ar) / BUDGET), min(1, reach(b, ar) / BUDGET)
            ok = na <= BUDGET and nb <= BUDGET
            print(f"   split {j['page']}:{k}  first {na:.0f} pt (fill {fa:.2f})  second {nb:.0f} pt (fill {fb:.2f})  {'OK' if ok else 'too tall'}  score {min(fa, fb):.2f}")


def recommend(cache_dir, script_path):
    """One split spec per failing page: the best-scoring K that keeps every inset on its host's page, most balanced first.
    Returns (specs, pages with no solver result, pages with a panel that has no placing height)."""
    text = open(script_path).read()
    pages = {int(m[1]) for m in re.finditer(r'^## PAGE (\d+)$', text, re.M)}
    hosts = {}                                    # inset panel (page, n) -> host panel n on the same page
    for m in re.finditer(r'^\*\*(\d+)\.(\d+)\*\* Inset[^\n]*?set into (?:the [^\n]*? of )?(\d+)\.(\d+)', text, re.M):
        hosts[(int(m[1]), int(m[2]))] = int(m[4])
    solved = {int(json.load(open(f))['page']) for f in glob.glob(cache_dir + '/page-??.json')}
    specs, dead = [], []
    for f in sorted(glob.glob(cache_dir + '/page-??.json')):
        j = json.load(open(f))
        if j.get('rows'): continue
        p = int(j['page']); ids = sorted(j['mins']); mins = {k: tuple(v) for k, v in j['mins'].items()}; ar = j['aspect_range']
        if any(mins[x][0] is None and mins[x][1] is None for x in ids): dead.append(p); continue
        best = None
        for k in range(2, len(ids) + 1):
            if any((p, n) in hosts and (n >= k) != (hosts[(p, n)] >= k) for n in range(1, len(ids) + 1)): continue
            a, b = ids[:k - 1], ids[k - 1:]
            na, nb = need(a, mins), need(b, mins)
            if na is None or nb is None or na > BUDGET or nb > BUDGET: continue
            score = min(min(1, reach(a, ar) / BUDGET), min(1, reach(b, ar) / BUDGET))
            key = (round(score, 2), -abs(na - nb))
            if best is None or key > best[0]: best = (key, k)
        specs.append(f'{p}:{best[1]}' if best else f'{p}:?')
    return specs, sorted(pages - solved), dead


if __name__ == '__main__':
    report(sys.argv[1])
    if len(sys.argv) > 2:
        sp, missing, dead = recommend(sys.argv[1], sys.argv[2])
        print('RECOMMEND', ' '.join(sp), '| missing', missing, '| no placing height', dead)
