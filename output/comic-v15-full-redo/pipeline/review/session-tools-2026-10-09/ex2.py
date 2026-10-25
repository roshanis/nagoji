import sys, json, pickle
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline')
import run_chapter as r, reserves as rv, script_pipeline as s
pkg = r.V15 / 'chapters' / 'ch02'
decisions = json.loads((pkg / 'review' / 'LEAN-SELECTION-drawn-merged-d3.json').read_text())['decisions']
faces_file = json.loads((pkg / 'review' / 'FACES-v5.json').read_text())['panels']
keep_file = json.loads((pkg / 'review' / 'KEEP-c4.json').read_text())['panels']
script = s.parse_script(r.V15 / 'scripts' / 'CHAPTER-02-SCRIPT.md')
pid, version = 'page-05-panel-05', 'v10'
frame = pkg / 'frames' / f'{pid}-{version}.png'
panel = next(p for page in script['pages'].values() for p in page['panels'] if p['id'] == pid)
decision = next(d for d in decisions if d['id'] == pid)
tails = r.parse_tails({str(t['copy_index']): [t['x'], t['y']] for t in decision['tails']}, panel['copy'], 1536, 1024)
faces = r.parse_faces(next(p for p in faces_file if (p['id'], p['version']) == (pid, version))['faces'], 1536, 1024)
keep = r.parse_keep([{k: z[k] for k in ('x0', 'y0', 'x1', 'y1')} for z in next(p for p in keep_file if (p['id'], p['version']) == (pid, version))['keep']], 1536, 1024)
print(panel['copy'])
print('tails', tails)
print('faces', faces)
print('keep', keep)
cap = {}
orig = rv.place_boxes
def spy(*a, **k):
    cap['a'] = a; cap['k'] = k
    return orig(*a, **k)
rv.place_boxes = spy
try:
    plan = r.drawn_geometry(frame, panel['copy'], {'id': pid, 'rect_pt': [36, 56.25, 369, 194]}, tails, faces, keep=keep)
    print('PLACED', [x['rect'] for x in plan['reserves']])
except Exception as e:
    print('ERR', str(e)[:400])
a, k = cap['a'], cap['k']
print('bounds', a[1]['visible_rect'], 'regions', len(a[1]['regions']), [r_['bbox'] for r_ in a[1]['regions']])
print('targets', a[3])
print('scale', k['scale'], 'rounded', k['rounded'])
print('options0', a[2][0][:3], 'n', [len(o) for o in a[2]])


rv.place_boxes = orig
orig_pb = rv._place_boxes
def wrap(image_path, found, options, targets, tail_margin, rounded, bleed, faces, face_margin, widen, scale, keep, near, top=0.35, strict=True, avoid=None):
    try:
        res = orig_pb(image_path, found, options, targets, tail_margin, rounded, bleed, faces, face_margin, widen, scale, keep, near, top, strict, avoid)
        print('  OK strict=%s top=%s near=%s avoid=%s short=%s boxes=%s' % (strict, top, near, bool(avoid), res.get('short_tail'), res['boxes']))
        return res
    except rv.PlacementError as e:
        print('  FAIL strict=%s top=%s near=%s avoid=%s: %s' % (strict, top, near, avoid, str(e)[:110]), 'blocker', e.blocker)
        raise
rv._place_boxes = wrap
try:
    rv.place_boxes(*a, **k)
except Exception as e:
    print('FINAL', str(e)[:200])
