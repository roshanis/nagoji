"""Kindle build of the V15 digital edition: starts from the checked digital EPUB and changes only
what KDP needs. Usage: src_dir cover.jpg out.epub
- cover page at KDP's 1600 x 2560, shown on its own (page-spread-center)
- "Digital edition, reading proof." removed from the copyright page
- a blank page wherever two right-hand or two left-hand pages would meet, so Kindle's
  two-page view keeps every page on its print side (KDP asks for matched spreads)"""
import sys, os, re, shutil, zipfile, datetime

src, cover, out = sys.argv[1:4]
work = out + '.d'
if os.path.exists(work): shutil.rmtree(work)
shutil.copytree(src, work)
O = os.path.join(work, 'OEBPS')

shutil.copy(cover, os.path.join(O, 'images', 'cover.jpg'))
p = os.path.join(O, 'text', 'cover.xhtml')
s = open(p, encoding='utf-8').read()
s = s.replace('width=1600, height=2311', 'width=1600, height=2560')
s = s.replace('<html xmlns=', '<html class="cover" xmlns=', 1)
open(p, 'w', encoding='utf-8').write(s)
p = os.path.join(O, 'css', 'book.css')
s = open(p, encoding='utf-8').read()
s = s.replace('body.cover img { display: block; width: 1600px; height: 2311px; }',
              'html.cover, body.cover { height: 2560px; }\nbody.cover img { display: block; width: 1600px; height: 2560px; }')
open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(O, 'text', 'rights.xhtml')
s = open(p, encoding='utf-8').read()
assert '<p>Digital edition, reading proof.</p>\n' in s
s = s.replace('<p>Digital edition, reading proof.</p>\n', '')
open(p, 'w', encoding='utf-8').write(s)

blank = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1600, height=2311"/>
<title>Blank page</title>
<link rel="stylesheet" type="text/css" href="../css/book.css"/>
</head>
<body class="page"></body>
</html>
'''
p = os.path.join(O, 'content.opf')
opf = open(p, encoding='utf-8').read()
# the graphic novel gets its own series on KDP, apart from the prose novels
assert '<meta property="belongs-to-collection" id="c1">Blood and Thrones</meta>' in opf
opf = opf.replace('<meta property="belongs-to-collection" id="c1">Blood and Thrones</meta>',
                  '<meta property="belongs-to-collection" id="c1">Blood and Thrones Graphic Novels</meta>')
opf = opf.replace('<itemref idref="cover" properties="page-spread-right"/>',
                  '<itemref idref="cover" properties="rendition:page-spread-center"/>')
refs = re.findall(r'<itemref idref="([^"]+)" properties="([^"]+)"/>', opf)
new, items, n, prev = [], [], 0, None
for idref, props in refs:
    side = 'left' if 'spread-left' in props else 'right' if 'spread-right' in props else None
    if side and prev == side:
        n += 1
        bid = 'blank-%02d' % n
        bside = 'right' if side == 'left' else 'left'
        open(os.path.join(O, 'text', bid + '.xhtml'), 'w', encoding='utf-8').write(blank)
        items.append('<item id="%s" href="text/%s.xhtml" media-type="application/xhtml+xml"/>' % (bid, bid))
        new.append('<itemref idref="%s" linear="yes" properties="page-spread-%s"/>' % (bid, bside))
    new.append('<itemref idref="%s" properties="%s"/>' % (idref, props))
    prev = side
spine_old = '\n'.join('<itemref idref="%s" properties="%s"/>' % r for r in refs)
assert spine_old in opf, 'spine layout changed'
opf = opf.replace(spine_old, '\n'.join(new))
opf = opf.replace('</manifest>', '\n'.join(items) + '\n</manifest>')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
opf = re.sub(r'<meta property="dcterms:modified">[^<]+</meta>', '<meta property="dcterms:modified">%s</meta>' % now, opf)
open(p, 'w', encoding='utf-8').write(opf)
print('blank pages added:', n)

if os.path.exists(out): os.remove(out)
with zipfile.ZipFile(out, 'w') as z:
    z.write(os.path.join(work, 'mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
    for root, dirs, files in os.walk(work):
        dirs.sort()
        for f in sorted(files):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, work)
            if rel == 'mimetype': continue
            z.write(full, rel, compress_type=zipfile.ZIP_STORED if f.endswith('.jpg') else zipfile.ZIP_DEFLATED)
print(out, os.path.getsize(out))
