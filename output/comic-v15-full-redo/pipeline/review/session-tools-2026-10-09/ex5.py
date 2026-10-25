import sys, json, math
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
import run_chapter as r, reserves as rv, script_pipeline as s
exec(open('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/ex2.py').read().split("cap = {}")[0].split("import run_chapter as r, reserves as rv, script_pipeline as s")[1])
cap = {}
orig = rv.place_boxes
def spy(*a, **k):
    cap['a'] = a; cap['k'] = k
    return orig(*a, **k)
rv.place_boxes = spy
try: r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
except Exception: pass
a, k = cap['a'], cap['k']
bounds = a[1]['visible_rect']; tg = a[3]; pts = k['scale']; fcs = k['faces']
print('faces incl heads:', [f for f in fcs if str(f[3]).startswith('head')])
boxes = [[572, 0, 953, 179], [1258, 0, 1534, 323], [0, 368, 579, 500], [1035, 345, 1522, 470]]
corner = [.45, .45, None, .45]
for model in ('long', 'short'):
    print('== model', model)
    for i in range(4):
        if tg[i] is None or corner[i] is None: continue
        w = rv.tail_wedge(boxes[i], corner[i], tg[i], bounds, pts, rv.speaker_head(tg[i], fcs), model == 'short')
        L = w[3]; (bx, by), (tx, ty), half, _ = w
        d = math.hypot(tx-bx, ty-by)
        print(' chunk', i, 'base', (round(bx), round(by)), 'mouth', (round(tx), round(ty)), 'dist', round(d), 'len', round(L), 'half', round(half,1), 'head', rv.speaker_head(tg[i], fcs))
        for j in range(4):
            if j != i and rv.tail_crosses(w, boxes[j]): print('   CROSSES box', j, boxes[j])
        for f in fcs:
            if rv.tail_meets_face(w, f): print('   meets face', f[3])
