import sys, json, re
sys.path.insert(0, 'pipeline')
import script_pipeline as sp
from layout_fit import layout_cues
s = sp.parse_script('scripts/CHAPTER-23-SCRIPT.md')
ov = json.load(open('scripts/CHAPTER-23-CAST-OVERRIDES.json'))
for page in s['pages'].values():
    for p in page['panels']:
        cast = set(ov[p['id']])
        d = p['description']
        ment = {k for k in sp.CAST_KEYS if sp._mentioned(d, k)}
        for pat, key in ((r'\b(?:the king|maharaja)\b', 'varma'), (r'\b(?:diwan|dalawa)\b', 'ramayyan')):
            if re.search(pat, d, re.I): ment.add(key)
        pron = bool(re.search(r'\b(?:him|his|he)\b', d, re.I)) and not (cast & sp.MALE_CAST)
        speakers = [c['speaker'] for c in p['copy']]
        copytext = ' '.join(c['text'] for c in p['copy'])
        cment = {k for k in sp.CAST_KEYS if sp._mentioned(copytext, k)}
        fp = bool(re.search(r"\b(my|i|me|we|us)\b", (d+' '+copytext).lower()))
        cues = layout_cues(p)
        tall = bool(re.search(r'^tall(?:er)?\b', d.strip(), re.I))
        print(p['id'], 'cast', sorted(cast), '| desc-missing', sorted(ment-cast), '| pron-needs-male' if pron else '', '| copy-ment', sorted(cment-cast), '| fp' if fp else '', '| spk', speakers, '| SOLO' if cues['solo'] else '', '| TALL' if tall else '')
