# Chapter 4 production review

Status: BLOCKED BEFORE BUILD. This is an incomplete production handoff, not an accepted chapter or print proof.

The approved script calls for six pages and 29 placed frames, beginning at folio 26. All 29 jobs received built-in imagegen candidates. There are 50 captured candidates, including one retry for each of 21 frames. Rejected versions remain preserved.

## Confirmed shared pipeline blocker

The approved page 6 introduction requires panel 6.2 to show broken, unreadable speech strokes, with only two clear instances of kapitan. The compositor has no such lettering mode. It wraps the raw source string and draws it with DIN drawString, so the visible result would be literal "... *kapitan* ... *kapitan* ...". The same raw handling prints asterisks around bhau and other italic terms.

The verifier demands those literal source markers. A read-only in-memory check passed the raw marked-up string and rejected the requested extracted words "kapitan kapitan" with: "Missing or duplicate script chunk: ... *kapitan* ... *kapitan* ...". The parser also discards the page-level special lettering instruction.

Evidence:
- scripts/CHAPTER-04-SCRIPT.md:187 and :197: approved special treatment and copy.
- pipeline/script_pipeline.py:90 to 100: raw copy is retained.
- pipeline/compositor.py:159 to 162: raw copy is measured and wrapped.
- pipeline/compositor.py:417 to 422: plain DIN drawString renders it.
- pipeline/compositor.py:428 to 440: exact raw verification requires the markers.

An independent reviewer confirmed the gap. The user expressly required stopping and reporting a pipeline bug rather than changing shared code while Chapters 2 and 3 run concurrently. Production stopped. No build or verify command was run, no PDF was authored, and no shared code was edited.

The pipeline owner needs to support styled terms, canonical text verification, and the unreadable speech treatment before this chapter can meet the approved script. This is not permission for this task to modify the shared pipeline.

## What was drawn and reviewed

Root inspected all page 1 and 2 candidates at native resolution, all ten initial page 3 and 4 candidates, all five initial page 5 candidates, and page 5 panel 5 v02. The page 3 and 4 worker inspected its eight corrective candidates at native resolution and reported continuing failures. Root did not inspect those eight corrective candidates, page 5 panels 1 and 2 v02, or page 6 candidates before the production stop. No final acceptance is claimed for them.

The pilot's nine r6 pages and the Nagoji and Ibrahim sheets were inspected. Prepared prompts, actual production prompts, reference hashes and captured source hashes are retained. The 50 frame hashes, actual prompt hashes and attached reference hashes were rechecked successfully at handoff.

| Frame | Latest candidate | Current finding |
| --- | --- | --- |
| 1.1 | v02 | Root and independent review pass; distant prone figure and wrapped hands corrected. |
| 1.2 | v02 | Root and independent review pass; chin corrected. |
| 1.3 | v02 | Root and independent review pass; chin corrected. |
| 1.4 | v02 | Conditional visual pass; six feet remain with short ankle sections. Script asks to see no more than feet. |
| 2.1 | v01 | Root and independent review pass; fisherman identity anchor. |
| 2.2 | v02 | Root and independent review pass; empty beach, bandages and stud corrected. |
| 2.3 | v02 | Root and independent review pass; empty beach, no premature brand, plain stud. |
| 2.4 | v02 | Root visual pass; hand wraps corrected; independent review pending. |
| 2.5 | v02 | Root visual pass with proposed crop; independent review pending. |
| 3.1 | v02 | Worker reports continuing costume, identity or brand deviations. Root review pending. |
| 3.2 | v01 | Root rejects reddish, overly distinct brand; needs pale unreadable ridges. |
| 3.3 | v02 | Worker reports continuing fisherman identity or costume deviations. Root review pending. |
| 3.4 | v02 | Worker reports continuing costume, identity or brand deviations. Root review pending. |
| 3.5 | v02 | Worker reports continuing costume, identity or brand deviations. Root review pending. |
| 4.1 | v02 | Worker reports continuing costume, identity or brand deviations. Root review pending. |
| 4.2 | v02 | Worker reports continuing fisherman identity or costume deviations. Root review pending. |
| 4.3 | v01 | Root rejects dungeon and chains, stubble, dangling ornament and outer-arm brand. |
| 4.4 | v02 | Worker reports continuing costume, identity or brand deviations. Root review pending. |
| 4.5 | v02 | Worker reports continuing costume or carrying deviations. Root review pending. |
| 5.1 | v02 | Corrective carry and geography pass generated; root review pending. |
| 5.2 | v02 | Worker reports improved inland village, carry and wraps; root review pending. |
| 5.3 | v01 | Root rejects adult in place of girl, harbour setting, missing wraps and letter-like brand. |
| 5.4 | v01 | Root rejects standing instead of carried Nagoji, missing wraps, brand and ear ornament. |
| 5.5 | v02 | Root rejects exposed shoulder where cloth should cover both, dangling ear ornament, chin and brand drift. |
| 6.1 | v02 | Woman's costume correction generated; root review pending. |
| 6.2 | v01 | Root review pending. Required special lettering is blocked by the shared pipeline. |
| 6.3 | v01 | Root review pending. |
| 6.4 | v01 | Root review pending. |
| 6.5 | v02 | Ibrahim vest correction generated; root review pending, including anatomical left scar and scale. |

## Regeneration record

Each listed frame has v01 and v02. A retry is not itself a pass.

| Frames regenerated | Why |
| --- | --- |
| 1.1 | Initial figure too close and missing hand wraps. |
| 1.2, 1.3 | Visible chin stubble fields conflicted with the required clean chin. |
| 1.4 | Too much lower leg above the feet. Short ankle sections remain in v02. |
| 2.2 | Unwanted fort and people, dangling ear ornament and absent finger wraps. |
| 2.3 | Unwanted guards and fort, premature brand and dangling ear ornament. |
| 2.4 | Missing visible hand bandages. |
| 2.5 | Initial frame did not work as the required narrow surf strip. |
| 3.1, 3.3, 3.4, 3.5 | Fisherman identities and costumes, invented settings or bystanders, brand and Nagoji continuity. |
| 4.1, 4.2, 4.4, 4.5 | Fisherman identities and costumes, invented settings or figures, brand and carrying staging. |
| 5.1 | Wrong carrier assignment, missing wraps and a misplaced mark on a shin. |
| 5.2 | Nagoji walking with bound wrists instead of being carried; hand wraps absent. |
| 5.5 | Healer drawn in a fitted blouse; other continuity issues remain in v02. |
| 6.1 | Healer's blouse or stitched upper garment required correction. |
| 6.5 | Ibrahim's clothing needed the short pale sleeveless vest and white mundu, without coat or decorative sash. |

The v01 page 3 and 4 failures also included invented dungeon settings, red turbans on the leader, a shirtless young fisherman, missing wraps, extra people, beard drift, and misplaced or pseudo-letter brands. These are rejected art, not accepted deviations.

## Layout, selections and preflight

LAYOUT.json was created with six pages, each totaling 523.5 pt including 2 pt row gaps. It includes the standalone brand insert and a 209.5 pt final panel on page 6.

A later page 2 proposal was tested only in memory: rows 102, [140,140], 180 and 95.5 pt. That proposal lets the surf strip fill its width with the reviewed crop. It has not replaced LAYOUT.json.

review/ROOT-NINE-PREFLIGHT-r1.json preserves measured visible rectangles, reserves, the proposed layout and copy/pixel checks for the nine page 1 and 2 frames. All measured copy fit, and every checked actual glyph rectangle had light support fraction 1.0. This limited check uses the current literal-markup engine, so it does not resolve the blocker or establish final print acceptance.

Five early selection files exist. The selections for 1.2, 1.3 and 1.4 reference rejected v01 images and are superseded by the visual findings above. They were retained because overwriting is prohibited. Do not build from those early selections. On resumption, use a new reviewed import manifest, as supported by the pilot workflow, to select corrected versions without overwriting history. The selections for 1.1 v02 and 2.1 v01 remain visually valid, subject to final page review.

No Real-ESRGAN pass, complete 29-frame reserve audit, PDF verification, font embedding check, final PPI audit or page-render review has occurred.

## Provenance and scope disclosure

The capture command records the prepared prompt. Additional immutable provenance records bind the actual production prompt and reference images. Pages 1, 2, 5 and 6 use candidates/*-provenance.json. Pages 3 and 4 use review/provenance-*.json. Preserve both the capture records and these enriched records. Some corrective generations were fresh draws using identity references rather than edits attaching the preceding rejected frame; inspect each actual provenance record before further retries.

A worker mistakenly created 18 duplicate provenance JSON files in output/comic-v15-full-redo/ch04/review/, outside the permitted chapters/ch04 folder. All 18 are byte-for-byte identical to the corresponding files in the correct folder. They were not deleted or moved because that requires explicit approval. review/OUT-OF-SCOPE-DUPLICATES-r1.json lists every path, byte count and hash. This was a scope violation, not an authorized change.

No scripts, continuity, concept sheets, shared pipeline code, or other chapter folder were edited by this task. The requested gpt-5.6-luna reviewer model was unavailable in the exposed model list; independent review used inherited Codex agents. No commit or publication was performed.

## Delivery status

| Requested item | Result |
| --- | --- |
| Final PDF path and SHA256 | None. Build stopped before authoring. |
| Final page count | Unavailable. Approved target is 6 pages. |
| Final placed image count | Unavailable. Approved target is 29 images. |
| Minimum and median effective PPI | Unavailable. No final PDF placements exist. |
| Render folder | None. No 300 DPI page renders were created. |
| Captured art | 50 candidates covering all 29 frames, under frames/. |
| Remaining deviations | Special lettering blocker, rejected or unreviewed later-page art, 1.4 ankle visibility, incomplete selection and print review, and the duplicate-file scope violation. |

After the pipeline owner resolves the lettering gap, recheck protected input hashes, review and correct the remaining art, record new selections additively, finalize layout, build the first PDF revision with first folio 26, verify all print gates, and inspect every 300 DPI page. This report does not approve any exception to those requirements.

## Resumed task status, 2026-09-30T14:45:55Z

Current status: BLOCKED ON BUILT-IN IMAGEGEN OUTPUT, not on the earlier lettering gap. See [the r2 resumed review](review/RESUME-REVIEW-r2.md) and [the exact tool failure](review/IMAGEGEN-BLOCKER-r2.json). A page 5.3 correction was rejected at imagegen output stage with HTTP 400 moderation_blocked. The pipeline procedure requires stopping on tool failure.

Four completed concurrent variants were preserved: 3.1 v03, 4.1 v03, 4.2 v03 and 5.1 v03. None is selected or accepted. Root and independent reviews found remaining defects or unverified lettering space. There are now 54 frame candidates and still only the five historical selection files, including the stale selections described above. Existing LAYOUT.json is preserved. No PDF or renders were built, and no final PPI, text or font pass is claimed. The detailed r2 review records the disagreements, remaining corrections, provenance and exact resume boundary.
