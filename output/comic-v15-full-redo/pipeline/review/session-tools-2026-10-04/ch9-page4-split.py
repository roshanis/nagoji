"""Dry run of the chapter 9 page 4 split: 4.1-4.3 stay, 4.4/4.5 -> 5.1/5.2, pages 5-11 -> 6-12.
Writes the renumbered script, art direction, cast overrides and CONTINUITY to $TMPDIR/ch9split/ (never the repo)."""
import json, re, os
from pathlib import Path
V = Path('/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo'); T = Path(os.environ['TMPDIR']) / 'ch9split'
def newpn(p, n):
    if p < 4 or (p == 4 and n <= 3): return p, n
    if p == 4: return 5, n - 3
    return p + 1, n
def newid(i):
    m = re.fullmatch(r'page-(\d\d)-panel-(\d\d)', i); p, n = newpn(int(m[1]), int(m[2])); return f'page-{p:02d}-panel-{n:02d}'
src = (V / 'scripts/CHAPTER-09-SCRIPT.md').read_text()
labels = set(re.findall(r'^\*\*(\d+\.\d+)\*\*', src, re.M))
log = []
# 1. page 4 intro and the new page 5 break before old 4.4
old_intro = 'Five panels. The first fencing. She tests his tongue, then his loyalty.'
assert src.count(old_intro) == 1
s = src.replace(old_intro, 'Three panels. The first fencing. She tests his tongue.')
assert s.count('\n**4.4**') == 1
# 2. page headers N>=5 -> N+1 (before inserting the new PAGE 5)
s = re.sub(r'^## PAGE (\d+)$', lambda m: f'## PAGE {int(m[1]) + 1 if int(m[1]) >= 5 else m[1]}', s, flags=re.M)
s = s.replace('\n**4.4**', '\n---\n\n## PAGE 5\n\nTwo panels. She tests his loyalty.\n\n**4.4**', 1)
# 3. every X.Y that is a chapter 9 panel label, anywhere in the text (labels, notes, change log)
def sub_label(m):
    if m[0] not in labels: return m[0]
    p, n = map(int, m[0].split('.')); q = newpn(p, n); new = f'{q[0]}.{q[1]}'
    if new != m[0]: log.append((m[0], new))
    return new
s = re.sub(r'(?<![\d.])(\d{1,2}\.\d)(?!\d|\.\d)', sub_label, s)
# 4. page references to this chapter's pages 5-11 in prose: "page N", "pages A, B and C", "Page N:"
def sub_pages(m):
    words = m[0]
    out = re.sub(r'\b(\d+)\b', lambda k: str(int(k[1]) + 1) if 5 <= int(k[1]) <= 11 else k[1], words)
    if out != words: log.append((words, out))
    return out
s = re.sub(r'(?<![Cc]hapter )\b[Pp]ages? \d+(?:(?:, | and | to )\d+)*', sub_pages, s)
# 5. the count in the header
old_pc = '- **Page count.** 11 pages against a target of 10 (range 8 to 12).'
assert s.count(old_pc) == 1
s = s.replace(old_pc, '- **Page count.** 12 pages against a target of 10 (range 8 to 12); page 4 was split in two on 2026-10-04 so that its lettering fits.')
old_turn = 'Turns are marked after pages 2, 9 and 11 only.'
assert s.count(old_turn) == 1, 'turn note'
s = s.replace(old_turn, old_turn + ' Since the page 4 split (2026-10-04), pages 9 and 11 fall on versos when page 1 is a verso, so those two turns now open onto a spread; restoring them needs an imposition change (author decision).')
assert s.count('11 pages, 53 panels.') == 1
s = s.replace('11 pages, 53 panels.', '12 pages, 53 panels.')
(T / 'CHAPTER-09-SCRIPT.md').write_text(s)
# art direction
a = json.loads((V / 'scripts/CHAPTER-09-ART-DIRECTION.json').read_text())
pages = a['pages']; newpages = {}
for k, v in pages.items():
    p = int(k)
    if p < 5: newpages[k] = v
    else: newpages[str(p + 1)] = v
newpages['5'] = pages['4']
a['pages'] = {str(k): newpages[str(k)] for k in sorted(map(int, newpages))}
for key in ('panels', 'character_notes', 'not_shown'):
    if isinstance(a.get(key), dict):
        a[key] = {(newid(k) if re.fullmatch(r'page-\d\d-panel-\d\d', k) else k): v for k, v in a[key].items()}
txt = json.dumps(a, indent=2, ensure_ascii=False)
assert not re.search(r'(?<![\d.])\d{1,2}\.\d(?![\d.])', json.dumps({k: a[k] for k in ('panels', 'character_notes', 'not_shown') if k in a})), 'X.Y text refs in art direction'
(T / 'CHAPTER-09-ART-DIRECTION.json').write_text(txt + '\n')
# cast overrides
raw = (V / 'scripts/CHAPTER-09-CAST-OVERRIDES.json').read_text(); c = json.loads(raw)
indent = 2 if raw.startswith('{\n  ') else (1 if raw.startswith('{\n ') else None)
(T / 'CHAPTER-09-CAST-OVERRIDES.json').write_text(json.dumps({newid(k): v for k, v in c.items()}, indent=indent, ensure_ascii=False) + '\n')
# CONTINUITY: the four approved anchors only
cont = (V / 'CONTINUITY.md').read_text()
for old, new in (('| 9 @2.4-5.1 |', '| 9 @2.4-6.1 |'), ('| 9 @5.2 |', '| 9 @6.2 |'), ('| 9 @5.3-10.5 |', '| 9 @6.3-11.5 |'), ('| 9 @11- |', '| 9 @12- |')):
    assert cont.count(old) == 1, old; cont = cont.replace(old, new)
(T / 'CONTINUITY.md').write_text(cont)
json.dump({f'page-{p:02d}-panel-{n:02d}': newid(f'page-{p:02d}-panel-{n:02d}') for p, n in sorted(tuple(map(int, l.split('.'))) for l in labels)}, open(T / 'idmap.json', 'w'), indent=1)
from collections import Counter
print('label/page substitutions:', Counter(log).most_common(80))
