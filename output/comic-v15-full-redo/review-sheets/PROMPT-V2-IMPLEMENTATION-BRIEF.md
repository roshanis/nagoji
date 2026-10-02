# Prompt assembly v2: implementation brief (2026-10-02)

Work in this git worktree only: `/private/tmp/claude-501/nagoji-v15-claude-worktree/output/comic-v15-full-redo`
(branch `claude/v15-comic-ch1-8`). It holds the V15 pipeline, scripts, CONTINUITY.md and every chapter's JSON and
prompt files, but no images (frames, renders and PDFs are excluded), so tests that need real frames skip.

## Spec

`review-sheets/PROMPT-ASSEMBLY-DESIGN-2026-10-02.md` holds the design (section "Design"), its adversarial review
("Adversarial review", 17 required changes), the rejection evidence and the code map. Implement the design WITH the
17 required changes from the review. Where they conflict, the review wins. Then apply the author's decisions below.

## Author decisions (binding)

1. Nagoji's ear ornament is the small flush gold STUD (as CONTINUITY.md says). The Nagoji sheet caveat says so ("not
   the hanging drop drawn on the sheet") and his MUST MATCH note repeats it.
2. Reference sheets stay unchanged: no cropped or retouched copies. Their faults are handled only by SHEET_CAVEATS
   lines (nagoji: fort, stone cell and fort wall backdrops, ear stud; ibrahim: pale scar, not red; padmini: hair thick
   and BLACK, ignore grey strands on the sheet), with the sheet sha256 check from the design.
3. Do NOT edit CONTINUITY.md. Write the proposed bible text to a NEW file `CONTINUITY-PROMPT-V2-PROPOSED.md` (the
   full file as it would read after the edits: the scoped-rules section, the chapter 9 span rows, the Padmini base
   line, any row clean-ups the lints need for chapter 9) and a unified diff `review-sheets/CONTINUITY-PROMPT-V2.diff`
   against CONTINUITY.md. The author reviews both before anything is applied. Unit tests use fixtures, not the live bible.
4. Draft `scripts/CHAPTER-09-ART-DIRECTION.json` from `scripts/CHAPTER-09-SCRIPT.md` (all 53 panels): settings with
   label, scopes, anchor, absent, time; page defaults; panel overrides (time, frame, distant, lettering_space, bleed,
   sheets off for inserts) where the script calls for them; character_notes; not_shown. Add `"status": "draft"` (the
   loader accepts "draft" and "approved"; prepare refuses a draft unless `--allow-draft` is passed, so a pilot can run).
   Keep every text free of em and en dashes.

## Musts

- TDD: write the failing tests first (design section 3 as amended by the review), see them fail, then implement.
- Chapters 1 to 8 stay byte-identical on v1. Add both freeze tests: v1 prompts of ch05 to ch08 rebuilt from their
  package snapshots (202 of 202), and v1 against the LIVE CONTINUITY.md for ch05 to ch08 (it currently matches the
  snapshots; this test must fail if a future bible edit would change a v1 prompt). Make the freeze tests fail, not
  skip, when chapters/ exists but a ch05 to ch08 package is incomplete.
- v2 prepare validates and assembles every prompt in memory before writing anything (a lint failure leaves no files).
- Add the read-only prompt audit (`script_pipeline.py audit --out <package>` plus a unit test) from the design's
  verification section.
- Add `--art-direction` (and `--allow-draft`) to `run_chapter.py prepare`; load_job checks the art direction hash.
- Update `pipeline/README.md` with a "Prompt assembly v2" section.
- Full suite must pass, from `pipeline/` with
  `PYTHONDONTWRITEBYTECODE=1 /Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python -m unittest test_compositor test_script_pipeline test_run_chapter test_reserves test_review_sheets test_layout_fit`
  (432 tests today; real-frame tests skip in this worktree).
- No em dashes or en dashes in any file. No deletions. No git commits or pushes (the orchestrator reviews and commits).
- Touch only: `pipeline/` (script_pipeline.py, run_chapter.py, their tests, README.md), the two new CONTINUITY
  proposal files, and `scripts/CHAPTER-09-ART-DIRECTION.json`.

## Report back

What changed (functions, CLI, files), the tests added (names), the suite result, the prompt audit numbers for a dry
run of chapter 9 into a scratch package (under $TMPDIR, using the PROPOSED bible through a test-only path or a
temporary copy, never editing CONTINUITY.md), and any open questions for the author.
