"""Build the web reader page from web-reader-template.html and manifest.json.

Run from output/comic-v15-digital after make_manifest.py and make_pages.py.
Writes web/index.html; the page images are web/images/*.jpg, published as pages/*.jpg
beside it (cover.jpg resized to 1000 px wide as pages/cover.jpg).
Labels and curly quotes come from make_epub.py, so both editions read the same.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from make_epub import curly, speaker_label  # noqa: E402

manifest = json.load(open("manifest.json"))
book = [{
    "n": c["chapter"],
    "title": curly(c["title"]),
    "pages": [{"i": p["image"], "s": p["side"][0],
               "t": [[speaker_label(l["speaker"]) or "", curly(l["text"])] for l in p["copy"]]}
              for p in c["pages"]],
} for c in manifest["chapters"]]
data = "window.BOOK=" + json.dumps(book, ensure_ascii=False, separators=(",", ":")) + ";"
template = open(os.path.join(os.path.dirname(__file__), "web-reader-template.html")).read()
os.makedirs("web", exist_ok=True)
# the published page serves the images as pages/; on disk they sit in web/images/
page = template.replace("/*BOOK*/", data).replace('"pages/', '"images/')
open("web/index.html", "w").write(page)
print("web/index.html")
