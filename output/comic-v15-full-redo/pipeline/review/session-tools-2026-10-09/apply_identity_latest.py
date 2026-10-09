import re
from pathlib import Path

def latest(pkg):
    R = Path('chapters') / pkg / 'review'
    names = [p.name for p in R.glob('LEAN-SELECTION-drawn-*.json')]
    for kind, dpat, fpat, kpat in (('split', r'LEAN-SELECTION-drawn-split-r(\d+)\.json', 'FACES-s{}.json', 'KEEP-s{}.json'),
                                    ('merged', r'LEAN-SELECTION-drawn-merged-r(\d+)\.json', None, None),
                                    ('plain', r'LEAN-SELECTION-drawn-r(\d+)\.json', 'FACES-v{}.json', 'KEEP-c{}.json')):
        ns = sorted(int(m.group(1)) for n in names for m in [re.fullmatch(dpat, n)] if m)
        if not ns: continue
        n = ns[-1]
        if kind == 'merged':           # ch07: merged-r3 with FACES-v4 and KEEP-c5
            fn = max(int(m.group(1)) for p in R.glob('FACES-v*.json') for m in [re.fullmatch(r'FACES-v(\d+)\.json', p.name)] if m)
            kn = max(int(m.group(1)) for p in R.glob('KEEP-c*.json') for m in [re.fullmatch(r'KEEP-c(\d+)\.json', p.name)] if m)
            return (f'LEAN-SELECTION-drawn-merged-r{n}.json', f'FACES-v{fn}.json', f'KEEP-c{kn}.json',
                    f'LEAN-SELECTION-drawn-merged-r{n + 1}.json', f'FACES-v{fn + 1}.json', f'KEEP-c{kn + 1}.json')
        return (dpat.replace(r'(\d+)', str(n)).replace('\\', ''), fpat.format(n), kpat.format(n),
                dpat.replace(r'(\d+)', str(n + 1)).replace('\\', ''), fpat.format(n + 1), kpat.format(n + 1))
    raise SystemExit(f'{pkg}: no decisions file')

