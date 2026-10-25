from PIL import Image
import sys
# usage: zoom.py src out scale x0,y0,x1,y1 ...  (fractions of W and H)
src,out,scale=sys.argv[1],sys.argv[2],float(sys.argv[3])
im=Image.open(src);W,H=im.size
tiles=[]
for c in sys.argv[4:]:
    x0,y0,x1,y1=map(float,c.split(','))
    cr=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
    cr=cr.resize((int(cr.width*scale),int(cr.height*scale)))
    tiles.append(cr)
tw=sum(t.width for t in tiles)+10*(len(tiles)-1); th=max(t.height for t in tiles)
o=Image.new('RGB',(tw,th),'white');x=0
for t in tiles: o.paste(t,(x,0)); x+=t.width+10
o.save(out)
