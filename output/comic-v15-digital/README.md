# V15 graphic novel: digital and Kindle editions (records and tools)

Published on Amazon Kindle in October 2026. This folder holds only the build tools and review records.
The page images, EPUB files, cover and page manifest stay on the author's Mac in the same path
(`output/comic-v15-digital/`), and are kept out of this public repository on purpose: the book's
pages and full lettering text must not be freely available online while it is sold on Kindle.

- `tools/`: make_pages, make_manifest, make_cover, make_epub, make_web (digital edition and web reader)
- `kindle/tools/`: make_kindle_epub, make_kindle_cover, detect_panels (Kindle build from the digital EPUB)
- `kindle/KDP-UPLOAD-PACK.md`: the KDP form answers used at upload
- `kindle/KINDLE-ITEMS.md`, `kindle/verdicts/`: Kindle review panel items and verdicts
- `review/`: digital edition review items and verdicts

The 2e sync records (V15 against the second edition text) are in `output/comic-v15-2e-sync/`.
Panel records for the manuscript and graphic novel reviews are in `review/panel-records/`.
The V15 print build records are on branch `claude/v15-comic-ch1-8` under `output/comic-v15-full-redo/`.
