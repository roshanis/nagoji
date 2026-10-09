import sys, json, re
sys.path.insert(0, 'pipeline')
import script_pipeline as sp
from layout_fit import layout_cues
for ch in (10, 12):
    s = sp.parse_script(f'scripts/CHAPTER-{ch}-SCRIPT.md')
    d = json.load(open(f'scripts/CHAPTER-{ch}-ART-DIRECTION.json'))
    ov = json.load(open(f'scripts/CHAPTER-{ch}-CAST-OVERRIDES.json'))
    for page in s['pages'].values():
        for p in page['panels']:
            pid = p['id']
            solo = layout_cues(p)['solo']
            fr = d['panels'].get(pid, {}).get('frame')
            ns = d['not_shown'].get(pid)
            copytext = ' '.join(c['text'] for c in p['copy'])
            king = bool(re.search(r'\b(king|maharaja)\b', copytext, re.I))
            cment = sorted({k for k in sp.CAST_KEYS if sp._mentioned(copytext, k)} - set(ov[pid]))
            if solo or fr or ns or cment or king:
                print(ch, pid, 'solo' if solo else '', 'frame=',fr, 'ns=',ns, 'copy-ment=',cment, 'king-in-copy' if king else '', [c['speaker'] for c in p['copy']], 'cast', ov[pid])
