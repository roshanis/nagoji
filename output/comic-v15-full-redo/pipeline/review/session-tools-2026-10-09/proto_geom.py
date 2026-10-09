"""Run auto-geometry for one panel with the prototype placer (scratch proto/reserves.py), writing to a scratch file.
Usage (from output/comic-v15-full-redo): proto_geom.py CH PKG GEOMDIR STEM LAYOUT OUT.json [--real]"""
import sys
from pathlib import Path
S = Path(__file__).resolve().parent
ch, pkg, gdir, stem, layout, out = sys.argv[1:7]
if '--real' not in sys.argv: sys.path.insert(0, str(S / 'proto'))
sys.path.insert(1, 'pipeline')
import run_chapter
g = Path(gdir)
argv = ['auto-geometry', '--package-dir', f'chapters/{pkg}', '--chapter', ch, '--candidate', f'chapters/{pkg}/candidates/{stem}.json',
        '--geometry-out', out, '--draw', '--tails', str(g / f'{stem}-tails.json'), '--layout', layout, '--unpainted']
for kind in ('faces', 'keep', 'styles'):
    f = g / f'{stem}-{kind}.json'
    if f.exists(): argv += [f'--{kind}', str(f)]
run_chapter.main(argv)
