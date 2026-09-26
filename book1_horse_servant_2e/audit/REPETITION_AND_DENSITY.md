# Repetition and Tic Density Audit

Source: `book1_horse_servant` (files matching `book*_chapter*.md`): 28 chapters, 94,043 words. Generated 2026-09-26 by `book1_horse_servant_2e/audit/tools/scan_slop.py`.

Locations are `ChNN:line` (line numbers in the source file). A `d` after a line number means that occurrence sits inside quoted speech. Rates are per 1000 words.

## Editor's summary

This is the first-edition baseline for the second-edition cut. Every number here comes from the tables below. Locations are `ChNN:line` in `book1_horse_servant/`. The scanner and its tests live in `book1_horse_servant_2e/audit/tools/` (standard library only, 44 tests). To measure an edited batch against this baseline, run this from the repository root:

`python3 book1_horse_servant_2e/audit/tools/scan_slop.py book1_horse_servant_2e/manuscript -b book1_horse_servant -o book1_horse_servant_2e/audit/<batch>.md`

To list every hit of one marker with its line, add `-k as_if`. That takes any key from section 5.1, `img:storm` for an image family, or `all`.

### What the numbers say

1. **Rhythm is the strongest machine signal, more than vocabulary.** 1,767 of 4,020 paragraphs (44%) are a single sentence, and among narration paragraphs the share is 56%. 490 of them are standalone one-liners inside narrative passages, not beats between lines of speech. The median sentence is 8 words, 44% of sentences are under 8 words, and only 2% run past 30. On top of that come 186 short paragraph-final kickers, 276 verbless fragments and 22 "Word. Word. Word." runs, six of them in Ch21.
2. **Correction constructions are everywhere.** The Not-but family has 227 hits: 86 "not X but Y", 100 sentences opening "Not ...", and 41 "X, not Y". The style sheet allows one per chapter, and only in dialogue, so 202 are over the limit. 25 of the 28 chapters use "not X but Y".
3. **The rationed words run at two to four times the sheet's limits.** "as if" appears 79 times across 27 chapters (52 over). "like a/the" appears 89 times (47 over). slowly, quietly and softly appear 101 times (51 over), plus 18 "carefully". "as though" never appears, so "as if" does all the work.
4. **Parts of the PLAN.md baseline table are wrong.** Corrected counts: the weight of 19, something else 9 (14 with variants such as something more or something heavier), for the first time 15 (not 9; seven are "for the first time since"), etched 1 (not 13), somehow 4, in that moment 4, a sense of 0. Section 5.2 has the full totals.
5. **Some passages are recycled word for word between chapters.** These are the cheapest fixes:
   - The three love scenes with the same woman share their stock lines: "afterward she lay with her head on my chest" (Ch17:257, Ch20:386), "she propped herself up to look at me" (Ch17:263, Ch20:400) and "she reached up and unpinned her hair" (Ch16:119, Ch20:356). Ch20 flags the hair as a deliberate echo ("the way it had that first night"), but the other two lines read as reuse.
   - Two different halls, the roadside compound at Ch05:125 and the coastal fort at Ch06:21 and Ch06:37, are described from the same template ("its wooden pillars carved with curling", "At the far end, on a slightly raised platform, a man sat with").
   - "I thought of Goa. Of Keshavrao's hand slipping from the rope." (Ch16:383, Ch24:621).
   - "she said, inclining her head the smallest fraction" (Ch09:68, Ch20:67).
   - "on the southeastern frontier where" (Ch11:149, Ch12:57), which is repeated exposition.
6. **Stock gestures recur.** Phrases: "a ghost of a smile" (Ch20, Ch24, Ch28), "the corner of her mouth" (3 chapters), "for a fraction of a heartbeat" (Ch11, and Ch22 twice), "the smell of ghee and" (4 chapters), "up from his palm leaves" (4 chapters). Whole sentences: "He looked at me." 6 times, "He shrugged." 5 times, "It was not a question." 4 times. Gesture markers: nodded 36, eyes or gaze plus a motion verb 44, jaw tightened 14, "studied me" and similar 18.
7. **Some repeats may be deliberate callbacks, so decide on those rather than cutting automatically.** "washed up on this coast" (8 uses in 4 chapters, 5 of them in speech), "men who do not fight are trampled" (Ch01, and Ch24 twice), "with one foot in each river" (Ch19, Ch22, Ch28), "this kingdom uses what it finds" (Ch25, Ch28). Keep one deliberate echo of each at most.
8. **Two motifs are overworked.** The weigh, weight and balance family appears 103 times in 26 chapters, 35 of them figurative, mostly "the weight of". Storm words appear 71 times in 21 chapters, and in the last two paragraphs of seven chapters (Ch01, 05, 07, 08, 13, 21, 25). Ch01 and Ch07 both close on "Storms do/did not ask permission". The style sheet saves the storm close for Ch13 alone.
9. **25 of 28 chapter endings carry at least one flag.** Final paragraphs open with a banned word: "For now" (Ch06, Ch09), "For the moment" (Ch19), "But" (Ch14, Ch18, Ch22, Ch25), "And some" (Ch17). Ch16 and Ch19 close on the same idea ("That was enough for now." and "For the moment, that was enough."). Only Ch23 ends on dialogue.
10. **The register slips into modern language.** Ch21's ledger reads like a modern intelligence dossier ("Risk assessment: HIGH", "Leverage: significant", "Timeline: before next monsoon"). Other examples: "the brutal efficiency of state-building" (Ch10:181), "I solved a logistics problem" (Ch20:292) and "Padmini Amma navigated these shifts" (Ch16:297).
11. **The dashes are clean, but the quote marks are not.** There are no em dashes and no double hyphens. However, Ch11 and Ch12 use straight double quotes only, 14 chapters mix straight and curly quotes, and apostrophes are mostly straight (541 straight, 49 curly). One mechanical copy-edit pass before the prose edit will keep later diffs readable.

### Where to start

- **Density ranking by tic index, top 10:** Ch20, Ch28, Ch19, Ch04, Ch01, Ch26, Ch02, Ch22, Ch21, Ch15. By raw hits per 1000 words, the leaders are Ch22 (40.1), Ch26 (37.4) and Ch19 (28.9).
- **Edit budget** (the minimum number of edits to meet the style sheet, section 2): Ch24 50, Ch20 42, Ch21 40, Ch16 39, Ch23 38, and 649 for the whole book.
- The planned pilot of chapters 1 to 3 is a fair test (Ch01 ranks 5th by index and Ch02 7th), but it is light on the problems of the long, dialogue-heavy late chapters. Adding Ch20 or Ch24 to the pilot would let the calibration cover them.
- Section 3 lists the 30 densest paragraphs as a line-edit worklist.

### Limits

These counts are heuristics: they point at passages to check, and do not judge them. The verbless-fragment count, the "figurative" image flag and the filter that drops concessive "not X, but he..." clauses all work on patterns, so each will miss or over-count a few cases. Spot-check them with `-k`. Lexical markers count dialogue too; the "In speech" columns and the `d` flags show where. Proper names are auto-detected (264 words) and break repeated phrases, so a repeat that differs only by a name is not reported.

## Contents

1. Density ranking
2. Style-sheet ration check
3. Hot-spot paragraphs
4. Top cross-chapter repeated phrases
5. Tic markers per chapter
6. Repeated images and similes
7. Sentence rhythm
8. Dashes and quote marks
9. Chapter endings
10. Repeated whole sentences
11. Appendix: other repeated phrases

## 1. Density ranking

Core markers only (the 18 in section 5). **Tic index** gives every marker equal weight: for each marker, (hits + 1) / (expected hits + 1), where expected = book rate x chapter length, capped at 3x, then averaged over the markers. 1.00 is the book average; the +1 stops one stray 'somehow' from dominating a short chapter. **Hits/1000** is the plain sum, which the common markers (one-sentence paragraphs, short kickers, soft adverbs) dominate. **Drivers** are markers at 1.5x expected or more.

| Rank | Chapter | Title | Words | Core hits | Hits/1000 | Raw rank | Tic index | Drivers (x book rate) |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | Ch20 | Guest in Velinadu | 4569 | 104 | 22.8 | 9 | 1.27 | first time 2.9, narr. ? 2.1, something X 1.8 |
| 2 | Ch28 | Servant of Padmanabha | 3487 | 93 | 26.7 | 7 | 1.21 | Not-opener 2.5, narr. ? 2.2, somehow 1.7 |
| 3 | Ch19 | Shadows of the Deccan | 2875 | 83 | 28.9 | 3 | 1.18 | narr. ? 2.4, short final 1.8, somehow 1.8 |
| 4 | Ch04 | The Fishermen of the Pepper Coast | 1704 | 28 | 16.4 | 23 | 1.13 | something X 3.0, narr. ? 1.7, short final 1.6 |
| 5 | Ch01 | Dungeons of Goa | 1941 | 33 | 17.0 | 20 | 1.12 | triads 2.1, narr. ? 1.7, something X 1.6 |
| 6 | Ch26 | Fire in the Pepper Fields | 2597 | 97 | 37.4 | 2 | 1.12 | 1-sent para 2.1, X, not Y 1.9, that moment 1.8 |
| 7 | Ch02 | The Slave Ship South | 1890 | 33 | 17.5 | 18 | 1.10 | X, not Y 2.2, soft adv. 1.8 |
| 8 | Ch22 | Command of the Kayamkulam Frontier | 3795 | 152 | 40.1 | 1 | 1.09 | Not X but Y 2.2, 1-sent para 2.2, triads 1.6 |
| 9 | Ch21 | Ramayyan's Ledger | 2135 | 59 | 27.6 | 6 | 1.07 | triads 3.0, short final 1.5 |
| 10 | Ch15 | Prisoners of a New King | 3945 | 76 | 19.3 | 15 | 1.03 | weight of 1.7, Not X but Y 1.5 |
| 11 | Ch09 | Princess of Velinadu | 3056 | 65 | 21.3 | 12 | 1.02 | soft adv. 2.1, weight of 1.9, as if 1.7 |
| 12 | Ch08 | Padmini Amma's Estate | 3420 | 53 | 15.5 | 26 | 1.01 | X, not Y 2.4, somehow 1.7 |
| 13 | Ch27 | The Last of the Old Houses | 2321 | 52 | 22.4 | 10 | 1.00 | etched 2.0, like a/the 1.6 |
| 14 | Ch18 | Dutch Come Bowing | 2643 | 68 | 25.7 | 8 | 1.00 | narr. ? 1.6, as if 1.6 |
| 15 | Ch10 | Lessons in Travancore | 2579 | 49 | 19.0 | 16 | 0.98 | as if 2.2, weight of 2.0, Not X but Y 1.8 |
| 16 | Ch17 | Adoption of the Stranger | 3278 | 51 | 15.6 | 25 | 0.98 | first time 2.0, like a/the 2.0, Not X but Y 1.8 |
| 17 | Ch07 | Horses in Wet Sand | 2859 | 56 | 19.6 | 14 | 0.96 | something X 2.1 |
| 18 | Ch16 | Building a New Army | 5713 | 112 | 19.6 | 13 | 0.95 | something X 1.6 |
| 19 | Ch05 | Road to Travancore | 2001 | 32 | 16.0 | 24 | 0.94 | something X 1.5 |
| 20 | Ch23 | First Campaign for the Tiger | 5094 | 145 | 28.5 | 4 | 0.93 | short final 1.7 |
| 21 | Ch03 | The Choice in the Storm | 2837 | 47 | 16.6 | 22 | 0.91 | Not X but Y 1.9, like a/the 1.9, short final 1.5 |
| 22 | Ch14 | The Siege of Colachel | 2639 | 46 | 17.4 | 19 | 0.90 | that moment 1.8, short final 1.6 |
| 23 | Ch25 | Ramayyan's Test | 3240 | 90 | 27.8 | 5 | 0.88 | 1-sent para 1.6, Not-opener 1.6, soft adv. 1.6 |
| 24 | Ch11 | Dutch on the Horizon | 6007 | 113 | 18.8 | 17 | 0.87 | that moment 1.6 |
| 25 | Ch24 | Under De Lannoy's Standard | 8306 | 184 | 22.2 | 11 | 0.86 |  |
| 26 | Ch13 | The Eve of Colachel | 4399 | 74 | 16.8 | 21 | 0.85 | weight of 1.6 |
| 27 | Ch12 | The Shadow from Arcot | 2010 | 31 | 15.4 | 27 | 0.84 | somehow 1.8 |
| 28 | Ch06 | The Coastal Hall | 2703 | 41 | 15.2 | 28 | 0.80 |  |

## 2. Style-sheet ration check

Counts against the per-chapter limits in `STYLE_SHEET.md` (sections 1 and 2). `n (+k)` means n found, k over the limit. The Not-but family is allowed once, in dialogue only, so every narration use is over. 'Vague depth words' groups the weight of, something X, etched, somehow, in that moment, a sense of, for the first time and the stock atmosphere phrases (some 'first time' uses may be literal and allowed). 'Verbless fragments' is a heuristic (narration sentences of up to 8 words with no subject pronoun and no common verb form), so treat it as a pointer, not a verdict. **Excess** is the minimum number of edits that chapter needs to meet the sheet.

| Chapter | Not-but family (1, dialogue only) | as if / as though (1) | like a / the (2) | slowly / quietly / softly (2) | narration questions (1) | verbless fragments (3) | triads (0) | vague depth words (0) | Excess |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ch01 | 5 (+4) | 2 (+1) | 1 | 3 (+1) | 1 | 5 (+2) | 2 (+2) | 3 (+3) | **13** |
| Ch02 | 5 (+4) | 2 (+1) | 3 (+1) | 4 (+2) | 0 | 5 (+2) | 1 (+1) | 2 (+2) | **13** |
| Ch03 | 6 (+6) | 2 (+1) | 6 (+4) | 0 | 0 | 13 (+10) | 0 | 1 (+1) | **22** |
| Ch04 | 3 (+2) | 1 | 1 | 3 (+1) | 1 | 12 (+9) | 1 (+1) | 3 (+3) | **16** |
| Ch05 | 5 (+4) | 1 | 2 | 2 | 0 | 3 | 1 (+1) | 3 (+3) | **8** |
| Ch06 | 3 (+2) | 3 (+2) | 0 | 3 (+1) | 0 | 2 | 0 | 2 (+2) | **7** |
| Ch07 | 4 (+3) | 3 (+2) | 4 (+2) | 5 (+3) | 0 | 10 (+7) | 0 | 4 (+4) | **21** |
| Ch08 | 13 (+12) | 4 (+3) | 5 (+3) | 2 | 0 | 2 | 0 | 1 (+1) | **19** |
| Ch09 | 6 (+5) | 5 (+4) | 3 (+1) | 7 (+5) | 0 | 2 | 0 | 2 (+2) | **17** |
| Ch10 | 8 (+7) | 6 (+5) | 0 | 0 | 0 | 9 (+6) | 1 (+1) | 2 (+2) | **21** |
| Ch11 | 9 (+8) | 5 (+4) | 3 (+1) | 6 (+4) | 0 | 13 (+10) | 1 (+1) | 5 (+5) | **33** |
| Ch12 | 2 (+1) | 1 | 0 | 2 | 0 | 3 | 0 | 1 (+1) | **2** |
| Ch13 | 9 (+8) | 3 (+2) | 6 (+4) | 5 (+3) | 0 | 0 | 0 | 3 (+3) | **20** |
| Ch14 | 3 (+3) | 1 | 2 | 2 | 0 | 6 (+3) | 0 | 2 (+2) | **8** |
| Ch15 | 11 (+10) | 3 (+2) | 6 (+4) | 7 (+5) | 0 | 7 (+4) | 1 (+1) | 2 (+2) | **28** |
| Ch16 | 19 (+18) | 4 (+3) | 4 (+2) | 6 (+4) | 0 | 11 (+8) | 0 | 4 (+4) | **39** |
| Ch17 | 11 (+10) | 1 | 7 (+5) | 1 | 0 | 3 | 0 | 3 (+3) | **18** |
| Ch18 | 5 (+4) | 4 (+3) | 0 | 3 (+1) | 1 | 11 (+8) | 1 (+1) | 1 (+1) | **18** |
| Ch19 | 7 (+7) | 3 (+2) | 3 (+1) | 2 | 2 (+1) | 18 (+15) | 1 (+1) | 2 (+2) | **29** |
| Ch20 | 13 (+12) | 7 (+6) | 5 (+3) | 4 (+2) | 2 (+1) | 12 (+9) | 0 | 9 (+9) | **42** |
| Ch21 | 2 (+1) | 1 | 1 | 2 | 0 | 34 (+31) | 6 (+6) | 2 (+2) | **40** |
| Ch22 | 13 (+12) | 2 (+1) | 6 (+4) | 5 (+3) | 0 | 15 (+12) | 2 (+2) | 2 (+2) | **36** |
| Ch23 | 13 (+12) | 5 (+4) | 4 (+2) | 5 (+3) | 0 | 18 (+15) | 1 (+1) | 1 (+1) | **38** |
| Ch24 | 21 (+20) | 6 (+5) | 10 (+8) | 8 (+6) | 0 | 12 (+9) | 0 | 2 (+2) | **50** |
| Ch25 | 8 (+7) | 1 | 0 | 7 (+5) | 0 | 11 (+8) | 0 | 1 (+1) | **21** |
| Ch26 | 6 (+5) | 1 | 2 | 4 (+2) | 0 | 6 (+3) | 0 | 4 (+4) | **14** |
| Ch27 | 5 (+4) | 0 | 4 (+2) | 2 | 0 | 16 (+13) | 1 (+1) | 1 (+1) | **21** |
| Ch28 | 12 (+11) | 2 (+1) | 1 | 1 | 2 (+1) | 17 (+14) | 2 (+2) | 6 (+6) | **35** |
| **Book** | 227 (+202) | 79 (+52) | 89 (+47) | 101 (+51) | 9 (+3) | 276 (+198) | 22 (+22) | 74 (+74) | **649** |

## 3. Hot-spot paragraphs

The 30 paragraphs where marker hits (core and extended, excluding the one-sentence paragraph count) cluster most: a worklist for the line edit. **Score** = distinct marker kinds + 0.5 for each repeat of a kind, so a paragraph mixing several tics outranks one long fragment list. Ties go to the shorter paragraph.

| Where | Score | Hits | Words | Markers | Opening |
|---|---:|---:|---:|---|---|
| Ch21:67 | 9.5 | 15 | 41 | fragments x9, modern words x3, triads x2, short final | Elayadathu Swaroopam (Kottarakkara). Chief: confined. Health: declining. Succession: dispu... |
| Ch21:59 | 9.5 | 16 | 81 | fragments x13, triads x2, short final | Padmini Amma. Landholdings. Kin ties. Temper. He had already noted her heir in that tight ... |
| Ch19:45 | 6.0 | 8 | 14 | fragments x4, Not-opener x2, triads, short final | Not a report. Not a record. A story. Yet stories carry their own weight. |
| Ch28:7 | 5.5 | 7 | 11 | fragments x3, Not-opener x2, something X, short final | Not for war council. Not for treaty. For something else entirely. |
| Ch02:35 | 5.5 | 6 | 38 | fragments x2, X, not Y, short final, perhaps, jaw | Instead, his jaw tightened. His hand rose, almost involuntarily, and made a small sign of ... |
| Ch10:195 | 5.0 | 8 | 26 | fragments x7, short final | Temple to market. Market to training ground. Training ground to backwaters. Backwaters to ... |
| Ch04:129 | 5.0 | 5 | 57 | short final, eyes/gaze +verb, long moment, said nothing, the way he | His eyes moved over me the way a horse trader's eyes move over new stock. He noted the bra... |
| Ch18:241 | 4.5 | 6 | 12 | fragments x4, triads, short final | I felt the room tighten around those names. Pune. English. Ally. Threat. |
| Ch21:201 | 4.5 | 6 | 15 | fragments x4, triads, short final | Of my line in it. Of Revathi's. Of Padmini's. Of Lannoy's. Of the king's own. |
| Ch28:183 | 4.5 | 6 | 15 | fragments x4, triads, short final | He gestured at the kingdom around us. The forts. The walls. The roads. The army. |
| Ch11:169 | 4.5 | 6 | 16 | fragments x4, Not-opener, short final | Not the same men from the ships. Envoys. Negotiators. Men with account books and careful s... |
| Ch15:93 | 4.5 | 5 | 31 | fragments x2, Not X but Y, triads, lesson | His crew had begun unloading the second boat. It was not salvage, I realised, but supplies... |
| Ch22:87 | 4.5 | 6 | 37 | fragments x4, triads, short final | He lifted the brass plate until the lamp's light touched the heir's face and spoke in a lo... |
| Ch28:75 | 4.5 | 6 | 37 | fragments x3, Not-opener x2, triads | A temple attendant stepped forward, carrying something that made the nobles shift and murm... |
| Ch05:175 | 4.0 | 5 | 3 | fragments x3, triads, short final | Horses. Guns. Storms. |
| Ch22:61 | 4.0 | 5 | 7 | fragments x3, triads, short final | Count the exits. The shadows. The people. |
| Ch23:209 | 4.0 | 5 | 9 | fragments x3, triads, short final | No neat lines. No open beach. No clear horizon. |
| Ch21:39 | 4.0 | 5 | 12 | fragments x3, triads, short final | Each name had lines of notes beside it. Places. Dates. Short phrases. |
| Ch23:193 | 4.0 | 5 | 12 | Not-opener x2, fragments x2, short final | Not cook smoke. Not temple lamps. Thick, black columns that meant burning. |
| Ch18:119 | 4.0 | 5 | 21 | fragments x3, short final, somewhere | The threat was clear. Somewhere, someone the Dutch could use was waiting. A claim. A griev... |
| Ch03:177 | 4.0 | 6 | 33 | fragments x5, short final | The broken mast. The men at the pumps. The open sea beyond, white-capped and hungry. Kesha... |
| Ch02:25 | 4.0 | 5 | 40 | fragments x3, triads, short final | The climb from the dungeon to the world of light was like being born through a tunnel of s... |
| Ch23:69 | 4.0 | 4 | 53 | as if, short final, fragments, perhaps | He steadied the child with an easy smile, then caught my eye and tipped his head, as if to... |
| Ch19:147 | 3.5 | 4 | 5 | fragments x2, Not-opener, short final | Not mistrust exactly. More calculation. |
| Ch14:111 | 3.5 | 4 | 19 | fragments x2, Not-opener, short final | Through the smoke and flame, I saw movement. Blue coats, grey coats, emerged from the wrec... |
| Ch11:267 | 3.5 | 5 | 23 | fragments x4, triads | I filed the name away. Kottarakkara. Elayadathu. Revathi's stillness. The king's jaw. Some... |
| Ch23:335 | 3.5 | 4 | 23 | fragments x2, Not-opener, something in | “You were thorough,” she said. Her voice was steady, but there was a flicker of something ... |
| Ch28:255 | 3.5 | 5 | 27 | fragments x4, short final | I thought of the map in the war hall, with its many colours. Red for Mysore. Black for the... |
| Ch04:99 | 3.5 | 4 | 28 | fragments x2, something X, narr. ? | The kapitan. A local headman, or something more? The word carried more weight here than it... |
| Ch27:13 | 3.5 | 5 | 30 | fragments x4, triads | And all around the coast, in blue: the Europeans. Dutch. Portuguese. British. French. Each... |

## 4. Top 40 cross-chapter repeated phrases

Maximal repeated word runs of 5 to 10 words (longer runs are merged and shown whole), found in 2 or more chapters. Sentence ends and proper names break a phrase, headings are excluded, and a phrase needs at least two content words. Ranked by **score** = uses x distinctiveness x sqrt(chapters), where distinctiveness sums ln(1 + chapters / chapters-containing-word) over the phrase's content words, so rare, specific wording and wide spread both push a phrase up while common filler sinks. 154 phrases qualify overall: 152 cross-chapter, 2 repeated 3+ times inside one chapter only. 264 words were treated as names.

| # | Phrase | Words | Uses | Chapters | In speech | Score | Locations |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | washed up on this coast | 5 | 8 | 4 | 5 | 31.1 | Ch16:21d,77d,153,433; Ch17:263d,265d; Ch25:234d; Ch27:61 |
| 2 | for the first time since | 5 | 7 | 7 | 0 | 26.4 | Ch01:107; Ch03:117; Ch06:187; Ch16:153; Ch20:412; Ch21:121; Ch22:409 |
| 3 | she said inclining her head the smallest fraction | 8 | 2 | 2 | 0 | 21.6 | Ch09:68; Ch20:67 |
| 4 | its wooden pillars carved with curling | 6 | 2 | 2 | 0 | 18.7 | Ch05:125; Ch06:21 |
| 5 | the smell of ghee and | 5 | 4 | 4 | 0 | 18.6 | Ch10:21; Ch23:67; Ch27:33; Ch28:9 |
| 6 | stood like a deer in torchlight | 6 | 2 | 2 | 1 | 17.5 | Ch22:109; Ch24:491d |
| 7 | startling birds from the trees | 5 | 2 | 2 | 0 | 17.2 | Ch16:417; Ch23:271 |
| 8 | a ghost of a smile | 5 | 3 | 3 | 0 | 16.5 | Ch20:85; Ch24:495; Ch28:227 |
| 9 | this kingdom uses what it finds | 6 | 2 | 2 | 1 | 16.1 | Ch25:318d; Ch28:243 |
| 10 | men who do not fight are trampled | 7 | 3 | 2 | 3 | 15.7 | Ch01:73d; Ch24:335d,365d |
| 11 | the sign of the cross | 5 | 4 | 2 | 1 | 15.7 | Ch24:311,355d,655; Ch25:236 |
| 12 | carry news as well as goods | 6 | 2 | 2 | 2 | 15.1 | Ch05:63d; Ch10:71d |
| 13 | the boys in the kalari | 5 | 3 | 3 | 0 | 14.3 | Ch09:162; Ch10:41; Ch16:25 |
| 14 | dressed in her finest white | 5 | 2 | 2 | 0 | 14.2 | Ch17:11; Ch20:214 |
| 15 | the wind blows in circles | 5 | 2 | 2 | 1 | 13.7 | Ch18:247d; Ch19:81 |
| 16 | up from his palm leaves | 5 | 4 | 4 | 0 | 13.6 | Ch07:119; Ch08:15; Ch13:103; Ch26:273 |
| 17 | on the southeastern frontier where | 5 | 2 | 2 | 0 | 13.5 | Ch11:149; Ch12:57 |
| 18 | worn smooth by generations of | 5 | 2 | 2 | 0 | 13.2 | Ch08:109; Ch24:497 |
| 19 | afterward she lay with her head on my chest | 9 | 2 | 2 | 0 | 13.0 | Ch17:257; Ch20:386 |
| 20 | the lords of the eight houses | 6 | 2 | 2 | 2 | 13.0 | Ch10:151d; Ch17:67d |
| 21 | with one foot in each river | 6 | 3 | 3 | 3 | 12.9 | Ch19:153d; Ch22:373d; Ch28:129d |
| 22 | she reached up and unpinned her hair | 7 | 2 | 2 | 0 | 12.9 | Ch16:119; Ch20:356 |
| 23 | the diwan inclined his head | 5 | 2 | 2 | 0 | 12.4 | Ch06:161; Ch07:105 |
| 24 | the boy on the palm tower | 6 | 2 | 2 | 0 | 11.8 | Ch13:11; Ch25:130 |
| 25 | an entry in a book | 5 | 2 | 2 | 1 | 11.8 | Ch01:7; Ch16:369d |
| 26 | the corner of her mouth | 5 | 3 | 3 | 0 | 11.7 | Ch04:95; Ch09:230; Ch17:223 |
| 27 | candles for a son who | 5 | 2 | 2 | 2 | 11.7 | Ch16:377d; Ch24:209d |
| 28 | for a fraction of a heartbeat | 6 | 3 | 2 | 0 | 11.7 | Ch11:281; Ch22:127,197 |
| 29 | he jerked his chin toward | 5 | 2 | 2 | 0 | 11.5 | Ch03:93; Ch05:115 |
| 30 | we reined in on a ridge | 6 | 2 | 2 | 0 | 11.5 | Ch23:249; Ch26:95 |
| 31 | at the far end on a slightly raised | 8 | 2 | 2 | 0 | 11.4 | Ch05:125; Ch06:37 |
| 32 | damp out better than canvas | 5 | 2 | 2 | 1 | 11.4 | Ch11:355d; Ch14:105 |
| 33 | took our people as slaves | 5 | 2 | 2 | 2 | 11.3 | Ch14:157d; Ch15:35d |
| 34 | the man they called kapitan | 5 | 2 | 2 | 0 | 11.3 | Ch04:127; Ch05:3 |
| 35 | the first time i saw | 5 | 3 | 3 | 0 | 11.3 | Ch08:45; Ch11:11; Ch17:137 |
| 36 | the nape of her neck | 5 | 2 | 2 | 0 | 11.1 | Ch08:65; Ch20:232 |
| 37 | under the jackfruit tree listening to | 6 | 2 | 2 | 0 | 11.1 | Ch08:231; Ch10:193 |
| 38 | horses to dance with muskets | 5 | 2 | 2 | 2 | 11.0 | Ch17:27d; Ch24:697d |
| 39 | voice dropping to a whisper that | 6 | 2 | 2 | 0 | 11.0 | Ch13:299; Ch23:507 |
| 40 | said his finger tracing the | 5 | 2 | 2 | 0 | 10.9 | Ch13:93; Ch27:15 |

**Repeated 3+ times inside a single chapter:**

| Phrase | Uses | Locations |
|---|---:|---|
| made the sign of the cross | 3 | Ch24:311,355d,655 |
| know what it means to | 3 | Ch24:549d,549d,731d |

## 5. Tic markers per chapter

### 5.1 Marker definitions

| Key | Column | Marker | What counts | Scope |
|---|---|---|---|---|
| not_but | Not X but Y | Not X, but Y | 'not ... but' within 8 words in one clause; skips 'did/could/would not ... but' | all text |
| not_opener | Not-opener | 'Not ...' sentence opener | sentence starting with Not that has no 'but' turn (the 'Not X. Y.' fragment) | all text |
| comma_not | X, not Y | 'X, not Y' correction | ', not a/the/in/for/because...' outside a Not-but span | all text |
| as_if | as if | as if | every 'as if' | all text |
| as_though | as though | as though | every 'as though' | all text |
| like_a | like a/the | like a / like the | 'like a/an/the'; skips verb use after would/did/not/I/you/we/they/to | all text |
| soft_adverbs | soft adv. | slowly / quietly / softly / carefully | the four soft adverbs | all text |
| weight_of | weight of | the weight of | 'the weight of' | all text |
| something_x | something X | something older / deeper / else | 'something' + older, deeper, else, larger, greater, heavier, darker, stranger, harder, colder, more | all text |
| first_time | first time | for the first time | 'for the first time' | all text |
| etched | etched | etched | etch, etched, etching | all text |
| somehow | somehow | somehow | 'somehow' | all text |
| in_that_moment | that moment | in that moment | 'in that/this moment/instant' | all text |
| sense_of | a sense of | a sense of | 'a sense of' | all text |
| triad | triads | three-fragment list | run of 3+ narration sentences of 1 to 3 words each ('Horses. Guns. Storms.') | narration |
| one_sentence_para | 1-sent para | one-sentence paragraph | narration paragraph (no quoted speech) that is a single sentence | narration |
| short_para_final | short final | short paragraph-final sentence | last sentence under 8 words in a narration paragraph of 2+ sentences (the kicker) | narration |
| rhetorical_q | narr. ? | rhetorical question in narration | narration sentence (outside quotes) ending in '?' | narration |

### 5.2 Book totals

| Marker | Total | Per 1000 | Chapters | Peak chapter | In speech |
|---|---:|---:|---:|---|---:|
| Not X, but Y | 86 | 0.91 | 25/28 | Ch22 (9) | 12% |
| 'Not ...' sentence opener | 100 | 1.06 | 25/28 | Ch24 (11) | 65% |
| 'X, not Y' correction | 41 | 0.44 | 19/28 | Ch08 (5) | 56% |
| as if | 79 | 0.84 | 27/28 | Ch20 (7) | 22% |
| as though | 0 | 0.00 | 0/28 |  |  |
| like a / like the | 89 | 0.95 | 23/28 | Ch24 (10) | 27% |
| slowly / quietly / softly / carefully | 119 | 1.27 | 26/28 | Ch24 (12) | 9% |
| the weight of | 19 | 0.20 | 13/28 | Ch09 (2) | 26% |
| something older / deeper / else | 14 | 0.15 | 9/28 | Ch04 (3) | 14% |
| for the first time | 15 | 0.16 | 11/28 | Ch20 (4) | 0% |
| etched | 1 | 0.01 | 1/28 | Ch27 (1) | 0% |
| somehow | 4 | 0.04 | 4/28 | Ch08 (1) | 0% |
| in that moment | 4 | 0.04 | 4/28 | Ch11 (1) | 25% |
| a sense of | 0 | 0.00 | 0/28 |  |  |
| three-fragment list | 22 | 0.23 | 14/28 | Ch21 (6) | 0% |
| one-sentence paragraph | 1279 | 13.60 | 28/28 | Ch24 (119) | 0% |
| short paragraph-final sentence | 186 | 1.98 | 28/28 | Ch23 (18) | 0% |
| rhetorical question in narration | 9 | 0.10 | 6/28 | Ch19 (2) | 0% |
| verbless fragment (ext.) | 276 | 2.93 | 27/28 | Ch21 (34) | 0% |
| the kind of / the sort of (ext.) | 5 | 0.05 | 5/28 | Ch01 (1) | 20% |
| stock atmosphere (ext.) | 17 | 0.18 | 13/28 | Ch05 (2) | 0% |
| gently / silently (ext.) | 8 | 0.09 | 7/28 | Ch08 (2) | 0% |
| somewhere (ext.) | 45 | 0.48 | 21/28 | Ch01 (5) | 13% |
| perhaps (ext.) | 51 | 0.54 | 25/28 | Ch27 (6) | 55% |
| nodded (ext.) | 36 | 0.38 | 18/28 | Ch24 (9) | 0% |
| jaw tightened (ext.) | 14 | 0.15 | 11/28 | Ch18 (2) | 0% |
| eyes / gaze + motion verb (ext.) | 44 | 0.47 | 19/28 | Ch11 (9) | 0% |
| appraising look (ext.) | 18 | 0.19 | 13/28 | Ch08 (3) | 0% |
| a long moment (ext.) | 10 | 0.11 | 9/28 | Ch24 (2) | 0% |
| said nothing / did not answer (ext.) | 10 | 0.11 | 10/28 | Ch01 (1) | 0% |
| something in his eyes / voice (ext.) | 3 | 0.03 | 3/28 | Ch15 (1) | 0% |
| the way he / she ... (ext.) | 28 | 0.30 | 16/28 | Ch24 (4) | 14% |
| narrated lesson (ext.) | 27 | 0.29 | 16/28 | Ch10 (6) | 11% |
| for now / that was enough (ext.) | 18 | 0.19 | 12/28 | Ch19 (4) | 44% |
| modern register (ext.) | 19 | 0.20 | 11/28 | Ch16 (3) | 11% |

Soft adverb breakdown: slowly 40, quietly 32, softly 29, carefully 18.

### 5.3 Contrast and simile markers

Each cell: count (per 1000 words).

| Chapter | Words | Not X but Y | Not-opener | X, not Y | as if | as though | like a/the |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ch01 | 1941 | 2 (1.0) | 3 (1.5) | 0 | 2 (1.0) | 0 | 1 (0.5) |
| Ch02 | 1890 | 0 | 2 (1.1) | 3 (1.6) | 2 (1.1) | 0 | 3 (1.6) |
| Ch03 | 2837 | 6 (2.1) | 0 | 0 | 2 (0.7) | 0 | 6 (2.1) |
| Ch04 | 1704 | 1 (0.6) | 2 (1.2) | 0 | 1 (0.6) | 0 | 1 (0.6) |
| Ch05 | 2001 | 3 (1.5) | 2 (1.0) | 0 | 1 (0.5) | 0 | 2 (1.0) |
| Ch06 | 2703 | 3 (1.1) | 0 | 0 | 3 (1.1) | 0 | 0 |
| Ch07 | 2859 | 0 | 2 (0.7) | 2 (0.7) | 3 (1.0) | 0 | 4 (1.4) |
| Ch08 | 3420 | 4 (1.2) | 4 (1.2) | 5 (1.5) | 4 (1.2) | 0 | 5 (1.5) |
| Ch09 | 3056 | 1 (0.3) | 4 (1.3) | 1 (0.3) | 5 (1.6) | 0 | 3 (1.0) |
| Ch10 | 2579 | 5 (1.9) | 3 (1.2) | 0 | 6 (2.3) | 0 | 0 |
| Ch11 | 6007 | 3 (0.5) | 4 (0.7) | 2 (0.3) | 5 (0.8) | 0 | 3 (0.5) |
| Ch12 | 2010 | 1 (0.5) | 0 | 1 (0.5) | 1 (0.5) | 0 | 0 |
| Ch13 | 4399 | 4 (0.9) | 3 (0.7) | 2 (0.5) | 3 (0.7) | 0 | 6 (1.4) |
| Ch14 | 2639 | 1 (0.4) | 1 (0.4) | 1 (0.4) | 1 (0.4) | 0 | 2 (0.8) |
| Ch15 | 3945 | 6 (1.5) | 3 (0.8) | 2 (0.5) | 3 (0.8) | 0 | 6 (1.5) |
| Ch16 | 5713 | 6 (1.1) | 9 (1.6) | 4 (0.7) | 4 (0.7) | 0 | 4 (0.7) |
| Ch17 | 3278 | 6 (1.8) | 3 (0.9) | 2 (0.6) | 1 (0.3) | 0 | 7 (2.1) |
| Ch18 | 2643 | 2 (0.8) | 2 (0.8) | 1 (0.4) | 4 (1.5) | 0 | 0 |
| Ch19 | 2875 | 3 (1.0) | 4 (1.4) | 0 | 3 (1.0) | 0 | 3 (1.0) |
| Ch20 | 4569 | 4 (0.9) | 5 (1.1) | 4 (0.9) | 7 (1.5) | 0 | 5 (1.1) |
| Ch21 | 2135 | 1 (0.5) | 1 (0.5) | 0 | 1 (0.5) | 0 | 1 (0.5) |
| Ch22 | 3795 | 9 (2.4) | 4 (1.1) | 0 | 2 (0.5) | 0 | 6 (1.6) |
| Ch23 | 5094 | 3 (0.6) | 7 (1.4) | 3 (0.6) | 5 (1.0) | 0 | 4 (0.8) |
| Ch24 | 8306 | 8 (1.0) | 11 (1.3) | 2 (0.2) | 6 (0.7) | 0 | 10 (1.2) |
| Ch25 | 3240 | 1 (0.3) | 6 (1.9) | 1 (0.3) | 1 (0.3) | 0 | 0 |
| Ch26 | 2597 | 1 (0.4) | 2 (0.8) | 3 (1.2) | 1 (0.4) | 0 | 2 (0.8) |
| Ch27 | 2321 | 2 (0.9) | 2 (0.9) | 1 (0.4) | 0 | 0 | 4 (1.7) |
| Ch28 | 3487 | 0 | 11 (3.2) | 1 (0.3) | 2 (0.6) | 0 | 1 (0.3) |
| **Book** | 94043 | 86 (0.9) | 100 (1.1) | 41 (0.4) | 79 (0.8) | 0 | 89 (0.9) |

### 5.4 Soft adverbs and vague depth words

Each cell: count (per 1000 words).

| Chapter | Words | soft adv. | weight of | something X | first time | etched | somehow | that moment | a sense of |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ch01 | 1941 | 4 (2.1) | 0 | 1 (0.5) | 1 (0.5) | 0 | 0 | 0 | 0 |
| Ch02 | 1890 | 5 (2.6) | 1 (0.5) | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch03 | 2837 | 0 | 0 | 0 | 1 (0.4) | 0 | 0 | 0 | 0 |
| Ch04 | 1704 | 4 (2.3) | 0 | 3 (1.8) | 0 | 0 | 0 | 0 | 0 |
| Ch05 | 2001 | 2 (1.0) | 0 | 1 (0.5) | 0 | 0 | 0 | 0 | 0 |
| Ch06 | 2703 | 3 (1.1) | 0 | 0 | 1 (0.4) | 0 | 0 | 0 | 0 |
| Ch07 | 2859 | 5 (1.7) | 0 | 2 (0.7) | 0 | 0 | 0 | 0 | 0 |
| Ch08 | 3420 | 4 (1.2) | 0 | 0 | 0 | 0 | 1 (0.3) | 0 | 0 |
| Ch09 | 3056 | 9 (2.9) | 2 (0.7) | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch10 | 2579 | 0 | 2 (0.8) | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch11 | 6007 | 8 (1.3) | 2 (0.3) | 0 | 0 | 0 | 0 | 1 (0.2) | 0 |
| Ch12 | 2010 | 3 (1.5) | 0 | 0 | 0 | 0 | 1 (0.5) | 0 | 0 |
| Ch13 | 4399 | 5 (1.1) | 2 (0.5) | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch14 | 2639 | 2 (0.8) | 1 (0.4) | 0 | 0 | 0 | 0 | 1 (0.4) | 0 |
| Ch15 | 3945 | 7 (1.8) | 2 (0.5) | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch16 | 5713 | 6 (1.1) | 1 (0.2) | 2 (0.4) | 1 (0.2) | 0 | 0 | 0 | 0 |
| Ch17 | 3278 | 1 (0.3) | 1 (0.3) | 0 | 2 (0.6) | 0 | 0 | 0 | 0 |
| Ch18 | 2643 | 4 (1.5) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch19 | 2875 | 3 (1.0) | 0 | 0 | 1 (0.3) | 0 | 1 (0.3) | 0 | 0 |
| Ch20 | 4569 | 4 (0.9) | 2 (0.4) | 2 (0.4) | 4 (0.9) | 0 | 0 | 0 | 0 |
| Ch21 | 2135 | 2 (0.9) | 1 (0.5) | 0 | 1 (0.5) | 0 | 0 | 0 | 0 |
| Ch22 | 3795 | 5 (1.3) | 0 | 0 | 1 (0.3) | 0 | 0 | 0 | 0 |
| Ch23 | 5094 | 5 (1.0) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch24 | 8306 | 12 (1.4) | 0 | 1 (0.1) | 0 | 0 | 0 | 1 (0.1) | 0 |
| Ch25 | 3240 | 7 (2.2) | 0 | 0 | 1 (0.3) | 0 | 0 | 0 | 0 |
| Ch26 | 2597 | 5 (1.9) | 1 (0.4) | 1 (0.4) | 0 | 0 | 0 | 1 (0.4) | 0 |
| Ch27 | 2321 | 2 (0.9) | 0 | 0 | 0 | 1 (0.4) | 0 | 0 | 0 |
| Ch28 | 3487 | 2 (0.6) | 1 (0.3) | 1 (0.3) | 1 (0.3) | 0 | 1 (0.3) | 0 | 0 |
| **Book** | 94043 | 119 (1.3) | 19 (0.2) | 14 (0.1) | 15 (0.2) | 1 (0.0) | 4 (0.0) | 4 (0.0) | 0 |

### 5.5 Structural markers

Each cell: count (per 1000 words).

| Chapter | Words | triads | 1-sent para | short final | narr. ? |
|---|---:|---:|---:|---:|---:|
| Ch01 | 1941 | 2 (1.0) | 13 (6.7) | 3 (1.5) | 1 (0.5) |
| Ch02 | 1890 | 1 (0.5) | 12 (6.3) | 4 (2.1) | 0 |
| Ch03 | 2837 | 0 | 23 (8.1) | 9 (3.2) | 0 |
| Ch04 | 1704 | 1 (0.6) | 8 (4.7) | 6 (3.5) | 1 (0.6) |
| Ch05 | 2001 | 1 (0.5) | 17 (8.5) | 3 (1.5) | 0 |
| Ch06 | 2703 | 0 | 27 (10.0) | 4 (1.5) | 0 |
| Ch07 | 2859 | 0 | 34 (11.9) | 4 (1.4) | 0 |
| Ch08 | 3420 | 0 | 23 (6.7) | 3 (0.9) | 0 |
| Ch09 | 3056 | 0 | 35 (11.5) | 5 (1.6) | 0 |
| Ch10 | 2579 | 1 (0.4) | 30 (11.6) | 2 (0.8) | 0 |
| Ch11 | 6007 | 1 (0.2) | 72 (12.0) | 12 (2.0) | 0 |
| Ch12 | 2010 | 0 | 21 (10.4) | 3 (1.5) | 0 |
| Ch13 | 4399 | 0 | 46 (10.5) | 3 (0.7) | 0 |
| Ch14 | 2639 | 0 | 27 (10.2) | 9 (3.4) | 0 |
| Ch15 | 3945 | 1 (0.3) | 36 (9.1) | 10 (2.5) | 0 |
| Ch16 | 5713 | 0 | 69 (12.1) | 6 (1.1) | 0 |
| Ch17 | 3278 | 0 | 26 (7.9) | 2 (0.6) | 0 |
| Ch18 | 2643 | 1 (0.4) | 45 (17.0) | 8 (3.0) | 1 (0.4) |
| Ch19 | 2875 | 1 (0.3) | 51 (17.7) | 11 (3.8) | 2 (0.7) |
| Ch20 | 4569 | 0 | 59 (12.9) | 6 (1.3) | 2 (0.4) |
| Ch21 | 2135 | 6 (2.8) | 38 (17.8) | 7 (3.3) | 0 |
| Ch22 | 3795 | 2 (0.5) | 116 (30.6) | 7 (1.8) | 0 |
| Ch23 | 5094 | 1 (0.2) | 99 (19.4) | 18 (3.5) | 0 |
| Ch24 | 8306 | 0 | 119 (14.3) | 14 (1.7) | 0 |
| Ch25 | 3240 | 0 | 70 (21.6) | 3 (0.9) | 0 |
| Ch26 | 2597 | 0 | 74 (28.5) | 6 (2.3) | 0 |
| Ch27 | 2321 | 1 (0.4) | 32 (13.8) | 7 (3.0) | 0 |
| Ch28 | 3487 | 2 (0.6) | 57 (16.3) | 11 (3.2) | 2 (0.6) |
| **Book** | 94043 | 22 (0.2) | 1279 (13.6) | 186 (2.0) | 9 (0.1) |

### 5.6 Extended markers: stock beats and gestures

Each cell: count (per 1000 words).

| Chapter | Words | nodded | jaw | eyes/gaze +verb | studied me | long moment | said nothing | something in | the way he |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ch01 | 1941 | 0 | 1 (0.5) | 1 (0.5) | 1 (0.5) | 0 | 1 (0.5) | 0 | 3 (1.5) |
| Ch02 | 1890 | 0 | 1 (0.5) | 2 (1.1) | 1 (0.5) | 0 | 0 | 0 | 0 |
| Ch03 | 2837 | 1 (0.4) | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0.4) |
| Ch04 | 1704 | 1 (0.6) | 0 | 2 (1.2) | 0 | 1 (0.6) | 1 (0.6) | 0 | 2 (1.2) |
| Ch05 | 2001 | 1 (0.5) | 0 | 2 (1.0) | 0 | 0 | 0 | 0 | 0 |
| Ch06 | 2703 | 0 | 0 | 2 (0.7) | 1 (0.4) | 0 | 0 | 0 | 0 |
| Ch07 | 2859 | 1 (0.3) | 1 (0.3) | 0 | 0 | 0 | 1 (0.3) | 0 | 1 (0.3) |
| Ch08 | 3420 | 2 (0.6) | 0 | 2 (0.6) | 3 (0.9) | 0 | 0 | 0 | 1 (0.3) |
| Ch09 | 3056 | 0 | 0 | 3 (1.0) | 1 (0.3) | 0 | 0 | 0 | 2 (0.7) |
| Ch10 | 2579 | 1 (0.4) | 0 | 1 (0.4) | 1 (0.4) | 0 | 0 | 0 | 0 |
| Ch11 | 6007 | 1 (0.2) | 1 (0.2) | 9 (1.5) | 0 | 0 | 1 (0.2) | 0 | 1 (0.2) |
| Ch12 | 2010 | 1 (0.5) | 0 | 0 | 1 (0.5) | 1 (0.5) | 1 (0.5) | 0 | 0 |
| Ch13 | 4399 | 2 (0.5) | 0 | 1 (0.2) | 1 (0.2) | 0 | 0 | 0 | 1 (0.2) |
| Ch14 | 2639 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ch15 | 3945 | 4 (1.0) | 0 | 0 | 2 (0.5) | 1 (0.3) | 0 | 1 (0.3) | 0 |
| Ch16 | 5713 | 2 (0.4) | 0 | 1 (0.2) | 0 | 0 | 1 (0.2) | 0 | 3 (0.5) |
| Ch17 | 3278 | 0 | 0 | 1 (0.3) | 0 | 1 (0.3) | 0 | 1 (0.3) | 1 (0.3) |
| Ch18 | 2643 | 0 | 2 (0.8) | 5 (1.9) | 0 | 1 (0.4) | 0 | 0 | 1 (0.4) |
| Ch19 | 2875 | 3 (1.0) | 0 | 0 | 2 (0.7) | 0 | 0 | 0 | 1 (0.3) |
| Ch20 | 4569 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 (0.7) |
| Ch21 | 2135 | 1 (0.5) | 0 | 1 (0.5) | 1 (0.5) | 0 | 0 | 0 | 2 (0.9) |
| Ch22 | 3795 | 1 (0.3) | 1 (0.3) | 2 (0.5) | 0 | 1 (0.3) | 0 | 0 | 0 |
| Ch23 | 5094 | 2 (0.4) | 2 (0.4) | 2 (0.4) | 0 | 1 (0.2) | 1 (0.2) | 1 (0.2) | 0 |
| Ch24 | 8306 | 9 (1.1) | 2 (0.2) | 5 (0.6) | 0 | 2 (0.2) | 1 (0.1) | 0 | 4 (0.5) |
| Ch25 | 3240 | 2 (0.6) | 1 (0.3) | 0 | 2 (0.6) | 0 | 1 (0.3) | 0 | 1 (0.3) |
| Ch26 | 2597 | 1 (0.4) | 1 (0.4) | 1 (0.4) | 0 | 0 | 0 | 0 | 0 |
| Ch27 | 2321 | 0 | 1 (0.4) | 1 (0.4) | 1 (0.4) | 1 (0.4) | 0 | 0 | 0 |
| Ch28 | 3487 | 0 | 0 | 0 | 0 | 0 | 1 (0.3) | 0 | 0 |
| **Book** | 94043 | 36 (0.4) | 14 (0.1) | 44 (0.5) | 18 (0.2) | 10 (0.1) | 10 (0.1) | 3 (0.0) | 28 (0.3) |

### 5.7 Extended markers: vague, summary and modern words

Each cell: count (per 1000 words).

| Chapter | Words | fragments | kind/sort of | stock air | gently/silently | somewhere | perhaps | lesson | for now | modern words |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ch01 | 1941 | 5 (2.6) | 1 (0.5) | 1 (0.5) | 0 | 5 (2.6) | 1 (0.5) | 1 (0.5) | 0 | 0 |
| Ch02 | 1890 | 5 (2.6) | 0 | 1 (0.5) | 0 | 3 (1.6) | 1 (0.5) | 0 | 1 (0.5) | 2 (1.1) |
| Ch03 | 2837 | 13 (4.6) | 0 | 0 | 0 | 2 (0.7) | 1 (0.4) | 1 (0.4) | 0 | 1 (0.4) |
| Ch04 | 1704 | 12 (7.0) | 1 (0.6) | 0 | 1 (0.6) | 2 (1.2) | 3 (1.8) | 1 (0.6) | 1 (0.6) | 0 |
| Ch05 | 2001 | 3 (1.5) | 0 | 2 (1.0) | 0 | 3 (1.5) | 1 (0.5) | 0 | 1 (0.5) | 0 |
| Ch06 | 2703 | 2 (0.7) | 0 | 1 (0.4) | 0 | 3 (1.1) | 1 (0.4) | 0 | 2 (0.7) | 0 |
| Ch07 | 2859 | 10 (3.5) | 0 | 2 (0.7) | 0 | 0 | 1 (0.3) | 1 (0.3) | 0 | 0 |
| Ch08 | 3420 | 2 (0.6) | 0 | 0 | 2 (0.6) | 1 (0.3) | 3 (0.9) | 1 (0.3) | 0 | 0 |
| Ch09 | 3056 | 2 (0.7) | 0 | 0 | 1 (0.3) | 2 (0.7) | 2 (0.7) | 0 | 2 (0.7) | 1 (0.3) |
| Ch10 | 2579 | 9 (3.5) | 0 | 0 | 1 (0.4) | 0 | 0 | 6 (2.3) | 0 | 1 (0.4) |
| Ch11 | 6007 | 13 (2.2) | 1 (0.2) | 2 (0.3) | 0 | 2 (0.3) | 1 (0.2) | 0 | 0 | 0 |
| Ch12 | 2010 | 3 (1.5) | 0 | 0 | 0 | 2 (1.0) | 1 (0.5) | 2 (1.0) | 1 (0.5) | 1 (0.5) |
| Ch13 | 4399 | 0 | 0 | 1 (0.2) | 0 | 1 (0.2) | 3 (0.7) | 2 (0.5) | 1 (0.2) | 2 (0.5) |
| Ch14 | 2639 | 6 (2.3) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 (0.8) |
| Ch15 | 3945 | 7 (1.8) | 0 | 0 | 0 | 0 | 3 (0.8) | 1 (0.3) | 0 | 0 |
| Ch16 | 5713 | 11 (1.9) | 0 | 0 | 0 | 2 (0.4) | 1 (0.2) | 1 (0.2) | 2 (0.4) | 3 (0.5) |
| Ch17 | 3278 | 3 (0.9) | 0 | 0 | 1 (0.3) | 1 (0.3) | 2 (0.6) | 2 (0.6) | 1 (0.3) | 0 |
| Ch18 | 2643 | 11 (4.2) | 0 | 1 (0.4) | 0 | 3 (1.1) | 2 (0.8) | 1 (0.4) | 0 | 0 |
| Ch19 | 2875 | 18 (6.3) | 0 | 0 | 0 | 3 (1.0) | 0 | 0 | 4 (1.4) | 0 |
| Ch20 | 4569 | 12 (2.6) | 0 | 1 (0.2) | 0 | 3 (0.7) | 3 (0.7) | 3 (0.7) | 0 | 1 (0.2) |
| Ch21 | 2135 | 34 (15.9) | 0 | 0 | 0 | 1 (0.5) | 1 (0.5) | 0 | 0 | 3 (1.4) |
| Ch22 | 3795 | 15 (4.0) | 0 | 1 (0.3) | 0 | 0 | 1 (0.3) | 1 (0.3) | 1 (0.3) | 2 (0.5) |
| Ch23 | 5094 | 18 (3.5) | 1 (0.2) | 1 (0.2) | 1 (0.2) | 1 (0.2) | 3 (0.6) | 0 | 0 | 0 |
| Ch24 | 8306 | 12 (1.4) | 0 | 0 | 0 | 1 (0.1) | 4 (0.5) | 2 (0.2) | 0 | 0 |
| Ch25 | 3240 | 11 (3.4) | 0 | 0 | 0 | 0 | 2 (0.6) | 0 | 1 (0.3) | 0 |
| Ch26 | 2597 | 6 (2.3) | 0 | 1 (0.4) | 0 | 0 | 2 (0.8) | 0 | 0 | 0 |
| Ch27 | 2321 | 16 (6.9) | 1 (0.4) | 0 | 0 | 1 (0.4) | 6 (2.6) | 0 | 0 | 0 |
| Ch28 | 3487 | 17 (4.9) | 0 | 2 (0.6) | 1 (0.3) | 3 (0.9) | 2 (0.6) | 1 (0.3) | 0 | 0 |
| **Book** | 94043 | 276 (2.9) | 5 (0.1) | 17 (0.2) | 8 (0.1) | 45 (0.5) | 51 (0.5) | 27 (0.3) | 18 (0.2) | 19 (0.2) |

Extended marker definitions: `fragment` = narration sentence of 1 to 8 words with no subject pronoun and no common or -ed verb form ('Together.', 'Fresh men.', 'Not yet.'); heuristic; `kind_of` = 'the/a kind of', 'the/a sort of'; `stock_atmosphere` = hung in the air, thick with, had nothing to do with, another world, the air was thick/heavy; `gently_silently` = 'gently', 'silently'; `somewhere` = vague placing: 'somewhere'; `perhaps` = 'perhaps'; `nodded` = 'nodded', 'nodding'; `jaw` = 'jaw' + tightened, set, clenched, hardened, worked; `eyes_verb` = 'eyes/gaze/glance' + narrowed, flicked, moved, lingered, rested, met, held, ...; `appraising` = studied/measured/weighed/considered/regarded + me/him/her/us/them; `long_moment` = 'a long moment'; `said_nothing` = 'said nothing', 'did not answer/reply/respond', 'made no answer', 'said no more'; `something_in` = 'something in his/her/their/my eyes, voice, face, manner, tone'; `noticing` = 'the way he/she/they/his/the ...'; `lesson` = 'I learned/understood/realised', 'the lesson', 'began to understand'; `provisional_close` = 'for now', 'for the moment', 'that/it was enough'; `modern_register` = modern management or therapy words the style sheet bans for a 1740s narrator: risk assessment, leverage, timeline, strategic, navigate, focus, process, journey, priority, okay, feedback ....

## 6. Repeated images and similes

### 6.1 Image families

All uses of each word family, literal or not. **Figurative** = inside a simile clause (the 8 words after like / as if / as though / as X as) or followed directly by 'of' (a tide of men, the weight of years). Spread lists chapter:count.

| Family | Uses | Chapters | Figurative | Spread | Figurative locations |
|---|---:|---:|---:|---|---|
| weigh / balance | 103 | 26 | 35 | 01:1, 02:6, 03:7, 04:2, 06:2, 07:3, 08:3, 09:6, 10:5, 11:5, 13:7, 14:2, 15:2, 16:3, 17:4, 18:4, 19:5, 20:5, 21:4, 22:7, 23:3, 24:5, 25:5, 26:1, 27:1, 28:5 | Ch02:15, Ch02:49, Ch07:23, Ch08:25, Ch09:44, Ch09:152, Ch10:139, Ch10:151, Ch11:317, Ch11:355, Ch13:189, Ch13:215, Ch13:273, Ch14:65 +19 |
| river / current | 43 | 19 | 6 | 01:1, 02:2, 03:2, 05:1, 06:3, 07:1, 08:1, 11:2, 12:2, 13:3, 14:2, 15:2, 16:2, 19:8, 21:1, 22:5, 23:2, 24:1, 28:2 | Ch02:3, Ch11:303, Ch14:49, Ch19:193, Ch22:409, Ch28:25 |
| storm | 71 | 21 | 5 | 01:1, 02:4, 03:17, 04:3, 05:5, 06:4, 07:3, 08:1, 09:1, 13:3, 14:4, 15:1, 16:5, 17:1, 19:5, 20:1, 21:3, 22:1, 24:4, 25:2, 28:2 | Ch07:145, Ch14:19, Ch16:5, Ch17:3, Ch21:207 |
| shadow | 38 | 19 | 5 | 01:1, 07:1, 08:2, 09:2, 10:1, 11:1, 12:5, 13:3, 14:1, 16:4, 17:4, 19:1, 20:2, 21:1, 22:3, 23:2, 24:1, 26:1, 28:2 | Ch01:75, Ch08:117, Ch10:5, Ch16:59, Ch19:143 |
| tide | 11 | 7 | 4 | 02:1, 03:1, 07:4, 09:1, 11:2, 13:1, 17:1 | Ch03:37, Ch07:77, Ch07:79, Ch09:114 |
| thread / web / knot | 44 | 16 | 4 | 01:2, 03:1, 04:1, 08:2, 09:1, 10:4, 11:3, 14:2, 16:1, 17:3, 18:1, 20:14, 22:2, 24:5, 26:1, 28:1 | Ch01:107, Ch10:175, Ch11:475, Ch24:749 |
| monsoon / rain | 50 | 19 | 4 | 01:4, 03:4, 04:1, 07:5, 09:2, 10:2, 12:1, 13:2, 14:3, 15:1, 16:2, 17:4, 19:1, 21:5, 22:1, 24:2, 25:5, 27:1, 28:4 | Ch07:145, Ch09:152, Ch15:61, Ch17:115 |
| wolf / snake / hawk | 19 | 9 | 4 | 06:1, 07:1, 11:1, 13:8, 14:1, 17:1, 19:1, 20:2, 28:3 | Ch11:91, Ch13:261, Ch20:17 |
| ghost / mask | 13 | 9 | 4 | 07:1, 11:2, 15:2, 19:1, 20:3, 23:1, 24:1, 25:1, 28:1 | Ch15:307, Ch20:85, Ch24:495, Ch28:227 |
| blade / steel | 77 | 20 | 2 | 03:1, 04:1, 06:1, 08:3, 09:2, 11:4, 13:2, 14:3, 15:4, 16:3, 17:8, 18:2, 19:1, 20:3, 21:2, 22:16, 23:10, 24:7, 26:2, 28:2 | Ch11:203, Ch16:159 |
| ledger / debt | 26 | 13 | 2 | 06:1, 10:1, 11:1, 12:1, 13:1, 14:1, 15:1, 16:7, 17:4, 19:2, 21:2, 22:1, 24:3 | Ch11:235, Ch16:405 |
| chain / iron | 103 | 22 | 2 | 01:9, 02:20, 03:32, 05:1, 06:2, 07:1, 08:1, 09:1, 10:1, 11:1, 12:2, 13:2, 15:1, 17:5, 18:1, 19:6, 20:1, 22:2, 23:2, 24:6, 25:4, 28:2 | Ch17:257, Ch18:23 |
| cage / trap / net | 16 | 13 | 2 | 04:1, 05:1, 06:1, 07:1, 09:1, 12:1, 13:1, 14:2, 15:1, 17:1, 22:1, 25:2, 28:2 | Ch06:145, Ch22:333 |
| wound / scar | 62 | 20 | 2 | 02:1, 04:8, 05:4, 06:1, 07:1, 09:5, 10:1, 11:3, 12:2, 13:1, 14:3, 15:3, 16:5, 17:4, 19:2, 20:4, 23:3, 24:3, 26:7, 28:1 | Ch15:133, Ch17:119 |
| salt | 36 | 18 | 2 | 02:2, 03:1, 04:6, 05:1, 06:2, 07:2, 08:3, 09:1, 10:1, 12:1, 13:2, 14:2, 15:1, 18:2, 19:3, 23:1, 24:4, 27:1 | Ch07:209, Ch15:7 |
| tiger | 7 | 6 | 1 | 06:1, 15:1, 17:1, 22:1, 23:2, 28:1 | Ch22:333 |
| fire / ember / ash | 48 | 15 | 1 | 03:1, 05:1, 10:1, 13:5, 14:6, 15:2, 16:1, 20:3, 21:1, 22:6, 23:1, 25:4, 26:10, 27:1, 28:5 | Ch28:289 |
| root / seed | 13 | 9 | 1 | 09:1, 13:1, 15:1, 19:4, 20:1, 21:2, 22:1, 23:1, 24:1 | Ch15:277 |
| forge / anvil | 12 | 9 | 0 | 01:2, 03:3, 06:1, 07:1, 14:1, 17:1, 24:1, 25:1, 27:1 |  |
| game / chess / dice | 8 | 8 | 0 | 01:1, 05:1, 07:1, 12:1, 14:1, 20:1, 27:1, 28:1 |  |

### 6.2 Figurative uses in context

Up to 8 per family, for the families that recur figuratively in 3 or more chapters.

| Family | Where | Context |
|---|---|---|
| weigh / balance | Ch02:15 | ...at my ankles. For a brief moment the weight of the iron vanished and my legs swung... |
| weigh / balance | Ch02:49 | When we reached the harbour the full weight of the Portuguese world pressed in. The... |
| weigh / balance | Ch07:23 | ...ways more than mine, it sat on me like a weight. |
| weigh / balance | Ch08:25 | ...up. His gaze was like a clerk’s scale, weighing gold against brass. |
| weigh / balance | Ch09:44 | ...who carries that name can speak with the weight of many fields behind her. Do not address... |
| weigh / balance | Ch09:152 | ...the name. I did not know the house. The weight of what she was not saying settled into the... |
| weigh / balance | Ch10:139 | ...ride. My head, too, buzzed with the weight of new connections. |
| weigh / balance | Ch10:151 | ...on pikes, some in exile, some under the weight of their own ruined walls. Only after those... |
| river / current | Ch02:3 | ...great church above rang for early Mass, a flood of sound rolling down through stone into... |
| river / current | Ch11:303 | ...Ramayyan guided the flow like a patient river pilot, steering around rocks, nudging here,... |
| river / current | Ch14:49 | He spat a stream of betel juice into the sand. |
| river / current | Ch19:193 | ...like silt finding the riverbed after a flood. I had been fighting the current for years.... |
| river / current | Ch22:409 | ...caught between currents, but like part of a river that had chosen its course. |
| river / current | Ch28:25 | ...the sanctum, their chants low and steady, a river of sound that had flowed here long before... |
| storm | Ch07:145 | ...a black mare with a temper like monsoon lightning and a stride that ate distance. She had... |
| storm | Ch14:19 | There was no grand charge, no thunder of hooves on wet sand as I had imagined in... |
| storm | Ch16:5 | ...not as fine as the mount I had lost in the storm, but steady, patient, willing to learn the... |
| storm | Ch17:3 | ...came to Padmini Amma’s estate not with the thunder of drums or the announcement of heralds,... |
| storm | Ch21:207 | ...against machines like the Dutch company and storm bent confederacies like my own. |
| shadow | Ch01:75 | The priest's mouth twitched, a shadow of something that might almost have been a... |
| shadow | Ch08:117 | ...where men in armour sat, they moved like shadows at the edge, leaving food and vanishing.... |
| shadow | Ch10:5 | ...markets came later, clustering under the shadow of those choices. |
| shadow | Ch16:59 | ...I was lying awake in my room, watching the shadows of palm fronds move across the ceiling. My... |
| shadow | Ch19:143 | The shadows of the Deccan had lengthened into... |
| tide | Ch03:37 | ...like something washed up by a strange tide. Too far to reach. Too close to ignore. |
| tide | Ch07:77 | ...break you. You must come at them like the tide, fast, from the angle they do not expect,... |
| tide | Ch07:79 | Raza Khan wiped his face. “To ride like the tide, one must first not drown in the sand.” |
| tide | Ch09:114 | ...Made them move like the fish I watch at low tide. Ramayyan filled a grove of palm leaves... |
| thread / web / knot | Ch01:107 | ...they dragged me into this fortress a thin thread of hope tugged at me. |
| thread / web / knot | Ch10:175 | ...foreign armies, but against the stubborn knots of the internal map. I learned that a... |
| thread / web / knot | Ch11:475 | ...hold. Some would snap. Either way, the fabric of this coast had been pulled a little... |
| thread / web / knot | Ch24:749 | ...and currency exchanges and the complex web of debts and favours that connected Kochi... |
| monsoon / rain | Ch07:145 | ...Kanka, a black mare with a temper like monsoon lightning and a stride that ate distance.... |
| monsoon / rain | Ch09:152 | ...saying settled into the air between us like monsoon humidity. |
| monsoon / rain | Ch15:61 | ...falling onto the beach sounded like a heavy rain. Some of the men wept. Others stood rigid,... |
| monsoon / rain | Ch17:115 | ...And he broods like an old woman when it rains.” |
| wolf / snake / hawk | Ch11:91 | ...foreign ships hovered off his coast like vultures?" |
| wolf / snake / hawk | Ch13:261 | ...natural stupas, the ancient homes of the serpents, flanked by hundreds of granite idols.... |
| wolf / snake / hawk | Ch20:17 | ...we were doing, circling each other like two hawks who had spotted the same thermal. |
| ghost / mask | Ch15:307 | When he straightened, he looked like a ghost of himself, a European skeleton wearing... |
| ghost / mask | Ch20:85 | “Because safety bores me,” she admitted, a ghost of a smile touching her lips. “But fear... |
| ghost / mask | Ch24:495 | ...Ramayyan tells you about my concerns.” A ghost of a smile crossed her face. “My concerns... |
| ghost / mask | Ch28:227 | ...was acceptable,” Duarte added, with a ghost of a smile. “High praise, from him.” |

### 6.3 Simile vehicles used in more than one chapter

From 'like (a/the) X' and 'as ADJ as (a) X'. 141 distinct vehicles, 20 of them reused across chapters.

| Vehicle | Uses | Chapters | Examples |
|---|---:|---:|---|
| man | 9 | 8 | Ch02:87 as tall as a man; Ch05:69 like a man; Ch11:149 like a man; Ch13:123 like a man; Ch14:163 like a man +4 |
| water | 9 | 8 | Ch01:103 like water; Ch07:209 like the waters; Ch10:57 like water; Ch12:13 like water; Ch13:5 like drinking warm water +4 |
| stone | 6 | 6 | Ch11:255 like a stone; Ch13:243 like a stone; Ch18:213 like stones; Ch23:519 like the stone; Ch25:230 like stones +1 |
| smoke | 5 | 5 | Ch01:97 like smoke; Ch17:95 like smoke; Ch18:113 like smoke; Ch24:545 like smoke; Ch26:51 like smoke |
| men | 3 | 3 | Ch10:21 like men; Ch11:41 like men; Ch13:85 like men |
| bead | 2 | 2 | Ch11:27 like beads; Ch26:99 like green beads |
| boy | 2 | 2 | Ch08:233 like boys; Ch20:260 like a boy |
| deer | 2 | 2 | Ch22:109 like a deer; Ch24:491 like a deer |
| fish | 2 | 2 | Ch07:111 like fish; Ch09:114 like the fish |
| guilt | 2 | 2 | Ch23:127 like guilt; Ch28:205 like guilt |
| heartbeat | 2 | 2 | Ch17:243 like a second heartbeat; Ch20:169 like a heartbeat |
| horse | 2 | 2 | Ch03:31 like horses; Ch09:80 Like a horse |
| hour | 2 | 2 | Ch14:131 like hours; Ch15:145 like an hour |
| insect | 2 | 2 | Ch10:109 like insects; Ch16:337 like dark insects |
| king | 2 | 2 | Ch22:51 like a king; Ch24:575 like a king |
| rope | 2 | 2 | Ch02:121 like a rope; Ch11:241 like rope |
| scar | 2 | 2 | Ch15:133 like a scar; Ch17:119 like a pale scar |
| vein | 2 | 2 | Ch07:175 like veins; Ch26:99 like a vein |
| weight | 2 | 2 | Ch07:23 like a weight; Ch19:113 like weights |
| woman | 2 | 2 | Ch17:115 like an old woman; Ch27:173 like a woman |

### 6.4 What follows 'as if' / 'as though'

First content word after the phrase, when it recurs (2+ chapters or 3+ uses).

| Next word | Uses | Chapters | Examples |
|---|---:|---:|---|
| already | 3 | 3 | Ch15:65 as if he were already measuring them; Ch20:216 as if already turning the scene into; Ch21:5 as if he were already filing the |
| waiting | 3 | 3 | Ch06:117 as if it were waiting for something; Ch13:5 as if waiting for something; Ch25:324 as if she had been waiting |
| belonged | 2 | 2 | Ch01:49 as if it still belonged to me; Ch02:79 as if it belonged to the creaking |
| counted | 2 | 2 | Ch06:121 as if you have counted men and; Ch16:329 as if I have counted,” I replied |
| seeing | 2 | 2 | Ch19:179 as if seeing them for the first; Ch28:127 as if seeing me for the first |

## 7. Sentence rhythm

Sentence length in words. CV = stdev / mean (higher = more varied). Short = under 8 words, long = over 30. **1-sent paras** counts every paragraph that is a single sentence (dialogue lines included); **narr. 1-sent** is the share among paragraphs with no quoted speech. **Standalone** counts one-sentence narration paragraphs with no speech on either side: the one-line kicker paragraphs inside narrative passages, as opposed to beats between lines of dialogue. **Speech** is the share of words inside quotation marks.

| Chapter | Words | Sentences | Mean | Median | Stdev | CV | Short | Long | Paras | 1-sent paras | Narr. 1-sent | Standalone | Speech |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ch01 | 1941 | 163 | 11.9 | 10 | 8.3 | 0.70 | 33% | 4% | 55 | 17 (31%) | 36% | 9 | 25% |
| Ch02 | 1890 | 166 | 11.4 | 10 | 7.4 | 0.65 | 36% | 2% | 65 | 18 (28%) | 28% | 6 | 14% |
| Ch03 | 2837 | 279 | 10.2 | 9 | 6.5 | 0.64 | 44% | 1% | 115 | 39 (34%) | 28% | 13 | 11% |
| Ch04 | 1704 | 176 | 9.7 | 8 | 6.0 | 0.62 | 43% | 1% | 64 | 15 (23%) | 21% | 4 | 16% |
| Ch05 | 2001 | 197 | 10.2 | 9 | 6.2 | 0.61 | 39% | 1% | 88 | 35 (40%) | 45% | 2 | 38% |
| Ch06 | 2703 | 221 | 12.2 | 11 | 8.2 | 0.67 | 33% | 1% | 96 | 36 (38%) | 44% | 7 | 27% |
| Ch07 | 2859 | 259 | 11.0 | 9 | 7.4 | 0.67 | 43% | 2% | 110 | 41 (37%) | 52% | 9 | 29% |
| Ch08 | 3420 | 341 | 10.0 | 9 | 7.1 | 0.71 | 45% | 2% | 120 | 38 (32%) | 40% | 6 | 45% |
| Ch09 | 3056 | 292 | 10.5 | 8 | 6.8 | 0.65 | 44% | 1% | 126 | 49 (39%) | 58% | 6 | 47% |
| Ch10 | 2579 | 219 | 11.8 | 9 | 8.7 | 0.74 | 38% | 5% | 98 | 44 (45%) | 57% | 7 | 35% |
| Ch11 | 6007 | 553 | 10.9 | 9 | 6.9 | 0.64 | 41% | 1% | 228 | 86 (38%) | 55% | 19 | 37% |
| Ch12 | 2010 | 196 | 10.3 | 8 | 6.7 | 0.66 | 46% | 1% | 75 | 28 (37%) | 50% | 6 | 43% |
| Ch13 | 4399 | 395 | 11.1 | 9 | 7.3 | 0.66 | 40% | 1% | 160 | 63 (39%) | 61% | 10 | 43% |
| Ch14 | 2639 | 222 | 11.9 | 10 | 7.8 | 0.66 | 40% | 3% | 92 | 32 (35%) | 39% | 18 | 11% |
| Ch15 | 3945 | 391 | 10.1 | 8 | 6.8 | 0.68 | 44% | 1% | 161 | 62 (39%) | 41% | 14 | 32% |
| Ch16 | 5713 | 518 | 11.0 | 9 | 8.0 | 0.72 | 44% | 4% | 219 | 100 (46%) | 56% | 21 | 34% |
| Ch17 | 3278 | 316 | 10.4 | 8 | 7.4 | 0.72 | 46% | 4% | 139 | 48 (35%) | 43% | 7 | 40% |
| Ch18 | 2643 | 264 | 10.0 | 8 | 7.3 | 0.73 | 47% | 2% | 132 | 62 (47%) | 68% | 9 | 43% |
| Ch19 | 2875 | 279 | 10.3 | 9 | 7.2 | 0.70 | 44% | 1% | 137 | 66 (48%) | 55% | 26 | 23% |
| Ch20 | 4569 | 436 | 10.5 | 8 | 7.4 | 0.71 | 43% | 3% | 202 | 95 (47%) | 54% | 22 | 35% |
| Ch21 | 2135 | 248 | 8.6 | 6 | 7.1 | 0.83 | 58% | 2% | 99 | 53 (54%) | 70% | 16 | 44% |
| Ch22 | 3795 | 358 | 10.6 | 8 | 7.8 | 0.73 | 45% | 2% | 204 | 130 (64%) | 77% | 76 | 27% |
| Ch23 | 5094 | 522 | 9.8 | 9 | 6.0 | 0.61 | 41% | 0% | 264 | 123 (47%) | 61% | 34 | 31% |
| Ch24 | 8306 | 899 | 9.2 | 7 | 6.8 | 0.74 | 52% | 1% | 402 | 188 (47%) | 68% | 25 | 52% |
| Ch25 | 3240 | 331 | 9.8 | 8 | 7.3 | 0.75 | 46% | 3% | 171 | 94 (55%) | 77% | 32 | 45% |
| Ch26 | 2597 | 258 | 10.1 | 8 | 6.5 | 0.65 | 45% | 0% | 141 | 86 (61%) | 79% | 39 | 42% |
| Ch27 | 2321 | 252 | 9.2 | 7 | 6.5 | 0.71 | 50% | 1% | 109 | 47 (43%) | 52% | 12 | 40% |
| Ch28 | 3487 | 341 | 10.2 | 8 | 7.5 | 0.73 | 49% | 2% | 148 | 72 (49%) | 57% | 35 | 27% |
| **Book** | 94043 | 9092 | 10.3 | 8 | 7.2 | 0.70 | 44% | 2% | 4020 | 1767 (44%) | 56% | 490 |  |

## 8. Dashes and quote marks

Em dash and double hyphen must both be zero (style sheet). Double hyphens are counted in prose lines only; horizontal rules and table rules are ignored. Mixed straight and curly quotes or apostrophes in one chapter are flagged for the copy edit (curly apostrophes also count closing single quotes).

| Chapter | Em dash | En dash | Double hyphen | Curly “” | Straight " | Curly ’ | Straight ' | Ellipses | Flag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Ch01 | 0 | 0 | 0 | 64 | 0 | 0 | 14 | 1 |  |
| Ch02 | 0 | 0 | 0 | 76 | 0 | 0 | 1 | 0 |  |
| Ch03 | 0 | 0 | 0 | 108 | 0 | 0 | 8 | 12 |  |
| Ch04 | 0 | 0 | 0 | 76 | 0 | 0 | 5 | 2 |  |
| Ch05 | 0 | 0 | 0 | 154 | 0 | 0 | 10 | 0 |  |
| Ch06 | 0 | 0 | 0 | 106 | 0 | 0 | 15 | 0 |  |
| Ch07 | 0 | 0 | 0 | 152 | 0 | 4 | 9 | 0 | mixed apostrophes |
| Ch08 | 0 | 0 | 0 | 197 | 4 | 5 | 23 | 2 | mixed quotes; mixed apostrophes |
| Ch09 | 0 | 0 | 0 | 230 | 0 | 0 | 15 | 0 |  |
| Ch10 | 0 | 0 | 0 | 154 | 0 | 0 | 20 | 0 |  |
| Ch11 | 0 | 0 | 0 | 0 | 358 | 0 | 50 | 0 | straight quotes only |
| Ch12 | 0 | 0 | 0 | 0 | 104 | 0 | 19 | 0 | straight quotes only |
| Ch13 | 0 | 0 | 0 | 226 | 64 | 3 | 17 | 1 | mixed quotes; mixed apostrophes |
| Ch14 | 0 | 0 | 0 | 50 | 26 | 4 | 11 | 0 | mixed quotes; mixed apostrophes |
| Ch15 | 0 | 0 | 0 | 202 | 42 | 2 | 11 | 0 | mixed quotes; mixed apostrophes |
| Ch16 | 0 | 0 | 0 | 260 | 56 | 2 | 22 | 2 | mixed quotes; mixed apostrophes |
| Ch17 | 0 | 0 | 0 | 260 | 0 | 9 | 13 | 1 | mixed apostrophes |
| Ch18 | 0 | 0 | 0 | 228 | 4 | 2 | 20 | 3 | mixed quotes; mixed apostrophes |
| Ch19 | 0 | 0 | 0 | 142 | 4 | 4 | 25 | 0 | mixed quotes; mixed apostrophes |
| Ch20 | 0 | 0 | 0 | 292 | 8 | 9 | 11 | 1 | mixed quotes; mixed apostrophes |
| Ch21 | 0 | 0 | 0 | 146 | 4 | 0 | 13 | 1 | mixed quotes |
| Ch22 | 0 | 0 | 0 | 188 | 0 | 1 | 40 | 5 | mixed apostrophes |
| Ch23 | 0 | 0 | 0 | 270 | 72 | 4 | 37 | 6 | mixed quotes; mixed apostrophes |
| Ch24 | 0 | 0 | 0 | 736 | 46 | 0 | 51 | 12 | mixed quotes |
| Ch25 | 0 | 0 | 0 | 248 | 20 | 0 | 27 | 3 | mixed quotes |
| Ch26 | 0 | 0 | 0 | 156 | 12 | 0 | 14 | 0 | mixed quotes |
| Ch27 | 0 | 0 | 0 | 162 | 0 | 0 | 21 | 1 |  |
| Ch28 | 0 | 0 | 0 | 148 | 14 | 0 | 19 | 0 | mixed quotes |
| **Book** | 0 | 0 | 0 | 5031 | 838 | 49 | 541 | 53 |  |

## 9. Chapter endings

The last paragraph of each chapter. The style sheet asks for endings on an action, an image or a line of dialogue, not a summary or moral, and bans final paragraphs opening with But, For now, For the moment, And some or Perhaps. **Tics** lists core markers firing inside that final paragraph.

| Chapter | Line | Final paragraph | Flags | Tics |
|---|---:|---|---|---|
| Ch01 | 113 | Storms do not ask permission. | one-sentence, short (<8 words), summary word (storms) |  |
| Ch02 | 131 | The Arabian Sea was beginning to remind us who owned this ship. | one-sentence, summary word (beginning) |  |
| Ch03 | 231 | The sea closed over my head like the hand of an angry god. | one-sentence | like a/the |
| Ch04 | 129 | ...pite the wounds. I had seen that look before, in market squares where men were sold. For a long moment he said nothing. In that silence, I was being weighed. | short (<8 words) |  |
| Ch05 | 177 | Sleep came slowly that night, but when it did, it carried no dreams of drowning. Only the steady beat of hooves on sand, and a distant roar like the sea. | summary word (carried) | like a/the, soft adv. |
| Ch06 | 193 | For now, Travancore was the forge. But the blade was meant for another war. | opens 'For now' |  |
| Ch07 | 225 | Storms did not ask permission. Perhaps horses, taught well, did not either. | short (<8 words), summary word (storms) |  |
| Ch08 | 243 | I had faced Portuguese interrogations and Arabian Sea storms. Somehow, this felt like the more delicate task. | summary word (storms) | like a/the, somehow |
| Ch09 | 254 | For now, I followed Padmini into the hall, where incense curled, drums spoke, and old Velinadu women weighed the future in words sharper than blades. | opens 'For now', one-sentence, summary word (future) |  |
| Ch10 | 201 | If I wished to survive, I would have to learn the same. | one-sentence, summary word (learn) |  |
| Ch11 | 477 | The horizon had begun to move nearer, whether it wished to or not. | one-sentence |  |
| Ch12 | 159 | I turned back toward the camp. There was still work to do. | short (<8 words) |  |
| Ch13 | 321 | The storm was here. | one-sentence, short (<8 words), summary word (storm) |  |
| Ch14 | 185 | ...ed away, I knew the silence to come would be more dangerous than the noise. Now came the words. And words, in my experience, could be sharper than any sword. | opens 'But' |  |
| Ch15 | 331 | ...r. And Travancore, this slip of land between the mountains and the sea, would become something no one, not even the great Companies of Europe, could swallow. |  |  |
| Ch16 | 439 | That was enough for now. | one-sentence, short (<8 words), summary word (enough) |  |
| Ch17 | 281 | And some doors, once opened, are never fully closed again. | opens 'And some', one-sentence |  |
| Ch18 | 269 | But as I went back to my lamp and my notes, I could taste dust on the wind, dry and far away, carrying the Deccan toward this coast. | opens 'But', one-sentence |  |
| Ch19 | 275 | For the moment, that was enough. | opens 'For the moment', one-sentence, short (<8 words), summary word (enough) |  |
| Ch20 | 420 | ... ran these stones and called this place home, even as they learned to ride under a king whose kingdom we had both helped, and hindered, and loved into being. | one-sentence, summary word (home, learned) |  |
| Ch21 | 215 | Both, I suspected, would matter when the next storm came. | one-sentence, summary word (storm) |  |
| Ch22 | 409 | But for the first time since Goa, I felt not like wreckage caught between currents, but like part of a river that had chosen its course. | opens 'But', one-sentence | Not X but Y, first time |
| Ch23 | 529 | “And claws,” I said, feeling a chill that had nothing to do with the wind. “God help anyone who thinks they can clip them.” |  |  |
| Ch24 | 831 | Together. | one-sentence, short (<8 words), summary word (together) |  |
| Ch25 | 348 | But when it did, at least I would not have to wonder whose side of the wall I was standing on. | opens 'But', one-sentence |  |
| Ch26 | 283 | Men like Ibrahim rarely walked in straight lines. Perhaps that was the only way to survive on a coast where every power wanted the same pepper. |  |  |
| Ch27 | 231 | Now came the work of making sure they could never rise again. | one-sentence |  |
| Ch28 | 305 | For as long as we live, and in the stories that outlast us. | one-sentence |  |

25 of 28 endings carry at least one flag.

**Words shared by the closing two paragraphs of 3+ chapters** (possible repeated closing ideas): sea (02, 03, 05, 07, 08, 12, 15); storm (01, 05, 07, 08, 13, 21, 25); came (04, 05, 14, 21, 27); coast (09, 11, 18, 26); house (04, 09, 22, 27); king (06, 09, 20, 23); blade (04, 06, 09); hand (03, 04, 06); horse (04, 05, 07); knew (07, 14, 15); men (04, 16, 26); moment (04, 10, 19); old (09, 22, 27); place (04, 06, 20); sand (05, 07, 12); side (02, 03, 25); stone (06, 15, 20); sword (06, 10, 14); way (04, 11, 26); word (09, 14, 23).

## 10. Repeated whole sentences

Narration sentences (any length) that recur word for word in 2+ chapters or 3+ times. Short motif lines and stock beats that the n-gram scan is too long to catch show up here.

| Sentence | Uses | Chapters | Locations |
|---|---:|---:|---|
| he looked at me | 6 | 5 | Ch13:185; Ch15:267; Ch16:375; Ch22:325,351; Ch23:511 |
| he shrugged | 5 | 4 | Ch07:207; Ch12:51; Ch15:99; Ch24:45,253 |
| it was not a question | 4 | 4 | Ch07:195; Ch09:92; Ch19:67; Ch24:153 |
| he smiled | 4 | 3 | Ch15:87; Ch24:741,817; Ch28:241 |
| he did not need to | 3 | 3 | Ch16:263; Ch18:107; Ch27:111 |
| he nodded | 3 | 3 | Ch16:423; Ch24:811; Ch25:160 |
| he turned to face me | 3 | 3 | Ch16:363; Ch24:207; Ch28:167 |
| he turned to me | 3 | 3 | Ch12:103; Ch17:87; Ch22:343 |
| i stepped closer | 3 | 3 | Ch17:239; Ch20:147; Ch24:363 |
| he paused | 4 | 2 | Ch24:135,299,763; Ch25:270 |
| for a heartbeat nothing happened | 2 | 2 | Ch14:97; Ch26:127 |
| he looked up at me | 2 | 2 | Ch11:89; Ch27:17 |
| he nodded slowly | 2 | 2 | Ch07:115; Ch15:317 |
| he smiled thinly | 2 | 2 | Ch12:37; Ch16:349 |
| he studied me | 2 | 2 | Ch08:35; Ch19:125 |
| he swallowed | 2 | 2 | Ch03:69; Ch24:329 |
| he was right | 2 | 2 | Ch03:89; Ch18:17 |
| her jaw tightened | 2 | 2 | Ch24:491; Ch27:213 |
| his jaw clenched | 2 | 2 | Ch22:313; Ch23:135 |
| i looked at ramayyan | 2 | 2 | Ch23:523; Ch28:65 |
| i shook my head | 2 | 2 | Ch16:347; Ch22:371 |
| i thought of goa | 2 | 2 | Ch16:383; Ch24:621 |
| i waited | 2 | 2 | Ch08:153; Ch24:555 |
| mats covered the floor | 2 | 2 | Ch06:35; Ch11:171 |
| of keshavrao's hand slipping from the rope | 2 | 2 | Ch16:383; Ch24:621 |
| ramayyan nodded slowly | 2 | 2 | Ch12:123; Ch21:139 |
| ramayyan's smile was thin | 2 | 2 | Ch12:63; Ch25:260 |
| she looked at me | 2 | 2 | Ch13:253; Ch18:205 |
| she propped herself up to look at me | 2 | 2 | Ch17:263; Ch20:400 |
| she reached up and unpinned her hair | 2 | 2 | Ch16:119; Ch20:356 |
| she snorted | 2 | 2 | Ch05:39; Ch20:157 |
| she turned to face me fully | 2 | 2 | Ch20:79; Ch24:485 |
| she turned to leave then paused | 2 | 2 | Ch24:511; Ch26:205 |
| too slow | 2 | 2 | Ch14:131; Ch23:227 |
| we stood in silence | 2 | 2 | Ch16:17; Ch24:339 |

## 11. Appendix: other repeated phrases

Cross-chapter phrases ranked 41 onward (showing 112 of 112), same columns as section 4.

| # | Phrase | Uses | Chapters | Score | Locations |
|---:|---|---:|---:|---:|---|
| 41 | the hairs on my arms | 2 | 2 | 10.6 | Ch13:261; Ch22:77 |
| 42 | the king said his voice dropping to a | 2 | 2 | 10.5 | Ch17:67; Ch23:507 |
| 43 | hand slipping from the rope | 2 | 2 | 10.5 | Ch16:383; Ch24:621 |
| 44 | swayed in the shade of the | 2 | 2 | 10.4 | Ch08:47; Ch23:421 |
| 45 | better than to disturb the | 2 | 2 | 10.3 | Ch13:249; Ch17:221d |
| 46 | the brand under my sleeve | 2 | 2 | 10.2 | Ch05:147; Ch08:75 |
| 47 | that belief did not matter | 2 | 2 | 10.2 | Ch01:101; Ch28:283 |
| 48 | whoever has the better powder | 2 | 2 | 10.2 | Ch01:73d; Ch24:335d |
| 49 | i drove my horse straight at | 2 | 2 | 9.8 | Ch15:139; Ch23:223 |
| 50 | traded on this coast longer than | 2 | 2 | 9.8 | Ch24:701d; Ch26:275d |
| 51 | wooden door in the corner | 2 | 2 | 9.8 | Ch16:109; Ch17:69 |
| 52 | the placement of a new | 2 | 2 | 9.7 | Ch16:257; Ch21:13 |
| 53 | the rain and let it wash away | 2 | 2 | 9.6 | Ch25:256; Ch28:299 |
| 54 | standing with one foot in each river | 2 | 2 | 9.6 | Ch22:373d; Ch28:129d |
| 55 | the boy on the palm | 3 | 3 | 9.5 | Ch11:107d; Ch13:11; Ch25:130 |
| 56 | the edge of the training ground | 2 | 2 | 9.4 | Ch16:217; Ch24:461 |
| 57 | the king said his voice | 3 | 2 | 9.4 | Ch17:67,99; Ch23:507 |
| 58 | he wore no crown only a simple | 2 | 2 | 9.4 | Ch05:127; Ch11:189 |
| 59 | a king who builds walls | 2 | 2 | 9.3 | Ch11:149; Ch12:35d |
| 60 | the sky was the colour of old | 2 | 2 | 9.2 | Ch09:4; Ch16:339 |
| 61 | a piece on the board | 2 | 2 | 9.1 | Ch11:333; Ch21:55d |
| 62 | written in salt and ash | 2 | 2 | 9.0 | Ch13:135; Ch14:7 |
| 63 | the bandage on his shoulder | 2 | 2 | 8.9 | Ch16:157; Ch23:515 |
| 64 | moved toward the cross at his throat | 2 | 2 | 8.9 | Ch24:329; Ch25:266 |
| 65 | smelled of coconut smoke and | 2 | 2 | 8.9 | Ch13:3; Ch21:207 |
| 66 | she propped herself up to look at me | 2 | 2 | 8.8 | Ch17:263; Ch20:400 |
| 67 | hands clasped behind his back | 2 | 2 | 8.7 | Ch11:373; Ch18:163 |
| 68 | sat on a low stool | 2 | 2 | 8.7 | Ch18:225; Ch23:95 |
| 69 | and the slow grinding of | 2 | 2 | 8.6 | Ch10:191; Ch15:5 |
| 70 | stood at the edge of the | 3 | 3 | 8.6 | Ch07:161; Ch18:21; Ch24:391 |
| 71 | house and a sliver of | 2 | 2 | 8.4 | Ch20:117d; Ch26:243d |
| 72 | she turned to face me fully | 2 | 2 | 8.4 | Ch20:79; Ch24:485 |
| 73 | the map in the war hall | 2 | 2 | 8.3 | Ch27:3; Ch28:255 |
| 74 | sat under the jackfruit tree | 2 | 2 | 8.2 | Ch10:193; Ch22:267 |
| 75 | for the first time i | 4 | 2 | 8.1 | Ch17:137; Ch20:406,406,408 |
| 76 | she turned to leave then paused | 2 | 2 | 7.9 | Ch24:511; Ch26:205 |
| 77 | she clicked her tongue and | 2 | 2 | 7.9 | Ch04:109; Ch16:39 |
| 78 | of the boys in the kalari | 2 | 2 | 7.8 | Ch09:162; Ch10:41 |
| 79 | the shade of the inner | 2 | 2 | 7.8 | Ch08:49; Ch09:198 |
| 80 | for a heartbeat nothing happened | 2 | 2 | 7.8 | Ch14:97; Ch26:127 |
| 81 | carrying the weight of a | 3 | 2 | 7.7 | Ch15:37,199; Ch20:222 |
| 82 | a simple cloth over his shoulder | 2 | 2 | 7.6 | Ch07:19; Ch11:189 |
| 83 | the simple white cloth of his | 2 | 2 | 7.6 | Ch13:91; Ch24:659 |
| 84 | he turned to face me | 3 | 3 | 7.6 | Ch16:363; Ch24:207; Ch28:167 |
| 85 | hung in the air like smoke | 2 | 2 | 7.5 | Ch18:113; Ch26:51 |
| 86 | but for the first time since | 3 | 3 | 7.4 | Ch03:117; Ch16:153; Ch22:409 |
| 87 | by the time the first | 3 | 3 | 7.4 | Ch22:25d; Ch24:3; Ch26:9 |
| 88 | the distant line of the sea | 2 | 2 | 7.4 | Ch16:275; Ch24:221 |
| 89 | for a moment surrounded by the | 2 | 2 | 7.3 | Ch20:304; Ch21:125 |
| 90 | said one evening as we watched | 2 | 2 | 7.1 | Ch16:321; Ch27:89 |
| 91 | the edge of the crowd | 2 | 2 | 7.0 | Ch11:309; Ch23:59 |
| 92 | he did not look up from his palm leaves | 2 | 2 | 7.0 | Ch08:15; Ch26:273 |
| 93 | before coming to rest against a | 2 | 2 | 6.7 | Ch03:27; Ch22:177 |
| 94 | i closed my eyes for a moment | 2 | 2 | 6.6 | Ch04:121; Ch06:99 |
| 95 | sat in a small room | 2 | 2 | 6.6 | Ch13:37; Ch22:331 |
| 96 | fights them too he said | 2 | 2 | 6.5 | Ch04:63d; Ch05:23d |
| 97 | we will stand in the same halls | 2 | 2 | 6.5 | Ch26:253d; Ch28:141d |
| 98 | her voice dropping to a | 2 | 2 | 6.4 | Ch08:195; Ch13:299 |
| 99 | his gaze slid to me | 2 | 2 | 6.4 | Ch09:32; Ch16:271 |
| 100 | at the corner of her mouth | 2 | 2 | 6.4 | Ch04:95; Ch17:223 |
| 101 | of hooves on sand and | 2 | 2 | 6.2 | Ch05:177; Ch21:211 |
| 102 | walked the length of the | 2 | 2 | 5.9 | Ch20:75; Ch28:27 |
| 103 | in the centre of the room | 2 | 2 | 5.9 | Ch21:19; Ch26:177 |
| 104 | put a hand on the | 2 | 2 | 5.8 | Ch15:49; Ch22:55 |
| 105 | the sea does not care | 2 | 2 | 5.8 | Ch11:407d; Ch13:205d |
| 106 | a woman who had learned | 2 | 2 | 5.7 | Ch16:147; Ch24:513 |
| 107 | at the far end of the | 2 | 2 | 5.6 | Ch02:79; Ch08:63 |
| 108 | before you washed up on this coast | 2 | 2 | 5.5 | Ch16:77d; Ch25:234d |
| 109 | washed up on this coast had | 2 | 2 | 5.5 | Ch16:433; Ch17:265d |
| 110 | was silent for a moment | 2 | 2 | 5.4 | Ch17:153; Ch24:481 |
| 111 | the man on the platform | 2 | 2 | 5.4 | Ch05:165; Ch06:47 |
| 112 | the king had given me | 2 | 2 | 5.2 | Ch07:9; Ch08:235 |
| 113 | the smell of salt and | 2 | 2 | 5.2 | Ch04:127; Ch12:151 |
| 114 | the air was thick with | 2 | 2 | 5.2 | Ch02:67; Ch11:69 |
| 115 | the edge of the village | 2 | 2 | 5.1 | Ch04:95; Ch20:19 |
| 116 | a man who had spent | 2 | 2 | 5.1 | Ch15:73; Ch22:187 |
| 117 | he said without looking at | 2 | 2 | 5.1 | Ch06:113; Ch28:165 |
| 118 | he said without looking up | 2 | 2 | 5.1 | Ch11:75; Ch20:292 |
| 119 | the men who died at | 2 | 2 | 5.1 | Ch18:97d; Ch24:807d |
| 120 | we did not have to wait long | 2 | 2 | 5.0 | Ch03:97; Ch23:189 |
| 121 | you trust him i asked | 2 | 2 | 5.0 | Ch11:441d; Ch18:253d |
| 122 | thought of the boy in | 2 | 2 | 5.0 | Ch11:287; Ch24:645 |
| 123 | at the edge of the hall | 2 | 2 | 5.0 | Ch11:279; Ch18:21 |
| 124 | did not want to be seen | 2 | 2 | 4.9 | Ch04:83; Ch07:33 |
| 125 | with a different kind of | 2 | 2 | 4.9 | Ch08:11; Ch23:75 |
| 126 | you are older she said | 2 | 2 | 4.8 | Ch17:39d; Ch20:374d |
| 127 | on the far side of the | 2 | 2 | 4.7 | Ch01:43; Ch23:233 |
| 128 | by the time the sun | 2 | 2 | 4.7 | Ch10:139; Ch23:329 |
| 129 | for a moment the world | 2 | 2 | 4.7 | Ch03:199; Ch20:262 |
| 130 | made a sound that was | 2 | 2 | 4.6 | Ch13:17; Ch22:105 |
| 131 | i left the room the | 2 | 2 | 4.6 | Ch19:141; Ch21:195 |
| 132 | that would come later when | 2 | 2 | 4.6 | Ch04:83; Ch11:455 |
| 133 | she came to the fort | 2 | 2 | 4.5 | Ch22:395; Ch26:215 |
| 134 | i had heard the name | 2 | 2 | 4.4 | Ch08:23; Ch12:7 |
| 135 | was quiet for a moment | 2 | 2 | 4.4 | Ch07:203; Ch24:757 |
| 136 | and turned it in his fingers | 2 | 2 | 4.4 | Ch12:11; Ch16:355 |
| 137 | in his hands he carried a | 2 | 2 | 4.4 | Ch22:69; Ch28:23 |
| 138 | i had last seen it | 2 | 2 | 4.4 | Ch06:99; Ch19:21 |
| 139 | a man who had already | 2 | 2 | 4.4 | Ch14:163; Ch15:37 |
| 140 | found their way to this | 2 | 2 | 4.3 | Ch19:251; Ch28:211 |
| 141 | walked to where she stood | 2 | 2 | 4.3 | Ch24:465; Ch27:193 |
| 142 | i had first seen him in the | 2 | 2 | 4.3 | Ch06:13; Ch22:51 |
| 143 | to this coast i said | 2 | 2 | 4.2 | Ch09:122d; Ch20:191d |
| 144 | the king sat on a | 2 | 2 | 4.2 | Ch11:171; Ch14:73 |
| 145 | a man who has seen | 2 | 2 | 4.1 | Ch04:63d; Ch16:323d |
| 146 | man who has seen how | 2 | 2 | 4.1 | Ch16:323d; Ch22:29d |
| 147 | and for a moment i saw | 2 | 2 | 4.1 | Ch11:405; Ch24:419 |
| 148 | and for the first time | 2 | 2 | 4.0 | Ch01:107; Ch17:137 |
| 149 | for the first time since i had | 2 | 2 | 4.0 | Ch16:153; Ch21:121 |
| 150 | it was the first time | 2 | 2 | 4.0 | Ch07:179; Ch14:163 |
| 151 | me for a long moment | 2 | 2 | 4.0 | Ch12:111; Ch24:577 |
| 152 | very still for a long moment | 2 | 2 | 4.0 | Ch15:295; Ch18:125 |

