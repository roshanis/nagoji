import sys, json
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
loader = SourceFileLoader('reserves', S+'reserves_x.py')
m = module_from_spec(spec_from_loader(loader.name, loader)); sys.modules['reserves']=m; loader.exec_module(m)
import run_chapter as r, reserves as rv, script_pipeline as s
exec(open(S+'ex2.py').read().split("cap = {}")[0].split("import run_chapter as r, reserves as rv, script_pipeline as s")[1])
rv.DEBUG = True
rv.FORCE_SHORT = frozenset(int(x) for x in sys.argv[1].split(',') if x)
orig_pb = rv._place_boxes
n = [0]
def wrap(*a, **k):
    n[0] += 1
    if n[0] > int(sys.argv[2]): rv.DEBUG = False
    print('--- call', n[0], 'near', k.get('near'), 'strict', k.get('strict'), 'top', k.get('top'), 'avoid', bool(k.get('avoid')))
    return orig_pb(*a, **k)
rv._place_boxes = wrap
try:
    plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
    print('PLACED', [x['rect'] for x in plan['reserves']])
except Exception as e:
    print('ERR', str(e)[:100])
