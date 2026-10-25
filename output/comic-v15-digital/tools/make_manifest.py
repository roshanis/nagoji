"""Collect chapter titles, page sides and lettering for the screen edition.

Run from output/comic-v15-full-redo. Writes ../comic-v15-digital/manifest.json.
The lettering comes from each final package's SCRIPT-SNAPSHOT.json, the script
text the V15 build checked every page against. The print side of each page comes
from the 2026-10-10 book plan, so readers that show two-page spreads keep the
page turns the print book was laid out for.
"""
import glob
import json
import os
import re

builds = json.load(open("pipeline/review/V15-FINAL-BUILDS-2026-10-10.json"))
plan = {c["chapter"]: c for c in json.load(open("pipeline/review/V15-IMPOSITION-2026-10-10.json"))["chapters"]}

chapters = []
for ch in range(1, 29):
    pkg, rev, _ = builds[str(ch)].split(":")
    snap = json.load(open(f"chapters/{pkg}/SCRIPT-SNAPSHOT.json"))["source"]
    renders = sorted(glob.glob(f"chapters/{pkg}/renders/{rev}/page-*.png"))
    assert snap["page_count"] == len(renders), (ch, snap["page_count"], len(renders))
    title = re.sub(r"^Chapter \d+:\s*", "", snap["title"])
    first = plan[ch]["first_folio"]
    pages = []
    for n in range(1, snap["page_count"] + 1):
        folio = first + n - 1
        lines = []
        for panel in snap["pages"][str(n)]["panels"]:
            for c in panel["copy"]:
                lines.append({"speaker": c["speaker"], "text": c["text"]})
        pages.append({
            "page": n,
            "image": f"ch{ch:02d}-p{n:02d}.jpg",
            "print_folio": folio,
            "side": "right" if folio % 2 else "left",
            "copy": lines,
        })
    chapters.append({"chapter": ch, "title": title, "pages": pages})

os.makedirs("../comic-v15-digital", exist_ok=True)
json.dump({"chapters": chapters}, open("../comic-v15-digital/manifest.json", "w"), ensure_ascii=False, indent=1)
print(sum(len(c["pages"]) for c in chapters), "pages")
speakers = {}
for c in chapters:
    for p in c["pages"]:
        for l in p["copy"]:
            speakers[l["speaker"]] = speakers.get(l["speaker"], 0) + 1
print(sorted(speakers.items(), key=lambda x: -x[1]))
