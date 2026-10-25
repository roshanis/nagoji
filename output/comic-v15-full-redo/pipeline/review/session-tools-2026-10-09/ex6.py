import sys, json, itertools
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
loader = SourceFileLoader('reserves', S+'reserves_x.py')
m = module_from_spec(spec_from_loader(loader.name, loader)); sys.modules['reserves']=m; loader.exec_module(m)
import run_chapter as r, reserves as rv, script_pipeline as s
exec(open(S+'ex2.py').read().split("cap = {}")[0].split("import run_chapter as r, reserves as rv, script_pipeline as s")[1])
for force in ([], [0], [1], [3], [0,1], [0,3], [1,3], [0,1,3]):
    rv.FORCE_SHORT = frozenset(force)
    try:
        plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
        print(force, 'PLACED', [x['rect'] for x in plan['reserves']])
    except Exception as e:
        print(force, 'ERR', str(e)[:100])
