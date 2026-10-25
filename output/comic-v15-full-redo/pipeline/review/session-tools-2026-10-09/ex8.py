import sys, time, json
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
if sys.argv[1]=='old':
    loader = SourceFileLoader('reserves', P+'reserves.py.backup-pre-2026-10-08')
    m = module_from_spec(spec_from_loader(loader.name, loader)); sys.modules['reserves']=m; loader.exec_module(m)
import run_chapter as r, reserves as rv, script_pipeline as s
exec(open('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/ex2.py').read().split("cap = {}")[0].split("import run_chapter as r, reserves as rv, script_pipeline as s")[1])
t=time.time()
try:
    plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
    print('PLACED', round(time.time()-t,1),'s')
except Exception as e:
    print('ERR', round(time.time()-t,1), 's', str(e)[:80])
