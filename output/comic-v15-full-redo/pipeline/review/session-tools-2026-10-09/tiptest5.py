import sys, math
from unittest import mock
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/')
import reserves as rv, test_reserves as T
from pathlib import Path
R=(.45,.4); SC=.3; B=[0,0,1200,600]
mouth=(660,250); N=(660,200,50,'Nagoji')
path = Path(S+'t5.png'); T.frame(boxes=[(150,50,300,120)]).save(path)
found = rv.find_regions(path, 1)
def go(faces, sizes, lift=False):
    ctx = mock.patch.object(rv, 'RULES', tuple(k for k in rv.RULES if k != 'tip')) if lift else mock.patch.object(rv, 'RULES', rv.RULES)
    with ctx:
        try:
            res = rv.place_boxes(path, found, sizes, [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
        except rv.PlacementError as e:
            return 'ERR '+str(e)[:130]
    b=res['boxes'][0]
    out=[]
    for short in (False, True):
        w=rv.tail_wedge(b, res['corner'][0], mouth, B, SC, rv.speaker_head(mouth,faces), short); tp=T.tip_of(w)
        out.append((round(tp[0]),round(tp[1]),[f[3] for f in faces if rv._on_body(tp,f)]))
    return res['boxes'], res['choice'], res['short_tail'], out
for D in [(500,60,60,'Duarte'), (500,70,60,'Duarte'), (480,60,60,'Duarte')]:
    print(D, 'body x', D[0]-2*D[2], D[0]+2*D[2], 'y', D[1]+D[2], D[1]+8*D[2])
    print('  pinned rule  ', go([N,D], [[(150,60)]]))
    print('  pinned lifted', go([N,D], [[(150,60)]], True))
    print('  2 sizes rule ', go([N,D], [[(150,60),(300,100)]]))
print('plain', go([N,(380,250,40,'Duarte')], [[(150,60)]]), go([N,(380,250,40,'Duarte')], [[(150,60)]], True))
