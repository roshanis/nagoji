# V15: full redo at proper adaptation density, drawn by Codex

Author decisions (2026-09-26): redo the whole graphic novel at Chapter 1 density with Codex
built-in imagegen (commercially usable under OpenAI terms), print at 300 DPI or more.

## Why

v7 and V14 run about 5 pages per chapter, roughly 650 words of the novel per page against a
normal 250-400, which is the root cause of the thin feel (compressed adoption, offstage
romance, Padmini's death in a subordinate clause). V15 targets about 300 words per page:
319 pages across 28 chapters (`PAGE-TARGETS.json`, each with a +/-20% range for dramatic weight).
A blind test (`output/model-comparison-v1/`) had Codex beat local Qwen-Image 2.1 in 15 of 15
judgements.

## Phases and gates

1. **Scripts.** Chapters 2-28 are scripted in the format of `scripts/CHAPTER-01-SCRIPT.md`. Each
   chapter has one writer, then three blind reviewers (manuscript fidelity, comic craft,
   continuity), then a reviser who checks every finding against the novel before applying it.
   GATE: the author reviews the scripts.
2. **Pilot fix of Chapter 1.** Upscale its 2 frames below 300 PPI, remove the nooses, redress
   the page-9 guards as Portuguese, and hold Nagoji to the V13 lock (clean-shaven chin,
   moustache, gold stud) by attaching the concept sheet. GATE: the author approves.
3. **Generation.** One Codex task per chapter, with the V13 concept sheets attached to every
   frame that shows a principal. Before preparing a chapter, write and verify
   `scripts/CHAPTER-NN-CAST-OVERRIDES.json` naming the characters actually visible in every panel
   (pronouns resolved, empty sets for landscapes and objects). Without it the pipeline infers cast
   from names and adds Nagoji to any panel with first-person narration: across chapters 2 to 28
   that puts his look and sheet into 296 of 1,372 panels that never describe him, the cause of
   the Chapter 1 panel 8.1 drift. GATE per chapter: every placed image at 300 PPI or more (upscale
   2x if not); all script text present; review against the must-keep beats.
   LEAN PATH (author decision 2026-09-30, to reduce Codex use): Codex only generates images, one
   attempt per job from a job list, and captures them (no reviewing, measuring, ledgers or builds).
   Claude picks the best candidate per panel from contact sheets (one reviewer per page), lettering
   reserves are detected automatically and fit-checked (run_chapter auto-geometry), builds and
   verification run as scripts, and the five-lens review checks each finished chapter. Only panels
   with no acceptable candidate go back to Codex, batched, with a precise prompt correction.
4. **Assembly.** Full book at a 6x9 in trim plus 0.125 in bleed, fonts embedded, text layer,
   separate wrap cover, spine from the final page count and chosen paper.
   File size: the lossless chapter masters run about 19 MB a page (Chapter 1 r4: 169 MB for 9
   pages), so 348 pages would be about 6.5 GB against KDP's 650 MB limit. At assembly, embed
   only each image's visible clip, resampled to 350 PPI, as JPEG quality 90 with 4:4:4 chroma.
   Chapter 1 measures 1.43 MB a page that way, about 500 MB for the book. Keep the chapter PDFs
   as masters. GATE: print-spec check, including every image at 300 PPI or more after resampling
   and the file under the printer's upload limit.

## Sources of truth

- `CONTINUITY.md` overrides any script on appearance.
- The novel, `book1_horse_servant/`, overrides any script on story.
- V14 (`output/comic-v14-chapter-quality-v1/`) is read-only reference for pipeline and style.
