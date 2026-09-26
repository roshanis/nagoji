# Second Edition Audit: Summary

*Horse of the Servant* (Blood and Thrones, Book 1), second-edition preparation.
Prepared 26 September 2026 from every report in `audit/`: the 30 unit audits in `audit/chapters/` (Foreword, Prequel, Chapters 1 to 28), `SOURCE_OF_TRUTH.md` (SoT below), `REPETITION_AND_DENSITY.md`, `OPENINGS_ENDINGS_MOTIFS.md` (OEM below), `REGISTER_AND_ANACHRONISM.md`, `REVIEW_BACKLOG.md` and `VOICE_BIBLE.md`, plus `STYLE_SHEET.md`, `PLAN.md`, the eight pilot files in `pilot/` and the six blind judge reports on them. I re-ran `audit/tools/scan_slop.py` on copies of the pilot files in scratch space to add rhythm measures the judges did not score.

Line references (`ch7:145`, or `L145` inside a chapter row) are to the frozen first-edition files in `book1_horse_servant/`. The companion file is `../STYLE_SHEET_v2.md`, the calibrated replacement for `STYLE_SHEET.md`. Nothing here changes the first edition, `STYLE_SHEET.md` or `PLAN.md`.

## 1. Executive summary

1. **The machine signal is rhythm and commentary, not vocabulary.** The obvious clichés are rare and there are no em dashes. What reads as machine-written is structural: 44% of all paragraphs are one sentence long (56% of narration paragraphs), 490 of those are standalone one-liners inside narration, 186 paragraphs end on a short kicker, and there are 227 "not X, but Y" constructions plus 24 two-sentence "It was not X. It was Y." pairs the scanner does not count. Around those sit explained subtext, named emotions, life maxims and chapter endings that summarise.
2. **Every unit needs work, and the late book needs the most.** The audits confirm **2,024 issues** across 30 units (402 more borderline, 647 flagged but defended). Chapters 1 to 7 score 3 of 5; the Foreword, the Prequel and 21 chapters score 4; Chapter 27 scores 5. The largest single chapter job is Chapter 24 (158 confirmed issues in 8,306 words). The densest units are the Prequel (34.0 confirmed issues per 1,000 words), Chapter 12 (30.3) and the Foreword (28.6).
3. **The cut is much larger than `PLAN.md` expects.** PLAN budgets 5 to 10 percent. The audits' scratch passes, weighted by length, remove **25.2% of the chapters** (about 23,700 of 94,043 words; 25.4% with the front matter; 26.0% if the Ch 23 temple section goes). The pilot line edit alone removed 9 to 12 percent of two dense passages at every intensity. The difference is block work: history lectures, codas, duplicated scenes. Plan for **20 to 25 percent overall**, a chapter text of roughly 70,000 to 75,000 words.
4. **Edit intensity: use one line standard everywhere, and vary scope by chapter.** Across two blind passages and six judge reports, the deep pass left the fewest machine tells (mean AI-residue score 8.0 of 10), read best (8.17) and won 3 of 6 picks. The medium pass kept the most meaning on the Ch 27 passage and won 2. The light pass left about 12 tells per passage per judge, scored 5.17 on residue, won 1 pick, and on Ch 27 it made the rhythm worse. The recommendation: **deep in narration, medium in dialogue, never in facts**, held in check by ten fidelity guardrails taken from the judges' own grafts (`STYLE_SHEET_v2.md` section 5). Retire the light pass. The Medium and Deep labels in the triage table are scope labels (which blocks get rebuilt); they do not change how hard a sentence is edited. Details in section 4.
5. **Endings are the biggest structural tic, and most are fixed by cutting.** 22 of 28 chapters end on a summary or a moral, and 25 of 28 carry at least one scanner flag in their last paragraphs. In 12 chapters a better last line already sits one to five paragraphs up. The audits give every unit a new ending; I reconciled them into one register with no repeated closing idea (`STYLE_SHEET_v2.md` section 7), which settles four collisions the chapter audits introduced.
6. **Motifs are overspent.** "Storm" appears 55 times in 20 chapters, 22 of them figurative; it keeps one plant (ch5:105) and one payoff (ch13:321). The book's real spine is the name (taken at ch1:5, changed in Ch 17, entered in Ramayyan's leaves in Chs 21 and 25), and only restatement weakens it. Teeth and the Tiger belong to Part IV. The title motif, the horse, has three continuity breaks.
7. **The register slips are concentrated and fixable as patterns.** 290 register findings (52 P1, 127 P2, 111 P3), heaviest in Chs 24, 16, 13, 23, 15 and 11. The most visible single intrusion is Ramayyan's ledger written as a modern risk register ("Risk assessment: HIGH. Timeline: before next monsoon.", ch21:72). Titles are wrong for the period: "diwan" 18 times, "Your Majesty", "Highness", "Sri Lanka", "Nair Brigade".
8. **Start from the chapter files, but settle two decisions first.** The published EPUB (25 Dec 2025) matches `manuscript_complete.md`; the chapter files differ from it in 13 of 37 units. They carry a changed De Lannoy arc (surrender with the garrison, where the published book has him desert) and about 2,500 words of unpublished exposition. `manuscript_v2.md` is stale and should never be a source or a sync target.
9. **Continuity work overlaps the prose work.** `REVIEW_BACKLOG.md` holds 167 items: 112 still present, 41 resolved, 14 unclear. The worst (Dhanaji's arrival, the "fled the Peshwa" backstory, the horses, De Lannoy's age and birthplace, Revathi as wife, callbacks to events that have not yet happened) touch the same sentences as the anti-slop edit, so they are fixed in the same pass and logged separately.
10. **The main risk is flattening the voice.** The audits defended 647 flags, and the pilot showed both ways the edit fails: the light pass leaves the tells, and the deep pass drops beats and adds new slop of its own ("Who was in the right never entered the sum", "get to choose"). `STYLE_SHEET_v2.md` section 6 is the Do-not-cut list built from the defended patterns.
11. **Order:** settle the 21 author decisions in section 6 and run a mechanical pass (Gate 0); edit Chapters 1 to 3 plus Chapter 27 as a calibration batch; then the Prequel and the rest of Part I, Parts II to IV in two batches each, the Foreword last, and the support documents after that (section 5).

## 2. Chapter triage

Severity is the audits' 1 to 5 scale. **Recommended intensity** gives the audit's scope label and the blocks it names; the line standard is the same everywhere (section 4.5). **Est. cut %** is the audit's scratch-pass estimate of words removed, blocks included. **Confirmed issues** is the adjudicated count, with the rate per 1,000 words. **Top issue types** merges the audits' category names (for example "simile stack" into simile, "stock gesture" into stock beat). **Ending** is the audit's verdict on the current ending. **Open backlog items** lists `REVIEW_BACKLOG.md` IDs still present or unclear for that unit.

| Unit | Severity | Recommended intensity (scope) | Est. cut % | Confirmed issues | Top issue types | Ending | Open backlog items |
|:-|:-:|:-|:-:|:-|:-|:-:|:-|
| Foreword | 4 | Deep. Collapse eight templated sections to about five; reduce the Walls section (L51 to 65) to one paragraph or drop it (D3); fix five factual errors; rename and date it (D21) | 35 | 43 (28.6/1k) | stock phrase 9, correction 8, kicker 5 | rewrite | SoT Decisions 1 and 2; SoT section 9.2 (Historical Note L15); placeholder signature and date |
| Prequel | 4 | Deep. Put Nagoji back into the documentary opening (L3 to 11) and the survey register (L31 to 47); compress the Travancore half (44% of the text); new ending | 28 | 44 (34.0/1k) | stock phrase 9, correction 8, kicker 8 | rewrite | BL-01, FM-06, FM-15 |
| 1 | 3 | Medium. Re-voice L7 and four interior paragraphs (39, 63, 71, 73); rebuild the closing cascade (L91 to 113, eleven paragraphs) | 22 | 43 (22.2/1k) | abstract depth 5, stock phrase 5, modern register 5 | rewrite | C10-01, C10-02, BL-01, N-21 (N-41 plant) |
| 2 | 3 | Medium. Five blocks: the Duarte beat (L29 to 41), the harbour walk (43 to 49), the shipboard-time essay (97), commentary after the promise (119 to 121), the ending (127 to 131) | 21 | 39 (20.6/1k) | stock phrase 8, abstract depth 6, explained subtext 4 | rewrite | C10-03, C10-04 |
| 3 | 3 | Medium. The lead-in (L11 to 45) and the resolution stack after Keshavrao's death (L209 to 231); the escape told twice (L99, L107 to 115) | 21 | 51 (18.0/1k) | kicker 10, stock phrase 9, correction 6 | revise | C10-06, N-20, N-39 |
| 4 | 3 | Medium. Opening (L3 to 13), the carry to the village (L77 to 89), the close (L121 to 129); the Malayalam comprehension logic | 17 | 39 (22.9/1k) | stock phrase 10, kicker 6, repetition 4 | revise | C10-08, N-20, N-21 |
| 5 | 3 | Medium. The close (L169 to 177, five endings); make the compound hall plain so Ch 6 is a step up; the seam with Ch 4 | 15 | 34 (17.0/1k) | stock phrase 5, correction 4, explained subtext 4 | rewrite | C10-10, C10-11, C10-12 |
| 6 | 3 | Medium. Approach (L3 to 33); the pitch sequence (L139 to 155, reorder); ending (L185 to 193); diwan to Dalawa (D19) | 19 | 55 (20.3/1k) | stock phrase 9, correction 8, filler 8 | rewrite | C10-12, C10-13, C12-05, BL-01, N-26 |
| 7 | 3 | Medium. The horse essay (L145 to 157, 465 words to about 200, D3); three section endings | 24 (9 points are the essay) | 53 (18.5/1k) | stock phrase 14, kicker 6, modern register 5 | rewrite | C10-14, F12-04, C18-04, C18-05, BL-01, N-03, N-26 |
| 8 | 4 | Medium. The *sambandham* lecture (L149 to 197, about 700 words to 320); the close (L231 to 243); the arrival (L47 to 61) | 30 (line level about 13) | 67 (19.6/1k) | stock phrase 13, modern register 11, correction 7 | revise | C10-15, C10-16, C10-41, C18-04, N-03, N-22, N-32, N-35 |
| 9 | 4 | Medium. The night coda (L220 to 254); stock reaction beats between speeches; duplicated plantain lines (L112, L128) | 20 | 59 (19.3/1k) | stock phrase 17, modern register 10, correction 5 | revise | C10-17, C18-05, N-21, N-28 |
| 10 | 4 | Deep. Rebuild sections two and three (L169 to 201, about 590 words to 300) from material the chapter already has | 27 | 51 (19.8/1k) | correction 8, stock phrase 8, modern register 6 | rewrite | C10-18, N-28, N-33, N-34, N-49 |
| 11 | 4 | Medium, heavy scope. Opening (L3 to 7), the Van Imhoff flashback (L119 to 153), the debrief (L413 to 443), seven codas (L451 to 477) | 20 | 78 (13.0/1k) | explained subtext 11, stock phrase 9, abstract depth 9 | rewrite | C10-20, C10-22, F13-01, N-01, N-10, N-27, N-28, N-36, N-49, N-51 |
| 12 | 4 | Deep. Rebuild the coda (L135 to 159) to about 130 words; the tribute point is stated seven times | 25 (half is the coda) | 61 (30.3/1k) | stock phrase 17, tricolon 6, continuity 6 | rewrite | F13-01, N-02, N-11, N-24, N-26, N-28 |
| 13 | 4 | Deep. The unpublished history block (L105 to 167, 991 words to about 450, D3); Sarpa Kavu and farewell (L249 to 309, about 960 words to 540) | 30 (12 points are the history block) | 96 (21.8/1k) | stock phrase 24, explained subtext 9, continuity 8 | revise | C10-23, F13-01, C18-03, N-01, N-11, N-12, N-13, N-27, N-28, N-47, N-50 |
| 14 | 4 | Deep. The opening briefing (L5 to 19, about 400 words to one paragraph); the triple ending; the parley staging | 28 | 63 (23.9/1k) | stock phrase 12, modern register 9, correction 7 | revise | CL-01, N-03, N-11, N-13, N-14, N-28, N-43, N-46, N-47 |
| 15 | 4 | Deep. Five moralising section endings; the surrender (L43 to 61); the wrap-up (L253 to 277); the case against the company argued four ways (L185 to 205) | 25 | 72 (18.3/1k) | stock phrase 15, modern register 11, explained subtext 7 | revise | F12-04, C18-04, CL-01, RV-02, BL-04, N-04, N-14, N-15, N-27, N-28, N-48, N-53 |
| 16 | 4 | Deep. De Lannoy's confession (L341 to 373, D2); the montage signposts; the blue-coat scene (L273 to 287, D8); the ending (L417 to 439) | 25 (29 if the blue coats go) | 94 (16.5/1k) | stock phrase 23, modern register 13, continuity 10 | rewrite | C10-29, F12-04, C18-02, C18-03, CL-01, BL-04, N-01, N-03, N-04, N-15, N-16, N-25, N-28, N-39, N-40 |
| 17 | 4 | Deep. The Revathi section (L199 to 281); the brochure description of the house (L49); two five-beat endings | 32 | 64 (19.5/1k) | stock phrase 12, explained subtext 10, modern register 9 | rewrite | C10-30, CL-06, N-21, N-29, N-31, N-40, N-41 |
| 18 | 4 | Medium. The threat block (L103 to 127); the opening (L3 to 13); four endings, end on L261 | 30 | 62 (23.5/1k) | stock beat 9, stock phrase 7, tricolon 6 | revise | C10-22, C10-33, N-07, N-45, N-48 |
| 19 | 4 | Deep in narration only; light in dialogue; almost nothing in the brother's letter. Opening (L3 to 11), vigil (L175 to 193), gate scene to the end | 37 | 65 (22.6/1k) | stock phrase 18, kicker 9, explained subtext 7 | revise | C10-34, C10-35, C18-05, RV-01, N-22, N-38, N-39 |
| 20 | 4 | Deep. The proposal (L77 to 151), the rite's glosses (L220 to 262), the feast menu and lecture (L278 to 306), the aftermath (L386 to 420) | 35 (28 on a lighter reading) | 86 (18.8/1k) | modern register 14, stock phrase 14, balanced antithesis 9 | rewrite | C10-36, C10-37, F12-04, BL-02, N-08, N-21, N-37 |
| 21 | 4 | Deep. Re-voice the ledger (L43 to 72) as a revenue clerk's leaves; the coda (L195 to 215) | 22 | 55 (25.8/1k) | stock phrase 12, modern register 9, kicker 7 | rewrite | C10-38, N-09, N-18, N-19, N-22, N-23 |
| 22 | 4 | Deep. The fight (L93 to 237, about 1,130 words); the aftermath (L267 to 305); the offer scene (L331 to 383); three stacked endings | 18 | 77 (20.3/1k) | stock phrase 18, continuity 9, modern register 8 | rewrite | C10-41, N-17, N-29, N-40, N-43 |
| 23 | 4 | Deep. The temple section (L415 to 529): cut if D7 is taken, re-voice if not; the seams at L343 to 381 | 20 (35 if the temple section goes) | 126 (24.7/1k) | stock phrase 34, modern register 20, correction 12 | rewrite | C10-41, C10-43, CL-09, N-01, N-17, N-29 |
| 24 | 4 | Deep. Thirteen aphoristic section endings, fixed as one pass; the Thoma and Avraham block (about 1,535 words, compress); the coat thesis stated five times | 26 | 158 (19.0/1k) | stock phrase 39, correction 19, modern register 14 | rewrite | C10-44, C18-05, CL-06, BL-04, N-04, N-16, N-29, N-39, N-41, N-53 |
| 25 | 4 | Deep. The Duarte revelation (about 1,150 words to 740); the coda (L336 to 348); the sent letter against the burned letter (D11) | 24 | 74 (22.8/1k) | modern register 15, stock phrase 11, kicker 10 | rewrite | C10-47, C12-03, N-02, N-06, N-39 |
| 26 | 4 | Deep. Commentary at the torch (L115 to 121) and the fight (L147 to 153); the king-over-house theme stated seven times; four endings | 18 | 68 (26.2/1k) | stock phrase 16, balanced antithesis 7, modern register 7 | revise | C10-48, C10-49, BL-03, N-40, N-52 |
| 27 | 5 | Deep. Open on Padmini's fever and pyre (move L31 to 41); the battle told as verdicts; five endings (L215 to 231) | 27 | 63 (27.1/1k) | stock phrase 14, correction 7, balanced antithesis 6 | revise | C12-03, C18-05, BL-03, N-18, N-19, N-53 |
| 28 | 4 | Deep. The ceremony built as a trailer (L3 to 97); the chapel scene states one idea seven times (L209 to 249); five endings after L279 | 37 | 84 (24.1/1k) | stock phrase 16, explained subtext 9, fragment list 9 | rewrite | C10-51, C10-52, CL-05, BL-04, N-04, N-05, N-09, N-18, N-26, N-30 |
| **All 30 units** | 3: seven units; 4: 22; 5: one | Medium 11 (Chs 1 to 9, 11, 18); Deep 19 | 25.4 weighted (chapters 25.2) | **2,024** (20.9/1k) | stock phrase 427, modern register 223, correction 178, kicker 167, explained subtext 149 | rewrite 19, revise 11 | 112 still present, 14 unclear |

Book-wide backlog items that belong to no single chapter: C10-53, F12-03, CL-07, CL-10, CL-11, CL-12, N-42, N-44. Character guide: FM-01 to FM-07 and FM-14. Glossary: FM-08 to FM-14.

How to read the triage:

- **Density and size point in different directions.** By rate, the worst units are the Prequel, Chapter 12, the Foreword and Chapter 27. By volume, they are Chapters 24 (158), 23 (126), 13 (96) and 16 (94). Plan batch time by volume and calibration by rate.
- **The Medium chapters are not light work.** Chapter 8 is Medium and still cuts about 30 percent, because one lecture and one close make up half of the cut. Medium means the line edit plus a few named blocks; Deep means the line edit plus scene rebuilding.
- **The cut falls on narration.** In the audits and in all six pilot versions, dialogue lost little beyond tags and stock beats, and the dialogue share of the text rose after every edit (Ch 1 passage from 29.5% to 31 or 32%; Ch 27 passage from 50.8% to 53 to 55%). A chapter whose dialogue share falls after editing is being over-cut.

## 3. Book-level findings

### 3.1 Rhythm and repetition

| Measure (first edition, 28 chapters) | Count | Old ration | What the adjudicated passes kept |
|:-|:-|:-|:-|
| One-sentence paragraphs | 1,767 of 4,020 (44%); 56% of narration paragraphs | none | a third to a half fewer (Ch 1: 13 to 7; Ch 9: 35 to 21; Ch 18: 45 to 26) |
| Standalone one-liners in narration | 490 | none | Ch 27 pilot passage: 8 to 1 |
| Short paragraph-final kickers | 186 | 1 a page | Ch 5: 3 to 1; Ch 18: 8 to 3 |
| Not-but family | 227, plus 24 two-sentence pairs the scanner misses | 1, dialogue only | none in narration, except one line whose second half is concrete; 1 or 2 in dialogue |
| "as if" | 79 in 27 chapters | 1 | 1, occasionally a second in dialogue |
| "like a / like the" | 89 | 2 | 0 to 2, from his own world |
| slowly, quietly, softly (and "carefully") | 101 (and 18) | 2 | 0 to 2, usually 1 that carries character |
| Verbless fragments | 276 | 3 for effect | 0 to 2 for effect; inventories exempt |
| Style-sheet excess (minimum edits to comply) | 649 | 0 | Ch 9: 17 to 2; Ch 19: 29 to 1 |

Other repetition that needs a decision rather than a cut:

- **Recycled sentences between chapters**: three love-scene lines shared by Chs 16, 17 and 20; two halls built from one template (ch5:125, ch6:21 and ch6:37); "I thought of Goa. Of Keshavrao's hand slipping from the rope." (ch16:383, ch24:621).
- **Stock gestures across the cast**: nodded 36, jaw tightened 15, mouth twitched 13, "said softly" or "said quietly" 36, "It was not a question." 6, "He did not need to." 6, Ramayyan's stylus as a reaction shot about a dozen times, Padmini's stick as punctuation about 30.
- **Scene-level duplication**: two uniform scenes (Chs 16 and 24); three temple knife attacks (Chs 21, 22, 23) with the extermination order given twice; three renunciations of the north (Chs 19, 22, 25); the list of attempts on the king's life three times (Chs 10, 21, 22); four "we outlast empires" speeches; two "my grandfather, my father, I" speeches in one chapter (ch24:659, ch24:767). These are Gate 0 decisions D7 to D9 and D14.

### 3.2 Motifs

| Motif | First edition | Second-edition home |
|:-|:-|:-|
| Storm | 55 hits in 20 chapters, 22 figurative; in the closing lines of Chs 1, 5, 7, 8, 13, 21, 25 | Literal in Chs 2 and 3; "the storm" as Nagoji's name for the wreck; one plant, the old woman at ch5:105 ("That one carries storms in his bones"); one payoff, ch13:321 ("The storm was here.") |
| Name and number | The spine: ch1:5 to 7, the renaming in Ch 17, the letter that kills "Nagoji" (Ch 19), the ledger (Chs 21, 25) | Keep every step; cut the restatements ("The stranger is gone" repeated, "The Deccan son was gone", "That boy was gone") |
| Counting and ledgers | "calculate" 24, "the weight of" 19, weigh 15 | Nagoji counts, Ramayyan writes; "the weight of" literal only |
| Horse (title) | 186 mentions; fades after Ch 16 | Fix the three breaks (D4): Kanka's sex and death, Kayal missing at Colachel, a mount "lost in the storm" that never existed |
| Teeth and Tiger | 36 teeth or tooth, spent early; nobody calls the king the Tiger in Part II ("Court of the Tiger") | Teeth planted at ch4:63, one Tiger plant in Part II (D13), both landed in Part IV |
| River, doors, threads | 31, 33 and 30 uses, mostly figurative | River: Ch 19 (Padmini) only. Doors: the hidden cellar only. Threads: the *tali* in Ch 20 only |
| Coat | Chs 15, 16, 24 | A mirrored pair: coat off (Ch 15), coat on (Ch 24); Ch 16's scene cut or shrunk (D8) |
| Jackfruit tree | 18 | Padmini's courtyard only; the hill shrine in Ch 22 gets another tree |

### 3.3 Openings and endings

- **Openings follow three templates.** Eight chapters open with a statement and then correct it (1, 3, 5, 7, 17, 19, 22, 27); seven open on a date and backstory (8, 11, 12, 14, 20, 24, 28); four open on a smell (13, 18, 23, 25). The strong openings (2, 13, 16, 21, 26, and Ch 1's first line) start on one concrete fact in scene.
- **Endings**: 22 of 28 end on a summary or moral; at least 20 end in a cascade of two to six one-line paragraphs; ten break the old sheet's rule on the last paragraph ("But", "For now", "For the moment", "And some", "And, in time", "Perhaps"). Chs 16 and 19 share one closing idea ("That was enough for now." / "For the moment, that was enough."), and Chs 1 and 7 share another ("Storms do not ask permission").
- **After reconciliation** the 30 units end on 11 images, 11 actions and 6 lines of dialogue, with one cliffhanger (Ch 13) and the Foreword on a fact. The full register is in `STYLE_SHEET_v2.md` section 7. Where a chapter audit and OEM disagree, the chapter audit wins, because it read the chapter against its neighbours (Chs 1, 2, 5, 7, 8, 10, 15, 17, 24 and 27 change this way). Four collisions remained, and I resolved them:
  1. **Chs 21 and 26 both ended on Ramayyan writing.** Ch 26 takes its own audit's alternative: move the Ibrahim coda (L269 to 281) before Revathi arrives, retime it "In the days after the fire", and end on Revathi at L249 ("I did not expect to like it when those days came.").
  2. **That would put Revathi on the last beat of both Chs 25 and 26.** Ch 25 takes its own audit's alternative: end on Padmini's walk to the gate, her last scene before she dies offstage in Ch 27, and cut Revathi's letter (her point is made in person in Ch 26). Fallback, if the author wants the letter: Ch 25 ends on it, Ch 26 ends on the stylus, and the echo of Ch 21 is accepted.
  3. **Three weapon endings**: Ch 6 (the hand at the empty sword hip), Ch 20 (the sword left leaning against the wall), Ch 23 (a nick in the talwar he does not remember making). Keep them as one deliberate arc of vow, peace and stain, and let no other chapter end on a weapon. Ch 23's version holds only if the temple section is cut (D7); otherwise use OEM's corridor line, "The Tiger has teeth."
  4. **Padmini in the last beat of Chs 8, 17, 19, 22 and 25.** Drop the stick from Ch 17's last sentence and end on the rain. Four remain, each doing a different job: introduction, homecoming, send-off, last scene.

### 3.4 Register and anachronism

- **290 findings**: modern idiom 63, management vocabulary 52, modern military jargon 49, wrong-period names and facts 32, scholars' labels 21, material culture 20, therapy register 18, machine images 16, typography 10, clock time and units 9.
- **Fix them as patterns**, in this order: (1) Ramayyan's leaves become a revenue clerk's notes (names, kin, lands, debts, grudges, short verbs; ch25:208 to 210 is the model); (2) office words (schedule, partners, network, logistics, "reach out"); (3) modern military words (perimeter, unit, casualty report, friendly fire, checkpoints); (4) therapy register ("your feelings to catch up", "you deserve one"); (5) machine images (reset, shockwave, thermal, controlled burn); (6) clock and measure (minutes, yards, pounds, percent, "half past eleven"); (7) titles (diwan to Dalawa, no Majesty or Highness, English for British, Lanka or Ceylon for Sri Lanka); (8) scholars' words (matrilineal, consolidation, state-building, foreshadowing); (9) the filing-cabinet habit (six things "filed away").
- The full lexicon and the house spelling list are in `STYLE_SHEET_v2.md` sections 9 and 10.

### 3.5 Source-of-truth and continuity risks

1. **Baseline.** The chapter files contain every published paragraph plus the author's later edits. Start there (D1), and keep the EPUB text, which now survives only in `manuscript_complete.md`, as the frozen first-edition reference. Log the 13 post-build unit differences as content changes, apart from anti-slop edits, so the Note to the Second Edition can describe them honestly.
2. **De Lannoy (D2).** The files have him surrender with the garrison; the published book has him desert before the end. The files still carry desertion leftovers (ch16:341 to 373, "Why did you cross?"), a dangling reference (ch14:163), a Rijtel against Donnadi muddle over who commands, the Historical Note's "crossed over" (L15), an age of 43 against a historical 26, and Arras against Zeeland (ch24:239).
3. **Unpublished exposition (D3).** About 2,500 words were added after the last build: the Foreword's walls, the Ch 7 horse essay, Ch 12's walls, the Ch 13 history block, Ch 16's pay and backstory. The style sheet would cut most of it anyway.
4. **Stale and misleading sources.** `manuscript_v2.md` is two builds old, yet the project `CLAUDE.md` still lists it as a file to keep in sync (D21). The LFS "accepted final reading proofs" are graphic-novel proofs, not the prose book. Which build readers bought is not recorded; SoT section 10 gives five quick checks against a retail copy.
5. **Build tools.** Pandoc is not installed on this machine, so Phase 4 (EPUB and print) needs setup before the end.
6. **Mechanical issues to clear first**: mixed straight and curly quotes in 14 or more chapters, two spaced hyphens used as dashes (ch13:121, ch16:369), five US spellings, leading spaces in Chs 23 and 25, an unclosed quote at ch8:87, name variants (Ponnam, *kapitan*, Valia), and about fifteen typos. Doing this first keeps the prose diffs readable.
7. **The highest-priority continuity items** (backlog order): Dhanaji's origin; the "fled the Peshwa" backstory; the horses; De Lannoy; Revathi as wife; callbacks to events not yet shown (the ch19:181 chaver, the ch18:121 ledger entry, the Ch 20 "marches", the Ch 21 broom); the Colachel dates and garrison numbers across Chs 11 to 15; the duplicate scenes; one-word history fixes (Thrippadidanam in January, "Nair Brigade", the Nayak of Madurai after 1736); history liberties to change or disclose; Kottarakkara's ruler; the front matter.

### 3.6 Where the audits disagree, and my rulings

| Question | One report | Another report | Ruling |
|:-|:-|:-|:-|
| "The sea does not care" (Ibrahim) | Ch 11 audit: home is ch11:407 | Ch 13 audit: ch13:205 is the best copy | ch11:407, the first use, where "Neither do I" makes it his. Ch 13 keeps "Best to have several listening" without the sea clause; ch15:105 goes |
| Ramayyan as a "river pilot" (ch11:303, ch13:103) | OEM: keep one | The river motif lives in Ch 19 | Cut both |
| Taste of ash (ch14:181 the king; ch26:191 Padmini) | OEM: keep one | Both chapter audits defend their line | Keep both: different speakers, and Padmini's ash is literal (her own fields). If only one survives, Ch 14's, which ends its chapter |
| Padmini's stick | OEM: three speaking uses (ch8, ch26:29, ch28:11) | Ch 8 audit keeps four in Ch 8; Ch 23 audit defends the cane struck and not struck (L377, L389) | A signature object, never punctuation. Ch 8 keeps two (her introduction and "She rose without leaning on the stick"); every other chapter one at most, where it does work |
| Savitri's "outlasting" line (N-53) | Ch 27 audit: keep the garden line (L157) | OEM: keep "stories outlast walls" (L219) | Keep the garden line, which Ch 28 pays off three times. At L219 keep "every succession you denied" (all three pilot judges asked for it back) and end on "They will remember me." Cut "stories outlast walls", "ruins and dust" and "Empires fall. Women remain." |
| "one foot in each river" | OEM: ch19:153 only | Ch 22 audit defends Padmini's "which current to trust" (L397) | Allow ch22:397 as the one echo, since Padmini is quoting herself; cut ch22:373 and 409 and ch28:129 |
| Italics | VOICE_BIBLE: first use in each chapter, then roman | REGISTER: every use, with chaver and kalari naturalised in roman | REGISTER's rule (D18). It is easier to check, and the pilot judges marked dropped italics on *huzurat* as an error |
| Company | the text: about 65 lower case, 22 capitalised | REGISTER: lower case | "the company"; full names capitalised; drop "Honourable" |
| "matrilineal" | used six times in narration and speech | REGISTER: "the law of the mothers" or *marumakkathayam* | Replace book-wide and in the glossary in one pass (the pilot's medium version already did so in Ch 27) |
| Duarte's "said softly" (ch1:69) | Ch 1 audit: cut | Pilot fidelity judge: its loss removes his gentle, manipulative manner | Keep it as Ch 1's one soft adverb |
| "landlocked" (ch1:7) | Ch 1 audit: drop | Two pilot judges: put it back | Keep |
| "Chimaji was coming for Goa" (ch1:63) | Ch 1 audit: frame it as his hope | Fidelity judge: "I told myself" turns certainty into hindsight | Frame it as hope here only, because Goa city never fell, and log it as a history correction. No other hindsight hedges |
| Ch 10 ending | OEM: a jackfruit-tree image | Ch 10 audit: that repeats Ch 8's close | Ch 10 audit's raid ending |
| Ch 24 ending | OEM: men drilling under the foreigner's tooth | Ch 24 audit: a wall at dusk collides with Ch 16 | Ch 24 audit's dialogue ending |
| Stair count, Chs 1 and 2 | OEM ends Ch 1 on "Nineteen, up to the light" | Ch 2 audit moves the count to the climb ("nineteen, in two turns"); Ch 1 ends on the clerk's chalk | Ch 2 carries the count; the number must agree in both chapters |
| "We do not plough" (ch8:33) | VOICE_BIBLE: his caste reflex, keep | Ch 19 shows a farming family; ch21:47 | Author (D20) |

### 3.7 Audit proposals that add facts, and need the author's approval

The pilot rewriters worked under a no-new-facts rule and declined every addition the audits proposed; the judges did not penalise the absence. Treat the audits' additions the same way. Staging the scene already implies is allowed without asking (João watching over the tongs, "the sweat of frightened men", "She looked down at her bound hands"). Everything below needs the author's yes, chapter by chapter.

- **New events or episodes**: Ch 10's raid on a *madampi* near Attingal; Ch 1's rumour of a southbound ship and the clerk chalking the wall; Ch 12's Nair at the cook fire; Ch 19's ferry clerk who writes Nagoji's answer on a leaf; Ch 27's letter under the Elayadathu seal and a horse from Nagoji's lines at the exile.
- **New numbers**: Ch 27's "three muskets to each of hers" and Thoma's light guns at Kottarakkara; Ch 2's twelfth mark and nineteen steps; Ch 14's "perhaps two hundred paces"; Ch 26's seven years for pepper vines (verify the figure).
- **New objects with story weight**: ink on Savitri's fingers (Ch 27); dew on the coat's buttons (Ch 15); Megha waiting at the steps (Ch 16); the unremembered nick in the talwar (Ch 23); the hands held out to the rain (Ch 28); the church bells of Bardez across the Chapora (Prequel).

### 3.8 What the scanner cannot see

- It misses the two-sentence correction ("It was not X. It was Y."). A plain search finds 24 in the chapters, 5 in the Foreword and 5 in the Prequel: `grep -nE "(was|is|were|are) not [^.?!]{1,80}\. (It|He|She|They) (was|is|were|are) "`.
- Its lexical markers count dialogue, and its one-sentence-paragraph count includes speech; use the narration figures.
- It cannot tell whether a simile's second half belongs to Nagoji, whether a fragment is an inventory, or whether a maxim passes the drill-ground test. It is a necessary check, not a sufficient one.
- OEM section 8 lists motif and tic counts worth adding to it (storm, teeth, river, door, thread, jaw, "It was not a question", "wore no crown", "for the first time", "washed up", stylus, and an endings check).

## 4. Pilot results

### 4.1 Setup

Two passages were rewritten at three intensities under three rules: keep every fact, keep the meaning of every line of dialogue, add no invented detail. Passage A is Ch 1, lines 5 to 69 (1,359 words; severity 3, mostly narration). Passage B is Ch 27, lines 99 to 231 (1,241 to 1,244 words depending on the counter; severity 5, about half dialogue). Labels were shuffled per passage and hidden from three judges, who scored each version from 1 to 10 for AI residue (higher means fewer machine tells), fidelity and readability, listed remaining tells and lost content, and picked one version to publish. Their stated lenses differed: judge 1 weighted leftover tells, judge 2 fidelity, judge 3 a demanding reader.

### 4.2 Scores

| Version | Passage | Intensity | Words, before to after | Word change | Mean AI residue | Mean fidelity | Mean readability | Judge picks |
|:-|:-|:-|:-|:-:|:-:|:-:|:-:|:-|
| A_K | Ch 1 | light | 1,359 to 1,237 | −9.0% | 5.67 | **8.33** | 7.00 | 1 (judge 2) |
| A_X | Ch 1 | medium | 1,359 to 1,197 | −11.9% | 7.67 | 7.33 | 7.67 | 1 (judge 3) |
| A_Q | Ch 1 | deep | 1,359 to 1,206 | −11.3% | **8.00** | 7.00 | **8.33** | 1 (judge 1) |
| B_X | Ch 27 | light | 1,241 to 1,104 | −11.0% | 4.67 | 7.33 | 6.33 | 0 |
| B_Q | Ch 27 | medium | 1,244 to 1,107 | −11.0% | 7.00 | **8.00** | 7.67 | 1 (judge 2) |
| B_K | Ch 27 | deep | 1,244 to 1,110 | −10.8% | **8.00** | 7.33 | **8.00** | 2 (judges 1 and 3) |
| **Light, pooled** | both | light | 2,600 to 2,341 | −10.0% | 5.17 | **7.83** | 6.67 | 1 of 6 |
| **Medium, pooled** | both | medium | 2,603 to 2,304 | −11.5% | 7.33 | 7.67 | 7.67 | 2 of 6 |
| **Deep, pooled** | both | deep | 2,603 to 2,316 | −11.0% | **8.00** | 7.17 | **8.17** | 3 of 6 |

Remaining tells listed per judge, mean: light 12.2, medium 8.2, deep 7.3. Lost-content items listed per judge, mean: light 8.5, medium 9.2, deep 10.5.

### 4.3 What the scanner adds

| Measure | A source | A light | A medium | A deep | B source | B light | B medium | B deep |
|:-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Core hits per 1,000 words | 9.6 | 7.3 | 5.0 | 4.1 | 25.8 | 19.0 | 7.2 | 5.4 |
| One-sentence share of narration paragraphs (%) | 27.8 | 17.6 | 17.6 | 17.6 | 60.6 | **65.4** | 31.2 | 33.3 |
| Standalone one-liners in narration | 4 | 2 | 2 | 2 | 8 | 7 | 1 | 1 |
| Short paragraph-final kickers | 0 | 1 | 0 | 0 | 4 | 1 | 1 | 0 |
| Short sentences (%) | 33.3 | 36.4 | 36.4 | 34.0 | 53.7 | 47.1 | 43.1 | 38.8 |

The light pass on Ch 27 cut sentences without joining the paragraphs they left behind, so the passage became choppier than the original. That is the pilot's clearest mechanical lesson: **when you cut, re-paragraph.**

### 4.4 What the judges rewarded and penalised

Rewarded:
- Abstractions replaced with things the reader can see: "João was watching my face over the tongs." for "They wanted to see grief; they wanted to use it as a lever."; "He sat our enemies at his own table"; "no open ground for a charge and no clean line for a volley".
- Fragments and triple anaphora folded into ordinary sentences, and one-line kicker paragraphs removed.
- A stock beat replaced by an act instead of simply deleted: "She looked down at her bound hands." for "Something flickered in her face. Memory. Pain." (two judges called it the best single fix in the pilot).
- Endings on an act ("I watched the road until she was gone from it.").

Penalised:
- **Surviving tells** (the light versions): "an unholy combination", "shimmered in the dim light", "He knows the game", the four-fold "Tell him", "Our eyes met", "Empires fall. Women remain."
- **New slop introduced by the rewrite**: "Who was in the right never entered the sum" (a new kicker); "I would get to choose how I died" and "You know where you stand" (modern idiom); "when you and I are ash" (purple); "murder dressed in manners" kept as an epigram.
- **Changed character beats**: "the groan was halfway out before I shut my teeth on it" turns a man who bites back the groan into one who lets it out.
- **Lost content the book needs**: the meaning of *huzurat*; "every succession you denied" (Savitri's actual case); "landlocked"; the pauses between the king's lines in the tent scene; the ownership thread in Savitri's argument; the concession that Travancore won by force, not by right.
- **Frames that contradict the character**: a simile making Savitri "a sardar's widow" defending "her husband's fort" imposes a patrilineal frame that her own speech rejects.

Every judge who chose a version asked for grafts from the other two. On Ch 1, judge 1 wanted deep plus "landlocked", the italics and the medium version's rain simile; judge 2 wanted light plus the medium version's tongs line and the deep version's single-sentence threat; judge 3 wanted medium plus the deep version's "the news of each running down the Konkan ahead of our horses" and "He knows how this is done". On Ch 27 all three asked for "every succession you denied" back and for one pause in the tent scene. Those grafts are the calibration: they describe a version with deep's residue score and medium's fidelity.

### 4.5 Recommendation on intensity

1. **Retire the light pass.** Every judge on both passages gave it the lowest residue score (5.17 pooled). It left about 12 tells per passage, won one pick (from the fidelity-weighted judge, on the easier passage) and made Ch 27's rhythm worse. A second edition whose purpose is removing machine patterns cannot ship a pass that leaves most of them in place.
2. **Adopt one line standard for every chapter: deep in narration, medium in dialogue, never in facts.** In narration, do what the deep versions did: rebuild paragraphs, replace abstractions with objects, fold fragments into sentences, end paragraphs on a fact or an act. In dialogue, do what the medium versions did: keep every line's meaning and its pauses, cut tags and stock beats, collapse triple anaphora to the concrete item. Add no facts. Apply the ten guardrails in `STYLE_SHEET_v2.md` section 5, which are the judges' grafts written as rules. Deep won residue and readability on both passages and 3 of 6 picks; the fidelity-weighted judge never chose it, and the guardrails target exactly the losses that judge listed.
3. **Should intensity vary by chapter? The line standard should not; the scope should.** The pilot measured how hard to edit a sentence, and the answer did not depend on the chapter: deep narration won on a severity-3 passage and on a severity-5 passage. What varies is how much of each chapter is rebuilt, which is the Medium or Deep label in the triage table. Medium chapters (1 to 9, 11, 18) get the line edit, a rebuilt ending and a few named blocks. Deep chapters (the Foreword, the Prequel, 10, 12 to 17, 19 to 28) also get scene-level rebuilding of the blocks listed. Inside a chapter, treat letters and dialogue lightly where the audit says so: Ch 19's letter from his brother is touchstone T11 and needs almost nothing.
4. **Expected yield.** The line standard removes about 10 to 12 percent of a dense passage. The named blocks bring each chapter toward its audit estimate. Treat a chapter that goes more than five points past its estimate, or loses dialogue share, as over-cut, and review it before accepting.
5. **Limits of the evidence.** Two passages, both dense, both chosen from the audits' problem areas; three judges who disagreed by lens. The calibration batch (Chs 1 to 3 and 27, whole) is the real test, and the author's read of it is the gate before the full pass.

## 5. Recommended editing order

| Step | Units | Words (1e) | Confirmed issues | Why in this position | Decisions needed first |
|:-|:-|:-:|:-:|:-|:-|
| 0. Gate 0 | none | | | Settle the decisions in section 6. Make the 2e working copies from the chapter files and run the mechanical pass (quotes, spaced hyphens, US spellings, leading spaces, the unclosed quote at ch8:87, name variants, typos) so later diffs show prose edits only. Commit the baseline scan | D1 to D21 as listed per batch |
| 1. Calibration | Chs 1, 2, 3, 27 | 8,989 | 196 | Chs 1 to 3 are the reader's first pages and the lowest-severity chapters, so they set the voice. Ch 27 is the only severity-5 chapter and holds the late-book dialogue problem the pilot tested. The author reviews all four; `STYLE_SHEET_v2.md` is adjusted once, then frozen | D1, D4, D14, D15, D18 |
| 2. Part I | Prequel, Chs 4, 5, 6 | 7,703 | 172 | Lowest severity. The plants must be placed before any payoff is edited: storm (ch5:105), teeth (ch4:63), the sword hip (ch6:191), "He wore no crown" (ch6:39) | D4, D12, D19 |
| 3a. Part II, first half | Chs 7 to 10 | 11,914 | 230 | Kayal, Padmini, Revathi and the court are introduced here; their signatures and rations are set for the rest of the book | D3, D4, D20 |
| 3b. Part II, second half | Chs 11 to 13 | 12,416 | 235 | The Colachel run-up; Ch 13 holds the storm payoff and the unpublished history block. Edit with Ch 14's opening in view (shared timeline and a duplicated bombardment) | D3, D5, D6, D10, D13 |
| 4a. Part III, first half | Chs 14 to 17 | 15,575 | 293 | Colachel, De Lannoy, the new army, the renaming | D2, D4, D8, D10 |
| 4b. Part III, second half | Chs 18 to 21 | 12,222 | 268 | The letters and the ledger; Ch 18's forward reference to Ch 21 and Ch 19's to Ch 22 must follow the D17 wording | D9, D11, D17 |
| 5a. Part IV, first half | Chs 22 to 24 | 17,195 | 361 | The heaviest batch by volume (Ch 24 alone has 158 issues); the temple-attack and uniform decisions change Chs 23 and 24 structurally | D7, D8, D9 |
| 5b. Part IV, second half | Chs 25, 26, 28 | 9,324 | 226 | The ending collisions in section 3.3 are settled here; Ch 28's last page answers Ch 1 | D11, D14, D16 |
| 6. Foreword | Foreword | 1,501 | 43 | Last, because it describes the edited book, and two of its sections depend on D2 and D3 | D2, D3, D21 |
| 7. Sync and build | glossary, character guide, Historical Note, synopsis, outline; Note to the Second Edition; EPUB and print | | | Support documents follow the edited chapters; content changes are listed apart from prose edits; install pandoc before the build | D21 |

Within each batch, edit in file order so plants are edited before payoffs, and check each new ending against the register as you go.

## 6. Author decisions (Gate 0)

Each row gives my recommendation. The Part I line edit can start once D1, D4, D12, D14, D15, D18 and D19 are settled; the rest are needed before the batch named in section 5.

| # | Decision | Recommendation | Affects |
|:-|:-|:-|:-|
| D1 | Baseline text | The chapter files (SoT section 8); freeze the EPUB text as the first-edition reference; log the 13 post-build differences as content changes | all |
| D2 | De Lannoy: surrender (files) or desertion (published) | SUPERSEDED by PLAN.md v2 section 2B: the project's source (de Lannoy 1997, kulaperumal.codex.md) has him desert at Kanyakumari on 2 August 1741, as the published text and Book 2 do. Original recommendation: Surrender, which is closer to history and is the author's latest text. Then fix ch16:341 to 373 ("why did you stay"), his age (N-04), Arras against Zeeland (ch24:239), ch14:163, Rijtel against Donnadi, the Historical Note (L15) and the character guide | FW, 11, 14, 15, 16, 24, 28, guide, Historical Note |
| D3 | The 2,500 words of unpublished exposition | Keep the facts, compressed as the audits propose: the Foreword's walls to one paragraph; the Ch 7 essay to about 200 words; the walls told once, at ch11:149; the Ch 13 block to about 450 words; the pay grievance told once, at ch16:373 | FW, 7, 12, 13, 16 |
| D4 | The horses (BL-01, N-03, FM-15) | Kanka is a black stallion shot at the capture (Ch 1, and the Prequel audit's ending); change prequel L23 and ch7:145. Kayal, the bay mare, carries him at Colachel (ch14:101 "him" becomes "her"). Choose whether Kayal or Megha dies at the start of Ch 16 | PQ, 1, 6, 7, 8, 14, 16 |
| D5 | Dhanaji's arrival (N-01, FM-02) | Add a short arrival beat before ch11:123; fix ch13:221 and ch16:21 | 11, 13, 16 |
| D6 | The "fled the Peshwa" backstory (N-02) | Replace with the capture history at ch11:129, ch12:71, 73, 141, 145 and ch25:64 | 11, 12, 25 |
| D7 | Two chaver attacks on the heir (N-17) | Cut ch23:415 to 529, give the extermination order once (Ch 22), reword ch24:387 | 22, 23, 24 |
| D8 | Two uniform scenes (N-16) | Cut Ch 16's blue coats (L273 to 287) to a sentence; keep Ch 24's scene | 16, 24 |
| D9 | Three renunciations of the north | Ch 19 is the family, Ch 22 the frontier only, Ch 25 the Maratha state; soften ch28:129 | 19, 22, 25, 28 |
| D10 | Colachel timeline (N-10 to N-14, F13-01) | Adopt the Ch 13 insert's date (the eve is 9 August 1741); one garrison figure; reconcile Ch 14's surrender with Ch 15's march-out | 11 to 15, glossary |
| D11 | Revathi (N-05, N-06) | She is his wife on every page of Ch 28 (L127, L153); keep the burning in Ch 25, which is the published text | 25, 28 |
| D12 | Storm | One plant (ch5:105) and one payoff (ch13:321); cut the other figurative storms. The Voice Bible's alternative adds ch1:113 as a second plant | 1 to 28 |
| D13 | The Tiger in Part II | Someone calls the king the Tiger once in the Ch 11 hall (L171 to 297); Part IV lands it | 11, 23 |
| D14 | Savitri's outlasting line (N-53) | Garden line kept; "every succession you denied" kept; "stories outlast walls" cut (section 3.6) | 27, 28 |
| D15 | Kottarakkara's ruler (N-18) | He dies confined (ch27:137, ch28:173); cut the flights to Kochi (ch27:63, 93) | 21, 27, 28 |
| D16 | History liberties (N-19, N-27, N-29, CL-05) | Move the Thrippadidanam to January (Ch 28); disclose Mathu Tharakan's birth year, the heir's age and Kottarakkara's date in the Author's Note, or change them | 11, 13, 15, 23, 27, 28, Note |
| D17 | Ramayyan's ledger wording (N-19) | Choose "To be settled before the monsoon" or "when the Dutch move", and carry it through ch18:121, ch25:90 and ch27:55 | 18, 21, 25, 27 |
| D18 | Italics | REGISTER's rule: italicise non-English common nouns every time; titles, forms of address, naturalised words, chaver and kalari in roman | all |
| D19 | Titles | "diwan" to Dalawa (18 changes), with one beat in Ch 6 where Nagoji is told the local word; no Majesty or Highness | 6, 7, 10, 13 to 28 |
| D20 | Family details | "We do not plough" (ch8:33) against the farming family of Ch 19 and ch21:47; the brother's name, Ramji (ch19:199) or Bhalerao (ch19:213), which collides with Book 3 | 8, 19, 21 |
| D21 | Front matter and housekeeping | Rename the Foreword (Author's Note or Preface) and confirm its date; add a Note to the Second Edition; align the Ch 14 and Ch 22 headings with their files; drop `manuscript_v2.md` from the sync list in `CLAUDE.md` if the author agrees | FW, 14, 22, repo |

## 7. Acceptance checks for each batch

1. **Scanner**: run `scan_slop.py` on the batch with the first edition as baseline (`-b`). Style-sheet excess of 2 or less per chapter (the audits' scratch passes reached 1 to 2); no marker rises; core hits per 1,000 words fall by at least 40 percent.
2. **Hand counts the scanner misses**: the two-sentence correction search in section 3.8, and the rations in `STYLE_SHEET_v2.md` section 3 that are not scanner markers (stylus reaction shots, the stick, epigrams per speaker per scene).
3. **Rhythm**: one-sentence paragraphs under 35 percent of narration paragraphs; no two standalone one-liners in a row in narration.
4. **Endings**: each chapter ends as the register in `STYLE_SHEET_v2.md` section 7 says, or the change is logged; the last paragraph does not open on But, For now, For the moment, And, Perhaps, Now, So or Yet; at most one short standalone paragraph in the last ten lines.
5. **Protect list**: every Do-not-cut item for the chapter (`STYLE_SHEET_v2.md` section 6) is present, or its change is logged with a reason.
6. **Fidelity**: no new facts (diff review against guardrail G1); dialogue share holds or rises; the cut is within five points of the audit estimate.
7. **Typography**: no em dashes, no double or spaced hyphens used as dashes, one quote style, house spellings (`STYLE_SHEET_v2.md` section 10).
8. **Read aloud**: the first and last pages of each chapter; the swap test on each scene's dialogue.
9. **Log**: anti-slop edits and content changes are recorded separately, with before and after word counts and scanner figures.
