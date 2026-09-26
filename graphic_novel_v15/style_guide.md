# V15 Style Guide

## Look

Hand-inked line with flat watercolour washes. One palette per scene (see `style.palettes`
in `characters.yaml`), so a reader knows where they are from colour alone: umber for the
dungeon, slate and teal for the storm, green and ochre for the coast.

Not wanted: glossy digital painting, airbrushed skin, bodybuilder bodies, film-star faces.
The negative prompt in `characters.yaml` carries these.

## Storytelling rules

1. **Show first, caption second.** A caption says only what the art cannot: time, place,
   memory, or one line of Nagoji's voice. At most 2 captions a page, 18 words each.
2. **Balloons are speech, not summary.** At most 22 words a balloon, 90 words of
   lettering a page. `tools/build.py check` warns past these limits.
3. **Set up every loss.** No character dies or leaves before the reader has seen them
   alive and wanted something.
4. **Let big moments breathe.** Use at least one silent panel at each turning point
   (Kanka falls, the empty hatch, the jump).
5. **Violence by implication.** Torture is shadow and cutaway; battle wounds are shown
   but not lingered on.
6. **Talk scenes need action.** In a council or negotiation, someone must be doing
   something: moving tokens on a map, pouring, walking, writing.

## Page template

- Trim 6.125 x 9.25 in, 300 dpi, the same as V13.
- Chapter openers only: a band with "CHAPTER N" and the title in Cinzel, and a rule
  underneath. No running headers on other pages.
- 30 px gutters, 6 px black panel borders, page number centred at the foot.
- Lettering: Comic Neue, upper case, 8 pt (7 pt minimum). Captions are rectangles in
  pale parchment; speech is a rounded balloon with a tail; shouts have a heavier outline;
  whispers have a broken outline.

## Workflow per chapter

1. Write or revise the chapter's pages in `script_*.yaml`.
2. `python tools/build.py check`, then fix every error and read every warning.
3. `python tools/build.py pages` with no art yet. Read the placeholder pages for pacing
   and lettering before spending anything on images.
4. `python tools/generate_qwen.py panels --pages N-M`.
5. Review each panel against the character anchors. Regenerate failures with
   `--only <id> --force`, or with a different `--seed`.
6. `python tools/build.py pages` and read the finished PDF.

## Fonts

Comic Neue and Cinzel, both under the SIL Open Font License 1.1 (licence texts in
`fonts/`), so they can be embedded in a published book.
