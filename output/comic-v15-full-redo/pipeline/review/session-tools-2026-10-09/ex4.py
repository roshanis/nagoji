import sys, json
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
import run_chapter as r, reserves as rv, script_pipeline as s
exec(open('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/ex2.py').read().split("cap = {}")[0].split("import run_chapter as r, reserves as rv, script_pipeline as s")[1])
mode = sys.argv[1]
orig_tw = rv.tail_wedge
if mode == 'allshort':
    rv.tail_wedge = lambda box, ratio, target, bounds, scale=1.0, head=None, short=False: orig_tw(box, ratio, target, bounds, scale, head, True)
if len(sys.argv) > 2:
    rv.REPAIR_ROUNDS = int(sys.argv[2])
try:
    plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
    print('PLACED', [x['rect'] for x in plan['reserves']])
    print('short', plan.get('short_tail'))
except Exception as e:
    print('ERR', str(e)[:300])
