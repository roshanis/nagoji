# Horse of the Servant: Second Edition Plan (v2)

Status: DRAFT v2, awaiting author decisions (section 3)
Updated: 2026-09-26
Replaces: PLAN v1 (same file, see git history). v1 was written from a grep sample. v2 is written from a full audit: 30 units read by two independent auditors plus an adjudicating editor, six book-wide studies, blind pilot rewrites judged by three lenses, a synthesis, and a completeness critic.

Controlling documents, in order of authority:
1. This plan
2. `STYLE_SHEET_v2.md` (calibrated rules, before/after examples from this book, Do-not-cut list). Replaces `STYLE_SHEET.md` once you approve it after calibration.
3. `audit/SUMMARY.md` (triage, rulings, decision table D1 to D21, acceptance checks)

---

## 1. What the audit found

The machine signal in this book is **rhythm and commentary, not vocabulary**. The obvious AI words are almost absent. What gives it away:

| Signal | First edition | Target |
|---|---|---|
| One-sentence paragraphs | 44% of all paragraphs, 56% of narration | under 35% of narration |
| Short "kicker" sentences closing a paragraph | 186 | a handful per chapter |
| "Not X, but Y" and "Not ..." corrections | 227 in 25 of 28 chapters | 1 per chapter, in dialogue |
| "as if" / "like a" / slowly, quietly, softly | 79 / 89 / 119 | 2 to 4x over the ration |
| Chapters ending on a summary or moral | 22 of 28 | 0 |
| Figurative "storm" | 22 uses | one plant (ch5) and one payoff (ch13) |
| Confirmed issues (after adjudication) | 2,024, with 647 flagged lines *defended* as real voice | |
| Out-of-period register | 290 findings, 52 serious (e.g. Ramayyan's ledger reads like a modern risk register; "diwan" for Dalawa; "Sri Lanka"; minutes, yards, percent) | |
| Continuity and history backlog | 167 items: 112 still present (horses, Dhanaji, De Lannoy's birthplace and age, Revathi, Colachel timeline, duplicate scenes) | |

Severity by chapter: Chs 1 to 7 are 3 of 5, Ch 27 is 5, everything else is 4. The biggest single job is Ch 24 (158 issues). By density the worst units are the Prequel, Ch 12 and the Foreword.

What Nagoji sounds like at his best (`audit/VOICE_BIBLE.md`): he **counts** when afraid, he puts tenderness into **horses and chores** instead of naming feelings, and his humour **makes things smaller**. The machine passages name the feeling, then explain it, then close on a maxim.

### Pilot: how hard to edit

Two passages (Ch 1 opening, Ch 27 core scene) were rewritten at three strengths and scored blind by three judges (scores out of 10; residue 10 = no machine tells left):

| Strength | AI residue | Fidelity | Readability | Judge picks |
|---|---|---|---|---|
| Light (tics only) | 5.2 | 7.8 | 6.7 | 1 of 6 |
| Medium (tics + tightening) | 7.3 | 7.7 | 7.7 | 2 of 6 |
| Deep (line-level re-voicing) | 8.0 | 7.2 | 8.2 | 3 of 6 |

The light pass fails: it cut sentences without rejoining them, so one-line paragraphs actually went up in Ch 27 (60% to 65%). The deep pass reads best but **introduced its own new slop** ("Who was in the right never entered the sum") and dropped details the book needs.

**Standard for the whole book:** deep in narration, medium in dialogue, never in facts. Chapters differ only in how many blocks get rebuilt (11 medium-scope units, 19 deep-scope). Expected cut: **15 to 25%** overall (the line edit alone cuts 9 to 12%; the rest is compressing named repeated blocks). A chapter that cuts more than 5 points past its estimate, or whose dialogue share falls, counts as over-cut.

---

## 2. Three things that must be settled before anything else

**A. Is there a first edition in the market, and which text is it?**
The repo holds no ASIN, ISBN or publish date. The 25 Dec 2025 EPUB (`Horse_of_the_Servant.epub`, matching `manuscript_complete.md`) is the probable published text. Thirteen chapter files were edited after that build (about +2,500 words and a changed De Lannoy arc), so **`book1_horse_servant/` is not the published text**. `manuscript_v2.md` is stale and must not be used (and should come off the CLAUDE.md sync list).
Action: you record the KDP facts (ASIN, formats, date, sales, reviews, and the status of the December publisher submissions) in `notes/edition_record.md`.

**B. De Lannoy: desertion or surrender?**
The audit synthesis recommended surrender. The critic caught that this contradicts your own research: `kulaperumal.codex.md`, from Mark de Lannoy's 1997 study, says he was born in Arras in 1715, **deserted at Kanyakumari on 2 August 1741**, and "must be a deserter, not a captive". The published first edition and Book 2 follow that. The later chapter files moved to surrender (the popular "captured at Colachel" account) and are internally inconsistent (Ch 16 still assumes desertion).
Recommendation: **keep desertion** unless you changed your mind on purpose. Then fix ch24:239 "Zeeland, where I was born" (Arras is right), his age in Ch 16 (about 26, not 43), and bring Chs 11, 14 to 16, 24, 28, the character guide and the Historical Note into line. Treat every other history ruling in the audit as unverified until the fact-check (section 7).

**C. The repo is public.**
`gh repo view` reports `roshanis/nagoji` as PUBLIC. It contains the full manuscript, the published EPUBs, and `The_Kulasekhara_Perumals_Refactored.epub`, a reworked copy of the copyrighted 1997 study. Details in the Ch 13 history block, the Foreword and the Historical Note appear drawn from it, and the Historical Note does not credit it.
Recommendation: decide whether the repo should be private. If it stays public, remove the study EPUB from tracking (it stays in history unless rewritten, which is a separate, destructive decision). In either case, credit the study in the Historical Note and run an overlap check for close paraphrase.

---

## 3. Author decisions (Gate 0)

Full table with affected chapters: `audit/SUMMARY.md` section 6. My recommendations, with D2 corrected:

| # | Decision | Recommendation |
|---|---|---|
| D1 | Baseline | Edit from the chapter files; freeze the published EPUB text as the 1e reference; log the 13 post-build differences as content changes |
| D2 | De Lannoy | **Desertion** (your source, the published text, Book 2). See 2B |
| D3 | 2,500 words of unpublished exposition | Keep the facts, compress (Foreword walls to one paragraph, Ch 7 essay to ~200 words, Ch 13 block to ~450) |
| D4 | The horses | One history: Kanka a black stallion shot at capture; Kayal the bay mare at Colachel; decide who dies at the start of Ch 16 |
| D5 / D6 | Dhanaji's arrival; "fled the Peshwa" backstory | Add a short arrival beat; replace the fugitive backstory with the capture history |
| D7 / D8 / D9 | Duplicate scenes | One chaver attack on the heir; one uniform scene (Ch 24); three distinct renunciations of the north |
| D10 | Colachel timeline | One date, one garrison size, one Dutch commander, consistent with the desertion arc |
| D11 | Revathi | His wife on every page of Ch 28; the Ch 25 letter stays burned |
| D12 / D13 | Storm; the Tiger | Storm: ch5 plant, ch13 payoff only. Tiger: planted once in the Ch 11 hall, landed in Part IV |
| D16 | History liberties | Thrippadidanam to January 1750; fix or disclose Mathu Tharakan (born 1741), the heir's age, Kottarakkara |
| D18 / D19 | Italics; titles | Italicise non-English common nouns every time; "diwan" becomes Dalawa (18 changes); no Majesty or Highness |
| D20 / D21 | Family details; front matter | Settle the brother's name against Book 3; move the Foreword to the back as an Author's Note so the sample opens on Ch 1 |

Part I can start once D1, D2, D4, D12, D18 and D19 are settled. The rest are needed before the batch that touches them.

---

## 4. How each chapter is edited

Three separate passes per chapter, each its own commit, so a prose diff never hides a plot change:

1. **Mechanical**: curly quotes, spaced hyphens, house spellings and italics (`STYLE_SHEET_v2.md` section 10), typos.
2. **Content** (only Gate 0 items): continuity, history, duplicate scenes. Each change logged with its decision ID.
3. **Prose**: the anti-slop line edit against `STYLE_SHEET_v2.md`.

For the prose pass, each chapter goes through this pipeline:

1. **Draft edit** at the standard strength, reading the chapter audit report, the Voice Bible touchstones and the Do-not-cut list first.
2. **Independent checks** run by separate reviewers, not the editor:
   - residue reader: what still sounds machine-written?
   - fidelity check: sentence-aligned diff against 1e; every lost fact, beat or change in dialogue meaning is listed
   - **editor-fingerprint check**: did the edit introduce a *new* house style (comma-and chains, balanced two-clause sentences, "the way a", participial tails, sameness of sentence length)? This guards against replacing one machine voice with another.
3. **Merge**: fix what the checks found, borrowing the best lines from the original where the edit lost them.
4. **Scanner**: `audit/tools/scan_slop.py book1_horse_servant_2e/manuscript -b <baseline>`. No marker may rise.
5. **Author pass**: you read the chapter aloud, mark every sentence you would not say, and write or personally reword every chapter ending. Nothing is accepted without your sign-off.

Every changed passage is tagged in `notes/changelog.md` with its provenance (AI-drafted, author-revised, author-written). This log supports both the KDP AI-content question and your own ownership of the voice.

**Voice reference before calibration:** you write a 500 to 1,000 word version of the Ch 1 opening yourself, without AI. That becomes the human benchmark the edits are measured against, alongside the Voice Bible.

---

## 5. Phases and timeline

Work happens on a `book1-2e` branch; `main` gets the result once you approve.

| Weeks | Phase | Output |
|---|---|---|
| 1 | **Gate 0**: sections 2 and 3 settled; tag the 1e build commit; copy the 1e EPUB text to `baseline/` with sha256 hashes; copy chapter files to `manuscript/`; write `notes/edition_record.md`, `notes/sources.md`, `notes/series_continuity.md`; add a 2e override to AGENTS.md (its "short punchy sentences, name the feeling" brief pushes toward the very tics being removed) | frozen baseline, decisions log |
| 2 to 4 | **Calibration**: Chs 1, 2, 3 and 27 (covers the mildest and the worst chapter) through the full pipeline; your read-aloud; small blind test (below); then freeze `STYLE_SHEET_v2.md` | calibrated, frozen style sheet |
| 5 to 12 | **Batches**, in file order so plants come before payoffs: Prequel + Chs 4 to 6; 7 to 10; 11 to 13 (Colachel unit, with D10); 14 to 17; 18 to 21; 22 to 24; 25, 26, 28 | about 1.5 weeks and 6 to 8 author hours per batch |
| 8 onward | **Sensitivity reads** begin after Part II so findings shape Parts III and IV | reader reports |
| 12 to 14 | **Whole-book**: your full read-aloud; fact-check sign-off; motif and ending register check across all chapters; Foreword/Author's Note last | locked text |
| 14 to 17 | **Beta readers** (4 weeks) | reader feedback, final fixes |
| 17 to 20 | **Production**: human copyedit, support docs, build, device proofs, KDP | published 2e |

---

## 6. Acceptance checks

**Per batch** (details in `audit/SUMMARY.md` section 7):
- Scanner: style-sheet excess of 2 or less per chapter; core hits per 1,000 words down at least 40%; no marker up; one-sentence narration paragraphs under 35%
- Editor-fingerprint: no fingerprint marker up more than 50% against 1e
- Endings match the ending register in `STYLE_SHEET_v2.md` section 7; no final paragraph opens on But, For now, For the moment, And, Perhaps
- Every Do-not-cut item survives or its change is logged
- No new facts; dialogue share holds; cut within 5 points of estimate
- No em dashes, one quote style, house spellings
- Your read-aloud sign-off

**Book-level:**
- **Blind reader test**: 5 to 8 readers see matched 1e and 2e passages plus a published human-written control. Target: readers pick the 2e passage as machine-written no more than 25% of the time. Run once at calibration and once at the end.
- Zero unlogged fact or plot changes
- Existing 1e reviews and publisher feedback collected now as the baseline to compare against

---

## 7. People the plan needs

- **You**: voice reference, Gate 0, every ending, read-aloud of every chapter, the Note to the Second Edition (under 250 words, back matter)
- **Fact-check**: `notes/sources.md` with named sources (de Lannoy 1997, Shungoonny Menon, Nagam Aiya's Travancore State Manual, sources for the 1737 to 1739 Vasai and Goa campaigns and the Goa Inquisition), then a fact table: claim, chapter:line, source and page, verdict
- **Two paid authenticity readers**: one Malayali reader with Nair and Travancore social history; one Marathi reader with Maratha caste history; spot reads for the Goan Catholic, Syrian Christian and Jewish scenes
- **8 to 12 beta readers**, including a few 1e readers, Malayali and Marathi readers, and one military-history reader, with a per-chapter form (where did you skim, what sounded generic, what stayed with you)
- **Human copyeditor** for British spelling, Indian-English usage, italics and diacritics

---

## 8. Publication mechanics

- Check the current KDP help pages before deciding. Likely route: ebook as an update to the same ASIN (keeps reviews); paperback as a new edition with its own ISBN
- Copyright page: "Second edition 2026. First published 2025."
- AI-content disclosure answered accurately from the provenance log; get professional advice before any copyright registration or contract that asks about AI
- The "Look Inside" span, blurb, tagline, bio and keywords go through the same style sheet and your read-aloud; readers judge the book by its first pages
- Build: `build_book1_2e_epub.sh` pointing at `book1_horse_servant_2e/manuscript/`, a pinned pandoc version (not currently installed) and EPUBCheck; proof in Kindle Previewer on phone, e-reader and tablet profiles and in the KDP print previewer
- Decide whether the omnibus is reissued with the 2e

## 9. Downstream sync

`notes/downstream.md` lists each artifact that depends on Book 1 text and its 2e action (update, freeze as 1e, or retire): Books 2 and 3 (series facts in `notes/series_continuity.md`), the omnibus, `glossary.md`, `front_matter_character_guide.md` (add Father Duarte and a dozen missing recurring characters; fix Karl August and the Nayak), `synopsys.md`, `novel_outline_bhimrao.md`, `Author_Historical_Note_nagoji.md`, `KDP_Metadata_Package.md`, and the comic adaptation (whose 2026 proofs already quote the post-build chapter files).

---

## 10. Folder map

```
book1_horse_servant_2e/
  PLAN.md               this plan
  STYLE_SHEET.md        v1 (superseded once v2 is frozen)
  STYLE_SHEET_v2.md     calibrated rules, examples, Do-not-cut list, ending register, house spellings
  audit/
    SUMMARY.md          triage, rulings, decisions D1 to D21, acceptance checks
    SOURCE_OF_TRUTH.md  which text is the first edition, chapter by chapter
    VOICE_BIBLE.md      Nagoji's voice: touchstones, contrasts, rules
    REPETITION_AND_DENSITY.md, OPENINGS_ENDINGS_MOTIFS.md,
    REGISTER_AND_ANACHRONISM.md, REVIEW_BACKLOG.md
    chapters/           one adjudicated report per chapter, with line-level fixes
    tools/scan_slop.py  rerunnable scanner (44 tests pass)
  pilot/                blind pilot passages A (Ch 1) and B (Ch 27), three versions each
  baseline/             (Gate 0) frozen 1e text with hashes
  manuscript/           (Gate 0) working 2e chapters
  notes/                changelog, edition record, sources, series continuity, downstream
```

## 11. Risks

| Risk | Guard |
|---|---|
| Over-cutting flattens the voice | Do-not-cut list; fidelity check; cut-percentage ceiling; your read-aloud |
| The AI editor swaps one machine voice for another | Editor-fingerprint check; blind reader test; you own the endings and touchstones |
| An audit "fix" reverses a deliberate, sourced choice (as nearly happened with D2) | No history change without a source in the fact table |
| Scope grows from polish into rewrite | Content changes split into required, optional, declined; only required by default; all listed in the Note to the Second Edition |
| Editing the wrong baseline | Frozen, hashed 1e text; every scanner report names its baseline |
| Public repo exposes the manuscript and a copyrighted source | Decision C above |
