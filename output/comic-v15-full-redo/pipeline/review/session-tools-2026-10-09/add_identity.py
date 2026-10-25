"""Append the 2026-10-08 identity paragraph to every correction whose panel shows Nagoji or Varma.
Usage: add_identity.py PACKAGE FIXES_IN.json FIXES_OUT.json   (run from output/comic-v15-full-redo)"""
import json, sys
from pathlib import Path
pkg, fin, fout = sys.argv[1:4]
job = json.loads((Path('chapters') / pkg / 'IMAGEGEN-JOBS.json').read_text()); ch = int(job['chapter'])
cast = {j['id']: j['cast'] for j in job['jobs']}
NAGOJI = ("Nagoji has a THICK, bushy curled handlebar moustache, thick curly black hair, one tiny flat gold stud flush on the earlobe "
          "with nothing hanging from it, a clean-shaven chin and a bare forehead with no mark; never pearls")
VARMA = ("Marthanda Varma has a THIN, neatly waxed moustache with sharp upturned points, straight sleek jet-black hair that is never "
         "curly and never grey, the white Vaishnavite namam with a red centre line on his forehead, a pearl drop hanging from each "
         "earlobe and a clean-shaven chin; when bare-headed his hair is combed sleek into one small knot on the left side of his head "
         "just above the left ear, never on the crown or at the back")
d = json.loads(Path(fin).read_text()); n = 0
for f in d['fixes']:
    who = cast.get(f['id'], [])
    parts = ([NAGOJI] if 'nagoji' in who else []) + ([VARMA] if 'varma' in who and ch <= 27 else [])
    if not parts: continue
    tail = (' The two men must never look alike.' if len(parts) == 2 else '')
    f['correction'] = f['correction'].rstrip() + ' IDENTITY (follow the attached sheets): ' + '. '.join(parts) + '.' + tail
    n += 1
for f in d['fixes']:
    for dash in ('—', '–'): assert dash not in f['correction'], f['id']
Path(fout).open('x').write(json.dumps(d, indent=1, ensure_ascii=False))
print(pkg, len(d['fixes']), 'fixes;', n, 'given the identity paragraph')
