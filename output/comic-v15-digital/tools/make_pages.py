"""Make screen-edition page images from the V15 print renders.

Run from output/comic-v15-full-redo. Writes to ../comic-v15-digital/.
Usage: python3 make_pages.py FIRST_CHAPTER LAST_CHAPTER

Every V15 render is 1838 x 2775 px (6 x 9 in trim plus bleed, 300 PPI) with the
same layout: running title from y 280, panels x 148 to 1692 and down to y 2542,
print folio at y 2576 to 2606. The crop keeps the title and panels with an even
cream margin and leaves out the bleed and the print folio, which would be wrong
on screen once the blank print pages are dropped.
"""
import glob
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

CROP = (112, 240, 1728, 2574)  # 1616 x 2334
SIZES = {"epub": 1600, "web": 1000}
QUALITY = {"epub": 82, "web": 80}
OUT = "../comic-v15-digital"


def job(args):
    src, ch, page = args
    im = Image.open(src).convert("RGB")
    assert im.size == (1838, 2775), (src, im.size)
    im = im.crop(CROP)
    for kind, width in SIZES.items():
        height = round(im.size[1] * width / im.size[0])
        out = f"{OUT}/{kind}/images/ch{ch:02d}-p{page:02d}.jpg"
        im.resize((width, height), Image.LANCZOS).save(
            out, "JPEG", quality=QUALITY[kind], optimize=True, progressive=True,
            subsampling=2)
    return out


def main():
    first, last = int(sys.argv[1]), int(sys.argv[2])
    builds = json.load(open("pipeline/review/V15-FINAL-BUILDS-2026-10-10.json"))
    for kind in SIZES:
        os.makedirs(f"{OUT}/{kind}/images", exist_ok=True)
    jobs = []
    for ch in range(first, last + 1):
        pkg, rev, _ = builds[str(ch)].split(":")
        files = sorted(glob.glob(f"chapters/{pkg}/renders/{rev}/page-*.png"))
        for f in files:
            page = int(os.path.basename(f)[5:7])
            jobs.append((f, ch, page))
    with ProcessPoolExecutor(4) as pool:
        for out in pool.map(job, jobs):
            print(out)


if __name__ == "__main__":
    main()
