# Horse of the Servant V15: final build, 2026-10-10

All 28 chapters are built: {{TOTAL_PAGES}} story pages and {{TOTAL_IMAGES}} placed images, the lowest at {{MIN_PPI}} PPI. With the blank pages of the book plan below, the book runs to folio {{LAST_FOLIO}}. Checks across the whole book: {{PROBLEMS}}.

## Your answers of 2026-10-10, done

- **"(voice-over)" is fine.** ch16 6.3 and ch20 9.2 (Revathi) and ch25 11.1 (Nagoji) now read "(voice-over)" in the scripts, so those lines are lettered as tailless boxes in the speaker's balloon style. Ramayyan's reply in ch25 11.1 keeps its "(off)" tail to the edge. Scripts backed up as `scripts/CHAPTER-NN-SCRIPT.md.backup-pre-voiceover-2026-10-10`; each package records the accepted change.
- **Spreads: done as below.** Every marked page turn was checked against the final folios; 43 of the 44 now land on the right side of the spread.
- **Shown: the chapter 21 leaf lettering and ch28 10.1.** The close-ups also caught one fault, now fixed: in ch21 13.2 the LEAF line ("Sawant, Nagoji.") had landed on the ledger page under the LEDGER line; each write zone now names the one line it holds, so the LEDGER line sits on the ledger page and the LEAF line on the palm leaf.

## The book

{{TABLE}}

## Page turns and spreads

Of the page turns the scripts mark, {{TURNS}} now land. A "*Page turn.*" after page P wants page P on a right-hand page, so the next page's reveal stays hidden until the reader turns; chapter 14 also asks for pages 3 and 4 to face each other. Two things put them back on the right side after the splits:

- **Each chapter opens on the side its turns need,** with a blank left-hand page before it where the running page count would put it on the wrong side, as books do for chapter openings. Blank pages at folios {{BLANKS}}. Chapters with no marked turns take whatever side they fall on.
- **One extra page break in five chapters whose own turns pulled in opposite directions,** each at the most natural break a reader judged in the allowed pages, and each checked so both halves still fill the page: ch7 page 7 before panel 3, ch14 page 7 before panel 3, ch16 page 9 before panel 5, ch24 pages 15, 19 and 33 before panel 3, ch25 page 12 before panel 3. A second reader then checked every new break on the built pages: all read naturally. For ch7 an alternative break (page 5 before panel 4) was also built and compared; it left the old page 7 with small panels floating in large bars, so the first break was kept. Its new page 8 still shows two modest gaps around the shallow afternoon-wheel panel.
- Every turn was verified against the folio actually printed in each final build.
- The one turn left on the wrong side is in chapter 1 (after page 4); fixing it would mean re-cutting chapter 1 with two more breaks, so it stays as you approved it.

{{IMPOSITION}}

Notes in the scripts that predate the splits (for example chapter 14's "Start this chapter on a right-hand page") describe the old numbering; the plan above follows the marked turns themselves.

## What was fixed (2026-10-09 and 10)

- **Varma drawn like Nagoji.** Tails-and-identity reviews read every speech balloon in all 28 chapters against the approved sheets. 14 panels where Varma read like Nagoji were redrawn with his sheet attached, composition kept: ch10 12.5; ch11 3.5, 4.5, 17.2; ch15 10.1; ch16 13.3; ch22 10.4, 11.4, 11.5, 13.1, 13.3; ch23 1.5, 22.2; ch28 10.1.
- **Tails pointing at the wrong person.** The placer now keeps two speakers' tails from crossing wherever another layout exists, without covering story-critical art; ch6 11.5, ch20 14.3 and ch20 15.2 (Revathi's tail now reaches her) had their zone or tail data fixed. The crossings that remain are listed in the book table; each panel has no other layout in its free space.
- **Pages that did not fit** were split under the standing rule; CONTINUITY anchors and the approved-sheet page spans were renumbered under your 2026-10-09 approval (backups in `pipeline/review/`).
- **Chapter 21:** LEAF and LEDGER lines lettered on the leaves' blank bands (sepia ink on a soft leaf-tone wash, no outline, no tail); 5.3 regenerated as a 3:2 frame so its narration sits on the lattice.
- **Pipeline (all test-first; 633 tests pass):** tailless voice-over and memory boxes; no-crossing tails; the inscribed style and write zones, now with per-line zones; accepted delivery-tag changes ("(off)" to "(voice-over)") that carry through later splits; the PDF check reads full-page images.

## Still open, for you

- Tails correct but ending near another man's hair because the speaker leans in behind him: ch6 2.3 and ch15 3.2. In ch7 11.4 Nagoji's "Kayal." tail ends on the horse's forelock, since his brow is pressed to the horse; his next balloon points clearly to his mouth.
- ch7 page 8: two modest gaps around the afternoon-wheel panel (its art is a wide strip). ch25 12.2: Ramayyan's "Perhaps he wanted to give you the chance" balloon wraps to one or two words per line against the edge.
- Script housekeeping: a few page intros and adaptation notes still describe the old page numbers after the splits (for example ch24's "End on the title question" now belongs to page 36, and ch25's notes cite ch24 panel numbers from before ch24's split). They do not affect the art or lettering.
- The forced crossing tails in the book table.
- About 100 milder Varma drift notes from the identity audit (a slightly fuller moustache, a loose lock), none judged to read as Nagoji; ch28 10.1's redrawn moustache is still a little full.
- Earlier accepted notes: Varma's knot at the back of the head in many panels; ch12 7.3 loose hair; ch16 1.2 and ch19 12.1 brand on the outer forearm; ch20 15.4 keep zones relaxed. Full list in `review-sheets/AUTHOR-LIST-accepted-faults-2026-10-09.json`.

## Records

- Book plan: `pipeline/review/V15-IMPOSITION-2026-10-10.json`; final builds: `pipeline/review/V15-FINAL-BUILDS-2026-10-10.json`.
- Disk: `pipeline/review/DISK-CLEANUP-2026-10-10.html` (what can be deleted) and `pipeline/review/TRASHED-2026-10-10.json` (the 18 superseded PDFs moved to the Trash).
- Split choices for the page turns: `pipeline/review/PAGE-TURN-SPLIT-PICKS-2026-10-10.json`.
- Reviews: `pipeline/review/TAIL-IDENTITY-REVIEW-*.json`; build logs `pipeline/review/solve-logs-2026-10-09/`; tools `pipeline/review/session-tools-2026-10-09/`.
