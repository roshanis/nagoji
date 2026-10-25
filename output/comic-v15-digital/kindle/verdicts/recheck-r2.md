# Round 2 re-check: Kindle edition of the V15 graphic novel

Re-checked for UX, graphic design, story, general editing and history, against the round-1 verdicts and the "Round 2 revisions" section of KINDLE-ITEMS.md. Files checked: KDP-UPLOAD-PACK.md, cover-drafts/A-charge.jpg and B-ridge.jpg (full size, 800, 160 and 80 px wide, 160 px greyscale), epub-text/OEBPS/content.opf, text/cover.xhtml, css/book.css, and the description against v15-panels.json.

Result: no REVISE or BLOCK remains. Every round-1 REVISE is resolved. Three small notes are below. None stops upload.

## User experience

1 (UX). PASS: The note about "A Graphic Novel" on busy art is resolved. The line now sits on a dark ramp. The background behind the line averages about 43 of 255, against about 116 in round 1. At 160 px wide it can now be read, and "RV MENON" reads clearly. At 80 px only the title and author read, which is fine. A still reads as a charge in greyscale.
2 (UX). PASS: no change since round 1.
3 (UX). PASS WITH NOTE: unchanged. The e-ink blank-page check is now in the pack's previewer row ("Kindle e-reader views").
4 (UX). PASS WITH NOTE: unchanged. The pack now asks for a phone panel check on ch 15 p1. The store page still promises no guided panel view. A splash page and the ch 14 p3 and p4 spread on a phone are not named in the pack, but they are optional.
5 (UX). PASS: "It ends at Colachel" is gone. Colachel is now the point where the war comes, and "What follows is harder" tells the buyer that half the book comes after the battle. The AI text disclosure now matches the copyright page. The series name is the same in the OPF and the pack. No em dashes, no banned word, nothing moving across a face.

## Graphic design

1 (design). PASS WITH NOTE: All the type fixes are in on A and B. The bottom shade starts higher and goes deeper. "A Graphic Novel" is in light gold with a dark stroke, "RV MENON" is larger with a stroke, and the series line is larger. Measured background behind the lower type on A: about 43 of 255 behind the subtitle and about 22 behind the author, so the light gold has roughly 9:1 contrast (round 1 was about 2:1). Crop: Dhanaji's whole turban is now inside the right edge, and the Dutch back in the lower left is smaller and has gone dark, so it no longer competes. Note: KINDLE-ITEMS says "both riders and both swords fully in frame". That is not quite true. Nagoji's lowered talwar in his left hand leaves the frame at the left edge, so only the hilt and part of the blade show. Dhanaji's horse's head is also clipped at the right edge. Both read as motion, not as crop mistakes, at every size I checked. Accept them, but correct the line in KINDLE-ITEMS. The cover page fix is correct: the cover's html element now has class="cover", and in book.css "html.cover, body.cover { height: 2560px; }" outranks the shared "html, body" rule (2311 px).
4 (design). PASS WITH NOTE: unchanged. The pack's previewer row now covers the "cover shows once" check. Before upload, confirm that the fonts folder is in the final EPUB (the epub-text snapshot still has no fonts or images folders).
5 (design). PASS: The series now agrees everywhere. KDP series "Blood and Thrones Graphic Novels", number 1. OPF belongs-to-collection "Blood and Thrones Graphic Novels", group-position 1. Description: "It is the first graphic novel of Blood and Thrones." The cover keeps "BLOOD AND THRONES · BOOK ONE", as recommended.

## Story editing

1 (story). PASS: C has been dropped (moved to cover-drafts/dropped/), so the spoiler of the burnt camp after the capitulation is gone. A and B are both honest and give nothing away. Note for the author: the EPUB's internal cover must match whichever cover is uploaded. If B is chosen, rebuild with B as images/cover.jpg (the pack says to upload "the same cover that is inside the EPUB").
4 (story). PASS WITH NOTE: unchanged. The pack names only ch 15 p1 for the phone check. The three layout-dependent beats from round 1 (ch 11 p9.4, ch 16 p21.2, ch 21 p10.5) are still worth paging through in the Previewer, but this is optional.
5 (story). PASS: Both fixes went in as suggested. The opening now uses the comic's own first beat. "A shrug, and an entry in a book." is verbatim from ch 1 p1.1 ("Not with ceremony or proclamation. A shrug, and an entry in a book."). The Colachel line no longer says the book ends there. Checked against v15-panels.json: "household horse" (ch 1 p1.2, ch 5 p7.2), "Captured by the Portuguese" (ch 5 p7.2 "Until the Portuguese netted me", ch 7 p10.4 Vasai), "useful stranger" (ch 4 p4.2, ch 6 p1.4, ch 8 p4.1), "old houses with long knives" (ch 22 p15.3 "whatever knives the old houses there had honed in the dark"), "letters from the north calling him home" (ch 19 p1.4 and p5.5, ch 25 p1.5), "a choice about whose man he is" (ch 19 p9.2 "Whose hands were they now?", ch 25 p15.4). Nothing past Colachel is spoiled: no De Lannoy, marriage, deaths or 1750.

## General editing

1 (editing). PASS: The contrast of "A Graphic Novel" is fixed (see design). The cover type is spelled and set the same on A and B and matches the title page and the KDP title and subtitle fields.
2 (editing). PASS WITH NOTE: unchanged. The author still needs to confirm the copyright page and credit wording, and the pack's checklist says so.
5 (editing). PASS: a, b, c, e, f, g, i, j and k are all in. a: the Colachel line is fixed. b: "ambitious king". c: "household horse". e: the audience question is now asked as KDP asks it (sexually explicit No, reading age 18+). f: AI text is declared plainly, matching the copyright page. g: $46, and the 70% plan's $2.99 to $9.99 limit. i: a category note says KDP's labels may differ, take the nearest match. j: the series matches everywhere. k: updates reach existing owners only on request to KDP support. h (keywords) was optional and is unchanged, which is acceptable. New copy is clean: 1,045 characters (limit 4,000), no em or en dashes (the only "---" strings are Markdown table rules), no banned word, nothing moving across a face, British "full-colour", $12.99 at 35% is about $4.55, correct. Small optional note: "Portuguese" now appears in paragraph 1 and paragraph 2 ("Captured by the Portuguese"). If the author wants it lighter, cut paragraph 2's first clause back to "Captured, he is shipped south in chains." Not required.

## History research

1 (history). PASS: no historical objection to A or B. C is dropped. No cover shows De Lannoy.
5 (history). PASS: Fix A is resolved (the book no longer "ends" at Colachel). Fix B is resolved: "a European company", as the Historical Note frames it, and the copy still avoids "first". "Captured at the edge of victory" is cut, and "Captured by the Portuguese" is supported by the comic (ch 5 p7.2, ch 7 p10.4). "Young" is gone. "Met" makes no claim about the outcome, so nothing conflicts with the Note. De Lannoy stays out of the description and keywords. The AI text disclosure now matches the copyright page and points the author to KDP's live guideline page before answering.

## Notes carried forward (none blocking)

- Correct the KINDLE-ITEMS round-2 line "both swords fully in frame". Nagoji's lowered talwar is cut by the left edge, and Dhanaji's horse's head is clipped at the right.
- If B is chosen, rebuild the EPUB with B as its internal cover.
- Confirm that fonts/ is in the final EPUB. Then do the Previewer checks listed in the pack: cover shows once, ch 14 spread, ch 15 p1 on phone, blank pages on e-ink.
