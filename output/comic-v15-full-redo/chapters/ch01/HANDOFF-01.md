# V15 Chapter 1 pilot handoff

Requested scope is Chapter 1 correction plus reusable per-chapter pipeline.
Writes are limited to this chapter package and ../../pipeline/, with one final
append to the root build log. Old editions, scripts and manuscripts are read-only.

Built-in imagegen is working directly. No Codex companion tool is exposed and
the managed sandbox cannot be disabled. No fallback model or API was used.

Art generation is complete or integrating for all pages. Page 3-4 agent is
finishing review/art-p03-p04.json. Other ledgers exist. Final refinements include
panel 1.3 r2 (flush stud), 2.4 r2, 5.3 r2 (plain black Duarte neckline), and
9.4 r2 (flush stud). Keep earlier candidates as production history.

Pipeline entry: ../../pipeline/run_chapter.py. Parser and compositor are generic;
the pilot importer adapts r3 rows and per-agent ledgers. It retains measured r3
viewports for malformed dictionary-reserve imports. Root reserve corrections
for 7.2 and 9.4 are in review/ROOT-RESERVE-REPAIRS-r1.json.

Runtime Python:
/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python
It has Pillow, ReportLab, pypdf and NumPy, but not fitz. Poppler is bundled.
The new PDF verifier reads actual pypdf graphics matrices and RGB streams.

Remaining work: complete pilot import; all-frame copy and pixel preflight;
automatic 2x upscale where below 300 PPI; create nine-page PDF and 300 DPI renders;
root and independent rendered-page review; source hash recheck; write REVIEW.md,
final evidence and one build-log entry. No final PDF or acceptance claim yet.

Thirteen focused pipeline tests currently pass. The original r3 DPI failures
were independently reproduced with the new placement math. Correction reviews
found an actual remaining white tab in 5.3 r1 and it was regenerated as r2.
An initial independent noose concern on 5.1 was rechecked and withdrawn: the
selected art has straight rope ends with stopper knots, with no open loops.
