"""After split_pages.py: make every page intro's leading panel count match the page's panels, in place on the dry-run
copy of a chapter script (never the live script). Lists intros that name an inset the page no longer holds, for a hand fix.
Usage: fix_intros.py SCRIPT.md"""
import re, sys
NUM = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight'}
WORD = {v.lower(): k for k, v in NUM.items()}
p = sys.argv[1]; s = open(p).read()
blocks = re.split(r'(?=^## PAGE \d+$)', s, flags=re.M)
out, fixed, flags, left = [], 0, [], []
for b in blocks:
    m = re.match(r'## PAGE (\d+)\n\n(.*?)\n', b)
    if not m:
        out.append(b); continue
    page, intro = int(m[1]), m[2]
    n = len(re.findall(rf'^\*\*{page}\.\d+\*\*', b, re.M))
    w = re.match(r'([A-Z][a-z]+) panels', intro)
    if w and w[1].lower() in WORD and WORD[w[1].lower()] != n and n in NUM:
        new = NUM[n] + intro[len(w[1]):]
        b = b.replace(intro, new, 1); fixed += 1; intro = new
    if not w or WORD.get(intro.split()[0].lower()) != n:
        left.append((page, n, intro[:70]))
    if re.search(r'\binset\b', intro, re.I) and not re.search(rf'^\*\*{page}\.\d+\*\* Inset', b, re.M):
        flags.append((page, intro[:90]))
    out.append(b)
open(p, 'w').write(''.join(out))
print('intros fixed', fixed, '| still not matching:', left, '| intros naming an inset the page no longer holds:', flags)
