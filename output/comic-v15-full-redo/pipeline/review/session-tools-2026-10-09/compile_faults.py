"""Compile the author's list of accepted faults for the 2026-10-08/09 V15 work: forced picks (past the two-correction
stopping rule), identity faults accepted as notes, and hand retouches, each with chapter, panel, version and text.
Usage (from output/comic-v15-full-redo): compile_faults.py OUT.json   (never overwrites)"""
import glob, json, re, sys
from pathlib import Path
out = Path(sys.argv[1])
if out.exists(): sys.exit(f'{out} exists')
items = []
# 1. forced picks: selection decisions whose issues say so
for f in sorted(glob.glob('review-sheets/SELECT-ZONES-*-2026-10-08.json')):
    label = re.search(r'SELECT-ZONES-(.+?)-2026', f)[1]
    try: d = json.load(open(f))['result']
    except Exception: continue
    for sel in d.get('selections', []):
        for x in sel.get('decisions', []):
            iss = x.get('issues') or ''
            if x.get('pick') and re.search(r'forced pick|least.bad|past the (two-correction )?stopping rule', iss, re.I):
                items.append({'kind': 'forced pick', 'chapter': sel['chapter'], 'round': label, 'panel': x['id'], 'version': x['pick'],
                              'faults': iss, 'retouch_hint': x.get('correction', '')})
# 2. identity verification: retries left as interim picks, with what remained
for f in sorted(glob.glob('review-sheets/IDVERIFY-*-2026-10-08.json')):
    d = json.load(open(f))['result']
    for x in d['items']:
        if x['verdict'] == 'retry':
            items.append({'kind': 'identity residue', 'chapter': x['chapter'], 'round': Path(f).stem, 'panel': x['id'], 'package': x['package'],
                          'faults': (x['remaining'] or x['new_faults']), 'note': x.get('notes', '')})
# 3. retouches (provenance)
rec = json.load(open('review-sheets/HAND-RETOUCH-2026-10-08.json'))
for fr in rec['frames']:
    items.append({'kind': 'hand retouch', 'package': fr['package'], 'panel': fr['id'], 'version': fr['version'], 'source': fr['source'],
                  'faults': fr['what'], 'sha256': fr['sha256']})
res = {'date': '2026-10-09', 'about': 'Accepted faults and hand retouches from the 2026-10-08/09 V15 work (new sheets, identity audit and fixes, head-aware tails). Identity residues were later retouched where the residue was an ear bead or a brand emblem; see the hand retouch entries for the same panel.',
       'counts': {k: sum(1 for i in items if i['kind'] == k) for k in ('forced pick', 'identity residue', 'hand retouch')},
       'renumbering_done': 'The author approved CONTINUITY anchor renumbering after page splits on 2026-10-09; anchors were renumbered for chapters 15, 17, 20, 22, 24 and 28 (backups pipeline/review/CONTINUITY-pre-anchors-chNN-2026-10-09.md), and the approved-sheet spans for 17.10/17.11 and 28.12/28.13.2 (backups pipeline/review/APPROVED-SHEETS-pre-ch17-split and -ch28-split-2026-10-09.json).',
       'items': items}
out.open('x').write(json.dumps(res, indent=1, ensure_ascii=False))
print(out, res['counts'])
