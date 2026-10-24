# Digital edition of the V15 graphic novel: items for the panel

Author's request (2026-10-20): "Can you start creating the digital comic", then "graphic novel". Shown the finished V15 print graphic novel, the author chose "Digital edition of V15" on a decision card: convert the finished V15 pages into a screen edition (fixed-layout EPUB plus a web reader), no blank print pages, lettering as text.

No manuscript text and no V15 art or lettering is changed. The edition is a repackaging of the 422 lettered V15 page renders (final builds listed in `output/comic-v15-full-redo/pipeline/review/V15-FINAL-BUILDS-2026-10-10.json` on git branch `claude/v15-comic-ch1-8`; scripts, CONTINUITY.md and the final report are on that branch under `output/comic-v15-full-redo/`). V15 follows the 1e post-build chapter files, not the 2e text; the author chose to build the digital edition from V15 as it stands.

## Files to look at (all under /mnt/project-files/graphic-novel-digital/)

- `review/epub-text/` the built EPUB with images left out: `OEBPS/content.opf`, `OEBPS/nav.xhtml`, `OEBPS/css/book.css`, `OEBPS/text/*.xhtml` (cover, title, rights, then ch01-p01 to ch28-p15). EPUBCheck 5.1.0: 0 errors, 0 warnings.
- `review/samples/` screen page images (web size, 1000 px wide; the EPUB uses the same crop at 1600 x 2311), `print-render-ch01-p01.png` (the V15 print render the crop comes from), `cover.jpg`, and `wide.png` / `phone.png` screenshots of the web reader.
- `review/web-reader-template.html` the web reader (the published page inlines `review/manifest.json`-derived data where the template says /*BOOK*/).
- `review/manifest.json` per page: image, print folio, print side, lettering from each final package's SCRIPT-SNAPSHOT.json.
- `tools/` the scripts: make_pages.py (crop and resize), make_manifest.py, make_cover.py, make_epub.py (speaker labels in `speaker_label`).

## Items

1. **Crop.** Every V15 render is 1838 x 2775 px with the same layout. The screen crop (112, 240, 1728, 2574) keeps the running chapter title and all panels with an even cream margin, and leaves out the bleed and the printed folio (page number), which would be wrong on screen once blank pages are dropped. Checked across all 422 pages: title starts at y 280, panels span x 148 to 1692 and end at y 2542, folio sits at y 2576 to 2606.
2. **Blank pages and spreads.** The 9 blank print pages (folios 16, 33, 56, 113, 138, 150, 243, 319, 394) are left out. Each page keeps its print side as `page-spread-left/right` in the EPUB spine, so readers that show two-page spreads keep the 43 page turns that land in print and the ch14 pages 3 and 4 facing pair; where two right-hand pages meet, the reading app supplies its own blank. The web reader pairs pages the same way in two-page mode and shows single pages on narrow screens.
3. **Provisional cover.** No V15 cover exists (the print plan calls for a separate wrap cover). The digital cover is a placeholder built from V15 frame ch11 page 21 panel 1 (Nagoji and Ibrahim on horseback on a ridge above the beach at sunset, ships offshore) with type: "BLOOD AND THRONES · BOOK ONE", "HORSE OF THE SERVANT", "A Graphic Novel", "RV MENON". Font: Cinzel Bold (OFL), italic line in Liberation Serif. It is marked provisional to the author.
4. **Title page and copyright page.** Text taken from `output/book-edition-v5/PUBLICATION-COPY.md` (author's earlier graphic-novel publication copy): title, subtitle "A Graphic Novel", series "Blood and Thrones, Book One", author "RV Menon"; copyright lines "Original novel copyright © 2025 RV Menon." and "Graphic novel edition copyright © 2026 RV Menon."; the rights paragraph; the AI-material scope line; the fiction line; the credit line "Based on the novel by RV Menon. Comic adaptation, dialogue revision, illustrations and lettering were developed with generative AI tools under the author's direction."; plus one new line, "Digital edition, reading proof." PUBLICATION-COPY.md itself notes ISBN and copyright registration are not done and the credit is "subject to the author's confirmation".
5. **Lettering as text for screen readers.** Each page file carries the page's captions and dialogue, in script order, in a visually hidden block linked to the image with aria-describedby; the image alt is "Chapter N, Title, page P." Speaker tags are turned into plain labels: CAPTION has no label (letters and palm-leaf captions are labelled "Letter" or "Written on the palm leaf"), LEAF and LEDGER become "Written on the palm leaf" and "Written in the ledger", names are title-cased (LANNOY and DE LANNOY both become "De Lannoy"), and lettering directions in parentheses are dropped except language and delivery that matter to a listener (in Marathi, in Malayalam, in Dutch, in Flemish, voice-over, memory, whispering). Pictures are not described yet; the accessibility summary says so.
6. **Web reader.** A private page on claude.ai that shows the same pages: chapter menu, page scrubber, tap or arrow or swipe to turn, two-page spreads on wide screens, and a "Text" drawer with the current page's captions and dialogue. Remembers the last page in the viewer's own browser.

## What the panel should not do

Do not review the V15 art, lettering or adaptation choices themselves (those went through their own V15 reviews and the author's approvals). Review only what this edition adds or changes.

## Correction to item 2

The scripts mark 43 page turns; 42 land in print and in this edition. The one that does not is Chapter 1, Dungeons of Goa, after page 4 (page 4 is a left page facing page 5, the interrogation room). The V15 final report records it as left "as you approved it"; the edition inherits it and does not change it. It is flagged to the author.

## Revisions applied after the first five verdicts (round 2)

EPUB (tools/make_epub.py, rebuilt; EPUBCheck 5.1.0 again 0 errors, 0 warnings; review/epub-text/ refreshed):
- UX 5: image no longer has aria-describedby; section no longer repeats the alt as aria-label. Lettering block stays in reading order (read once).
- Editing 5.1 / Story: script *asterisks* now render as <i> in the page text (no literal asterisks left in OEBPS/text).
- Editing 5.2: "letter" now matches only the word (CAPTION (stitched lettering) on ch20 p2 is now "Stitched on the cloth"; the ch20 2.5 direction shows the message stitched into a green cloth). "PADMINI (off, small lettering)" no longer becomes a letter.
- Editing 5.3: descriptive tags in sentence case ("Chief in gold chains", "Chief with hair stick", "Chief in white"); names stay title case. "GUARD 2" becomes "Second guard", "SAILOR 2" "Second sailor".
- Editing 5.4: "(inset, past)" maps to "memory".
- Design 4 / Editing 4: dc:rights now "Original novel copyright © 2025 RV Menon. Graphic novel edition copyright © 2026 RV Menon. All rights reserved in the copyrightable human-authored portions of this work."
- Design 4: title and copyright pages now use embedded fonts (Cinzel Bold for title, series and author; EB Garamond regular and italic for text; both SIL OFL 1.1, license files kept beside the build in output/comic-v15-digital/fonts/).
- Design 2a: page-list labels now use the print folios (1 to 431, skipping the blank folios), with pageBreakSource and printPageNumbers metadata, so a cited page number matches print.
- Editing 6: cover alt text is the same in both outputs: "Cover of Horse of the Servant, a graphic novel by RV Menon."

Web reader (review/web-reader-template.html; new screenshots review/samples/wide2.png, phone2.png, phone3.png):
- UX 6a: turn arrows visible at rest (opacity .35).
- UX 6b: the phone Text drawer has its own Previous page and Next page buttons, and swipe works on the drawer too.
- UX 6c: Space, arrows and Page keys no longer turn the page when a button has focus.
- UX 6d: drawer text is an aria-live polite region, so new lettering is announced after a turn.
- UX 6e / Design 6d: a Credits page (the same text as the EPUB copyright page, in EB Garamond and Cinzel) follows the cover as a left-hand page facing Chapter 1 page 1, as in the EPUB.
- Design 6c: page range reads "p 3 and 4", no dash.
- Editing 6: drawer note now reads "Turn the page to begin. Nagoji's narration is in italics; dialogue and written messages carry a label." Script italics show as italics in the drawer.
- Page total counts comic pages only (422).

Not changed, for the author to decide (no reviewer blocked):
- Phone legibility (UX 1, Design 6b): lettering is about 5 to 7 px on a 390 px phone; the Text drawer is the phone reading path. Tap-to-zoom could come later.
- Portuguese lines carry no language label (UX 5): the scripts do not tag Portuguese, and ch04 pages 3 and 4 mark Malayalam and Konkani by brackets at page level only (History 5). Adding labels would mean adding information the scripts do not record per line.
- Chaver label on ch22 p5 (Story 5): the transcript names him before Nagoji's recognition on p6. A neutral label would be new wording, so it is left for the author.
- "Digital edition, reading proof." stays on the copyright page until the author decides to release (UX 4).
- Cover is provisional; "A Graphic Novel" line is weak at thumbnail size (UX 3, Design 3).
- ch20 tag: script says REVATHI (voice-over), the lettered snapshot says REVATHI (off) (Editing 5.5). The edition follows what was lettered.
- Copyright text was taken from output/book-edition-v5/PUBLICATION-COPY.md on the author's Mac (not in git); its own status note says the credit is subject to the author's confirmation.

## Round 3 revisions (after the round 2 re-checks)

- Design 4: every text the edition writes now uses curly quotes and apostrophes (style sheet 9.4): chapter titles in nav, alt text and hidden headings, the transcript lines, the copyright page, and the web reader's menu, drawer and Credits page (function `curly` in make_epub.py; the web data is built with the same function). The V15 page art keeps its own lettering.
- Design 6: on the Credits and Chapter 1 page 1 spread, the chapter menu, footer and drawer heading now take their label from Chapter 1 page 1.
- Editing 5: one rule for labels. One-word tags are names and are capitalised; multi-word tags are roles in sentence case ("Drill master", "Old woman", "Wary fisherman", "Senior envoy", "Dutch scribe", "Nair chief"), keeping Nair, Rani and Dutch capitalised ("Second Nair", "Senior Rani"); true multi-word names are listed (De Lannoy, Karl August, Raza Khan, Van Imhoff, João).
- Editing 6: drawer note now "Captions are in italics; dialogue and written messages carry a label."
- EPUB rebuilt; EPUBCheck 5.1.0: 0 errors, 0 warnings. review/epub-text/ and review/samples/ refreshed. Web reader republished.

## Round 4 revisions (after the adversarial review)

Web reader only (review/web-reader-template.html; screenshot review/samples/wide3.png shows the ch3/ch4 spread):
- Adversarial 6a: the menu, footer and drawer now follow the page the reader went to. On a spread that crosses chapters the footer reads "Ch 3 p 10 and Ch 4 p 1", the menu stays on the chosen chapter, and the drawer gives each chapter its own heading. Checked in a browser: choosing chapter 4 in two-page view leaves the menu on 4.
- Adversarial 6b: the key guard now ignores only Space and Enter on a focused button, so arrow and Page keys keep turning pages after a click on an arrow (checked: click on › then ArrowRight moves on).
- Adversarial note: the page image area is no longer a live region while the Text drawer is open, so a turn is announced once.
EPUB unchanged from round 3.

## Round 5 revision

- UX and Adversarial 6: the Previous and Next buttons now sit in a wrapper around the page area only, so they never cover the Text drawer. Measured in a browser at 1400 px with the drawer open: Next button spans x 759 to 971, drawer starts at x 971. review/samples/wide3.png now shows the ch3 p10 and ch4 p1 spread with the drawer open: menu "4. The Fishermen of the Pepper Coast", footer "Ch 3 p 10 and Ch 4 p 1", drawer headings for Chapter 3 and Chapter 4.
