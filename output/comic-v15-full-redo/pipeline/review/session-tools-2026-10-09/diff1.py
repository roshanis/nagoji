import sys, random, time, math
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, P)
import reserves as rv
loader = SourceFileLoader('reserves_old', P+'reserves.py.backup-pre-2026-10-08')
old = module_from_spec(spec_from_loader(loader.name, loader)); loader.exec_module(old)
import test_reserves as T
R=(.45,.4); SC=.3; B=[0,0,1200,600]
random.seed(int(sys.argv[1])); budget=float(sys.argv[2])
t0=time.time(); n=0; stats={'both':0,'old_only':0,'new_only':0,'neither':0,'invalid':0,'short_used':0}
bad=[]
while time.time()-t0 < budget:
    k = random.choice([2,3,4])
    painted = random.random() < .5
    boxes = []
    if painted:
        for j in range(random.choice([1,2])):
            x0=random.randrange(20,800,10); y0=random.randrange(20,450,10)
            boxes.append((x0,y0,x0+random.choice([150,250,350]),y0+random.choice([70,100])))
    path = Path(S+'rnd%d.png' % __import__('os').getpid()); T.frame(boxes=boxes).save(path) if boxes else T.quiet_frame(busy=((0,300,1200,600),)).save(path)
    found = rv.find_regions(path, len(boxes)); found_o = old.find_regions(path, len(boxes))
    targets=[]
    for _ in range(k):
        r_=random.random()
        if r_<.15: targets.append(None)
        elif r_<.3: targets.append(random.choice([(0,random.randrange(50,550)),(1200,random.randrange(50,550)),(random.randrange(50,1150),0),(random.randrange(50,1150),600)]))
        else: targets.append((random.randrange(60,1140,10), random.randrange(60,540,10)))
    sizes=[[(random.choice([300,400,500]), random.choice([100,140])),(260,100)] for _ in range(k)]
    faces=[(t[0], t[1]-30, random.choice([40,60]), 'F%d'%i) for i,t in enumerate(targets) if t is not None and random.random()<.8 and 0<t[0]<1200 and 0<t[1]<600]
    rounded=[R if t is not None else None for t in targets]
    kw=dict(rounded=rounded, scale=SC, tail_margin=12, faces=faces)
    n+=1
    try: ro = old.place_boxes(path, found_o, sizes, targets, **kw)
    except old.PlacementError: ro=None
    try: rn = rv.place_boxes(path, found, sizes, targets, **kw)
    except rv.PlacementError: rn=None
    if ro and rn: stats['both']+=1
    elif ro and not rn: stats['old_only']+=1; bad.append(('old_only',boxes,targets,sizes,faces))
    elif rn and not ro: stats['new_only']+=1
    else: stats['neither']+=1
    if rn:
        if any(rn['short_tail']): stats['short_used']+=1
        # validity of the new result under its own flags (cross + face rules)
        boxes_=rn['boxes']
        for i,t in enumerate(targets):
            if t is None or rounded[i] is None: continue
            w = rv.tail_wedge(boxes_[i], rn['corner'][i], t, B, SC, rv.speaker_head(t, faces), rn['short_tail'][i])
            if w is None: continue
            for j,b in enumerate(boxes_):
                if j!=i and rv.tail_crosses(w,b): stats['invalid']+=1; bad.append(('cross',i,j,boxes,targets,sizes,faces)); break
print(n, stats)
for b in bad[:3]: print(b)
