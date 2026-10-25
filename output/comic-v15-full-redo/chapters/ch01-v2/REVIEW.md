# Chapter 1: Dungeons of Goa, r7 review

Completed all 19 confirmed r6 issues in the new ch01-v2 package. The old ch01 package remains unchanged. This is the completed r7 digital proof; no new author approval is asserted.

## Delivery and observed checks

- PDF: `pdf/Horse-of-the-Servant-V15-Chapter-01-r7.pdf`
- SHA256: `258902a0bc996d7c9290f634dd03e1198004269574693c3d7e8d7343e4307779`
- Pages: 9; folios 1 through 9; placed images: 41.
- Effective PPI: minimum 357.46339957; median 416.78049893; required minimum 300.
- Build return code 0; separate verify return code 0. Both exact commands and full output are retained in review/BUILD-COMMAND-r7.json and review/VERIFY-COMMAND-r7.json.
- All 58 script chunks verified once in script order on their correct pages. All 49 reserves passed copy fitting and glyph-pixel checks.
- Embedded font streams independently inspected: DINCondensed-Bold, Georgia, Georgia-Bold and Georgia-Italic. All four have nonempty FontFile2 streams.
- Every one of 41 final selected frames lives inside ch01-v2 and its file hash matches the manifest.
- Personally inspected all nine 300 DPI Poppler renders in `renders/r7/`. Independent reviewer also passed pages 5 through 9. Evidence: review/FINAL-VISUAL-REVIEW-r7.json.
- 336 protected baseline files retain their original hashes, including all old ch01 files and the prepared inputs. No shared code was edited. Evidence: review/INTEGRITY-r7.json.

## Resolution of the 19 issues

| Issue | Panel | Resolution |
| --- | --- | --- |
| 1 | 6.4 | Resolved. Removed Duarte entirely according to the audited cast. The panel contains bound Nagoji and background Joao, so the forbidden Roman collar tab is gone. |
| 2 | 7.5 | Resolved. Rebuilt Duarte from the approved sheet and corrected 7.2 face. Narrow gaunt jaw, grey swept hair, clean-shaven face, plain standing collar and restrained mouth twitch pass native and page review. |
| 3 | 8.3 | Resolved. Overhead priest is now grey-haired, gaunt, clean-shaven Duarte in a plain collar and small cross. Joao retains his full dark beard. |
| 4 | 8.5 | Resolved. Replaced the ornate crucifix with a small plain cross. The wrist-stopping action remains clear. |
| 5 | 2.3, 3.4 | Resolved. Joao now has dark beard growth across cheeks, jaw and chin, matching the approved gaoler sheet. |
| 6 | 6.5 | Resolved. Memory now uses Nagoji identity, curled moustache, clean chin and small gold stud; rust-red turban, cream tunic and red sash; Kanka is a black mare. The memory bleeds into the present frame. |
| 7 | 4.1 | Resolved. Escorts now wear tricorne hats, cream shirts and brown garrison clothing matching the visual period of the retained 9.2 guards. |
| 8 | 2.2 | Resolved. Removed wrist manacle and its wall chain. Nagoji hands and wrists are cloth-bandaged. |
| 9 | 4.2 | Resolved. Wrists remain separately bandaged and unchained. Ankles retain the transport irons. |
| 10 | 4.3, 4.4 | Resolved. Both ankle cuffs and their connecting chain are clearly visible, with bare feet. |
| 11 | 8.6 | Resolved. Audited cast is Duarte alone, looking away from the stool. The incorrectly shown captive and dark wrist manacles are removed. |
| 12 | 4.4 | Resolved. Removed the maroon sash. Captivity ochre tunic and cream dhoti remain. |
| 13 | Pages 5 to 8 | Resolved. New 5.1 is the canonical set reference: windowless barrel vault, torch and brazier, horizontal iron ring with straight knotted ropes, one stool and tool table. Every contradictory chamber view was redrawn using this set lineage and character sheets. No daylight, chapel, altar or nooses remain. Retained 7.3,8.1,8.2 are close-ups without a conflicting setting. |
| 14 | 4.4 | Resolved. Duarte leads and Joao follows Nagoji into the doorway, preserving the escort from 4.2. |
| 15 | 9.1 | Resolved. Nagoji slumps with closed eyes and a tilted head. Fingers look puffy and stiff beneath bulky, fresh but grimy wrapping. No blood or gore. Independent and page-scale review pass. |
| 16 | 6.4 | Resolved. Joao is smaller and farther back at the tool table, looking down while lifting tongs. Nagoji remains bound on the foreground stool; Duarte is absent. |
| 17 | 7.5 | Resolved. Regenerated the off-panel balloon and shortened its tail. Both lie fully within the visible frame with a dark margin on the right. All source copy fits. |
| 18 | 8.6 | Resolved. Duarte two balloons sit on the left beside his face with short tails. Joao single off-panel reply sits on the right. Script order is Enough, Joao reply, Duarte final line. No tail crosses another figure. |
| 19 | Page 6 | Resolved. Copied the r6 layout and adjusted page6 row heights to 134,111.5,65,110,95pt. All five actual placements are x=36pt,width=369pt with exactly 2pt between rows. Final 6.1 viewport removes white canvas; all others fit their matching viewports. Native final page and independent review confirm flush edges and even gutters. |

## Every redrawn panel

24 panels redrawn with built-in imagegen. All selected originals were inspected at native resolution against the approved sheets and chapter 1 continuity row. The new establishing panel 5.1 received a 2x pipeline upscale for effective PPI; its original is retained.

| Panel | Final selected frame | Reason and visual review |
| --- | --- | --- |
| 2.2 | `frames/page-02-panel-02-v01.png` | Native review: removed wrist manacle and shoulder/wall chain; bandaged hands remain. Duarte gaunt, grey swept hair and plain black collar. Original staging retained. Luna independently passed. |
| 2.3 | `frames/page-02-panel-03-v01.png` | Native review: Joao full dark beard matches approved sheet; boot-tap staging, Nagoji clean chin and captivity costume retained. Luna independently passed. Musical symbol anchor preserved. |
| 3.4 | `frames/page-03-panel-04-v01.png` | Native review: Joao full beard across cheeks, jaw and chin, broad body, laughing with hands on belt. Root and Luna passed likeness against approved sheet. |
| 4.1 | `frames/page-04-panel-01-v01.png` | Native review: both guards now have tricornes and cream/brown garrison dress matching9.2. Hauling pose, bandaged wrists, ankle irons and bare feet preserved; no sash. Root and Luna passed. |
| 4.2 | `frames/page-04-panel-02-v02.png` | Native review: cloth bandages on unchained wrists, both ankle irons, correct escort cast and clothes. Caption fits blank reserve. |
| 4.3 | `frames/page-04-panel-03-v02.png` | Native review: both ankle cuffs joined by continuous short iron chain, bare feet, cream dhoti. Caption fits. |
| 4.4 | `frames/page-04-panel-04-v01.png` | Native review: Duarte ahead and Joao behind remain escorting Nagoji to red-lit doorway. Both ankle cuffs connected, wrists bandaged without chains; maroon sash removed. Room still withheld. Root and Luna passed. |
| 5.1 | `frames/page-05-panel-01-v01-2x.png` | Native review: canonical windowless barrel-vaulted heavy stone chamber, torch and floor brazier only, ceiling ring, straight ropes without nooses, single stool and plain tool table. Root and Luna passed. |
| 5.2 | `frames/page-05-panel-02-v01.png` | Native review: window and exterior/daylight removed; same plain tool table, dark stone and floor brazier as canonical room, no figures. Tools and blank caption retained. |
| 5.3 | `frames/page-05-panel-03-v04.png` | Native review: correct three-person staging, Nagoji bound by rope at cloth-wrapped wrists, both ankle irons linked, Joao checking knot, Duarte back. One occupied stool, canonical windowless chamber. Larger caption fits. |
| 6.1 | `frames/page-06-panel-01-v02.png` | Native review: gaunt grey-haired Duarte, plain collar and cross, canonical windowless room, no duplicate stool. Dialogue fits. Final additive build-input viewport excludes the native white canvas below the border and trims equal side wall slivers, preserving the complete balloon and figure for an even page6 gutter. |
| 6.2 | `frames/page-06-panel-02-v03.png` | Native review: Nagoji unmoved, bound stool with wrist ropes and cloth bandages, both linked ankle irons and bare feet, no second stool, canonical chamber. Whole figure and balloon inside flush viewport. |
| 6.3 | `frames/page-06-panel-03-v01.png` | Native review: Nagoji eyes and small ear stud, canonical torchlit wall. Viewport keeps full balloon and tail on flush page6 row. |
| 6.4 | `frames/page-06-panel-04-v04.png` | Native review: audited cast Nagoji foreground bound to stool; full-bearded Joao smaller in background picking tongs without looking up. No Duarte. Both ankle irons, wrist cloth and ropes, canonical room, no extra stool. Full balloon fits. |
| 6.5 | `frames/page-06-panel-05-v01.png` | Native and independent review: Nagoji identity preserved in memory, thick curled moustache, clean chin, tiny gold stud, rust turban cream tunic red sash and black Kanka. Canonical room on present side. |
| 7.1 | `frames/page-07-panel-01-v01.png` | Native review: Nagoji recovered and flat, cloth-bound wrists and canonical windowless chamber. Tight viewport retains his face, hands and entire balloon. |
| 7.2 | `frames/page-07-panel-02-v01.png` | Native review: Duarte narrow lined face, grey swept hair, clean chin, plain collar and cross. Canonical room. Dialogue fits; crop removes unused stool corner. |
| 7.4 | `frames/page-07-panel-04-v02.png` | Native review: Nagoji alone per audited cast, moustache with clean chin, bandaged wrists bound with rope and ankle irons. Canonical set, extra empty stool removed. Dialogue fits. |
| 7.5 | `frames/page-07-panel-05-v03.png` | Native and independent identity review: gaunt narrow Duarte face, grey swept hair, plain standing collar, small mouth twitch. Joao off-panel balloon and full tail inside frame with clear dark right margin. Copy fits. |
| 8.3 | `frames/page-08-panel-03-v01.png` | Native and independent review: overhead wide preserves distance, on-model grey gaunt Duarte, full-bearded Joao, bandaged Nagoji. Canonical room with ring, straight ropes, brazier and tool table. No chapel or daylight. |
| 8.4 | `frames/page-08-panel-04-v02.png` | Native and independent review: canonical vaulted stone ceiling, horizontal iron spreader ring and straight ropes with knotted ends, no nooses or window. Caption fits. |
| 8.5 | `frames/page-08-panel-05-v01.png` | Native and independent review: small plain cross, Duarte stops Joao wrist above brazier; blurred Nagoji behind. Canonical windowless room. Lettering fits blank balloon. |
| 8.6 | `frames/page-08-panel-06-v01.png` | Native and independent review: Duarte alone, gaunt grey-haired face turned away, no captive or wrist manacles. Two left balloons point to Duarte; right off-panel Joao balloon has contained tail. All three chunks retain script order. |
| 9.1 | `frames/page-09-panel-01-v02.png` | Native and independent review: exhausted slumped Nagoji, eyes closed, puffy stiff fingers beneath fresh bulky grimy linen bandages, no blood or gore. Correct cell, no wrist manacles, ankle irons. Caption fits. |

## Reuse, provenance and retained trials

The 17 other panels use exact copies of their r6 selected frames. Their original prompt paths, prompt hashes, reference hashes, visual review and geometry were retained and compared with SELECTION-MANIFEST-r6.json. Source paths and SHA256 values are recorded in review/REUSED-FRAMES-r7.json and each selection r6_reuse record. Both the selected 3.5 2x frame and its original were copied into this package.

The prepared IMAGEGEN-JOBS.json was never regenerated. Raw capture metadata is retained; the additive candidates/*-r7-*.json records bind each correction to the exact prompt and references actually used. Some later edits attach their immediate corrected predecessor; the reference ancestry leads to the canonical 5.1 frame and approved character sheets. No provenance was invented to make those later calls appear to attach a reference they did not.

Sixteen rejected candidates remain with their prompts, hashes and geometry trials. Reasons are recorded in review/REJECTED-CANDIDATES-r7.json. They include identity drift, duplicate stools, absent ankle irons, inadequate lettering space, a changed camera aspect, a mismatched ring, a clipped tail and an insufficiently injured aftermath.

LAYOUT.json preserves the r6 rows except page 6. review/SELECTION-INPUT-r7.json is an additive assembly input that refines the 6.1 viewport without overwriting its earlier selection record. The build used the requested chapter/package/layout/folio/revision arguments plus this manifest argument. SELECTION-MANIFEST-r7.json is the authoritative final placed-art manifest.

## Unresolved items and review limits

None of the 19 requested issues remains unresolved. Captions in 5.3 and a few short strips are snug but contained and pass the measured minimum clearance. The larger 5.3 caption covers part of the torch sconce, a reviewed composition tradeoff. Other r6 layouts and all untouched art were preserved as instructed. This review does not claim a fresh five-lens review of the entire novel, physical print proof acceptance, or author acceptance of r7.
