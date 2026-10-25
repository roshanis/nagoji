import sys, json
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
old=sys.argv[1]=='old'
if old:
    loader = SourceFileLoader('reserves', P+'reserves.py.backup-pre-2026-10-08')
    m = module_from_spec(spec_from_loader(loader.name, loader)); sys.modules['reserves']=m; loader.exec_module(m)
import run_chapter as r, reserves as rv, script_pipeline as s
exec(open('/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/ex2.py').read().split("cap = {}")[0].split("import run_chapter as r, reserves as rv, script_pipeline as s")[1])
orig_pb = rv._place_boxes
def wrap(image_path, found, options, targets, tail_margin, rounded, bleed, faces, face_margin, widen, scale, keep, near, top=0.35, strict=True, avoid=None):
    try:
        res = orig_pb(image_path, found, options, targets, tail_margin, rounded, bleed, faces, face_margin, widen, scale, keep, near, top, strict, avoid)
        print('  OK strict=%s top=%s near=%s avoid=%s short=%s boxes=%s' % (strict, top, near, bool(avoid), res.get('short_tail'), res['boxes']))
        return res
    except rv.PlacementError as e:
        print('  FAIL strict=%s top=%s near=%s avoid=%s: %s' % (strict, top, near, avoid, str(e)[:110]))
        raise
rv._place_boxes = wrap
plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
print('PLACED', [x['rect'] for x in plan['reserves']])
