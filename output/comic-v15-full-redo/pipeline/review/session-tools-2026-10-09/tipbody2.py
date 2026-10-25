import sys, math
from unittest import mock
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/')
import reserves as rv, test_reserves as T
from pathlib import Path
R=(.45,.4); SC=.3; B=[0,0,1200,600]
def run(region, size, faces, mouth, label, bodies=True):
    path = Path(S+'b.png'); T.frame(boxes=[region]).save(path)
    found = rv.find_regions(path, 1)
    try:
        if bodies: res = rv.place_boxes(path, found, [[size]], [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
        else:
            with mock.patch.object(rv, 'BODY_DEPTH', 0):
                res = rv.place_boxes(path, found, [[size]], [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
    except rv.PlacementError as e:
        print(label, 'FAIL', str(e)[:90]); return
    box, corner = res['boxes'][0], res['corner'][0]
    out = []
    for short in (False, True):
        w = rv.tail_wedge(box, corner, mouth, B, SC, rv.speaker_head(mouth, faces), short)
        tp = T.tip_of(w)
        out.append((round(tp[0]), round(tp[1]), [f[3] for f in faces if rv._on_body(tp, f)]))
    print(label, 'box', box, 'short_tail', res['short_tail'], 'long tip', out[0], 'short tip', out[1])
K=(820,330,40,'K'); MOUTH=(820,345)
run((150,280,450,360),(420,110),[K,(650,40,40,'V')],MOUTH,'orig t1 (bodies ignored)',False)
run((150,280,450,360),(420,110),[K,(650,40,40,'V')],MOUTH,'orig t1 (bodies)')
run((230,280,530,360),(300,80),[K,(650,40,40,'V')],MOUTH,'orig t2')
run((150,280,450,360),(420,110),[(640,330,40,'K'),(650,40,40,'V')],(640,345),'orig t3')
for V in [(740,40,40,'V'),(760,60,40,'V')]:
    run((150,280,450,360),(420,110),[K,V],MOUTH,'new t1 ign %s'%(V,),False)
    run((150,280,450,360),(420,110),[K,V],MOUTH,'new t1 %s'%(V,))
    run((300,280,600,360),(300,80),[K,V],MOUTH,'new t2 %s'%(V,))
print('---- t3 search')
for K, V, region, size, mouth in [((820,330,40,'K'),(780,100,40,'V'),(150,400,450,480),(420,100),(820,350)),
                                  ((820,330,40,'K'),(780,100,40,'V'),(150,420,450,500),(420,100),(820,355)),
                                  ((820,300,40,'K'),(790,60,40,'V'),(150,400,450,480),(420,100),(820,320)),
                                  ((820,300,40,'K'),(790,60,40,'V'),(300,400,600,480),(300,90),(820,320))]:
    print(K, V, region, mouth, 'K body y>=', K[1]+K[2], 'V body y<=', V[1]+8*V[2])
    run(region, size, [K,V], mouth, '   with bodies')
    run(region, size, [K,V], mouth, '   ignoring bodies', False)
