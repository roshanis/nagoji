# V15 per-chapter production pipeline

Entry point: `run_chapter.py`. The pilot is Chapter 1. Sources remain read-only.
The pipeline prepares frames, calls built-in imagegen through a Codex bridge,
records reviewed selections, enforces 300 effective PPI, composes native text,
verifies the final PDF, and renders every page at 300 DPI.

## Runtime

Use Python with Pillow, ReportLab, pypdf and NumPy. On this machine:

```sh
V15_PY=/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
V15_RUN=output/comic-v15-full-redo/pipeline/run_chapter.py
```

Poppler is discovered on PATH or in the bundled Codex runtime. The print fallback
uses the author's reviewed `~/AI/upscalers/upscale2x.py` with
`~/AI/qwen-image-2.1-lab/.venv/bin/python`. Its script, model and licence hashes
are recorded for each upscale. No installer, model download, API-key fallback,
or sandbox-setting change is performed.

## Run chapter N

1. After the author has approved `scripts/CHAPTER-NN-SCRIPT.md`, prepare it with its verified
   cast file, which must list every panel (prepare refuses a missing or partial one):

   ```sh
   PYTHONDONTWRITEBYTECODE=1 "$V15_PY" "$V15_RUN" prepare --chapter 2 \
     --cast-overrides output/comic-v15-full-redo/scripts/CHAPTER-02-CAST-OVERRIDES.json
   ```

   This writes only that chapter's package under `chapters/ch02/`. It records
   script, continuity and V13 lock hashes, parses every page and panel, preserves
   quoted caption/dialogue copy exactly, and creates `IMAGEGEN-JOBS.json`.
   Chapter numbering is 1 through 28; page count is unrestricted. The optional
   ninth page in Chapter 1 is included. Inputs are rehashed before generation
   and build. Concurrent script changes stop the run instead of mixing versions.
   An author's later change to a script's directions (never its panels or copy) is
   accepted per package: copy the prepared script into the package as `SCRIPT-SOURCE.md`
   before editing, then run `run_chapter.py accept-script-revision --chapter N --reason
   "..."`. It refuses unless the frozen copy is the prepared script and the edited script
   parses to the same panels with the same speakers and text, and records the new hash
   in `SCRIPT-REVISIONS.json`, which the input check then accepts. When the author
   shortens or rewords lines (as for chapter 7 page 12), add `--allow-lettering`: the
   text of existing balloons and captions may then change, but never the panels, the
   number of balloons or their speakers, and the new text may not hold an em or en dash.
   Each changed line is logged with its old and new text under `lettering_changes`.
   The balloons are sized from the text, so fit and build again afterwards.

2. Review inferred cast and framing before generation. Pronouns, offscreen speech,
   memories and unnamed figures need editorial judgement. Supply
   `--cast-overrides path.json` on preparation to assign the exact visible cast:

   ```json
   {"page-01-panel-01": ["nagoji", "duarte"], "page-01-panel-02": []}
   ```

   `CONTINUITY.md` provides permanent identity and the chapter's costume.
   Nagoji and Varma receive the corresponding V13 sheets on every applicable job.
   Only explicit `temple_priest` can attach the Hindu ritual-priest sheet.
   The concept must never stand in for Duarte, Ramayyan or bystanders. Principals
   without a V13 sheet use their bible description; no nonexistent sheet is claimed.
   Captions and speech are supplied solely to plan lettering space, never to render
   as image lettering. Newly prepared chapters ask the generator for clear, low-detail
   space and for no painted balloons, boxes or frames at all (the compositor draws them;
   see "Drawn balloons and captions" below). A panel whose description sets it alone in
   a full-width row (layout_fit.layout_cues: "full width", "strip", "tier", "splash")
   also gets a "FRAME SHAPE" line asking for a wide strip about 3 to 1, since the
   generator returns 3:2 unless told. A package prepared earlier keeps its old
   prompts, because preparing again refuses to overwrite a prompt that differs.
   The approved story remains intact where appearance differs.

3. Run `imagegen_driver.js` in Codex `functions.exec` with `chapter = N`.
   It is a tool-runtime bridge, not a Node or shell program. Each invocation
   reads the next job, views its references, calls actual built-in imagegen,
   displays the result and copies the candidate into the chapter package.
   Repeat for each frame. Tool failure means stop and report, with no substitute.
   For correction jobs, attach the original frame plus all applicable concept
   sheets, inspect both first, and save the exact revised prompt and reference
   hashes in the candidate record. Preserve rejected candidates additively.

4. Inspect each candidate at native resolution for identity, costume, nooses,
   anachronisms, composition, hands, silent beats and blank reserves. Measure its
   `visible_rect` and each reserve in top-left source-pixel coordinates. Example
   geometry file:

   ```json
   {"visible_rect":[10,10,1526,1014],
    "reserves":[{"kind":"caption","rect":[30,35,700,170],"copy_indices":[0]}]}
   ```

   Lettering supports paired markdown italics, for example
   `Easy, *bhau*. You are on land now.` Canonical copy removes the paired
   asterisks before wrapping and verification. The paired words use the same
   8.5-point DIN face and colour with a 12-degree synthetic oblique; the rest
   stays upright. Fit and native-pixel audits include the oblique ink bounds.
   Unpaired asterisks remain literal. A standalone `*No text.*` direction remains
   a direction, with no lettering. Plain copy without markers keeps its existing
   PDF output byte for byte.

   For Chapter 4 panel 6.2, add `"style":"unreadable"` to its speech reserve:

   ```json
   {"kind":"speech","rect":[30,35,700,170],"copy_indices":[0],"style":"unreadable"}
   ```

   The rectangle above is an example only; retain the reviewed source-pixel
   rectangle for panel `page-06-panel-02`. Keep the script unchanged:
   `... *kapitan* ... *kapitan* ...`. In this mode, outside words and punctuation
   become broken vector waves at DIN x-height, with whitespace retained as gaps.
   Only the paired words appear as clear oblique text, in order. Wave widths
   participate in wrapping; their stroke bounds participate in fit and native
   pixel audits. PDF verification checks only the clear words for that chunk.
   Omit `style` for normal lettering. The only accepted explicit value is
   `"unreadable"`; other values, including null, are rejected at the build gate.
   The mode applies to every chunk listed in that reserve.

   `copy_indices` indexes that panel's exact parsed chunks. A reserve may contain
   multiple consecutive chunks; every chunk must occur once. Add `sound_origin`
   only where the script requires musical marks. Chapter 1's ledger inscription
   is explicitly enabled using `ledger_inscription: true` plus `ledger_rect`.
   Select a reviewed candidate:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 "$V15_PY" "$V15_RUN" select --chapter 2 \
     --candidate output/comic-v15-full-redo/chapters/ch02/candidates/page-01-panel-01-v01.json \
     --geometry path-to-measured-geometry.json --reviewer Codex \
     --review-note 'Identity, action, blank reserves and continuity visually passed.'
   ```

   Selection is an explicit editorial step. The pipeline does not claim automated
   facial, costume or historical acceptance from a text prompt or successful API call.

5. Review page layout. Equal-height rows are the initial default. Dramatic weighting
   should be expressed in a `LAYOUT.json` with `page_rows`: full-width rows are
   numbers; side-by-side panels are lists of equal row heights. Every page must
   total 523.5 points including 2-point gaps. Chapter 1 preserves its exact r3 rows.
   The compositor retains aspect ratio, visible crop, native 8.5-point DIN lettering,
   embedded Georgia headings, and fails when lettering does not fit. It never
   shrinks the script text to conceal an inadequate reserve.

6. Build and verify:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 "$V15_PY" "$V15_RUN" build --chapter 2 \
     --layout output/comic-v15-full-redo/chapters/ch02/LAYOUT.json --first-folio 10
   PYTHONDONTWRITEBYTECODE=1 "$V15_PY" "$V15_RUN" verify --chapter 2 --first-folio 10
   ```

   The delivered pilot uses `--manifest output/comic-v15-full-redo/chapters/ch01/SELECTION-INPUT-r5.json`
   and `--revision r5` to import its copied V14 r3 selections and regenerated
   candidates. Use a fresh revision to rebuild; an existing output is protected.
   An import must meet the
   same frame hash, prompt hash, reference, visual-review and exact-copy gates.
   Reused originals must be copied into the new package and retain source hashes.

## Moving panels to a new page: import-frame

Prepare a new sibling package from the revised script, then import each chosen
candidate from the original package. For example, move chapter 5 panel 8.4 to 9.1:

```sh
PYTHONDONTWRITEBYTECODE=1 "$V15_PY" "$V15_RUN" import-frame --chapter 5 \
  --package-dir output/comic-v15-full-redo/chapters/ch05-split \
  --from-package output/comic-v15-full-redo/chapters/ch05 \
  --source page-08-panel-04-v03 --frame-id page-09-panel-01
```

The target panel must be a prepared job, and both packages' recorded scripts must
have identical speakers and text, chunk for chunk. The target is validated through
`load_job` as usual. Source lettering comes from the source package's
`SCRIPT-SOURCE.md`, whose SHA256 must match the script hash in `IMAGEGEN-JOBS.json`.
Matching entries in `SCRIPT-REVISIONS.json` apply their recorded `lettering_changes`
in order; entries without lettering changes preserve the frozen copy's lettering.
This keeps old panel IDs available after the author repaginates the live script.
Only when `SCRIPT-SOURCE.md` is absent may import read the live source script, and
its hash must match the prepared hash or an accepted revision for that script.
A mismatched frozen copy or unrecorded live hash is refused, even when the job
contains embedded script pages. The source frame must match its
recorded SHA256, and the source and target packages must differ. The command copies
the frame to the next free target version without overwriting frames or records.
It prints the new candidate JSON with `origin: "imported"` and `imported_from`
containing the source package, candidate record path and SHA256, and original panel
ID. The generating prompt and its hash remain those of the source candidate.
Review starts as `pending`; measure geometry and review the new panel before
selection. Selection and build retain the original prompt hash check.
`--from-package` and `--source` apply only to `import-frame`.

## Prompt assembly v2

Chapter 9 and later require an art direction sidecar. Chapters 1 through 8 keep
the v1 prompt path unless a separate sibling package explicitly opts into v2.
The sidecar is selected with `run_chapter.py prepare --art-direction FILE`.
Draft sidecars require `--allow-draft`; preparation still validates every panel
before it writes the package. A v2 job records `prompt_profile: "v2"`, the
sidecar path and SHA256 under `art_direction`, a `setting` on every job, and
`ART-DIRECTION-SNAPSHOT.json`. `load_job` rejects unknown profiles, requires
the sidecar record for v2, and accepts a changed or unavailable source only
when the recorded package snapshot has the original hash.

The sidecar schema is:

```json
{
  "prompt_profile": "v2",
  "chapter": 9,
  "status": "draft",
  "settings": {
    "verandah": {
      "label": "the palace verandah",
      "scopes": ["kerala", "court"],
      "anchor": "carved wooden pillars and a view of the wet garden",
      "absent": "no fort, European building or stone cell",
      "time": "morning light",
      "allow_terms": []
    }
  },
  "pages": {"1": "verandah"},
  "panels": {
    "page-01-panel-01": {
      "setting": "verandah",
      "time": "morning light",
      "frame": "standard",
      "distant": false,
      "lettering_space": "upper wall",
      "bleed": "none",
      "sheets": true
    }
  },
  "character_notes": {},
  "not_shown": {}
}
```

Every panel must resolve to one known setting. Setting scopes, anchors and
absent text are linted, and the prompt places the setting label in the header
and the setting anchor in the final paragraph. Scoped continuity rules replace
the v1 standing block. Prompt lettering summarizes count, speaker and length
without quoting copy, then asks for clear low detail space and states the no
text rule once. Reference sheets are listed in attachment order and their
approved hashes and caveats are checked. Cast gaps, foreign terms in Indian
settings, stale look rows, unknown sidecar keys and forbidden dash characters
fail preparation before any output is written.

The valid setting scopes are `kerala`, `court`, `coast`, `travancore_camp`,
`dutch`, `portuguese`, `deccan`, `carnatic` and `sea`. `allow_terms` is an
optional list of otherwise guarded words for that setting. Page defaults are
merged first, then panel overrides. Panel overrides may set `setting`, `time`,
`frame` (`strip`, `standard` or `tall`), `distant` (boolean),
`lettering_space`, `bleed` and `sheets` (boolean). A frame contradiction with
the script, such as a strip override that conflicts with a required tall
composition, is rejected for review. `not_shown` changes the prompt by stating
which named person is outside the frame; it also satisfies the cast lint for
that panel. A sidecar must declare `status` as `draft` or `approved`.

The author approved the proposed bible on 2026-10-02
(`review-sheets/CONTINUITY-PROMPT-V2-REVIEW.html`) and it is now `CONTINUITY.md`,
with one addition: Padmini's grey hair from chapter 16. The applied change is
`review-sheets/CONTINUITY-PROMPT-V2-APPLIED.diff`, and the bible from before it is
`pipeline/review/CONTINUITY-pre-prompt-v2-2026-10-02.md`.
`CONTINUITY-PROMPT-V2-PROPOSED.md` is kept only as the record of what was reviewed.
Chapter 8 is pinned to its own `CONTINUITY-SNAPSHOT.md`: the new Padmini line would
change 29 of its v1 prompts, so the live-bible freeze test covers chapters 5 to 7
and the snapshot freeze covers 5 to 8. Never prepare chapters 1 to 8 again against
the live bible. A pilot uses the live bible and the draft Chapter 9 sidecar
through a scratch package:

```sh
TMP_PACKAGE="${TMPDIR:-/tmp}/nagoji-ch09-v2-pilot"
PYTHONDONTWRITEBYTECODE=1 "$V15_PY" pipeline/script_pipeline.py prepare \
  --chapter 9 --out "$TMP_PACKAGE" \
  --scripts-dir scripts \
  --cast-overrides scripts/CHAPTER-09-CAST-OVERRIDES.json \
  --art-direction scripts/CHAPTER-09-ART-DIRECTION.json --allow-draft
PYTHONDONTWRITEBYTECODE=1 "$V15_PY" pipeline/script_pipeline.py audit \
  --out "$TMP_PACKAGE"
```

The audit is read-only and checks the prompts actually sent, using candidate
records and selected rows when they exist. It reports the number ending in a
SETTING paragraph, copy leaks, foreign terms outside author text, rule share,
median length against v1, no text rule count, reference sheet order and the
Chapter 9 boots and barefoot split. Audit corrected prompts as well as base
prompts. The initial nine-panel pilot is 1.5, 2.2, 5.4, 8.5, 9.2, 5.2, 3.1,
10.5 and 9.1. Read those v2 prompts beside their v1 in-memory versions and
keep any A/B comparison outside the package and before editing the live bible.
The capture gate requires an appended or moderated v2 prompt to repeat the
exact final SETTING paragraph as its final blank-line paragraph. A v2 correction may also be set in just before
the prepared final SETTING paragraph (the prepared text before it unchanged, SETTING still last);
the chapter 9 correction batches use that layout. v1 corrections are only ever appended. This worktree
contains no images and performs no image generation.

Do not bypass hash checks or replace the production sidecar. A v1 versus v2 A/B
comparison must use the bible from before the edit (the backup above), as the
Chapter 9 acceptance test does with the Chapter 5 snapshot.

Padmini's sheet caveat says her hair is BLACK with no grey. That is right through
chapter 15. From chapter 16 her bible row adds grey threading, so the caveat must
become chapter-aware before chapter 16 is prepared.

## Lean review path

Codex only generates images. Frame review and lettering-space measurement run locally
with three small tools that never write into a chapter package except through the
existing `capture` and `select` commands.

1. Contact sheets. `review_sheets.py` writes one PNG per panel (all candidate frames,
   labelled `v01`, `v02`, ..., under the panel id and cast) and an `INDEX.json` that maps
   each panel to its sheet and to each candidate's record, frame and hash. The output
   directory must be new and outside the package. Provenance files are not candidates;
   an extra record such as `r7-a01` is listed only if it adds a frame.

   ```sh
   PYTHONDONTWRITEBYTECODE=1 "$V15_PY" output/comic-v15-full-redo/pipeline/review_sheets.py \
     --package-dir output/comic-v15-full-redo/chapters/ch03 --out /path/to/new/sheets-dir
   ```

2. Capture a corrected generation with its real prompt. `capture --prompt FILE` records
   FILE as the candidate's `prompt_path` and `prompt_sha256`, and keeps the prepared prompt
   as `base_prompt_path` and `base_prompt_sha256`. FILE must exist and must begin with the
   prepared prompt text, so a correction can only be appended. Nothing is written if it
   is refused. Without `--prompt`, `capture` is unchanged.

   ```sh
   ... capture --chapter 3 --frame-id page-04-panel-01 --generated GENERATED.png \
     --prompt output/comic-v15-full-redo/chapters/ch03/prompts/page-04-panel-01-generation-v05.txt
   ```

3. Measure the reserves. `auto-geometry` detects one blank outlined shape per copy chunk,
   applies the compositor's own fit measurement at the panel's placed size (the
   chapter's `LAYOUT.json` `page_rows` if present, else the default rows), runs the same
   native light-pixel audit as the build, and only then writes the geometry file (it
   never overwrites one). Otherwise it exits non-zero and says why (too few shapes, or
   which chunk does not fit and by how much). Pass the file to `select --geometry`.

   ```sh
   ... auto-geometry --chapter 3 --candidate output/comic-v15-full-redo/chapters/ch03/candidates/page-04-panel-01-v05.json \
     --geometry-out /path/to/page-04-panel-01-geometry.json [--inset 2]
   ```

   The rectangle in each reserve is the largest blank rectangle inside the shape, inset
   6 px. When a reserve misses by a few points, retry with `--inset 2` (0 to 8 allowed);
   the fit and pixel checks still apply. `reserves.py IMAGE --speakers CAPTION,NAGOJI`
   prints the raw detection for one frame.

   `--layout FILE` (a file with `page_rows`, such as `fit-layout` writes, or another
   chapter's `LAYOUT.json`) is passed through to the same `geometry_for_script` that
   `build --layout` uses, so `auto-geometry` (with or without `--draw`) measures against
   those rows instead of the package's `LAYOUT.json`. Use it to try a fitted layout
   before it replaces the chapter's; the file is only read.

### Drawn balloons and captions

Generators paint balloons with tails to the wrong speaker, boxes with no tail, and the
wrong number of areas, and the painted ones are often too small for the text (the
pipeline never shrinks lettering). So the compositor can draw them. A reserve gains two
optional fields; without them a page is byte for byte what it was:

```json
{"kind":"speech","draw":"speech","rect":[611,0,1003,203],"copy_indices":[1],"tail":[1213,566]}
```

- `"draw": "caption"` draws a white rectangle with a 0.8 pt black stroke at `rect`.
  `"draw": "speech"` draws a white rounded shape (corner radius 45 percent of the shorter
  side) with the same stroke. `tail` is `[x, y]` in source pixels, the speaker's mouth. It
  adds a tapered tail from the nearest edge, stroked and filled first and then covered by the balloon so no
  outline crosses its base. With `tail_head` (`[x, y, r]`, the speaker's head circle in source pixels, written by
  `auto-geometry --draw` for an on-frame speaker) the tail stops 3 pt outside the head; with none, or where the tail's line
  misses it, it stops 12 percent of the way short of the mouth (4 to 12 pt), and never shorter than 8 pt or past 90 percent of
  the way. `tail_short: true` (only with a `tail`; written by the planner for a balloon only the old tail could place, see
  below) draws the legacy short tail instead, ignoring the head: about 60 percent of the way, 8 to 28 pt. A target inside the balloon is refused, except one on the panel
  edge (an off-frame speaker) inside a balloon that touches that edge, which draws no tail. A tail to an off-frame
  speaker (a mouth point within 0.5 pt of the panel edge, or beyond it) runs all the way to the border, so it reads
  as pointing out of the panel rather than at whoever stands between the balloon and the edge; the planner checks
  that full length against faces and other balloons. Every face counts for such a tail, since none is its speaker's
  (until chapter 6 r1 only tails to on-frame speakers were checked, and an off-panel tail in 4.5 ran across Varma's eyes).
- `rect` is the shape. Text is centred inside it with at least 5 pt of padding (a balloon
  adds a little more so the text clears its rounded corners), and the fit check uses that
  padded interior. The shape is clipped to the panel. It may run past an edge of `visible_rect`
  only so far that its text area and that padding (the shape inset by the corner clearance, about
  0.29 of the radius) stay inside it, and the panel border is drawn over the cut; a caption's text
  area plus padding is its whole rectangle, so a caption stays inside.
  Italics and the `unreadable` style work as before; text verification is unchanged.
  `audit_reserve_pixels` skips drawn reserves, whose text sits on their own white fill.
  Upscaling scales `tail` with `rect`.
- Prompts for newly prepared chapters no longer say "Reserve exactly N blank outlined text
  area(s)". They ask for clear, low-detail space (sky, wall, floor, shadow) for N lettering
  areas, preferably in the upper part of the frame, and for no balloons, boxes, frames or
  text of any kind. The prompt also says this replaces any mention of blank balloon or
  caption reserves, because the standing rule in `CONTINUITY.md` ("blank balloon and
  caption reserves only") still reads that way and should be reworded there.

`auto-geometry --draw` plans the boxes. Speech chunks need their speaker's mouth from
`--tails FILE`, a JSON list (one `[x_frac, y_frac]` or `null` per copy index) or map
(`{"1": [0.5, 0.9]}`), as fractions of the source image. A speech chunk with no point
fails and names the chunk; a point is never guessed, and a caption takes none.

```sh
... auto-geometry --chapter 4 --candidate output/comic-v15-full-redo/chapters/ch04/candidates/page-01-panel-04-v01.json \
  --geometry-out /path/to/page-01-panel-04-geometry.json --draw --tails /path/to/tails.json
```

For each chunk in reading order the tool sizes the wrapped text at the panel's placed
size (wrap width the larger of the painted region's width and 36 percent of the visible
width, never narrower than the longest word) plus padding. If a painted blank region was
found for that chunk, the box is centred on it and covers its bounding box plus 8 px, so
no painted outline shows. Otherwise the box goes in the frame's quietest clear window:
lowest edge density, near the top, after the previous box, clear of every tail target.
Boxes are kept inside `visible_rect` and apart from each other.

A balloon with a tail is placed so that its tail reads as pointing at its own speaker. The tail's path, the wedge as
the compositor draws it (as wide as its base where it starts, tapering to its tip) and the line on from its tip to the
mouth, never crosses another balloon (a later chunk's painted region stands for its balloon), no balloon sits across
another's tail, and, when the speaker is in the frame, the path
never enters a face zone that is not the speaker's own (the zone nearest the mouth, and any that holds the mouth or
overlaps it). Readers also credit a balloon to whoever its drawn tail's tip lands nearest, and the tip stops just outside
the speaker's head (the head circle every on-frame tail point implies, see `tail_head`), so the tip is never nearer to another face
zone than to the speaker's own (distances to each zone's edge, 0 inside it). Nor does the tip land on another figure's
body: a face zone stands for a person, whose body is taken as the column two face radii either side of the face, from
its bottom down to eight radii below its centre (`BODY_HALF_WIDTH`, `BODY_DEPTH`). A tip there reads as theirs even
when the speaker's face is the nearer face, unless it is on the speaker's own body as well (chapter 6 r2, 9.5:
Ramayyan's order tailed onto Varma's knee). A balloon with no painted region goes as near its speaker (for a voice off frame, its point on the
edge, since the tail shows where the voice comes from) as it validly can: windows are ranked by
tail length, quietness only breaking ties between similar lengths, and a tail longer than 35 percent of the visible
frame's diagonal is taken only when nothing shorter is valid (if that leaves a chunk unplaced, nearness is given up
only where needed, with the rules above still holding: first for the failing chunk, then for it and one earlier chunk at a
time, the nearest first, and only then for every chunk). Boxes also read in script order, judged by their tops as
a reader takes them. A strict rule is tried first: tops within a quarter of the shorter box's height are level, and a level later box lies to the right; otherwise the later box starts lower, and if it sits to the LEFT it must start below the earlier box (overlapping it by at most a tenth of the shorter height), because a box at the left inside another's band is read first by some readers and second by others. The planner places boxes as high as a rule allows, so a looser threshold is always met right at its edge. Only when no placement meets the strict rule is the lenient one used (tops within 0.4 of the shorter height, or a later box starting lower by less than two thirds of it, or a later box starting lower with at least half of the shorter height inside the earlier box's band, are level; otherwise it starts lower). The band test catches a short box beside a tall one: chapter 2 r2, 5.3, put a one-line reply at the left, 135 px below the top of a three-line balloon but inside its band, and readers took the reply first. Placement is greedy, so an early chunk can take the quiet bottom of the frame and strand the rest; each rule is tried at the usual top preference (`TOP_WEIGHT`, 0.35) and then at stronger ones (`TOP_RETRY`). Greedy placement never revisits a chunk, so when every attempt fails because an earlier chunk's box stops a later one (a tail would cross it, or the later box would read before it), the panel is re-placed with that box barred from the spot it took, up to `REPAIR_ROUNDS` (4) times; a panel that placed without repair is placed exactly as before. A chunk that cannot meet these fails naming the chunk and what is in the way ("its
tail would cross chunk 1's balloon", "its tail would cross a face (Duarte)", "its tail tip would point at another figure
(Duarte)", "its box would read before chunk 0's").

A chunk that no position of any wrap lets through with that long tail is tried again with the legacy short tail (60 percent of
the way, 28 pt at most), and, if that places it, the reserve gets `tail_short: true` and the chunk is listed as `short_tail` in the
report; later chunks are checked against the tail each earlier chunk was placed with. If the greedy order still strands a
chunk, the planner as it was before tails knew heads is the last resort (every balloon with the short tail), and the long tail goes
back on each balloon whose long tail reads right in that layout. Where neither places the panel the error is the long
tail's, as ever.

Two more wishes are soft: a chunk meets them where any position of any wrap allows, and is placed without them, as it
always was, where none does. A balloon for a voice off frame keeps at least 8 pt plus the 0.8 pt stroke between its box
and the frame edge its speaker is beyond, so the compositor draws a tail and not a stub clipped by the panel border; the
chunks that could not (they touch the edge, or sit too near it) are listed as `edge_voice_no_tail`. `--keep` zones are
avoided by every box: a box may cover less than a tenth of a zone's area (the part inside the crop), and the chunks that
cover more are reported as `keep_overlaps` (`{chunk: [keep index]}`). When a chunk cannot have both, it keeps off the
keep zones and gives up its tail room.

With `--draw`, `visible_rect` is a cover crop. A generated frame is 3:2, but a page slot can be a full-width
strip (3.7) or a half-width cell, and the compositor fits `visible_rect` inside the slot without cropping it,
so a 3:2 frame in a strip would sit as a narrow image between empty bars. The planner first crops the art toward
the slot's shape (`reserves.cover_crop`): its height for a wide slot, its width for a tall one. The crop keeps
inside it every face zone, every head a tail point implies, every painted region (outline included), every
`--keep` zone and every tail point that is on the frame, and never less than 45 percent (`MIN_KEEP`) of the art's
height or width; it is
centred on what it keeps as far as the art allows. Where those keeps or the 45 percent stop the crop short of the
slot's shape, the compositor fits what remains with side bars. A tail point on the art's edge is an off-frame
speaker and is not kept; if the crop cuts that edge away, the point is moved onto the crop's edge so its tail still
points off frame. A silent panel is cropped too, keeping only its `--faces` and `--keep` zones. The geometry file carries both
`visible_rect` (the crop) and `art_rect` (the art), `select` copies both into the row, and `fit-layout` reads
`art_rect` and models the same crop. A cropped frame is magnified, so its effective PPI is lower than the uncropped
frame's in the same slot, and the build's DPI gate may upscale frames it used to pass.

A box never covers a speaker's mouth (its own tail point or another chunk's) or comes within
3 pt of it, so its tail stays visible:

- When the box centred on its region would, it is grown away from the tail point: the side
  nearest the point stays at the region's edge and the box extends the other way, along the
  vector from the point through the region's centre, then the two perpendicular ways, clamped
  inside `visible_rect`. Any other position that still covers the region and clears every
  neighbour and tail point is tried after that.
- If a box still cannot be placed, narrower wraps (more lines) are tried with the same
  growth, and boxes that collide are shifted apart, before the chunk fails.
- If the painted region itself contains a tail point, the planner alone (`place_boxes` with no
  face zones) covers the largest part of it that keeps the point clear and lists the chunk as
  partly covered. `auto-geometry --draw` does not reach that case: a mouth inside the painted
  balloon means the balloon is over the speaker's face, and the head zone below fails it first.
- A tail point on the frame's edge (fraction 0 or 1, or outside `visible_rect`) is an
  off-frame speaker: it never blocks a box and is never an error. The compositor draws its tail
  toward the edge when there is room, and draws no tail when the balloon touches that edge; the
  planner leaves that room unless it cannot (see `edge_voice_no_tail` above).

A balloon or caption never covers a face. Every tail point implies a head: a zone centred half a
radius above the mouth, with radius 0.09 of the frame height, unless a given face already covers
the mouth (two chunks from one speaker share a zone, and a tail at the frame edge implies none,
its speaker being off frame). `--faces FILE` adds faces that have no tail, for example a listener
a balloon would otherwise sit on:

```json
[{"x": 0.31, "y": 0.32, "r": 0.13, "name": "Nagoji"}, {"x": 0.60, "y": 0.17, "r": 0.14}]
```

`x` and `y` are the face's centre and `r` its radius, as fractions of the frame, `r` of its
height; `name` is used in messages. Every box, measured to its rounded shape and including any
bleed, stays clear of every zone: the planner picks a position or a narrower wrap that does,
and the quiet-window search for a chunk with no painted region avoids them too. If a painted
region itself reaches a face, or every box that holds the text and hides the region would,
the chunk fails with "would cover a face", naming the chunk and the face. Nothing is shipped
with a covered face; regenerate that frame. The command's output lists `face_clearance` (for each
box, its distance in px and pt to the nearest face, and which) and the `head_zones` it added.
Only a painted balloon's own tail or a face you list protects a head: a head that is neither
(Nagoji, listening) needs a `--faces` entry.

`--keep FILE` names story-critical areas (a gripping hand, a prop, a brand) that the cover crop must keep in view, as it
keeps faces: a JSON list of `{"x0": 0.6, "y0": 0.7, "x1": 0.8, "y1": 0.95}` as fractions of the frame's width (x) and
height (y); other keys such as `"what"` are ignored. A keep zone constrains the crop, for spoken and silent
panels alike, and is a soft obstacle to boxes (see above: avoided when a place exists, covered and reported when none
does). If it cannot fit with the faces and painted regions inside the slot's shape the
crop is left taller (side bars) rather than cutting any of them. `fit-layout` reads `<frame stem>-keep.json` from
`--faces-dir` in the same format, and `--probe` passes the zones to the planner.

`--styles FILE` (JSON `{copy index: style}`, for example `{"0": "unreadable"}`) letters that chunk in
the style: its box is sized for the styled wrap and the reserve carries `"style"`, so the build
measures the same lines the planner did. Only the listed chunks are styled; a chunk given a style
after planning would re-wrap at build and fail the fit check.

When a chunk cannot be placed, the error says why: the regions too close together, a box
that would always overlap its neighbours, or a box that must reach the mouth. The same fit
measurement runs before anything is written. `--inset` does not apply with `--draw`. Without
`--draw`, `auto-geometry` is unchanged.

A balloon's text area is inset from its edge by 5 pt of padding plus a corner clearance that grows
with its shorter side (0.29 of the corner radius). A box made taller than its text needs, because
the painted region it must cover is taller, therefore has a narrower text area than the wrap was
sized for, and the copy could re-wrap to an extra line ("copy does not fit its reserve"). The planner
widens such a box so its text area keeps the width its wrap needs, exactly by the corner rule and
plus a pixel, and checks the widened box like any other (frame, neighbours, tail points, faces,
hidden corners, bleed). A box that already has that width is left exactly as it was, and captions,
which have no corner clearance, are never widened.

A balloon's corners are rounded, so covering a painted region's bounding box is not enough:
a rectangular painted region would show a white wedge at each corner. Over a painted region a
balloon therefore hides every painted pixel (the region's interior plus its outline ring, about
5 px), corners included, which for a rectangular region means its corners lie inside the rounded
shape (a corner needs about 0.29 of the radius of room). The box grows evenly by the least
amount that achieves this, or its corner radius is reduced (reserve field `"corner"`, a share of
the shorter side, 0.45 by default and never below 0.40 so it still reads as a balloon),
whichever keeps the box smaller. `corner` appears in the geometry only when it was reduced.
Ellipse-shaped painted regions, whose bounding-box corners are empty, need no growth. Captions
are rectangles and need nothing. The check is on painted pixels, not just bounding boxes, so a
rounded or elliptical painted region is not over-covered.

A painted balloon in the frame's corner leaves no room to grow outward, so where its painted
region touches a frame edge (within 6 pt of it) and its corners cannot be hidden inside the frame,
the balloon may run off that edge. The panel clips it there and draws its border over the cut, as a
comic balloon cut by the panel edge. It may do this only on the sides its region touches, only as far
as its text area and padding allow (see above), and then by no more than needed. The command's output
lists such chunks as `bleeds`, with the pixels past the frame on each side. The same holds for a
balloon whose box is pinned to an edge by a large text block. A chunk whose corners still cannot be
hidden fails with "the corners of its painted region cannot be hidden": for example two painted
balloons so close that their boxes need more corner room than lies between them.

### Malayalam lines: angle brackets

Chapter 4 letters speech Nagoji cannot follow inside angle brackets (`<Kill him.>`), typed into the script. Chapter 5
instead tags such lines `(Malayalam)` and asks for a distinct treatment, and its r2 lettered them as plain balloons, so
Nagoji seemed to understand Malayalam unaided. `run_chapter.lettered_script` is what auto-geometry, fit-layout, build
and verify read: `parse_script`, with every line whose speaker tag names Malayalam put inside angle brackets (a line
already bracketed is left alone). The script file, `parse_script` and the image prompts are unchanged, and
accept-script-revision still compares the raw lettering.

### Art with no painted balloons: `--unpainted`

Chapters generated with the lettering update (no balloons, boxes or text in the art) have nothing painted to cover,
but the region finder can still read a pale outlined area of the art as a painted blank: chapter 6 r1, 9.5, had open
sky between a pillar and the roof, and its first balloon was made to cover all of it, which reached the king's face at
every row height. `--unpainted` on `auto-geometry --draw` and on `fit-layout` says the art has no painted regions:
the planner measures none (each box goes in the quietest clear space near its speaker) and the fitter keeps none in
the crop. It applies to the whole run (it sets `run_chapter.UNPAINTED`, the default for `drawn_geometry` and
`fit_inputs`), so pass it to every assemble and fit of such a chapter, and never to a chapter whose frames carry
painted reserves (chapters 1 to 4 have some).

### Fitting row heights to the lettering

`LAYOUT.json` row heights are drawn before any text is measured, so a strip that carries two or
three speech lines can be left with no clear area for its balloons ("no clear area of W x H px
remains"). `fit-layout` keeps a prior layout's row structure (which panels share a row, as in
`page_rows`) and re-balances the heights within each page (`--structures`, below, chooses the structure too). It never touches `LAYOUT.json`, refuses
to overwrite `--layout-out`, and writes a layout file that `build --layout` and
`auto-geometry --layout` accept (`--layout` makes `auto-geometry` place against those rows instead
of the package's `LAYOUT.json`, so a fitted layout can be tried first).

```sh
... run_chapter.py fit-layout --chapter 4 \
  --manifest output/comic-v15-full-redo/chapters/ch04/SELECTION-INPUT-drawn-r4.json \
  --decisions output/comic-v15-full-redo/chapters/ch04/review/LEAN-SELECTION-drawn-merged-r2.json \
  --faces-dir output/comic-v15-full-redo/chapters/ch04/review/geometry-drawn-r4 \
  --layout output/comic-v15-full-redo/chapters/ch04/LAYOUT.json --layout-out /path/to/LAYOUT-fitted.json
```

`--manifest` supplies each frame's art rectangle (`art_rect` when its row has one, else `visible_rect`), width and
height (a selection manifest's `frames`);
`--decisions` supplies the picked candidate's frame (measured with `art_bounds`) for panels the manifest
lacks, and a panel with neither is fitted as art that fills its slot. `--faces-dir` holds
`<frame stem>-faces.json` files, read as written: the assembler already scaled their radii (0.55 of the
whole-head zones), and auto-geometry places balloons against them unscaled, so the fit must too.
`--face-scale` (default 1) multiplies them again only for hand-made, unscaled face files. For each panel the fit estimates the lettering load, the padded balloon or caption
boxes its chunks need at the real 8.5 pt DIN wrap (36 percent of the placed clip's width), against the
usable area, the placed clip minus its face zones. The clip models the planner: the art is cover-cropped toward the
slot's shape, keeping every face zone, every painted region the planner would keep (measured with `find_regions` for
each panel that has copy, once per frame) and every `-keep.json` zone, and 45 percent of its height or width, then
aspect-fitted. A frame whose painted regions span its width cannot be narrowed, so the fit sees it letterboxed in a
tall slot, as the planner will. In order of priority:

1. Every page still totals exactly 523.5 pt with its 2 pt gaps, in whole tenths of a point, so
   `geometry_for_script` accepts it.
2. The page's minimum usable-to-needed ratio is maximised, up to `--margin` (default 3).
3. A row whose art cannot span the column is given the smallest height at which the cropped art does (with
   no face zones, painted regions or keep zones in the way, the column width over the art's aspect divided by 45 percent), where the page
   budget allows, evening out the fill. The fill is the share of the slot's area (the column's width times the row's
   height) that the placed art covers, so art that spans the column but sits boxed above and below in a tall slot
   counts as under-filled, as art with bars at the sides does.
4. Any budget left goes to the lowest ratios that can still improve, then is spread over rows with headroom.

No row drops below 55 pt or below 60 percent of its prior height (a silent row may drop to 55 pt), and
none grows beyond twice its prior. The command prints, per page, each row's prior and new height, the
minimum ratio before and after, each panel's ratio and fill before and after (`fill_before`, `fill_after`: the share of its
slot's area the art covers; `fill_width_before` and `fill_width_after` give the share of the column's width it spans), and a `status`:
`ok` (every row reaches the margin), `tight` (the page cannot reach it inside the bounds) or
`cannot_fit` (a row's lettering needs more area than its panel has, or a probed floor is unmet), with a
`reason`. The bounds are never violated; a page that cannot fit is reported instead.

The ratio is an area proxy. It knows nothing of tail keep-outs, balloon collisions or reading order, and sees
painted regions and face zones only through the crop they hold open (and faces' area), so the ratio at which a panel is actually placed varies widely (on chapter 4 from about 1.4
to 11). `--probe` (needs `--faces-dir`, which must also hold each frame's `<stem>-tails.json`, as
`geometry-drawn-rN` does) asks the planner instead: each row's panels are scanned upward from the row's
lower bound, in 5 pt steps, for the first height at which `auto-geometry --draw`'s plan, fit measurement
and pixel audit all pass. That height becomes a floor the ratio fit works above. The chosen heights are
then verified, and a panel that fails at its chosen height (placement is not monotone in height) is
pinned to the nearest height that works and the fit repeated. The output's `probe` section lists the
floors, the pins, whether each probed panel `verified` at its final height, the panels that fail there
whatever the height (`unplaceable`, left to the ratio fit), the panels the 5 pt scan missed but that are
placed at their final height (`off_grid`, a narrow window such as the 2 percent aspect tolerance gives),
and the panels without a tails file or frame (`unprobed`). A probed floor the
page cannot give is reported as `cannot_fit`. Probing runs the planner about 10 times per panel (226 runs, a few minutes, for chapter 4's 25 probed panels).

With `fit-layout --probe`, opt in to `--keep-max F` (`0 < F <= 1`) to reject a placement when its boxes cover more
than that share of any keep zone's visible area. It also applies with `--structures` and parallel workers. The value
is recorded as `keep_max` in the layout's `fitted_from` and the returned report; omitting it preserves the existing
behavior. `auto-geometry --draw` reports `keep_coverage` beside `keep_overlaps`: one fraction per keep zone, summing
box intersections with the zone's part inside `visible_rect`, or zero if the zone has no visible part. Placement is unchanged.

**Choosing the rows too: `--structures`.** Frames from the image generator are mostly 3:2, and five full-width
rows of 3:2 art on one page cannot all span the column (the crop is limited), so many panels come out narrower than the
column with empty bars at the sides, while two 3:2 panels side by side fill it naturally. With `--structures`, each page
is fitted for every way of grouping its panels, in reading order, into consecutive rows of one or two panels (5 panels:
8 structures), and the best is written. Add `--structures` to the command above (and `--probe`, to have the planner
verify the best candidates). Rows of three are not tried. The prior layout's own structure (hand-made for
chapters 1 to 4, one full-width row per panel where a page has none) is always a candidate, and wins a tie. Without the
flag nothing changes.

With `fit-layout --structures --probe`, `--jobs N` runs independent pages in spawned workers, defaulting to the CPU
count minus two (at least one), capped at the page count. `--jobs 1` keeps the in-process path. Both paths retain the
same page order, layout, report and total planner call count; worker errors propagate to the command. `--jobs` is
refused outside `fit-layout --structures --probe`.

Script layout cues, read from each panel's `description` (case-insensitive, from its first two sentences):

- Alone in its row: "full width", "full-width", "full page width" (so "Full-width tier" and "Wide, full page width" too);
  and the words "strip", "tier" and "splash" among the first six words ("Narrow strip.", "Bottom strip.",
  "Widescreen strip, top.", "Large, most of a tier."). Not "a strip of beach", not a strip mentioned later in the scene
  text, and not when the first sentence asks for panels side by side ("Split tier, two narrow panels side by side.",
  "Left half of the third tier.", "side by side"), which asks for the opposite. A panel alone in its row also floors
  that row at the height where its crop spans 95 percent of the column (`SPAN_SHARE`), so a "Full-width tier, not a
  narrow strip" is never shown as a narrow centred box because the lettering rows took the height first; the
  structure report lists that floor as the cue's `min_pt`.
- A floor on its row height, 0.9 x the share x 523.5 pt: "about a third of the page" (also "a full third", "one third"),
  "two thirds of the page", "two fifths of the page", "half the page", "top half of the page", "lower half of the
  page", "a quarter of the page", "a sixth of the page" (halves, thirds, quarters, fifths and sixths, with or without
  "of"), and "about the bottom 40 percent of the page", "45%" or "about 40 percent". A share outside 0 to 1 is ignored.
- No constraint: "inset", "insert", "small", and camera words such as "wide" ("Wide, shot from a distance").

A candidate that pairs a panel which must be alone is dropped, and so is one whose rows cannot all be given their
floors within the page (a row is never taller than twice the height it starts from). The prior structure is kept and
flagged `cues_ok: false` instead; it then ranks last. Each candidate starts from rows in proportion to the prior
heights of its panels and is fitted exactly as above, with each size cue as a floor on its row (`cue_min_pt` and
`cue_met` in the row's report; unlike a probed floor it is not proof, and the row is still judged against the margin).
Candidates are ranked by, in order:

1. every lettered panel's usable-to-needed ratio is at least 1;
2. the page's minimum fill (the share of each slot's area that the placed art covers, so a 3:2 frame that cannot be
   narrowed and sits letterboxed in a tall half-width slot counts for little; a panel with no frame counts as 1);
3. the page's mean fill;
4. the page's minimum lettering ratio.

Fills compare to three places; a tie goes to the prior structure, then to the earlier grouping. With `--probe`, the top
3 candidates of each page are probe-fitted at their own row widths (one shared planner cache), and the best one whose
probe verifies every probed panel is chosen (the verified ones are ranked again on the heights they came back with); if
none does, the best analytic candidate stands and is reported as unverified (`verified: false`). The output's `probe`
section is then the chosen candidates' (`planner_calls` counts all of them). Each page's report gains `structure`: the
chosen row sizes (`chosen`, for example `[1, 2, 2]`), the prior's (`prior`), the chosen `min_fill`, `mean_fill` and
`min_ratio`, `verified` (true, false, or null when nothing asked the planner), `candidates` and `excluded` counts, the
`cues` read from the script, and every scored `alternatives` entry (`structure`, `rows_pt`, `min_fill`, `mean_fill`,
`min_ratio`, `cues_ok`, `verified`, `prior`, `chosen`), best first. With `--structures` the page's "before" numbers
(`ratio_before`, `fill_before`, `fill_width_before`, `min_ratio_before`, a row's `prior_pt`) are the prior layout's own, and a row the prior
did not have has no prior height. The layout file's `fitted_from` gains `"structures": true`, and the report a
`structure_search` summary (`pages_changed`). The fill counts area, not width: a tall two-panel row whose art is
letterboxed top and bottom no longer counts as filled, so it loses to rows that do not letterbox when lettering allows
(before, fill counted the width only, and such a row ranked as perfect). A `strip` cue keeps a panel alone without capping its height.

What these tools do not do:

- They do not judge identity, costume, hands, nooses, anachronisms or composition. Look at
  the contact sheet for those, and still inspect every 300 DPI page render.
- Without `--draw`, `visible_rect` is the whole frame unless the frame has a white letterbox or border,
  or a flat black one (edge rows or columns at least 99.5 percent below 10 in every channel; dark art is
  textured and never qualifies), which is trimmed (plus 2 px). A thin white or cream paper margin with specks or
  a faint line (at least 90 percent of its pixels above 215 in every channel on average, no deeper than 3 percent
  of the frame, ending sharply) is trimmed too, so it is never found as a painted shape; a pale sky runs deeper
  and fades in, so it is kept. Deliberate cropping stays a hand decision; `--draw` applies the cover crop
  described above.
- Shapes must be near-white (every channel above 215), outlined, and at least 0.55 percent of the frame
  (`MIN_AREA_FRACTION`): bright patches of sky or cloth framed by dark edges measured 0.3 to 0.46 percent, and the
  smallest real painted box in the reviewed selections is about three times that. Cream parchment
  boxes are found only where they are light enough; otherwise detection fails cleanly.
- Speech ellipses give a smaller rectangle than a hand measurement, because the tool takes
  a rectangle that is entirely blank, not just the text's ink box. A reserve holding
  several chunks, and the `unreadable` style, remain hand measured; `style` is never set.
- On Codex's accepted Chapter 2 and Chapter 1 v2 selections, detection matched the hand
  measured reserves 90 of 90 times. Fit success is lower, because hand measurements
  are looser: about 54 percent of single-chunk frames at the default inset, 66 percent at
  `--inset 2`.

## Print and acceptance gates

- PDF media and bleed are 441 x 666 points, or 6.125 x 9.25 inches. Trim is
  432 x 648 points, or 6 x 9 inches. The 0.125-inch bleed is top, bottom and
  outside edge; the binding edge has no extra bleed. Trim alternates with folio parity.
- Effective PPI is native pixels divided by the actual image transform size in
  inches. Cropping and aspect fitting are included. PNG DPI tags do not qualify.
- Below 300 PPI, Real-ESRGAN x2plus creates a separate 2x frame and scales every
  source-pixel coordinate, including reserves and sound anchors. Originals remain.
  Upscaling improves pixel density; it is recorded and never described as new
  native imagegen detail. A 2x file left by a build that failed later is reused
  only if it is an exact 2x RGB image that, shrunk back, differs from its source
  by at most 12 levels on average (a real upscale: 3 to 4; another image: about
  70); the action then records `reused_existing_output` and that difference.
  Anything else at that path still stops the build.
- The verifier independently reads PDF graphics matrices and embedded pixels.
  Every RGB image must match its selected source exactly, every placement must
  meet 300 PPI, every scripted chunk must be present on the correct page in order,
  and all used lettering fonts must be embedded.
- Actual glyph rectangles must fit measured reserves and have at least 99 percent
  light native support. A technical pass is followed by direct inspection of all
  300 DPI page renders and independent review of changed art.
- `DPI-REPORT.json`, native-copy checks, placement report, manifest hashes and
  render hashes are emitted. `REVIEW.md` must describe corrections and remaining
  deviations honestly. The author approves the Chapter 1 pilot before subsequent
  chapters enter the generation phase.

The pipeline does not publish, commit, modify a script, or modify old editions.
Existing frames, manifests, PDFs and renders are never overwritten. Use a new
revision and preserve earlier evidence when a frame, reserve or layout needs
revision. The stable `DPI-REPORT.json` delivery pointer is updated only after its
previous bytes have been backed up under `review/`; a versioned report is also kept.

## Checks

```sh
PYTHONDONTWRITEBYTECODE=1 "$V15_PY" -m unittest discover \
  -s output/comic-v15-full-redo/pipeline -p 'test_*.py'
```

The reusable compositor derives its text metrics, aspect-fit policy, symbol drawing
and lettering helpers from the read-only Chapter 1 r3 wrapper. It has no runtime
dependency on the shared V14 compositor or a prior chapter's acceptance state.

All principal descriptions are read from the continuity bible, including labels
with parenthetical chapter notes such as Ibrahim, Thoma, Avraham and Nandini.
Nagoji's full constant identity restrictions are preserved along with the matching
chapter costume row. Future script compatibility checks should call `parse_script`
without running `prepare`, because preparation writes a chapter package.
