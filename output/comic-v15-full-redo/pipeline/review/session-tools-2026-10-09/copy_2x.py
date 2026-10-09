"""Carry print upscales (frames/<stem>-2x.png) into a split package so its build does not upscale again. Follows a
chain of import maps (old stem -> new stem, as written by the split import step) from the first package to the last,
and copies each 2x file that exists anywhere along the chain to the last package under the frame's final stem,
never overwriting. The compositor still checks every reused file against its source (compositor REUSE_MAX_MEAN_DIFF).
Usage: copy_2x.py PKG0 MAP01 PKG1 [MAP12 PKG2 ...]   (package dirs and IMPORT-MAP json files, in order)"""
import json, shutil, sys
from pathlib import Path
args = sys.argv[1:]
pkgs, maps = [Path(a) for a in args[0::2]], [json.loads(Path(a).read_text()) for a in args[1::2]]
dst = pkgs[-1] / 'frames'; n = 0
for i, mp in enumerate(maps):                       # stems first seen in package i, followed to the last package
    for stem in mp:
        final = stem
        for later in maps[i:]:
            final = later.get(final)
            if final is None: break
        if final is None: continue
        src = pkgs[i] / 'frames' / f'{stem}-2x.png'
        out = dst / f'{final}-2x.png'
        if src.is_file() and not out.exists():
            shutil.copyfile(src, out); n += 1
print(n, '2x files carried into', dst)
