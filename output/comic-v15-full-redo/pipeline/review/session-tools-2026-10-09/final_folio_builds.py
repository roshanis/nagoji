"""Folio-only builds at the imposition plan's first folios, each chapter from its final b-pass manifest and solved layout,
under the next free revision. Prints one line per chapter and writes the final builds map (package:revision:b tag).
Usage (from output/comic-v15-full-redo): final_folio_builds.py IMPOSITION.json SOURCES.json OUT_MAP.json CH [CH ...]
SOURCES.json: {"3": ["ch03", "s12t-b", "LAYOUT-fitted-s12.json"], ...}; OUT_MAP gains (or keeps) an entry per chapter."""
import json, re, subprocess, sys
from pathlib import Path
PY = '/Users/roshanvenugopal/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
plan = {r['chapter']: r for r in json.loads(Path(sys.argv[1]).read_text())['chapters']}
src, out = json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3])
final = json.loads(out.read_text()) if out.exists() else {}
for ch in map(int, sys.argv[4:]):
    pkg, btag, layout = src[str(ch)]
    p = Path('chapters') / pkg
    used = list((p / 'review').glob('RENDERS-r*.json')) + list((p / 'pdf').glob('*-r*.pdf')) + list(p.glob('SELECTION-MANIFEST-r*.json')) \
        + [d for d in (p / 'renders').glob('r*') if d.is_dir()]      # a failed build can leave any of these behind
    revs = [int(m[1]) for f in used for m in [re.search(r'-?r(\d+)(\.json|\.pdf)?$', f.name)] if m]
    rev = f'r{max(revs, default=0) + 1}'
    cmd = [PY, 'pipeline/run_chapter.py', 'build', '--chapter', str(ch), '--manifest', str(p / f'SELECTION-INPUT-{btag}.json'),
           '--layout', str(p / layout), '--first-folio', str(plan[ch]['first_folio']), '--revision', rev]
    if pkg not in (f'ch{ch:02d}', f'ch{ch}'): cmd[3:3] = ['--package-dir', str(p)]     # before --chapter, not between it and its value
    r = subprocess.run(cmd, capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin', 'TMPDIR': '/tmp/claude-501'})
    ppi = re.search(r'"minimum_ppi": ([0-9.]+)', r.stdout)
    if r.returncode or not ppi:
        print(f'ch{ch} {pkg} {rev} at {plan[ch]["first_folio"]}: FAILED', (r.stderr or r.stdout).strip().splitlines()[-1:]); continue
    final[str(ch)] = f'{pkg}:{rev}:{btag}'; out.write_text(json.dumps(final, indent=1))
    print(f'ch{ch} {pkg} {rev} at {plan[ch]["first_folio"]}: min {float(ppi[1]):.1f} PPI', flush=True)
