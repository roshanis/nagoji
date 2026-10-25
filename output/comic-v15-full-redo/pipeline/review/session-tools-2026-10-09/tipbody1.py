import sys, math
from unittest import mock
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/')
import reserves as rv, test_reserves as T
from pathlib import Path
path = Path(S+'quiet.png'); T.quiet_frame(busy=()).save(path)
found = rv.find_regions(path, 0)
R=(.45,.4); SC=.3; B=[0,0,1200,600]
def tip(res, mouth, faces):
    w = rv.tail_wedge(res['boxes'][0], res['corner'][0], mouth, B, SC, rv.speaker_head(mouth, faces), res['short_tail'][0])
    return T.tip_of(w)
def on_body(p, f): return rv._on_body(p, f)
for K, V, mouth in [((820,330,40,'K'),(700,150,40,'V'),(820,345)), ((820,330,40,'K'),(720,120,40,'V'),(820,345)), ((820,330,40,'K'),(650,40,40,'V'),(820,345))]:
    faces=[K,V]
    with mock.patch.object(rv,'BODY_DEPTH',0):
        old = rv.place_boxes(path, found, [[(300,100)]], [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
    new = rv.place_boxes(path, found, [[(300,100)]], [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
    print(K, V)
    print('  old', old['boxes'], old['short_tail'], 'tip', [round(v) for v in tip(old, mouth, faces)], 'on V', on_body(tip(old,mouth,faces), V), 'on K', on_body(tip(old,mouth,faces), K))
    print('  new', new['boxes'], new['short_tail'], 'tip', [round(v) for v in tip(new, mouth, faces)], 'on V', on_body(tip(new,mouth,faces), V))
