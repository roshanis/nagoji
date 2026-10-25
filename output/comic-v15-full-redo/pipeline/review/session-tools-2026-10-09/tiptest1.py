import sys, math, itertools
from unittest import mock
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/')
import reserves as rv, test_reserves as T
from pathlib import Path
R=(.45,.4); SC=.3; B=[0,0,1200,600]
path = Path(S+'tt.png'); T.frame(boxes=[(150,50,300,120)]).save(path)
found = rv.find_regions(path, 1)
def gaps(res, mouth, faces):
    w = rv.tail_wedge(res['boxes'][0], res['corner'][0], mouth, B, SC, rv.speaker_head(mouth, faces), res['short_tail'][0])
    tip = T.tip_of(w)
    return {f[3]: max(0.0, math.hypot(tip[0]-f[0], tip[1]-f[1]) - f[2]) for f in faces}, tip
def place(mouth, faces, sizes, lift=False):
    ctx = mock.patch.object(rv, 'RULES', tuple(k for k in rv.RULES if k != 'tip')) if lift else mock.patch.object(rv, 'RULES', rv.RULES)
    with ctx:
        return rv.place_boxes(path, found, sizes, [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
mouth = (660, 250)
nag = (660, 120, 50, 'Nagoji')     # does not hold the mouth: no head
hits = []
for dx in range(-260, 40, 10):
    for dy in range(-60, 100, 10):
        for rD in (30, 35, 40):
            duarte = (mouth[0] + dx, mouth[1] + dy, rD, 'Duarte')
            faces = [nag, duarte]
            try:
                old = place(mouth, faces, [[(300,100)]], True)
                new = place(mouth, faces, [[(300,100)]])
            except rv.PlacementError:
                continue
            go, to = gaps(old, mouth, faces); gn, tn = gaps(new, mouth, faces)
            if go['Duarte'] < go['Nagoji'] and gn['Nagoji'] <= gn['Duarte'] and old['boxes'] != new['boxes']:
                hits.append((duarte, old['boxes'][0], round(go['Duarte']), round(go['Nagoji']), new['boxes'][0], round(gn['Nagoji']), round(gn['Duarte']), new['short_tail']))
print(len(hits))
for h in hits[:20]: print(h)
