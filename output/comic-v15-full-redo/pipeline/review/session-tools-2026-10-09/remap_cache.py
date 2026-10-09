"""Carry solve_page probe caches across a page split: every cached planner answer [[panel id, width, height], fits]
in OLD_DIR's page-NN-probe-cache.jsonl files is rewritten with the panel's new id (IDMAP from split_pages.py) and
appended to NEW_DIR's cache for the panel's new page. Valid only when the frames, faces, tails and keep zones are
the same in both packages (an import-frame split). Usage: remap_cache.py OLD_DIR NEW_DIR IDMAP.json"""
import json, sys
from pathlib import Path
old, new, idmap = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text())
new.mkdir(parents=True, exist_ok=True)
out, n = {}, 0
for f in sorted(old.glob('page-*-probe-cache.jsonl')):
    for line in f.read_text().splitlines():
        try:
            (pid, w, h), v = json.loads(line)
        except ValueError:
            continue
        nid = idmap.get(pid)
        if not nid:
            continue
        out.setdefault(int(nid[5:7]), []).append(json.dumps([[nid, w, h], v])); n += 1
for page, lines in out.items():
    with (new / f'page-{page:02d}-probe-cache.jsonl').open('a') as fh:
        fh.write('\n'.join(lines) + '\n')
print(n, 'answers carried into', len(out), 'pages')
