import sys, math
from unittest import mock
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/')
import reserves as rv, test_reserves as T
from pathlib import Path
R=(.45,.4); SC=.3; B=[0,0,1200,600]
mouth=(660,250); N=(660,200,50,'Nagoji')
def run(p1, faces, label):
    path = Path(S+'t4.png'); T.frame(boxes=[(150,50,300,120), p1]).save(path)
    found = rv.find_regions(path, 2)
    try:
        res = rv.place_boxes(path, found, [[(150,60)],[(100,40)]], [mouth, None], faces=faces, scale=SC, tail_margin=12, rounded=[R, None])
        print(label, 'OK', res['boxes'], res['short_tail'], res['corner'])
        return res
    except rv.PlacementError as e:
        print(label, 'ERR', str(e)[:140])
for p1 in [(440,60,560,142), (450,70,570,140), (470,60,590,150)]:
    print('p1', p1)
    r0 = run(p1, [N], '  no Duarte')
    if r0:
        b=r0['boxes']; w_l=rv.tail_wedge(b[0], r0['corner'][0], mouth, B, SC, rv.speaker_head(mouth,[N]), False); w_s=rv.tail_wedge(b[0], r0['corner'][0], mouth, B, SC, None, True)
        print('   long crosses p1 box', rv.tail_crosses(w_l, b[1]), 'short', rv.tail_crosses(w_s, b[1]), 'tips', T.tip_of(w_l), T.tip_of(w_s))
    run(p1, [N, (380,250,40,'Duarte')], '  Duarte')
