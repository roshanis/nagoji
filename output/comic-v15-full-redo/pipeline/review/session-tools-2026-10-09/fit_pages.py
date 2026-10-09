"""Chunked fit-layout --structures --probe: run run_chapter._structure_page (the same worker the parallel fit uses) for
some pages and save each page's result as soon as it is done, so long chapters can be fitted in pieces that each finish
inside a time limit. fit_merge.py assembles the pieces exactly as run_chapter.structure_fit does.

Each page also keeps a persistent cache of planner answers (page-NN-probe-cache.jsonl): a page cut off by the time
limit reuses every probe it already made when it is run again. The planner is deterministic, and a cached answer still
counts as a planner call, so the layout, report and planner_calls are the same as an uninterrupted run.
Usage: fit_pages.py CH PKGDIR MANIFEST DECISIONS FACES_DIR LAYOUT_IN OUT_DIR PAGES(comma) JOBS [KEEP_MAX]"""
import sys, json, concurrent.futures, multiprocessing
from pathlib import Path
sys.path.insert(0, 'pipeline')
import run_chapter as rc, layout_fit as lf


def cached_page(page_no, page, prior, inputs, tails_dir, margin, cache_path, keep_max=None):
    """Spawn worker: run_chapter._structure_page with SlotProbe.fits backed by an append-only answer cache on disk."""
    disk = {}
    path = Path(cache_path)
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                key, answer = json.loads(line)
            except ValueError:
                continue                                   # a line cut short when the last run was stopped
            disk[tuple(key)] = answer
    original = rc.SlotProbe.fits
    log = path.open('a')

    def fits(self, panel_id, width_pt, height_pt):
        key = (panel_id, round(width_pt, 3), round(height_pt, 3))
        if key not in self.cache and key in disk:
            self.calls += 1                                # counted as the uninterrupted run would count it
            self.cache[key] = disk[key]
        if key in self.cache:
            return self.cache[key]
        answer = original(self, panel_id, width_pt, height_pt)
        log.write(json.dumps([list(key), answer]) + '\n'); log.flush()
        return answer

    rc.SlotProbe.fits = fits
    try:
        return rc._structure_page(page_no, page, prior, inputs, tails_dir, margin, True, keep_max)
    finally:
        rc.SlotProbe.fits = original; log.close()


def main():
    ch, pkg, manifest, dec, faces_dir, layout_in, out_dir, pages, jobs = sys.argv[1:10]
    keep_max = float(sys.argv[10]) if len(sys.argv) > 10 else None     # fit-layout --keep-max
    rc.UNPAINTED = True
    out = rc.package(int(ch), Path(pkg)); job = rc.load_job(out); script = rc.lettered_script(Path(job['script']['path']))
    prior = json.loads(Path(layout_in).read_text())['page_rows']
    inputs = rc.fit_inputs(out, Path(manifest), Path(dec), Path(faces_dir), rc.FACE_SCALE, script)
    od = Path(out_dir); od.mkdir(parents=True, exist_ok=True)
    todo = [p for p in pages.split(',') if p and not (od / f'page-{int(p):02d}.json').exists()]
    if not todo:
        print('nothing to do'); return
    key = lambda p: next(k for k in script['pages'] if str(k) == str(p))
    with concurrent.futures.ProcessPoolExecutor(max_workers=max(1, min(int(jobs), len(todo))),
                                                mp_context=multiprocessing.get_context('spawn')) as pool:
        futs = {pool.submit(cached_page, str(p), script['pages'][key(p)], prior.get(str(p)), inputs, faces_dir, lf.MARGIN,
                            str(od / f'page-{int(p):02d}-probe-cache.jsonl'), keep_max): p for p in todo}
        for fut in concurrent.futures.as_completed(futs):
            p = futs[fut]; rows, page, probed, calls = fut.result()
            (od / f'page-{int(p):02d}.json').write_text(json.dumps({'page': str(p), 'rows': rows, 'report': page, 'calls': calls,
                'probed': [[k[0], list(k[1]), v] for k, v in probed.items()]}))
            print('done page', p, 'calls', calls, flush=True)


if __name__ == '__main__':
    main()
