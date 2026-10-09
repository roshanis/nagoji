import sys, math, itertools, random
from unittest import mock
S='/private/tmp/claude-501/-Users-roshanvenugopal-Documents-github-nagoji/5c3fc8e7-1cfa-40f2-9ebb-05a9d514337c/scratchpad/'
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline/')
import reserves as rv, test_reserves as T
from pathlib import Path
R=(.45,.4); SC=.3; B=[0,0,1200,600]
K=(820,330,40,'K'); mouth=(820,345)
random.seed(5)
hits=[]
regions = [(150,280,450,360),(150,60,450,140),(300,60,500,130)]
for ri, region in enumerate(regions):
    path = Path(S+'r%d.png'%ri); T.frame(boxes=[region]).save(path)
    found = rv.find_regions(path, 1)
    for vx in range(560, 800, 20):
        for vy in range(20, 200, 20):
            V=(vx,vy,40,'V'); faces=[K,V]
            for sizes in ([(330,90),(520,110)], [(330,90),(420,110)], [(330,90),(600,130)]):
                res={}
                ok=True
                for name,sz in (('a',[sizes[0]]),('b',[sizes[1]]),('ab',sizes)):
                    try:
                        res[name]=rv.place_boxes(path, found, [sz], [mouth], faces=faces, scale=SC, tail_margin=12, rounded=[R])
                    except rv.PlacementError:
                        res[name]=None
                # want: a only with short, b with long, ab picks size index 1 with long
                if res['a'] and res['a']['short_tail']==[True] and res['b'] and res['b']['short_tail']==[False] and res['ab'] and res['ab']['choice']==[1] and res['ab']['short_tail']==[False]:
                    hits.append((region, V, sizes, res['a']['boxes'], res['b']['boxes']))
print(len(hits))
for h in hits[:12]: print(h)
