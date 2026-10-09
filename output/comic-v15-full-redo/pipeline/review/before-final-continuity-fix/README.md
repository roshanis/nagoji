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

1. After the author has approved `scripts/CHAPTER-NN-SCRIPT.md`, prepare it:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 "$V15_PY" "$V15_RUN" prepare --chapter 2
   ```

   This writes only that chapter's package under `chapters/ch02/`. It records
   script, continuity and V13 lock hashes, parses every page and panel, preserves
   quoted caption/dialogue copy exactly, and creates `IMAGEGEN-JOBS.json`.
   Chapter numbering is 1 through 28; page count is unrestricted. The optional
   ninth page in Chapter 1 is included. Inputs are rehashed before generation
   and build. Concurrent script changes stop the run instead of mixing versions.

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
   Captions and speech are supplied solely to plan empty reserves, never to render
   as image lettering. The approved story remains intact where appearance differs.

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

   The pilot uses `--manifest chapters/ch01/SELECTION-INPUT-r1.json` to import
   its copied r3 selections and regenerated candidates. An import must meet the
   same frame hash, prompt hash, reference, visual-review and exact-copy gates.
   Reused originals must be copied into the new package and retain source hashes.

## Print and acceptance gates

- PDF media and bleed are 441 x 666 points, or 6.125 x 9.25 inches. Trim is
  432 x 648 points, or 6 x 9 inches. The 0.125-inch bleed is top, bottom and
  outside edge; the binding edge has no extra bleed. Trim alternates with folio parity.
- Effective PPI is native pixels divided by the actual image transform size in
  inches. Cropping and aspect fitting are included. PNG DPI tags do not qualify.
- Below 300 PPI, Real-ESRGAN x2plus creates a separate 2x frame and scales every
  source-pixel coordinate, including reserves and sound anchors. Originals remain.
  Upscaling improves pixel density; it is recorded and never described as new
  native imagegen detail.
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
