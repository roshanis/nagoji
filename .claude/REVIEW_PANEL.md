# Six-Reviewer Panel

Every proposed change to the manuscript or its support documents goes through six reviewer agents before it is shown to the author as ready, and before it is applied. The author asked for this on 17 October 2026. The panel advises; the author still approves every change (2e plan, section 2).

The six reviewers live in `.claude/agents/`:

| Agent | Lens | Asks |
|---|---|---|
| `reviewer-user-experience` | The reader's experience | Will a first-time reader follow it, stay immersed, and not lose anything they need later? |
| `reviewer-graphic-design` | The book as a designed object | Does it hold up on the page and in the EPUB: headings, breaks, typography, front and back matter, map, glossary? |
| `reviewer-story-editing` | Structure, arc, character, motif | Does it serve the chapter, the arc and the motif plan, with POV and timeline intact? |
| `reviewer-general-editing` | Line and copy editing | Does it follow the style sheet, house spellings, glossary and phrase bans, and is the original quoted exactly? |
| `reviewer-history-research` | Historical accuracy and period register | Does it agree with the Historical Note and the period, with nothing invented? |
| `reviewer-adversarial` | Red team | What breaks if we accept this? Is any other reviewer wrong? |

## What counts as a change

Anything that would alter text a reader sees or that the support documents record: a suggestion in a `review/chNN_suggestions.md` file, an edit applied to a chapter file, a mechanical pass (for example italicising Portuguese words), a change to front or back matter, the glossary, the character guide, the synopsis, the outline, the Historical Note, `epub.css` or a build script.

A mechanical pass is reviewed once as a rule plus a representative sample (at least ten instances, spread across chapters), not instance by instance. Any instance the sample shows to be an exception is reviewed on its own.

## How to run the panel

1. Write the change as a numbered list of items. Each item quotes the original verbatim, cites chapter number and title (and file and line where known), and gives the suggested text and a one-line reason. Line-level only; no whole-passage rewrites unless the author asked for one.
2. Launch the first five reviewers in parallel, giving each the same item list and the paths of the files touched.
3. Launch `reviewer-adversarial` last, giving it the item list and the five verdicts.
4. Apply the pass rule below. Revise and re-run only the reviewers whose concerns the revision addresses, plus the adversarial reviewer.
5. Record the verdicts (see "Recording") and only then present the change to the author.

## Verdicts

Each reviewer returns one verdict per item:

- **PASS**: no concerns in this lens.
- **PASS WITH NOTE**: acceptable; the note is for the author's information.
- **REVISE**: acceptable only with the specific fix the reviewer gives, written line-level with the original quoted.
- **BLOCK**: must not go ahead, with the rule, document or passage that it breaks.
- **N/A**: the item does not touch this lens (for example, a pure prose cut with no typography effect for graphic design). Say why in a few words.

## Pass rule

An item survives only if:

- no reviewer returns BLOCK, and
- every REVISE has been applied and the reviewer who asked for it has re-run and returned PASS or PASS WITH NOTE, and
- the adversarial reviewer has seen the final wording.

A BLOCK that rests on a settled author decision (2e plan, section 2) stands. A BLOCK that would reopen a settled decision is itself invalid; the adversarial reviewer should say so. When two reviewers disagree and neither BLOCKs, the item goes to the author with both views quoted, rather than being decided by the panel.

## Recording

Under each item in the suggestions file, add a panel line:

> Panel: UX PASS · Design N/A · Story PASS WITH NOTE (motif 7.1 storm plant kept) · Editing PASS · History PASS · Adversarial PASS

Then list any notes, revisions made, and dropped items with the reason. Suggestions files live in `review/` in the project's shared folder (`/mnt/project-files/review/`) when it exists, otherwise in `book1_horse_servant_2e/review/`. A change applied without a panel line has not been reviewed.

## Sources every reviewer uses

When `/mnt/project-files/uploads/hearth/` exists, the author's uploaded copies are the current versions. Otherwise use the repo paths. `/mnt/project-files/.notes/inputs.md` maps upload IDs to names.

| Document | Uploaded copy | Repo path |
|---|---|---|
| 2e manuscript, all 28 chapters | `01_manuscript_2e_chapters.md` | `book1_horse_servant/book*_chapter*.md` |
| Glossary | `02_glossary.md` | `book1_horse_servant/glossary.md` |
| Character guide | `03_character_guide.md` | `book1_horse_servant/front_matter_character_guide.md` |
| Historical Note | `04_historical_note.md` | `Author_Historical_Note_nagoji.md` |
| Style sheet | `05_style_sheet.md` | `book1_horse_servant_2e/STYLE_SHEET_v2.md` |
| Series continuity | `06_series_continuity.md` | (upload only) |
| 2e plan and settled decisions | `07_2e_plan.md` | `book1_horse_servant_2e/PLAN.md` (older) |
| Synopsis | `08_synopsis.md` | `synopsys.md` |
| Outline | `09_outline.md` | `novel_outline_bhimrao.md` |

Also: `book1_horse_servant_2e/audit/` (VOICE_BIBLE, REVIEW_BACKLOG, REGISTER_AND_ANACHRONISM, OPENINGS_ENDINGS_MOTIFS, SOURCE_OF_TRUTH), `kulaperumal.codex.md` (De Lannoy source notes), `review/book_wide_phrase_bans.md`, and the build script `build_book1_epub.sh` with `epub.css`.

Known stale spots, so no reviewer reports them as contradictions with a change: the synopsis and character guide still say "diwan"; the outline still says De Lannoy was "captured at Colachel" (settled: desertion, plan 2B); `manuscript_v2.md` is stale and must not be used as a source.

## House rules every reviewer enforces

- No em dashes, double hyphens or spaced hyphens used as dashes, in suggested text or in reviewers' own notes.
- The author prefers their own prose. Suggestions are line-level, mostly cuts in the author's own words, with the original quoted alongside.
- The 2e prose pass is endings and one-line kickers only (plan, section 2). Anything wider needs the author's explicit request.
- Chapters stay self-contained. Never propose splitting or merging chapters.
- POV and timeline stay clear. No anachronistic language or concepts (style sheet section 8).
- Never use the word "bubbles" in any form. Never describe an expression, smile or light going or moving across a face.
- Settled decisions in the 2e plan are not reopened.
- Uncertain historical claims are flagged, never filled in.
- Quotations from the manuscript cite chapter number and title.

## Output format for every reviewer

```
## <Reviewer name>

### Item <n>: <short label>
Verdict: PASS | PASS WITH NOTE | REVISE | BLOCK | N/A
Why: <one to three sentences, citing the rule, document section or passage>
Fix (REVISE only):
> Original: "<verbatim>"
> Suggested: "<text>"

### Overall
<one or two sentences: anything that cuts across items>
```

Reviewers are read-only. They never edit the manuscript or support files.
