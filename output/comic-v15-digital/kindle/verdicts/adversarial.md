## Adversarial (red team): Kindle edition of the V15 graphic novel, round 2

Checked against files, not against the other verdicts: KINDLE-ITEMS.md (with Round 2), the five verdicts and recheck-r2.md, KDP-UPLOAD-PACK.md, cover-drafts/A-charge.jpg and B-ridge.jpg (full, 800, 160, 100 and 60 px, greyscale), epub-text/ (content.opf, text/, css/), tools/make_kindle_epub.py and make_kindle_cover.py, v15-panels.json (1,709 panels, 422 pages, 28 chapters), and the built EPUB itself (the device copy at output/comic-v15-digital/kindle/upload/, 310,737,186 bytes).

1. PASS WITH NOTE: A is right and holds at 160, 100 and 60 px and in greyscale. The cover inside the upload EPUB is pixel-identical to cover-drafts/A-charge.jpg (mean difference 0), so the uploaded and in-book covers match. The Round 2 line "both riders and both swords fully in frame" is wrong (Nagoji's lowered talwar leaves the left edge), as recheck-r2 says; it reads as motion and needs no re-render, only a corrected line in KINDLE-ITEMS.
2. PASS WITH NOTE: "reading proof" is gone from rights.xhtml in the actual EPUB (0 hits). The copyright and credit wording still awaits the author's confirmation, and it now drives the AI answer on the KDP form (see 5).
3. PASS: re-ran the spine myself. Without the blanks there are exactly nine same-side clashes, at the nine places listed; with them, 434 itemrefs and none. Every blank sits between a chapter's last page and the next opener.
4. PASS WITH NOTE: book-type comic, original-resolution 1600x2311 and orientation-lock none are in the shipped OPF, with no Region Magnification, so automatic Virtual Panels is the right expectation. Nothing on the store page promises guided view; keep it so.
5. REVISE: the description now passes (accurate, no dashes, no banned word, nothing crossing a face). The pack around it has four problems every reviewer missed: an unverified claim inside the AI disclosure, a public GitHub copy of earlier comic pages, file paths I cannot find on the Mac, and a previewer step that may stall on a 311 MB file. Fixes below.

## Notes

### Item 5a: AI disclosure (the one that could misrepresent the book)

The text answer is now right in direction (declare the text), but the pack adds an assertion nobody verified: "The source novel is your own writing." The captions quote the novel's prose (ch 1 p1.1 "The first thing they took was my name." is novel text). The repo's AGENTS.md casts an AI agent as the manuscript's writer ("You are a literary historical writer and editor crafting riveting narrative history"), and the 2e plan tags passages as "AI-drafted, author-revised, author-written". Only the author knows how the 1e novel was written. The pack should not answer that for him, and KDP treats AI-drafted text as AI-generated even after heavy editing.

> Original: "The source novel is your own writing. Only AI used to edit or check text you wrote yourself counts as AI-assisted."
> Suggested: "Many captions quote the novel. If AI tools drafted any of those novel passages, count them as AI-generated too. Only AI used to edit or check text you wrote yourself counts as AI-assisted."

Images answer ("entire work") is correct and covers the cover art. Contributors "None" is consistent.

### Item 5b: public copies of the comic (rejection or delay risk)

`gh api repos/roshanis/nagoji` reports visibility "public". The repo tracks earlier versions of these comic pages (output/comic-v14-chapter-quality-v1/chapter-06 to chapter-17 PDFs, output/pdf/Horse-of-the-Servant-V13-Reference-Redesign-r1.pdf) and the novel EPUBs. KDP Select requires the ebook not to be available elsewhere in digital form, and KDP's content review can hold a book whose content it finds free online until the publisher proves rights, which would cost days against a hard deadline. Making the repo private is reversible and the author's call.

> Original: "| KDP Select | Your choice. Select means 90 days exclusive to Amazon, and the book can then be read in Kindle Unlimited. |"
> Suggested: "| KDP Select | Your choice. Select means 90 days exclusive to Amazon, and the book can then be read in Kindle Unlimited. Enrol only if no version of the comic is online (see the GitHub step below). |"

Add as the first bullet under "Before you press Publish":
> Suggested: "Make the GitHub repository roshanis/nagoji private, or remove the comic PDFs from it. It is public and holds earlier versions of these pages (V14 chapters 6 to 17, the V13 reference PDF). KDP can hold a book whose pages it finds free online until you prove your rights, and KDP Select does not allow it."

If the web edition in output/comic-v15-digital/web is hosted anywhere public, the same applies.

### Item 5c: file paths and cover choice

The only copy of the Kindle EPUB I can see on the device is under kindle/upload/, not kindle/build/, and there is no kindle/cover-drafts/ folder there (only cover-src/ with the raw frames). The author chose A, so "(or B)" now invites a mismatch with the cover inside the EPUB.

> Original: "**Manuscript:** `output/comic-v15-digital/kindle/build/Horse-of-the-Servant-Graphic-Novel-Kindle.epub` on your Mac."
> Suggested: "**Manuscript:** `output/comic-v15-digital/kindle/upload/Horse-of-the-Servant-Graphic-Novel-Kindle.epub` on your Mac."

> Original: "**Cover:** `output/comic-v15-digital/kindle/cover-drafts/A-charge.jpg` (or B-ridge.jpg), a 1600 x 2560 JPEG."
> Suggested: "**Cover:** A-charge.jpg, a 1600 x 2560 JPEG, from the project Library (graphic-novel-kindle/cover-drafts/). Save it to your Mac first. It is the cover already inside the EPUB."

> Original: "- Pick the cover (A or B)."
> Suggested: "- Cover: A (chosen, and already inside the EPUB)."

### Item 5d: previewer and launch checks

> Original: "- Look through the online previewer."
> Suggested: "- Check the book in Kindle Previewer 3 on your Mac; the online previewer may stall on a 311 MB file."

Add after the 72 hours line:
> Suggested: "- The novel already sells on Kindle under the same title and author. Once the comic is live, check that Amazon has not shown it as another edition on the novel's page. If it has, ask KDP support to separate them."

Deadline note: the 72 hours is typical, but a large comic with AI declared can be held for manual review. Submit as early as possible this week; the deadline is to submit, not to go live.

### Description: checked line by line against v15-panels.json

- "the first thing they take is his name. A shrug, and an entry in a book.": ch 1 p1.1, verbatim. Good.
- "household horse": ch 1 p1.1. "Captured by the Portuguese": ch 5 p7.2, ch 7 p10.4 (Vasai). "shipped south": ch 2 title "The Slave Ship South". "storm tears the ship apart": ch 3. "pepper coast": ch 4 title. "useful stranger": supported.
- "ambitious king": ch 12 p1.5 "every ambitious man"; the comic itself says "young King" (ch 10 p12.1). Either is defensible; "ambitious" avoids the age question.
- "letters from the north calling him home": ch 19 (brother's letter) and ch 25 p2.3 "If you return now, you will have estates confirmed". Supported.
- "old houses with long knives": ch 22 p7.5 "For the old houses", ch 22 p15.3. "a choice about whose man he is": ch 19 p6.2, ch 25 p15.4. Supported.
- "422 pages across 28 chapters": 422 distinct pages, 28 chapters. Correct.
- No De Lannoy, no 1750 ending, no outcome of the march: no spoiler, and no exposure of the 1e/2e staging gap.
- 1,045 characters, plain paragraphs, no em or en dash, no banned word, nothing moving across a face. "across" appears once, in "422 pages across 28 chapters", which is harmless.

### Other things verified

- Fonts are in the built EPUB (cinzel-700, eb-garamond-400 and italic), closing the recheck's open note.
- Upload EPUB and the epub-text snapshot differ only in dcterms:modified (02:14:56Z vs 02:13:51Z) and the cover file; the snapshot is one rebuild behind, nothing else.
- html.cover and body.cover 2560 px is in the shipped book.css.
- Royalty: 310 MB x $0.15 is $46.50; 35% of $12.99 is $4.55. Correct.

## Panel check

- All five reviewers and recheck-r2 PASS item 5 without noticing the public GitHub repo. That is the largest remaining risk of a hold on KDP and a KDP Select breach.
- History (round 1): "The novel's prose stays human-authored" is an unsupported assertion, and the reviser carried it into the pack as "The source novel is your own writing." Disputed; see 5a.
- Recheck-r2, design note on item 4: "confirm that the fonts folder is in the final EPUB". Resolved: fonts are present in the upload EPUB.
- Recheck-r2, story note on item 1 ("If B is chosen, rebuild"): moot. A is chosen and is inside the EPUB.
- No BLOCK anywhere rests on a stale document or reopens the settled V15 staging decision. No reviewer disagreement needs the author beyond the KDP Select and GitHub choice.

## Re-check (after the coordinator applied the item 5 fixes)

I re-read KDP-UPLOAD-PACK.md and KINDLE-ITEMS.md from the mount. The pack has no em or en dash, no spaced or double hyphen used as a dash, no banned word, and nothing moving across a face.

- 1 (KINDLE-ITEMS cover line): PASS. It now says Nagoji's talwar and Dhanaji's horse's head run off the edges.
- 5a (AI text): PASS. The suggested wording is in, and the unverified "your own writing" claim is gone.
- 5b (GitHub and KDP Select): PASS. The Select row has the caveat, and the GitHub bullet is first under "Before you press Publish", with the web edition covered.
- 5c (paths and cover): PASS WITH NOTE. Manuscript and cover both point to kindle/upload/, and the checklist says "Cover: A". My staged view of the Mac folder predates the cover copy and shows only the EPUB. Before uploading, the author should confirm Horse-of-the-Servant-Kindle-cover.jpg is in that folder.
- 5d (previewer, edition, timing): PASS WITH NOTE. All three lines are in. Optional wording fix, because today is Thursday:
  > Original: "Submit as early in the week as you can."
  > Suggested: "Submit as soon as you can."

Item 5 now stands at PASS WITH NOTE. No REVISE remains.
