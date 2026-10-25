import sys, random, math
sys.path.insert(0, '/Users/roshanvenugopal/Documents/github/nagoji/output/comic-v15-full-redo/pipeline')
import reserves as rv
BOUNDS=[0,0,1200,600]; S=.3
random.seed(1)
hits=[]
for _ in range(200000):
    # chunk 0 painted A, chunk 1 painted B (to the right, level, or lower)
    ax0=random.randrange(20,500,10); ay0=random.randrange(20,300,10); aw=random.randrange(200,420,10); ah=random.randrange(60,140,10)
    A=[ax0-8,ay0-8,ax0+aw+8,ay0+ah+8]
    bx0=random.randrange(ax0+aw+30,1000,10); by0=random.randrange(20,400,10); bw=random.randrange(200,300,10); bh=random.randrange(60,140,10)
    if bx0+bw>1180: continue
    B=[bx0-8,by0-8,bx0+bw+8,by0+bh+8]
    t=(random.randrange(20,1180,10), random.randrange(20,580,10))
    if A[0]-12<t[0]<A[2]+12 and A[1]-12<t[1]<A[3]+12: continue
    if B[0]-12<t[0]<B[2]+12 and B[1]-12<t[1]<B[3]+12: continue
    wl=rv.tail_wedge(B,.45,t,BOUNDS,S); ws=rv.tail_wedge(B,.45,t,BOUNDS,S,short=True)
    if wl is None: continue
    if rv.tail_crosses(wl,A) and not rv.tail_crosses(ws,A):
        # margin: how robustly
        hits.append((A,B,t))
print(len(hits))
for h in hits[:15]: print(h)
