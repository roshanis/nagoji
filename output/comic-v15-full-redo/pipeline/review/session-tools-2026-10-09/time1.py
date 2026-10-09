import sys, json, time
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
old = sys.argv[1]=='old'
if old:
    loader = SourceFileLoader('reserves', P+'reserves.py.backup-pre-2026-10-08')
    m = module_from_spec(spec_from_loader(loader.name, loader)); sys.modules['reserves']=m; loader.exec_module(m)
import run_chapter as r, reserves as rv
import test_run_chapter as T
t = T.RealTallCoverTests('test_page_06_panel_03_in_a_184_5_pt_row_fits'); t.setUp()
# failing placement: page-01-panel-04-v01 at 109.7 pt; also a placing one
for stem, h in (('page-01-panel-04-v01', 109.7), ('page-06-panel-03-v03', 184.5), ('page-04-panel-05-v05', 120.0)):
    panel, frame, row, tails, faces = t.inputs(stem)
    slot = {'id': panel['id'], 'rect_pt': [36, 56.25, 369, h]}
    t0 = time.time()
    try:
        plan = r.drawn_geometry(frame, panel['copy'], slot, tails, faces)
        res = 'placed'
    except Exception as e:
        res = 'ERR ' + str(e)[:60]
    except KeyError as e:
        res = 'KeyError ' + str(e)
    print(sys.argv[1], stem, h, res, round(time.time()-t0, 2), 's')
