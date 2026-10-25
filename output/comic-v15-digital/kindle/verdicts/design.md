## Graphic design reviewer: Kindle edition of the V15 graphic novel

1. REVISE: Cover A is the right choice, but its "A Graphic Novel" and "RV MENON" lines sit on mid-tone dust and are weak at full size and lost at thumbnail size; fix the bottom shade and type in make_kindle_cover.py (below) and re-render. EPUB cover page packaging is correct.
2. PASS: the line is removed cleanly; the four remaining paragraphs keep their block position (top 900 px) and still fit the 1600 x 2311 page. Wording still awaits the author's confirmation, as stated.
3. PASS: all nine blanks sit exactly where the items file says; I checked all 422 page-list entries and every odd print page is page-spread-right and every even one page-spread-left, with no side clashes in the 434-item spine. Blanks use the 1600 x 2311 viewport and the cream page background, carry no page-list entry, and the page-list skips their print numbers (for example 15, then 17). The ch 14 p3 and p4 spread is left then right, as it should be.
4. PASS WITH NOTE: book-type comic, fixed-layout true, original-resolution 1600x2311 and orientation-lock none are all present and unchanged. Holding Region Magnification is sound. original-resolution does not match the taller 1600 x 2560 cover page; that is normal for comics but check the cover in Kindle Previewer 3 (see notes).
5. REVISE: the series story does not agree across the four places a buyer sees it. The cover says "BLOOD AND THRONES · BOOK ONE", content.opf says belongs-to-collection "Blood and Thrones" group-position 1, the description ends "It is Book One of Blood and Thrones", but the pack advises against putting the book in the "Blood and Thrones" series and suggests "Blood and Thrones Graphic Novels". Pick one and make all four match (fix below). The rest of the pack is outside this lens; the description has no em or en dashes and no banned words.

## Notes

### Item 1: cover

Views checked: full size, 800 px, 160 px and 80 px wide, plus 100% crops of faces and the type areas.

Ranking: A, then C, then B.
- A (charge): best genre signal and the most energy at 160 px and 80 px; the title band reads cleanly at every size. Faults: (a) the lower type sits on light dust (mean luminance about 116 of 255 behind "A Graphic Novel", 121 behind the author), so gold on tan is low contrast; at 160 px "A Graphic Novel" is unreadable and "RV MENON" only just readable. (b) Crop: the blue rider's turban is cut by the right edge and a faceless blue Dutch back fills the lower left corner, which reads as a dark mass at thumbnail size.
- C (beach): the strongest single face at thumbnail size and bright sky gives good separation under the title. Faults: "A Graphic Novel" is laid straight over the horse's head and harness and is illegible; a second rider is cut to a sliver at the left edge, which looks like a mistake.
- B (ridge): the cleanest type, but about 40% of the cover is empty black, the figures are small and seen from behind, and at 80 px it reads as a dark, static cover. Weakest for a battle comic on a store page.
- Art when upscaled: at 100% the frames show the smooth, slightly waxy texture of upscaling but no blockiness or haloing; fine for Kindle and store display. No change needed.

Fixes for tools/make_kindle_cover.py (apply in crop mode; they help A and C):
1. Bottom shade. Replace the m2 loop (now from H-640, linear to 230) with a deeper, earlier ramp:
   for y in range(H - 900, H): d2.line([(0, y), (W, y)], fill=min(245, round(245 * (y - (H - 900)) / 600)))
   This puts about 175 of 255 dark behind "A Graphic Novel" (now about 62) and full 245 behind the author, while keeping the riders' upper bodies untouched.
2. Subtitle. "A Graphic Novel": size 76 to 88, colour gold (220, 178, 108) to light gold (238, 206, 150), position H - 470 unchanged.
3. Author. "RV MENON": size 96 to 120, y from H - 330 to H - 310. It is the second most important line on a store thumbnail and should be the largest type after the title.
4. Type edge. For the two lower lines, replace the hard 4/5 px offset shadow with a dark stroke so they hold over texture: draw.text((x, y), text, font=font, fill=fill, stroke_width=3, stroke_fill=(18, 12, 8)). Keep the offset shadow for the title if preferred.
5. Series line. 50 to 58 px. It will still not read at 160 px (normal for a series line) but gains at full size.
6. Crop for A. Re-run with cx at 0.53 to 0.56 and pick the value that brings the blue rider's whole turban inside the right edge while keeping Nagoji's face, his sword and the left rider's sword fully in frame; the foreground Dutch back should then take less of the lower left corner. Check at 160 px after the change.
Title sizes (158 and 210) and the dark title band (0 to 640 px with the 220 px fade) are good as they are. If C is chosen instead, also move the subtitle and author up to clear the horse's head or rely on fix 1 to darken it, and shift cx right to drop the sliver rider.

### Item 1: EPUB cover page
- cover.xhtml viewport 1600 x 2560 and body.cover height 2560 px are correct; spine uses rendition:page-spread-center so the cover stands alone, followed by title on the right. Valid EPUB 3 mixing of the prefixed center value with the unprefixed left and right values.
- Minor: the shared rule "html, body { height: 2311px; overflow: hidden }" still gives the cover's html element 2311 px. Most readers size from the viewport so the cover will not clip, but to be safe add class="cover" to the cover's html element and "html.cover { height: 2560px; }" in book.css.
- Check in Kindle Previewer 3 (desktop, not only the online previewer, given the 311 MB file) that the cover does not show twice (KDP's own cover plus the in-book cover page) and is not letterboxed against the 1600x2311 original-resolution. If it shows twice, drop the cover itemref from the spine and make the title page the first page.
- The Kindle epub-text snapshot omits the fonts folder that the digital snapshot has; the build copies the full source, and EPUBCheck passing means the fonts are in the EPUB. No action, but confirm before upload that fonts/ is in the final file.

### Item 5: series fix
Recommended: use the pack's "Blood and Thrones Graphic Novels" as the KDP series, number 1; change the OPF belongs-to-collection text to "Blood and Thrones Graphic Novels"; leave the cover line "BLOOD AND THRONES · BOOK ONE" (it names the story's place in the saga and is short enough to read); change the description's last sentence from "It is Book One of Blood and Thrones." to "It is the first graphic novel of Blood and Thrones." Alternatively leave the series blank in KDP and remove the belongs-to-collection block from the OPF. Either way the four should not contradict each other.

### Overall
Packaging is clean: spine pairing, page-list and spreads are exactly right. The only design work before upload is a cover re-render with the bottom shade and lower type fixes, and aligning the series name.
