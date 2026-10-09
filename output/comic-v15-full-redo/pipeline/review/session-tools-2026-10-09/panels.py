import sys, numpy as np
from PIL import Image
def runs(b):
    out=[];start=None
    for i,v in enumerate(b):
        if v and start is None: start=i
        if not v and start is not None: out.append((start,i-1)); start=None
    if start is not None: out.append((start,len(b)-1))
    return out
for p in sys.argv[1:]:
    a=np.asarray(Image.open(p).convert('RGB')).astype(int)
    paper=a[30,30]
    m=(np.abs(a-paper).sum(axis=2)>45)
    # ignore title region and page number: restrict y from 330 to 2560
    H,W=m.shape
    rowsum=m[:, :].sum(axis=1)
    bands=[r for r in runs(rowsum>200) if r[1]-r[0]>40]
    print(p.split('/')[-1])
    for (y0,y1) in bands:
        colsum=m[y0:y1+1].sum(axis=0)
        cols=[c for c in runs(colsum>(y1-y0)*0.3) if c[1]-c[0]>40]
        # per column refine y extents
        segs=[]
        for (x0,x1) in cols:
            rs=m[y0:y1+1,x0:x1+1].sum(axis=1)
            rr=[r for r in runs(rs>(x1-x0)*0.3)]
            segs.append((x0,x1,y0+rr[0][0],y0+rr[-1][1]) if rr else (x0,x1,y0,y1))
        print('  band',y0,y1,'panels',segs)
