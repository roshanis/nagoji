import json, sys, collections
src, dst = sys.argv[1:3]
r = json.load(open(src))['result']
with open(dst, 'x') as f: json.dump(r, f, indent=1)
conf = r['confirmed']
sev = lambda x: (x.get('verdict') or {}).get('severity') or x['severity']
print('keys', list(r.keys()), '| confirmed', len(conf), collections.Counter(sev(x) for x in conf))
for x in sorted(conf, key=lambda x: (['blocker', 'major', 'minor'].index(sev(x)) if sev(x) in ('blocker', 'major', 'minor') else 3, x['page'])):
    if sev(x) in ('blocker', 'major'):
        print(f"[{sev(x)}] p{x['page']} {x.get('panel')} ({x.get('lens')}): {x['description'][:230]}")
