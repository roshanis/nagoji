"""Dry run of one or more page splits in a chapter: each SPEC "P:K" moves panels K.. of page P to a new page P+1, and
every later page shifts by one. Writes the renumbered script, art direction and cast overrides, plus idmap.json, to
OUT_DIR (never the repo). CONTINUITY page anchors are not touched: check them by hand.
Usage: split_pages.py CH OUT_DIR P:K [P:K ...]   (specs in the ORIGINAL page numbering)"""
import json, re, sys
from pathlib import Path
V = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo')
ch, out = int(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
specs = sorted((int(a), int(b)) for a, b in (s.split(':') for s in sys.argv[3:]))
NUM = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight'}
split_at = dict(specs)


def newpn(p, n):
    shift = sum(1 for sp, _ in specs if sp < p)               # pages split before this one
    if p in split_at and n >= split_at[p]:
        return p + shift + 1, n - split_at[p] + 1
    return p + shift, n


def newid(i):
    m = re.fullmatch(r'page-(\d\d)-panel-(\d\d)', i); p, n = newpn(int(m[1]), int(m[2])); return f'page-{p:02d}-panel-{n:02d}'


src = (V / f'scripts/CHAPTER-{ch:02d}-SCRIPT.md').read_text()
labels = set(re.findall(r'^\*\*(\d+\.\d+)\*\*', src, re.M))
counts = {}
for lab in labels:
    p, n = map(int, lab.split('.')); counts[p] = max(counts.get(p, 0), n)
s = src
# 1. the split pages' intro counts, and the new page headers before panel K (original numbering, before renumbering)
for p, k in specs:
    head = re.search(rf'^## PAGE {p}\n\n(.*?)\n', s, re.M)
    assert head, f'no PAGE {p} intro'
    intro = head.group(1)
    first, kept, moved = NUM[counts[p]], k - 1, counts[p] - k + 1
    if intro.startswith(f'{first} panels.'):
        s = s.replace(intro, intro.replace(f'{first} panels.', f'{NUM[kept]} panels.', 1), 1)
    marker = f'\n**{p}.{k}**'
    assert s.count(marker) == 1, marker
    s = s.replace(marker, f'\n---\n\n## PAGE {p}+\n\n{NUM[moved]} panels, continuing page {p}.\n\n**{p}.{k}**', 1)
# 2. page headers, renumbered (the inserted ones carry a + until now)
def head_sub(m):
    p = int(m[1]); plus = m[2] == '+'
    shift = sum(1 for sp, _ in specs if sp < p)
    return f'## PAGE {p + shift + (1 if plus else 0)}'
s = re.sub(r'^## PAGE (\d+)(\+?)$', head_sub, s, flags=re.M)
# 3. every X.Y that is a panel label, anywhere in the text
log = []
def sub_label(m):
    if m[0] not in labels: return m[0]
    p, n = map(int, m[0].split('.')); q = newpn(p, n); new = f'{q[0]}.{q[1]}'
    if new != m[0]: log.append((m[0], new))
    return new
s = re.sub(r'(?<![\d.])(\d{1,2}\.\d)(?!\d|\.\d)', sub_label, s)
# 4. page references in prose to pages after a split
def sub_pages(m):
    words = m[0]
    out_ = re.sub(r'\b(\d+)\b', lambda k: str(int(k[1]) + sum(1 for sp, _ in specs if sp < int(k[1]))) if int(k[1]) in counts else k[1], words)
    if out_ != words: log.append((words, out_))
    return out_
s = re.sub(r'(?<![Cc]hapter )\b[Pp]ages? \d+(?:(?:, | and | to )\d+)*', sub_pages, s)
pages_before, pages_after = len(counts), len(counts) + len(specs)
s = re.sub(rf'\b{pages_before} pages, ', f'{pages_after} pages, ', s, count=1)
(out / f'CHAPTER-{ch:02d}-SCRIPT.md').write_text(s)
# art direction (chapters 1 to 8 have none: prompt profile v1)
adp = V / f'scripts/CHAPTER-{ch:02d}-ART-DIRECTION.json'
a = json.loads(adp.read_text()) if adp.exists() else None
if a is None: print('no art direction file; skipped')
if a is not None:
    newpages = {}
    for k_, v in a.get('pages', {}).items():
        p = int(k_); newpages[str(newpn(p, 1)[0])] = v
        if p in split_at: newpages[str(newpn(p, 99)[0])] = v
    a['pages'] = {k_: newpages[k_] for k_ in sorted(newpages, key=int)}
    for key in ('panels', 'not_shown'):
        if isinstance(a.get(key), dict):
            a[key] = {(newid(k_) if re.fullmatch(r'page-\d\d-panel-\d\d', k_) else k_): v for k_, v in a[key].items()}
    (out / f'CHAPTER-{ch:02d}-ART-DIRECTION.json').write_text(json.dumps(a, indent=2, ensure_ascii=False) + '\n')
raw = (V / f'scripts/CHAPTER-{ch:02d}-CAST-OVERRIDES.json').read_text(); c = json.loads(raw)
indent = 2 if raw.startswith('{\n  ') else (1 if raw.startswith('{\n ') else None)
(out / f'CHAPTER-{ch:02d}-CAST-OVERRIDES.json').write_text(json.dumps({newid(k_): v for k_, v in c.items()}, indent=indent, ensure_ascii=False) + '\n')
ids = {f'page-{p:02d}-panel-{n:02d}': newid(f'page-{p:02d}-panel-{n:02d}') for p, n in sorted(tuple(map(int, l.split('.'))) for l in labels)}
json.dump(ids, open(out / 'idmap.json', 'w'), indent=1)
from collections import Counter
print('pages', pages_before, '->', pages_after, '| substitutions', Counter(log).most_common(40))
