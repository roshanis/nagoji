"""Normalise zone-file versions written as full frame stems ('page-08-panel-02-v02') to 'v02', in place, for zone
files this session just wrote. Usage: norm_versions.py FILE [FILE ...]"""
import json, re, sys
for f in sys.argv[1:]:
    d = json.load(open(f)); n = 0
    for p in d['panels']:
        m = re.fullmatch(r'.*-(v\d+)', str(p.get('version', '')))
        if m and p['version'] != m[1]: p['version'] = m[1]; n += 1
    json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
    print(f, 'normalised', n)
