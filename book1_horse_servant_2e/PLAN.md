# Horse of the Servant: Second Edition Plan

Status: DRAFT, awaiting author GO
Created: 2026-09-26
Source (first edition, frozen): `../book1_horse_servant/` (28 chapters + front matter, about 99,000 words)

## Goal

A second edition whose prose reads as one human voice: Nagoji's. Strip the patterns readers now recognize as machine-written, without changing plot, history, or chapter structure.

Secondary goals (only if you want them, decide below):
- Fix continuity and history issues logged in past reviews (`codex.review.*`, `claude.review.*`, `review/`)
- Refresh front matter: a short "Note to the Second Edition"
- Rebuild the EPUB/print files from the new folder

## What "AI slop" means in this book (baseline scan, first edition)

The obvious clichés are already rare (no "tapestry", "delve", "testament to", no em dashes). The problem is subtler: structural tics that repeat across chapters.

| Pattern | Example from the text | Count |
|---|---|---|
| "Not X, but Y" / "Not X. Y." correction fragments | "Not in threat, but in promise." | ~57 |
| "as if" similes | | ~80 |
| "like a ..." similes | "like the hand of an angry god" | ~67 |
| Soft adverbs (slowly / quietly / softly) | | ~95 |
| Three-word fragment lists | "Horses. Guns. Storms." / "Wariness. Interest. The calculation..." | frequent |
| One-line kicker paragraphs after a scene | "This was where the Portuguese forged information." | frequent |
| Chapter endings that sum up a lesson or a mood | "That was enough for now." / "For the moment, that was enough." / "Together." | most of the 28 chapters |
| Repeated motif lines | "Storms do not ask permission" (ch1, ch7), "the next storm" (ch21) | several |
| Vague depth words | "something older / deeper / else" (9), "the weight of" (19), "etched" (13), "for the first time" (9) | |
| Explaining the subtext right after showing it | "They wanted to see grief; they wanted to use it as a lever." | frequent |

The full rules are in `STYLE_SHEET.md`.

## Folder layout

```
book1_horse_servant_2e/
  PLAN.md            this file
  STYLE_SHEET.md     the anti-slop rules every edit follows
  manuscript/        working copies of chapters (2e text lives here)
  audit/             per-chapter scan reports, before/after counts
  notes/             change log, decisions, open questions
```

The first edition folder is never edited. All work happens on copies.

## Phases

**Phase 0: Set up (no prose changes)**
1. Copy the 28 chapters, front matter and glossary into `manuscript/`.
2. Write `audit/scan_slop.py`: counts each pattern in STYLE_SHEET.md per chapter and flags lines. Output goes to `audit/baseline.md`.
3. Commit the baseline so every later change can be diffed.

**Phase 1: Pilot (Chapters 1 to 3)**
4. Line-edit Chapter 1 by hand against the style sheet. You review it.
5. Adjust the style sheet based on what you accept or reject (this calibrates how hard to cut).
6. Edit Chapters 2 and 3 with the calibrated rules. You review.

**Phase 2: Full pass (Chapters 4 to 28)**
7. Edit in batches of four or five chapters, one batch per "Book" part (Parts 1 to 4).
8. After each batch: re-run the scan, record before/after counts in `audit/`, log changes in `notes/changelog.md`.
9. You review each batch before the next begins.

**Phase 3: Continuity and whole-book read**
10. Read straight through for voice consistency, repeated images across chapters, and chapter endings.
11. Check names, dates, and terms against `glossary.md` and `front_matter_character_guide.md`.

**Phase 4: Production**
12. Update support docs to match (`synopsys.md`, `novel_outline_bhimrao.md`, `glossary.md`, `Author_Historical_Note_nagoji.md`), or make 2e copies of them.
13. Add a "Note to the Second Edition".
14. Build the 2e EPUB and print PDF; do a proof read of the built files.

## Ground rules for the edit

- Plot, history, dialogue meaning and chapter order stay the same.
- Cut before rewriting. Most fixes are deletions.
- Keep Nagoji's first-person 1738 to 1750s voice. No modern idiom.
- No em dashes.
- Word count may drop 5 to 10 percent. That is expected.
- Each chapter stays self-contained; no splitting or merging.

## Checks (in place of tests, since this is prose)

- [ ] Slop scan counts drop in every chapter, and no chapter gains new hits
- [ ] No em dashes (scan enforces it)
- [ ] Named characters, places and dates unchanged unless listed in the changelog
- [ ] Word-count diff per chapter recorded
- [ ] Author sign-off on every batch

## Decisions needed from you

1. **How deep?** (a) Language only: cut the tics, keep every scene as is. (b) Language plus tightening: also trim over-explained or repeated passages. I recommend (b).
2. **Fold in the old review fixes** (continuity and history notes from past reviews)? I recommend yes, logged separately from the prose changes.
3. **Who does the edit?** Chapter by chapter with you approving each, or batches of 4 to 5 chapters. I recommend a pilot of Chapters 1 to 3 first, then batches.
4. **Edition name/file:** "Horse of the Servant, Second Edition" OK?

## Risk

- Nothing destructive: the first edition folder and the existing EPUB stay untouched.
- The main risk is over-cutting and flattening the voice. The pilot phase is there to catch that early.
