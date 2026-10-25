import sys, random, time, math
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
P='/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/'
sys.path.insert(0, P)
import reserves as rv
import test_reserves as T
from pathlib import Path
path = Path(S+'quiet.png'); T.quiet_frame(busy=()).save(path)
found = rv.find_regions(path, 0)
orig = rv.tail_wedge
R=(.45,.4); SC=.3
random.seed(int(sys.argv[1]))
t0=time.time(); n=0; hits=[]
while time.time()-t0 < float(sys.argv[2]):
    k = random.choice([3,4])
    targets = [(random.randrange(40,1160,10), random.randrange(40,560,10)) for _ in range(k)]
    sizes = [[(random.choice([400,500,600]), random.choice([140,180]))] for _ in range(k)]
    faces = []
    for t in targets:
        faces.append((t[0], t[1]-30, random.choice([45,70]), 'F%d'%len(faces)))
    n+=1
    rv.tail_wedge = orig
    try:
        rv.place_boxes(path, found, sizes, targets, rounded=[R]*k, scale=SC, tail_margin=12, faces=faces)
        continue
    except rv.PlacementError as e:
        pass
    rv.tail_wedge = lambda box, ratio, target, bounds, scale=1.0, head=None, short=False: orig(box, ratio, target, bounds, scale, head, True)
    try:
        res = rv.place_boxes(path, found, sizes, targets, rounded=[R]*k, scale=SC, tail_margin=12, faces=faces)
        hits.append((targets, sizes, faces, res['boxes']))
    except rv.PlacementError:
        pass
print('trials', n, 'hits', len(hits))
for h in hits[:6]: print(h)
