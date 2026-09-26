# Source of Truth: Horse of the Servant, First Edition Text

Audit date: 26 September 2026
Scope: which text is the first edition of *Horse of the Servant* (Blood and Thrones, Book 1), and which text the second edition should start from.
Method: read-only. Git history (`git log`, `git show <commit>:<path>`), every committed build of `Horse_of_the_Servant.epub` unzipped into scratch space, and a paragraph-by-paragraph comparison of normalised text (quotes, ellipses, emphasis marks and whitespace normalised; every paragraph of every unit compared, plus a word-level similarity ratio). Nothing in the repo was modified, staged or fetched.

## 1. Short answer

1. **The first edition as built is `Horse_of_the_Servant.epub` at HEAD** (commit `819b98b`, 25 Dec 2025; EPUB `dc:date` 2025-12-25T19:46:45Z; sha256 `b462fc7a...`). Its text matches `manuscript_complete.md` at HEAD **exactly**, in every unit: front matter, all 28 chapters and end matter (4,118 of 4,118 prose paragraphs; the glossary matches entry for entry). The omnibus EPUB built 25 seconds later (`Blood_and_Thrones_Omnibus.epub`, 19:47:10Z) carries the same Book 1 text.
2. **The chapter files in `book1_horse_servant/` are not the first edition in 13 of 37 units.** They were edited after the last EPUB build and committed in the same commit (build 13:46 CST, commit 15:22 CST). Those edits were never compiled into any EPUB. Net effect: about +2,500 words, and De Lannoy's arc changes from *desertion before the battle* (EPUB) to *surrender with the garrison* (files). The other 24 units are identical to the EPUB.
3. **`manuscript_v2.md` is stale.** It has not changed since 15 Dec 2025 (`e2a291b`). It is the exact text of the 16 Dec 2025 EPUB build, two builds behind the current one: no Foreword, the old Chapter 12 "Threads of Alliance", the old short Chapter 11, "Arcot" horsemen, Cochin/Calicut/Ceylon, heavy use of "ledger", and the spelling "chevar". Do not use it as a source for anything.
4. **The "accepted final reading proofs" (`fe263cf`) are graphic-novel proofs, not the prose book.** The LFS files are present locally, but they hold condensed comic lettering. They show that the 2026 comic work adapted the post-build chapter files.
5. **Caveat: the repo does not record which build readers actually bought.** There is no ASIN, no ISBN for the novel, and no upload date anywhere in the repo (`output/book-edition-v5/ISBN-AND-COPYRIGHT-NEXT-STEPS.md` says "The source novel's ISBN, if one exists"). The 25 Dec build is the most likely published file because it is the last committed release artifact and replaced every earlier build. There is also some indirect evidence: on 17 Dec (`2646fe0`) the author added submission packages for HarperCollins India, Penguin India, Niyogi and Pegasus, which suggests the book had not been self-published by then. That would rule out the 14 to 16 Dec builds. Section 10 lists five checks that tell the builds apart in under two minutes against a retail copy.

**Recommendation:** start the second edition from the **chapter files** (the author's latest text, which already contain everything in the EPUB). Keep the EPUB text on record as the frozen first-edition reference, and log the 13 post-build differences as content changes separate from the anti-slop edits. Before the prose pass starts, settle the De Lannoy arc and fix the loose ends it leaves (Section 9). Details are in Section 8.

Note for `PLAN.md`: it describes `../book1_horse_servant/` as "Source (first edition, frozen)". That holds for 24 units only. For the other 13, the first-edition text now exists only in `manuscript_complete.md` and the EPUB.

## 2. Build lineage

| Commit | Date (CST) | EPUB built from | State of the text |
|:-|:-|:-|:-|
| `60ed6cf`, `5d7af12`, `c0c545b` | 14 Dec 2025 | `manuscript_v2.md` (by hand) | Broken builds: all 28 chapters in one XHTML file (7 spine files). Replaced within hours. |
| `1937ec0` to `e2a291b` | 14 to 15 Dec 2025 | `manuscript_v2.md` (by hand) | Valid EPUBs. The `e2a291b` EPUB (16 Dec 03:41Z) matches today's `manuscript_v2.md` exactly. No Foreword. Chapter 12 "Threads of Alliance". De Lannoy commands the garrison and is captured. |
| `2646fe0` | 17 Dec 2025 | (no rebuild) | Publisher submission packages added. |
| `72c8052` | 23 Dec 2025 | `manuscript_complete.md`, made by the new `build_epub.sh` from `finished_book1/` | Foreword added. De Lannoy desertion subplot added (5 hits for "crossed the lines / crossed over"). Still "Threads of Alliance" and Arcot horsemen. `manuscript_complete.md` equals the chapter files exactly. |
| `819b98b` | 25 Dec 2025, EPUB 13:46, commit 15:22 | `manuscript_complete.md`, made by `build_book1_epub.sh` from `book1_horse_servant/` | **Current EPUB.** Chapters 11 and 12 rebuilt, Madurai/Nayak instead of Arcot/Nawab, modern place names, "ledger" cut from 36 to 6, "chaver" spelling, Kanyakumari skirmish in Ch 15. |
| `819b98b` (after the build) | 25 Dec 2025, before 15:22 | never built | Chapter files revised further: De Lannoy surrenders, new exposition in the Foreword and Chs 7, 12, 13 and 16, Bhonsle correction in Ch 25. |

Evidence that the chapter files are newer than the EPUB, not older: the build script regenerates `manuscript_complete.md` from the chapter files on every run, so `manuscript_complete.md` is a snapshot of them at build time. For every diverging unit except Ch 12 (a new chapter, so neither version resembles the 23 Dec text), `manuscript_complete.md` at HEAD is closer to the 23 Dec chapter files than today's chapter files are (for example Ch 13: 0.996 against 0.882 similarity; Ch 16: 0.997 against 0.922). So the extra changes were made after the build. `git status` shows no uncommitted changes to any source file.

## 3. Build script inputs

`build_book1_epub.sh` (renamed from `build_epub.sh` in `819b98b`; no other `build_book1*` exists) joins these files, in this order, into `manuscript_complete.md`, then runs pandoc (split at level 1, table of contents two levels deep, `epub.css`, cover `images/cover.jpg`):

1. `title_page.md`
2. `dedication.md`
3. `front_matter_publication_notes.md` (the Copyright page)
4. `book1_horse_servant/front_matter_foreword.md`
5. `book1_horse_servant/front_matter_prequel.md`
6. `book1_horse_servant/front_matter_character_guide.md`
7. `book1_horse_servant/book*_chapter*.md` (shell glob; alphabetical order gives the right Chapter 1 to 28 sequence)
8. `Author_Historical_Note_nagoji.md`
9. `book1_horse_servant/glossary.md`
10. `front_matter_about_author.md`

`manuscript_v2.md` is not an input to any current script. Before 23 Dec it was fed to pandoc by hand. Pandoc is not installed on this machine at present, so a 2e rebuild will need it. The Ch 1 map (`images/map_malabar.jpg`) is embedded in the EPUB.

Filename and heading differences to keep in mind: `book3_chapter14_charge_at_colachel.md` is headed "The Siege of Colachel", and `book4_chapter22_command_of_the_marches.md` is headed "Command of the Kayamkulam Frontier". The EPUB uses the headings.

## 4. Per-chapter table

"EPUB" means the HEAD EPUB, which equals `manuscript_complete.md`. Paragraph counts are EPUB paragraphs. "Line edits" are small wording changes inside otherwise identical paragraphs.

| Unit | Chapter file vs EPUB | manuscript_v2 vs EPUB | Newest source | Notes |
|:-|:-|:-|:-|:-|
| Title page | Identical (`title_page.md`) | Differs: has "Blood and Thrones, Part 1", no tagline | `title_page.md` | |
| Dedication | Identical (`dedication.md`) | Identical | `dedication.md` | |
| Copyright | Identical (`front_matter_publication_notes.md`) | Identical text; placed before the Dedication | same | |
| Foreword | **Differs**: 8-paragraph "The Walls" section added; De Lannoy paragraph rewritten; +266 words | **Absent** | Chapter file (post-build) | Foreword first appears in the 23 Dec build |
| Prequel | Identical (1,300 w) | 3 line edits (Kochi, Vasai, Kozhikode glosses) | File = EPUB | |
| Character Guide | **Differs**: De Lannoy entry (surrender) | 7 entries differ (Nawab of Arcot entry, place names, De Lannoy) | Chapter file (post-build) | |
| Ch 1 Dungeons of Goa | Identical (1,941 w) | 2 line edits | File = EPUB | |
| Ch 2 The Slave Ship South | Identical (1,890 w) | 6 edits (one paragraph split, Ceylon, hyphenation) | File = EPUB | |
| Ch 3 The Choice in the Storm | Identical (2,837 w) | 2 line edits | File = EPUB | |
| Ch 4 The Fishermen of the Pepper Coast | Identical (1,704 w) | 4 line edits | File = EPUB | |
| Ch 5 Road to Travancore | Identical (2,001 w) | 3 edits (Arcot to Madurai) | File = EPUB | |
| Ch 6 The Coastal Hall | Identical (2,703 w) | 7 edits (king's konda hair, Nawab of Arcot to Nayak of Madurai, paragraph split) | File = EPUB | |
| Ch 7 Horses in Wet Sand | **Differs**: 5 new paragraphs on horse economics; no EPUB paragraph altered; +420 w | 15 edits (Arcot to Madurai throughout, Bassein to Vasai) | Chapter file (post-build) | |
| Ch 8 Padmini Amma's Estate | Identical (3,420 w) | mv2 lacks 3 paragraphs on inland fights (181 w); Arcot | File = EPUB | |
| Ch 9 Princess of Velinadu | Identical (3,056 w) | 2 line edits | File = EPUB | |
| Ch 10 Lessons in Travancore | Identical (2,579 w) | 1 line edit | File = EPUB | |
| Ch 11 Dutch on the Horizon | **Differs**: 8 paragraphs (early "Lannoy" naming removed, 1663 date, new closing line); +9 w | **Stale**: old 2,457-word chapter. 137 of 232 EPUB paragraphs missing | Chapter file (post-build) | EPUB Ch 11 = old Ch 11 + old Ch 12 merged, plus a new Van Imhoff flashback |
| Ch 12 The Shadow from Arcot | **Differs**: 6 new paragraphs (Aramboli walls dialogue); +182 w | **Different chapter**: "Threads of Alliance" (3,334 w). 0 shared paragraphs | Chapter file (post-build) | New chapter written for the 25 Dec build |
| Ch 13 The Eve of Colachel | **Differs**: one line expanded into a 29-paragraph history block; +897 w | 7 edits (new Ramayyan-as-general paragraph, Ceylon, Arcot) | Chapter file (post-build) | Largest unbuilt addition |
| Ch 14 The Siege of Colachel | **Differs**: 10 EPUB paragraphs cut or replaced (desertion becomes a surrender parley); -107 w | 22 paragraphs differ; mv2 lacks the 1741 dating, the November bombardment, the Tiruvattar vow and the desertion block (EPUB +461 w) | Chapter file (post-build) | Plot-level divergence |
| Ch 15 Prisoners of a New King | **Differs**: 6 paragraphs (De Lannoy among the prisoners, 24 officers); +37 w | 46 paragraphs differ; mv2 lacks the 24-paragraph Kanyakumari skirmish (EPUB +906 w) | Chapter file (post-build) | |
| Ch 16 Building a New Army | **Differs**: 6 paragraphs changed, 22 new (Company pay grievances, De Lannoy backstory); +744 w | 12 edits (Tiruvattar, Flanders to Arras/Low Countries, Madurai, Kappittan) | Chapter file (post-build) | **Internally inconsistent** (Section 9) |
| Ch 17 Adoption of the Stranger | Identical (3,278 w) | 1 line edit | File = EPUB | |
| Ch 18 Dutch Come Bowing | Identical (2,643 w) | 1 line edit | File = EPUB | |
| Ch 19 Shadows of the Deccan | Identical (2,875 w) | 1 line edit (chaver) | File = EPUB | |
| Ch 20 Guest in Velinadu | Identical (4,569 w) | 2 line edits (ledger) | File = EPUB | |
| Ch 21 Ramayyan's Ledger | Identical (2,135 w) | 3 line edits | File = EPUB | |
| Ch 22 Command of the Kayamkulam Frontier | Identical (3,795 w) | 20 edits, nearly all chevar to chaver | File = EPUB | |
| Ch 23 First Campaign for the Tiger | Identical (5,094 w) | 5 line edits | File = EPUB | |
| Ch 24 Under De Lannoy's Standard | **Differs**: 1 paragraph (he recalls surrendering, not crossing) | 19 edits (Kochi, Madurai, "crossed the lines") | Chapter file (post-build) | |
| Ch 25 Ramayyan's Test | **Differs**: 5 paragraphs (Pune to Raghuji Bhonsle's camp; Konkan to Carnatic); +17 w | 5 edits (ledger) | Chapter file (post-build) | |
| Ch 26 Fire in the Pepper Fields | Identical (2,597 w) | 2 line edits | File = EPUB | |
| Ch 27 The Last of the Old Houses | Identical (2,321 w) | 4 line edits (Kochi, ledger) | File = EPUB | |
| Ch 28 Servant of Padmanabha | **Differs**: 1 paragraph ("surrendered at Colachel") | 7 edits (Kochi, Nayak of Madurai, "crossed the lines") | Chapter file (post-build) | |
| Author's Historical Note | Identical (`Author_Historical_Note_nagoji.md`) | 6 edits (mv2 says De Lannoy was captured; chevar) | File = EPUB | Still says De Lannoy "crossed over" (Section 9) |
| Glossary | **Differs**: +1 entry (Chumkam); +38 w | 22 entries differ; mv2 has 73 entries against the EPUB's 86 (-280 w) | Chapter file (post-build) | |
| About the Author | Identical (`front_matter_about_author.md`) | Identical | same | |

How this fits the earlier quick check (manuscript_v2 against the chapter files): that check mixed two separate gaps. In Chs 11, 12, 14 and 15, **manuscript_v2 is out of date**. In Chs 7, 13 and 16, **the chapter files contain unbuilt additions**. In both cases the EPUB sits between the two.

## 5. Substantive divergences: chapter files vs EPUB (never published)

Line numbers refer to the chapter files. The EPUB text for each unit is in `manuscript_complete.md` at the line ranges in Section 8.

### 5.1 De Lannoy: desertion (EPUB) changed to surrender (files)

- **EPUB version (23 and 25 Dec builds):** a watch boy half-hears "Lannoy. Lannu." in Ch 11. In Ch 14, eight days before the end, the tall officer disappears from the Dutch ramparts and has "crossed the lines at Kanyakumari". Varma calls him a pragmatist, not a deserter, and afterwards he walks out from *our* lines, in Travancore cloth, to talk the garrison into terms. In Ch 15 he acts as go-between, Donnadi calls him a traitor, and 23 officers are taken. Chs 24 and 28, the Character Guide and the Historical Note all say he crossed over.
- **Chapter files:** Ch 11 (lines 11, 79, 455) removes the early naming and adds "I did not yet know his name... when he surrendered at Colachel". Ch 14 (lines 149 to 163) cuts the six-paragraph desertion block. De Lannoy now steps out of the *Dutch* lines, names himself and says he speaks for the garrison, and there is an exchange with Ramayyan. Ch 15 (lines 27 to 65): Donnadi is senior surviving officer, De Lannoy stands in the Dutch ranks, and 24 officers are taken "with Joseph Donnadi and Eustachius De Lannoy among them". Ch 24 (line 201), Ch 28 (line 211), the Character Guide (line 21) and the Foreword (line 91) all say he surrendered.
- **Not carried through:** `Author_Historical_Note_nagoji.md` line 15 still says he "crossed over during the Colachel campaign". Ch 16's new dialogue (lines 341 to 373) assumes he deserted (see 5.3).
- The historical record has De Lannoy captured at Colachel, so the files move toward history. The 16 Dec build (manuscript_v2) also had him fighting and being captured. The desertion version existed only in the 23 and 25 Dec builds.

### 5.2 New exposition passages

- **Foreword, "The Walls" (lines 51 to 65, 8 paragraphs):** Aramboli and Shenkottai earthworks, Van Imhoff's 1739 visit, the later Nedumkotta (Travancore Lines). Its key sentence ("A king who builds walls sends a message") is repeated almost word for word by Ramayyan in Ch 12.
- **Ch 7 (lines 149 to 157, 5 paragraphs):** the cost and hardiness of Madurai, Arab and Maravar horses, and why commanders mixed their cavalry.
- **Ch 12 (lines 31 to 39, 6 paragraphs):** Ramayyan on the Aramboli walls. This overlaps the Foreword section and the earthworks paragraph already in Ch 11.
- **Ch 13 (lines 111 to 167, 29 paragraphs replacing one line):** Van Imhoff's blockade plan and the *chumkam* customs tax; pepper moved inland through Kottar; recap of the November bombardment and the February landing under Stein van Gollenesse; the Tengapattanam raid and slave prices; Jesuit intelligence; the engineer Leslorant; commander Hackert leaving Rijtel in charge; the Nedumangad and Desinganadu coalition falling apart. The glossary's new Chumkam entry supports it. The November bombardment is also told in Ch 14's third paragraph (present in the EPUB and in the files).
- **Ch 16 (lines 167 to 175, 4 new paragraphs):** about a third of the Dutch prisoners enlist; Company pay grievances. **Lines 341 to 373 (13 new paragraphs):** Nagoji asks "Why did you cross?"; De Lannoy talks about Arras, being a Catholic in a Calvinist company, seventeen years of service, his age of forty-three, and Ceylon. The closing lines are rewritten. Line 15: the horse line becomes "my third horse here but the best of the three".

### 5.3 Historical and continuity corrections

- **Ch 25 (lines 38, 52, 64, 196):** the Deccan letter now comes from Raghuji Bhonsle's camp, not Pune, and Nagoji's old sardar is from the Carnatic campaigns, not the Konkan. This matches Ch 12's account of the Bhonsle capturing Chanda Sahib.
- **Ch 11 (line 5):** Kochi taken from the Portuguese "in 1663, nearly eighty years before"; the "(Cochin)" gloss is dropped there (the Prequel already gives it).

## 6. What changed between the 16 Dec build (manuscript_v2) and the EPUB

These are first-edition revisions. The EPUB and the chapter files both have them; manuscript_v2 has none of them.

- **Structure:** old Ch 11 "Dutch on the Horizon" (102 paragraphs) and old Ch 12 "Threads of Alliance" (126 paragraphs) were merged into a new Ch 11 of 232 paragraphs (about 6,000 words). Of the old paragraphs, 99 and 109 survive in it. New material: the Van Imhoff meeting at Tengapattanam (the eight-kalanju insult over the hiranyagarbha gold) and the Dutch envoys at court. A new Ch 12 "The Shadow from Arcot" (about 1,830 words) covers Chanda Sahib's tribute raids, Shenkottai, and the Maratha capture of Chanda Sahib at Tiruchirappalli in 1741.
- **Ch 14:** dated "In 1741"; the November bombardment paragraph; Varma's Tiruvattar vow; the church used as powder store; Ramayyan as a field general; the desertion block (added on 23 Dec).
- **Ch 15:** capitulation dated 12 and 13 August; Donnadi replaces "Lannoy" as the Dutch commander; a new 24-paragraph cavalry fight against a Dutch relief party out of Kanyakumari (still in the chapter files, lines 115 onward).
- **Ch 8:** 3 new paragraphs on inland skirmishes before the King's ola.
- **Global renames:** Raza Khan's horsemen come from the Nayak of Madurai, not the Nawab of Arcot (Chs 5 to 9, 13 to 16, 23, 24, 28, Character Guide, Glossary). Modern place names follow the AGENTS.md rule: Kochi, Kozhikode, Vasai, Sri Lanka, Anchuthengu, Desinganadu. Kappithan/Kapitan become Kappittan. Chevar becomes chaver (31 instances). "Ledger" is cut from 36 to 6, replaced by records, accounts, books, tally, register or palm leaves. Compound words are hyphenated.
- **Glossary:** grows from 73 to 86 entries (new: Kulasekhara Perumal, Nayak, the three Kappittan titles, Huzurat, Dvija, Sri Pandaravaka, Ola, Aramboli Lines, Kalanju, Nedumkotta, Hiranyagarbha); Chevar and Kapitan renamed; the Arcot and Madurai entries rewritten.
- **Historical Note:** De Lannoy changes from "captured at Colachel" (16 Dec) to "crossed over" (25 Dec).

## 7. Front matter and end matter

| Unit | EPUB (25 Dec) | Chapter and root files | manuscript_v2 |
|:-|:-|:-|:-|
| Title page | Title, RV Menon, tagline "1738: The Pepper Coast..." | Same | Title, "Blood and Thrones, Part 1", RV Menon; no tagline |
| Order | Title, Dedication, Copyright, Foreword, Prequel, Character Guide | Same (set by the build script) | Title, Copyright, Dedication, Prequel, Character Guide |
| Dedication | Parents, spouse, history lovers, Suraj | Same | Same |
| Copyright | 2025 RV Menon, fiction disclaimer | Same | Same |
| Foreword | 40 paragraphs, 1,208 w; De Lannoy "crossing the lines at Kanyakumari" | +"The Walls" section; De Lannoy surrenders | Absent |
| Prequel | 1,300 w | Same | Older place names |
| Character Guide | De Lannoy "crossed over"; Nayak of Madurai | De Lannoy "surrendered with the garrison" | Nawab of Arcot; De Lannoy's "defeat" |
| Historical Note | De Lannoy "crossed over" | Same as EPUB (not updated) | "captured at Colachel" |
| Glossary | 86 entries | 87 (+Chumkam) | 73 entries |
| About the Author | Same everywhere | Same | Same |

Pandoc also makes its own title page from metadata, so the title appears twice in the EPUB (`title_page.xhtml` and the `title_page.md` unit). This is cosmetic and worth fixing in the 2e build.

## 8. Recommended second-edition baseline

**Recommendation: start every unit from the chapter files in `book1_horse_servant/`** (plus the root front and end matter files the build script uses). Reasons:

1. They contain every first-edition revision. Every EPUB paragraph appears in them, except where the author deliberately rewrote it after the build.
2. They are the author's last committed decisions. The 25 Dec editorial review (`claude.review.2025-12-25.md`, item 1.1) treats the surrender version as intended. The 2026 comic work took these files as the source (build-log line 592; the comic source snapshots follow the file wording in Chs 15 and 16).
3. On De Lannoy they are closer to history. PLAN.md's goal is to keep plot and history. Here the published plot and the history disagree, so the author has to choose (Decision 1 below).

**Conditions:**
- Freeze the first-edition text as a reference, and do not edit it. For the 13 diverging units it exists only in `manuscript_complete.md` at these line ranges: Foreword 20 to 118, Character Guide 171 to 218, Ch 7 1199 to 1414, Ch 11 2116 to 2601, Ch 12 2602 to 2749, Ch 13 2750 to 3015, Ch 14 3016 to 3205, Ch 15 3206 to 3533, Ch 16 3534 to 3941, Ch 24 6347 to 7178, Ch 25 7179 to 7527, Ch 28 8044 to 8349, Glossary 8435 to 8534.
- Log the Section 5 deltas in `notes/changelog.md` as "content changes since the first edition", kept apart from anti-slop edits, so the Note to the Second Edition can describe them honestly.
- Fix the items in Section 9 before the slop pass. Otherwise the pass will polish contradictions.

**Decision 1 for the author:** keep the surrender arc (recommended; it fits history and six of the seven revised units), or keep the published desertion arc (then use the `manuscript_complete.md` text for Foreword, Character Guide and Chs 11, 14, 15, 24 and 28, and keep only the non-De-Lannoy additions).
**Decision 2 for the author:** keep the post-build exposition (Foreword walls, Ch 7 horses, Ch 12 walls, Ch 13 history block, Ch 16 pay and backstory), or drop it back to the published text. It is about 2,500 words, mostly explanation, and would be heavily cut by the style sheet anyway.

| Unit | 2e baseline | Confidence | Reasoning |
|:-|:-|:-|:-|
| Title, Dedication, Copyright, About the Author | Root files (`title_page.md`, `dedication.md`, `front_matter_publication_notes.md`, `front_matter_about_author.md`) | High | Identical to the EPUB |
| Foreword | `front_matter_foreword.md` | Medium | Post-build: walls section and surrender. Depends on Decisions 1 and 2. Walls wording repeats in Ch 12. |
| Prequel | `front_matter_prequel.md` | High | Identical to the EPUB |
| Character Guide | `front_matter_character_guide.md` | Medium | Only the De Lannoy entry differs (Decision 1) |
| Chs 1 to 6 | Chapter files | High | Identical to the EPUB |
| Ch 7 | Chapter file | Medium | +5 exposition paragraphs, never published (Decision 2) |
| Chs 8 to 10 | Chapter files | High | Identical to the EPUB |
| Ch 11 | Chapter file | High | Small edits that keep De Lannoy unnamed until Colachel; needed if the surrender arc stays |
| Ch 12 | Chapter file | Medium | +6 walls paragraphs (Decision 2); duplicate motif |
| Ch 13 | Chapter file | Medium | +29-paragraph history block (Decision 2); overlaps Ch 14; one spaced hyphen used as a dash |
| Ch 14 | Chapter file | Medium | Core of the surrender arc (Decision 1); fix the dangling line 163 |
| Ch 15 | Chapter file | Medium | Surrender arc (Decision 1); check Donnadi vs Rijtel as commander |
| Ch 16 | Chapter file, **after reconciliation** | Low until fixed | Lines 341 to 361 contradict the surrender arc; age and service figures need checking |
| Chs 17 to 23 | Chapter files | High | Identical to the EPUB |
| Ch 24 | Chapter file | High | One sentence, consistent with the surrender arc |
| Ch 25 | Chapter file | High | Historical correction (Bhonsle, not Pune) that matches Ch 12 |
| Chs 26, 27 | Chapter files | High | Identical to the EPUB |
| Ch 28 | Chapter file | High | One sentence, consistent with the surrender arc |
| Historical Note | `Author_Historical_Note_nagoji.md`, **with line 15 updated** | Medium | Identical to the EPUB, but contradicts the surrender arc |
| Glossary | `book1_horse_servant/glossary.md` | High | +Chumkam entry only |

Never use `manuscript_v2.md` as a baseline or as a sync target. The CLAUDE.md "Files To Keep In Sync" list still names it, but it is 10 days older than the published build.

## 9. Fix list before the prose pass

1. **Ch 16, lines 341 to 361:** "Why did you cross?... Before the battle ended... You walked away from your own men" and "That alone would not make a man desert" assume the desertion arc. Line 369 ("you had already won") assumes surrender. Rewrite as "why did you stay / why did you take service", or cut back to the EPUB exchange. Also: "I am forty-three years old" and "seventeen years" of Company service. De Lannoy's birth year is usually given as 1715, which would make him about 26 in 1741; check this. The line "Arras... A city in Flanders" is loose (Arras is in Artois). The 2026 comic Ch 16 proof carries the same "WHY DID YOU CROSS?" line.
2. **Historical Note, line 15:** "crossed over during the Colachel campaign" contradicts the surrender arc.
3. **Ch 14, line 163:** "It was the first time I heard those words from his own mouth" refers back to the ola quote the revision deleted. There is no earlier instance any more.
4. **Ch 14 and Ch 15:** Ch 14 line 151 has "Rijtel and the other surviving officers" behind De Lannoy, and Ch 13's new block says Rijtel was left in command. Ch 15 line 27 calls Donnadi "the senior surviving officer". Make them agree.
5. **Dashes:** two spaced hyphens used as dashes, both in unbuilt text (Ch 13 line 121, Ch 16 line 369). There are no em dashes and no double-hyphen dashes anywhere; lines of three hyphens occur only as scene-break markers.
6. **Duplicated material:** the walls motif (Foreword line 59, Ch 11 earthworks paragraph, Ch 12 lines 31 to 39); the November bombardment (Ch 13 new block and Ch 14 third paragraph).
7. **Existing first-edition issues noticed in passing** (in both the EPUB and the files): Ch 12 has Nagoji say he "fled the Peshwa's justice" and speaks of "my exile" and having "left Pune before the campaign", which does not fit his capture at Goa in the Prequel and Ch 1. Ch 23 line 505 still has "political fallout", which the 25 Dec review flagged as anachronistic.
8. **Quote style:** 14 chapter files mix straight and curly quotes (pandoc smart quotes hide this in the EPUB). Normalise once in the 2e copies.

## 10. How to confirm what readers bought

Open the retail or KDP copy and check:

| Check | 16 Dec build (manuscript_v2) | 23 Dec build | 25 Dec build (current EPUB) | Chapter files (unbuilt) |
|:-|:-|:-|:-|:-|
| Is there a Foreword? | No | Yes | Yes | Yes, with "The Walls" |
| Chapter 12 title | Threads of Alliance | Threads of Alliance | The Shadow from Arcot | The Shadow from Arcot |
| Ch 7 first sentence: whose horses? | Arcot | Arcot | Madurai | Madurai |
| Ch 14: how does De Lannoy reach Travancore? | Commands the garrison, captured | Crossed the lines at Kanyakumari | Crossed the lines at Kanyakumari | Parleys for the garrison and surrenders |
| Ch 13 mentions "chumkam"? | No | No | No | Yes |

If the retail copy is the 16 or 23 Dec build, this report's "first edition" label moves to that build. The recommended baseline (chapter files) does not change, but the changelog would need the extra deltas listed in Section 6.

## 11. Accepted final reading proofs (commit `fe263cf`)

- 14 PDFs tracked with Git LFS. All are present locally (`git lfs ls-files` marks them as downloaded; each starts with a valid `%PDF` header; sizes run from 77 MB to 841 MB). Nothing was fetched.
- What they contain: `output/comic-v14-chapter-quality-v1/chapter-06` to `chapter-17` frame proofs (graphic novel, V14), `output/pdf/Horse-of-the-Servant-V13-Reference-Redesign-r1.pdf` (full comic reference), and `output/pdf/The-Dutchmans-Son-Complete-Reading-Proof-v2.pdf` (Book 2). They are image pages with short capital-letter lettering. They are not prose proofs and cannot serve as a text baseline.
- Which prose they follow: the `SOURCE-SNAPSHOT-v1.json` text for Ch 15 ("HIS EYES WERE ON UDAYAGIRI") and Ch 16 ("WHY DID YOU CROSS?") matches the post-build chapter files, not the EPUB. Their chapter titles (Ch 12 "The Shadow from Arcot", Ch 14 "The Siege of Colachel", Ch 22 "Command of the Kayamkulam Frontier") match both. `output/book-edition-v5/README.md` states that the graphic novel has not been published and has no ISBN.

## Appendix: reproducing this audit

- EPUB builds: `git show <commit>:Horse_of_the_Servant.epub`, unzipped outside the repo. Chapter units come from the OPF spine; paragraphs from `<p>`, `<li>` and heading elements.
- Markdown units: split on `# ` headings, then paragraphs on blank lines (list items one per line). Normalisation: curly quotes to straight, ellipsis to three dots, dashes to hyphen, `*`, `_` and `\` removed, attribute braces removed, whitespace collapsed.
- For each unit: exact paragraph set membership in both directions, word counts, and `difflib` word-sequence similarity. Divergent units were diffed paragraph by paragraph and read by hand.
- Hashes at HEAD (sha256, first 16 hex digits): EPUB `b462fc7af37419eb`, `manuscript_complete.md` `1644129e145724ca`, `manuscript_v2.md` `9296c0105d137d30`, omnibus EPUB `e17b10de776f0118`.
