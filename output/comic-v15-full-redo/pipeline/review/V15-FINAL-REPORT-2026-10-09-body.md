# Horse of the Servant V15: final build, 2026-10-09

All 28 chapters are built: {{TOTAL_PAGES}} pages and {{TOTAL_IMAGES}} placed images, the lowest at {{MIN_PPI}} PPI. Checks across the whole book: {{PROBLEMS}}.

## The book

{{TABLE}}

"Crossing tails left" lists panels (page.panel) where two speakers' tails still cross because the panel has no other free space that keeps every balloon in reading order; each was searched for a layout without the crossing and none exists. {{CROSSINGS}} panels in all.

## What was fixed today

### Varma drawn like Nagoji

- Two tails-and-identity reviews read every speech balloon in all 28 chapters on tail check sheets: each balloon numbered, its tail point ringed, the speaker named, the three approved sheets (Nagoji commander, Nagoji as Ananthan Pillai, Marthanda Varma) as the reference.
- 14 panels where Varma read like Nagoji (Nagoji's heavy curled moustache, curly hair, the wrong forehead mark) were redrawn as edits of the existing art with Varma's sheet attached, composition kept: ch10 12.5; ch11 3.5, 4.5, 17.2; ch15 10.1; ch16 13.3; ch22 10.4, 11.4, 11.5, 13.1, 13.3; ch23 1.5, 22.2; ch28 10.1 (the aged king, matched to his own look in 10.2).
- Each redraw was checked by eye before it was used: thin waxed moustache, sleek hair with the side knot, the vertical namam, pearl drops. Where the two men share a panel (ch22 11.5 and 13.3) they now read as two different men.

### Tails pointing at the wrong person

- The balloon placer had no rule against two speakers' tails crossing in an X (it happens when the person on the right speaks first). It now searches again for a layout without the X, and keeps it only if it covers no story-critical art the first layout left clear. Panels without a crossing come out exactly as before. A scan of the built chapters found 16 such panels; after the rebuilds only the forced ones in the table remain.
- ch6 11.5: Ramayyan's tail ran across Varma's chin; Varma's face zone now covers his chin and neck, so the tail goes round.
- ch20 14.3: the off-panel priest's tail ended on a woman in the crowd; it now runs to the panel's upper right edge.

### Pages that did not fit

- Pages too full for their lettering were split, under the standing rule: ch13, 14, 15, 16, 18, 20, 25 earlier today, then ch17 (pages 6, 7, 9), ch21 (pages 2, 3, 4, 5, 8), ch22 (page 1), ch23 (pages 2, 4, 5, 6), ch24 (pages 11, 12, 23, 28), ch26 (pages 8, 10) and ch28 (pages 9, 10). Insets stay with their host panel; page intros were corrected where an inset moved.
- ch19 5.3: both of Varma's lines aim at the top edge (he is above the frame), through a face zone that was only a sliver of his chin; that zone was dropped.
- ch22 3.4 (the chaver's eyes in close-up): its face zone had its centre off the frame; it now sits on the brows and eyes.
- ch27 7.3 (Savitri's force, a 3:1 strip): one keep zone (her retainers at the left) was relaxed so the two captions could be placed; every face stays clear.
- ch21 5.3 (the Pune memory): the 3:1 strip could not hold three long narration balloons without covering the executioner's shadow. It was regenerated once as a 3:2 frame with the dark lattice across the top; the three balloons now sit on the lattice and the scene is clear.

### The palm-leaf records in chapter 21

- LEAF and LEDGER lines are now lettered as inscriptions: no balloon outline and no tail, dark sepia ink on a soft leaf-tone wash, placed inside a write zone marked on each leaf's blank bands, as the script asks.

### Renumbering under your 2026-10-09 approval

- CONTINUITY.md page.panel anchors renumbered for chapters 15, 17, 20, 22, 24 and 28 (row text unchanged; backups `pipeline/review/CONTINUITY-pre-anchors-chNN-2026-10-09.md`).
- The approved-sheet spans moved with the pages: Nagoji commander now ends at 17.13 (was 17.10), Ananthan Pillai starts at 17.14 (was 17.11) and runs to 28.14 (was 28.12), and resumes at 28.15.2 (was 28.13.2). Backups `pipeline/review/APPROVED-SHEETS-pre-ch17-split-2026-10-09.json` and `...-ch28-split-...`.

### Pipeline changes, all test-first (627 tests pass)

- A copy chunk repeated inside a longer chunk no longer fails the text check.
- "(voice-over)" and "(memory)" speech is a tailless box.
- Tails of two speakers kept from crossing (final lettering only; the page fitter is unchanged).
- The inscribed style and write zones for LEAF and LEDGER lines (built by Codex to a test-first spec, reviewed and re-tested here).
- The PDF check can read a full-page image upscaled for 300 PPI (a single-panel page in ch26 embedded 75.5 MB, past the reader's old limit).

## For you to decide or check

- "(off)" narration over a flashback where the narrator is also drawn as his younger self: ch16 6.3, ch20 9.2, ch25 11.1. The tail runs to the panel edge, as the script's "(off)" asks, but a reader sees the speaker in the panel. Changing those speaker tags to "(voice-over)" would letter them as tailless boxes. That is a script change, so it is yours.
- Tails correct but ending near another man's hair, because the speaker leans in behind him: ch6 2.3 (Ibrahim behind Nagoji) and ch15 3.2 (De Lannoy over Donnadi).
- The forced crossing tails in the table above.
- Spreads: splits renumbered many pages, so pages the scripts meant to face each other may now fall across a page turn.
- The earlier identity audit noted milder Varma drift (a slightly fuller moustache, a loose lock) in about 100 panels; the two reviews did not judge any of those to read as Nagoji, so they stand as notes. ch28 10.1's redrawn moustache is still a little full.
- Notes accepted earlier and still open: Varma's knot sits at the back of the head in many panels; ch12 7.3 loose hair at the neck; ch16 1.2 and ch19 12.1 brand on the outer forearm; ch20 15.4 keep zones relaxed. The full list of forced picks, identity residues and hand retouches is in `review-sheets/AUTHOR-LIST-accepted-faults-2026-10-09.json`.
- The chapter 21 inscriptions: please check you like the wash-and-sepia look on the leaves.

## Records

- Reviews: `pipeline/review/TAIL-IDENTITY-REVIEW-2026-10-09.json`, `-B-` and `-C-`; tail check sheets in `pipeline/review/tail-sheets-2026-10-09*`.
- Build logs: `pipeline/review/solve-logs-2026-10-09/`; tools: `pipeline/review/session-tools-2026-10-09/`.
- Image jobs: `review-sheets/LEAN-BATCH-191` to `199` with their generation logs.
