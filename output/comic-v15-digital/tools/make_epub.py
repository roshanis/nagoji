"""Build the fixed-layout EPUB 3 screen edition of the V15 graphic novel.

Run from output/comic-v15-digital after make_pages.py and make_manifest.py,
with cover.jpg in this folder. Writes Horse-of-the-Servant-Graphic-Novel-digital.epub.

Each page is one image at 1600 x 2311 px. The print blank pages are left out;
every page keeps its print side (page-spread-left/right), so a reader that shows
two-page spreads puts the marked page turns where the print book has them and
supplies its own blank where two right-hand pages meet. The lettering of each
page is in the page file as text for screen readers.
"""
import datetime
import html
import json
import re
import uuid
import zipfile

W, H = 1600, 2311
TITLE = "Horse of the Servant"
SUBTITLE = "A Graphic Novel"
AUTHOR = "RV Menon"
OUT = "Horse-of-the-Servant-Graphic-Novel-digital.epub"
BOOK_ID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "nagoji/horse-of-the-servant/graphic-novel/v15/digital"))

KEEP = [
    (r"in marathi", "in Marathi"),
    (r"malayalam", "in Malayalam"),
    (r"in dutch", "in Dutch"),
    (r"flemish", "in Flemish"),
    (r"voice-over", "voice-over"),
    (r"memory", "memory"),
    (r"flashback", "memory"),
    (r"\bpast\b", "memory"),
    (r"whisper|under his breath", "whispering"),
]
NAMES = {"LANNOY": "De Lannoy", "DE LANNOY": "De Lannoy", "JOÃO": "João", "VAN IMHOFF": "Van Imhoff",
         "GUARD 2": "Second guard", "SAILOR 2": "Second sailor", "KARL AUGUST": "Karl August",
         "RAZA KHAN": "Raza Khan"}
PROPER = {"nair": "Nair", "rani": "Rani", "dutch": "Dutch"}


def speaker_label(tag):
    """'RAMAYYAN (whisper)' -> 'Ramayyan, whispering'; captions return a kind or None."""
    base, _, rest = tag.partition("(")
    base = base.strip()
    rest = rest.lower()
    if base == "CAPTION":
        if re.search(r"\bletter\b", rest):
            return "Letter"
        if "stitched" in rest:
            return "Stitched on the cloth"
        if "leaf" in rest:
            return "Written on the palm leaf"
        return None
    if base == "LEAF":
        return "Written on the palm leaf"
    if base == "LEDGER":
        return "Written in the ledger"
    words = base.split()
    if base in NAMES:
        name = NAMES[base]
    else:
        # one-word names are capitalised; multi-word tags are roles and take sentence case
        # ("CHIEF IN GOLD CHAINS" -> "Chief in gold chains"), keeping Nair, Rani and Dutch
        name = " ".join([words[0].capitalize()] + [PROPER.get(w.lower(), w.lower()) for w in words[1:]])
    notes = []
    for pattern, label in KEEP:
        if re.search(pattern, rest) and label not in notes:
            notes.append(label)
    return name + (", " + ", ".join(notes) if notes else "")


def curly(s):
    """Style sheet 9.4: curly quotes and apostrophes in all text this edition writes."""
    s = re.sub(r'(^|[\s(\[])"', "\\1\u201c", s)
    s = s.replace('"', "\u201d")
    s = re.sub(r"(^|[\s(\[])'", "\\1\u2018", s)
    return s.replace("'", "\u2019")


def esc(s):
    return html.escape(curly(s), quote=False).replace('"', "&quot;")


def lettering(s):
    """Escape a lettered line and turn the script's *italics* into <i>."""
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", esc(s))


def page_xhtml(title, body, css_class="page"):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<title>{esc(title)}</title>
<link rel="stylesheet" type="text/css" href="../css/book.css"/>
</head>
<body class="{css_class}">
{body}
</body>
</html>
"""


def comic_page(ch, page, chapter_title):
    pid = f"ch{ch:02d}-p{page['page']:02d}"
    lines = []
    for c in page["copy"]:
        label = speaker_label(c["speaker"])
        text = lettering(c["text"])
        lines.append(f"<p><b>{esc(label)}:</b> {text}</p>" if label else f"<p>{text}</p>")
    alt = f"Chapter {ch}, {chapter_title}, page {page['page']}."
    body = (
        f'<section epub:type="bodymatter chapter">\n'
        f'<img src="../images/{page["image"]}" alt="{esc(alt)}"/>\n'
        f'<div class="sr">\n' + "\n".join(lines) + "\n</div>\n</section>"
    )
    if page["page"] == 1:
        body = f'<h1 class="sr">Chapter {ch}: {esc(chapter_title)}</h1>\n' + body
    return pid, page_xhtml(f"{TITLE}, chapter {ch}, page {page['page']}", body)


CSS = f"""@font-face {{ font-family: "Cinzel"; font-weight: 700; src: url("../fonts/cinzel-700.woff") format("woff"); }}
@font-face {{ font-family: "EB Garamond"; font-style: normal; src: url("../fonts/eb-garamond-400.woff") format("woff"); }}
@font-face {{ font-family: "EB Garamond"; font-style: italic; src: url("../fonts/eb-garamond-400-italic.woff") format("woff"); }}
@page {{ margin: 0; }}
html, body {{ margin: 0; padding: 0; width: {W}px; height: {H}px; overflow: hidden; }}
body.page {{ background: #f7f0de; }}
body.page img {{ display: block; width: {W}px; height: {H}px; }}
body.cover {{ background: #140e0a; }}
body.cover img {{ display: block; width: {W}px; height: {H}px; }}
.sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
body.front {{ background: #f7f0de; color: #2a1d12; font-family: "EB Garamond", Georgia, serif; }}
.front .block {{ position: absolute; left: 180px; right: 180px; text-align: center; }}
.front h1, .front .series, .front .author {{ font-family: "Cinzel", Georgia, serif; font-weight: 700; }}
.front h1 {{ font-size: 120px; letter-spacing: 4px; margin: 0; line-height: 1.1; }}
.front .sub {{ font-size: 56px; font-style: italic; margin-top: 50px; }}
.front .series {{ font-size: 42px; letter-spacing: 6px; text-transform: uppercase; color: #7a5a2e; }}
.front .author {{ font-size: 72px; letter-spacing: 8px; text-transform: uppercase; }}
.front .rule {{ width: 300px; height: 4px; background: #7a5a2e; margin: 70px auto; }}
.front p {{ font-size: 38px; line-height: 1.5; margin: 0 0 34px 0; text-align: left; }}
"""


def front_pages():
    title = f"""<section epub:type="titlepage">
<div class="block" style="top: 380px;"><div class="series">Blood and Thrones · Book One</div></div>
<div class="block" style="top: 620px;"><h1>Horse of the Servant</h1><div class="sub">{SUBTITLE}</div><div class="rule"></div></div>
<div class="block" style="top: 1700px;"><div class="author">{AUTHOR}</div></div>
</section>"""
    rights = """<section epub:type="copyright-page">
<div class="block" style="top: 900px;">
<p>Original novel copyright © 2025 RV Menon.<br/>Graphic novel edition copyright © 2026 RV Menon.</p>
<p>All rights reserved in the copyrightable human-authored portions of this work. Except as permitted by applicable law, no copyright-protected portion may be reproduced, distributed or adapted without the copyright holder\u2019s written permission. No claim is made to material generated solely by artificial intelligence.</p>
<p>This is a work of historical fiction. Some characters, timelines and scenes are invented or compressed.</p>
<p>Based on the novel by RV Menon. Comic adaptation, dialogue revision, illustrations and lettering were developed with generative AI tools under the author\u2019s direction.</p>
<p>Digital edition, reading proof.</p>
</div>
</section>"""
    return [
        ("title", page_xhtml(TITLE, title, "front"), "right"),
        ("rights", page_xhtml("Copyright", rights, "front"), "left"),
    ]


def main():
    manifest = json.load(open("manifest.json"))
    chapters = manifest["chapters"]
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    items = []   # (id, href, media-type, properties)
    spine = []   # (idref, page-spread)
    files = {}   # path in OEBPS -> bytes or ('disk', path)
    nav_chapters = []
    page_list = []

    files["css/book.css"] = CSS.encode()
    items.append(("css", "css/book.css", "text/css", None))
    for i, (name, mime) in enumerate([("cinzel-700.woff", "font/woff"),
                                      ("eb-garamond-400.woff", "font/woff"),
                                      ("eb-garamond-400-italic.woff", "font/woff")]):
        files[f"fonts/{name}"] = ("disk", f"fonts/{name}")
        items.append((f"font{i}", f"fonts/{name}", mime, None))
    files["images/cover.jpg"] = ("disk", "cover.jpg")
    items.append(("cover-image", "images/cover.jpg", "image/jpeg", "cover-image"))
    cover_body = f'<section epub:type="cover"><img src="../images/cover.jpg" alt="Cover of {TITLE}, a graphic novel by {AUTHOR}."/></section>'
    files["text/cover.xhtml"] = page_xhtml("Cover", cover_body, "cover").encode()
    items.append(("cover", "text/cover.xhtml", "application/xhtml+xml", None))
    spine.append(("cover", "right"))

    for pid, xhtml, side in front_pages():
        files[f"text/{pid}.xhtml"] = xhtml.encode()
        items.append((pid, f"text/{pid}.xhtml", "application/xhtml+xml", None))
        spine.append((pid, side))

    n = 0
    for c in chapters:
        ch = c["chapter"]
        for page in c["pages"]:
            n += 1
            pid, xhtml = comic_page(ch, page, c["title"])
            files[f"text/{pid}.xhtml"] = xhtml.encode()
            files[f"images/{page['image']}"] = ("disk", f"epub/images/{page['image']}")
            items.append((pid, f"text/{pid}.xhtml", "application/xhtml+xml", None))
            items.append(("img-" + pid, f"images/{page['image']}", "image/jpeg", None))
            spine.append((pid, page["side"]))
            page_list.append((f"text/{pid}.xhtml", page["print_folio"]))
            if page["page"] == 1:
                nav_chapters.append((f"text/{pid}.xhtml", f"Chapter {ch}: {c['title']}"))

    toc = "\n".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in nav_chapters)
    plist = "\n".join(f'<li><a href="{h}">{n}</a></li>' for h, n in page_list)
    nav = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head><meta charset="UTF-8"/><title>Contents</title></head>
<body>
<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>
<li><a href="text/cover.xhtml">Cover</a></li>
<li><a href="text/title.xhtml">Title page</a></li>
{toc}
</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><ol>
<li><a epub:type="cover" href="text/cover.xhtml">Cover</a></li>
<li><a epub:type="bodymatter" href="{nav_chapters[0][0]}">Chapter 1</a></li>
</ol></nav>
<nav epub:type="page-list" hidden="hidden"><ol>
{plist}
</ol></nav>
</body>
</html>
"""
    files["nav.xhtml"] = nav.encode()
    items.append(("nav", "nav.xhtml", "application/xhtml+xml", "nav"))

    manifest_xml = "\n".join(
        f'<item id="{i}" href="{h}" media-type="{m}"' + (f' properties="{p}"' if p else "") + "/>"
        for i, h, m, p in items)
    spine_xml = "\n".join(
        f'<itemref idref="{i}" properties="page-spread-{s}"/>' for i, s in spine)
    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en"
  prefix="rendition: http://www.idpf.org/vocab/rendition/#">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
<dc:title id="t1">{TITLE}</dc:title>
<meta refines="#t1" property="title-type">main</meta>
<dc:title id="t2">{SUBTITLE}</dc:title>
<meta refines="#t2" property="title-type">subtitle</meta>
<dc:creator id="a1">{AUTHOR}</dc:creator>
<meta refines="#a1" property="role" scheme="marc:relators">aut</meta>
<dc:language>en</dc:language>
<dc:rights>Original novel copyright © 2025 RV Menon. Graphic novel edition copyright © 2026 RV Menon. All rights reserved in the copyrightable human-authored portions of this work.</dc:rights>
<dc:subject>Graphic novels</dc:subject>
<dc:subject>Historical fiction</dc:subject>
<meta property="belongs-to-collection" id="c1">Blood and Thrones</meta>
<meta refines="#c1" property="collection-type">series</meta>
<meta refines="#c1" property="group-position">1</meta>
<meta property="dcterms:modified">{now}</meta>
<meta property="pageBreakSource">Horse of the Servant, graphic novel, V15 print edition</meta>
<meta property="rendition:layout">pre-paginated</meta>
<meta property="rendition:orientation">auto</meta>
<meta property="rendition:spread">landscape</meta>
<meta name="cover" content="cover-image"/>
<meta name="fixed-layout" content="true"/>
<meta name="book-type" content="comic"/>
<meta name="original-resolution" content="{W}x{H}"/>
<meta name="primary-writing-mode" content="horizontal-lr"/>
<meta name="orientation-lock" content="none"/>
<meta property="schema:accessMode">visual</meta>
<meta property="schema:accessMode">textual</meta>
<meta property="schema:accessModeSufficient">visual</meta>
<meta property="schema:accessibilityFeature">tableOfContents</meta>
<meta property="schema:accessibilityFeature">readingOrder</meta>
<meta property="schema:accessibilityFeature">printPageNumbers</meta>
<meta property="schema:accessibilityHazard">none</meta>
<meta property="schema:accessibilitySummary">A fixed-layout graphic novel. Every page carries its captions and dialogue as text for screen readers. The pictures themselves are not yet described.</meta>
</metadata>
<manifest>
{manifest_xml}
</manifest>
<spine>
{spine_xml}
</spine>
</package>
"""
    container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""
    with zipfile.ZipFile(OUT, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        for path, data in files.items():
            if isinstance(data, tuple):
                z.write(data[1], "OEBPS/" + path, compress_type=zipfile.ZIP_STORED)
            else:
                z.writestr("OEBPS/" + path, data, compress_type=zipfile.ZIP_DEFLATED)
    print(OUT, n, "comic pages")


if __name__ == "__main__":
    main()
