"""Renumber a chapter's CONTINUITY.md row anchors ("| CH @start-end |", with or without leading spaces) through one or
more page-split id maps (split_pages.py idmap.json, oldest first). A page.panel follows its panel; a page-only start
goes to the new page of that page's first panel and a page-only end to the new page of its last panel; an open end stays
open. Only the anchor changes, never the row text. Backs up CONTINUITY.md first (never overwrites a backup).
Usage (from output/comic-v15-full-redo): renumber_anchors.py CH BACKUP_NAME IDMAP.json [IDMAP.json ...] [--dry-run]"""
import json, re, shutil, sys
from pathlib import Path
args = [a for a in sys.argv[1:] if a != '--dry-run']; dry = '--dry-run' in sys.argv
ch, backup, maps = int(args[0]), Path('pipeline/review') / args[1], [json.loads(Path(a).read_text()) for a in args[2:]]


def stage(ref, mp, end):
    """One map: 'P.N' or 'P' (as a start or an end) -> new text."""
    pages = {}
    for k in mp:
        m = re.fullmatch(r'page-(\d+)-panel-(\d+)', k); pages.setdefault(int(m[1]), []).append(int(m[2]))
    new = lambda p, n: tuple(int(x) for x in re.fullmatch(r'page-(\d+)-panel-(\d+)', mp[f'page-{p:02d}-panel-{n:02d}']).groups())
    if '.' in ref:
        p, n = map(int, ref.split('.')); q = new(p, n); return f'{q[0]}.{q[1]}'
    p = int(ref)
    if p not in pages: return ref
    n = max(pages[p]) if end else min(pages[p])
    return str(new(p, n)[0])


def renum(spec):
    m = re.fullmatch(r'(\d+(?:\.\d+)?)(?:(-)(\d+(?:\.\d+)?)?)?', spec)
    if not m: raise ValueError(f'unreadable anchor @{spec}')
    a, dash, b = m[1], m[2], m[3]
    for mp in maps:
        a = stage(a, mp, False)
        if b: b = stage(b, mp, True)
    return a + (dash or '') + (b or '')


src = Path('CONTINUITY.md'); text = src.read_text(); changes = []
def sub(m):
    old = m[2]; new = renum(old)
    if new != old: changes.append((old, new))
    return f'{m[1]}@{new} |'
out = re.sub(rf'^(\s*\| *{ch} )@([0-9.\-]+) \|', sub, text, flags=re.M)
print(f'chapter {ch}:', changes or 'no anchor changes')
if not dry and changes:
    if backup.exists(): sys.exit(f'{backup} exists')
    shutil.copyfile(src, backup); src.write_text(out); print('written; backup', backup)
