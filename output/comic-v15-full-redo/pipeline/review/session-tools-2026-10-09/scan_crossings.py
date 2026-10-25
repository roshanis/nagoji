"""List panels of built V15 chapters whose drawn tails (as the compositor draws them) cross another speaker's tail.
Usage (from output/comic-v15-full-redo): scan_crossings.py PKG:REV:BTAG [...]"""
import json, sys, math
from pathlib import Path
sys.path.insert(0, 'pipeline')
import reserves as rv, compositor as c
total = 0
for spec in sys.argv[1:]:
    pkg, rev, btag = spec.split(':')
    p = Path('chapters') / pkg
    frames = {f['id']: f for f in json.loads((p / f'SELECTION-INPUT-{btag}.json').read_text())['frames']}
    places = {x['frame_id']: x for x in json.loads((p / f'review/COMPOSITION-{rev}.json').read_text())['placements']}
    hits = []
    for pid, fr in sorted(frames.items()):
        sp = [r for r in fr['reserves'] if r.get('draw') == 'speech' and r.get('tail')]
        if len(sp) < 2: continue
        scale = places[pid]['matrix'][0] / fr['width']
        w = [rv.tail_wedge(r['rect'], r.get('corner', c.BALLOON_RADIUS_RATIO), r['tail'], fr['visible_rect'], scale,
                           tuple(r['tail_head']) if r.get('tail_head') else None, bool(r.get('tail_short'))) for r in sp]
        for i in range(len(sp)):
            for j in range(i + 1, len(sp)):
                if w[i] and w[j] and math.dist(sp[i]['tail'], sp[j]['tail']) > rv.SAME_SPEAKER_PX and rv.tails_cross(w[i], w[j]):
                    hits.append(f"{pid[5:7]}.{pid[-2:]}"); break
            else: continue
            break
    total += len(hits)
    print(f'{pkg} {rev}: {len(hits)} crossing panels {hits}')
print('total', total)
