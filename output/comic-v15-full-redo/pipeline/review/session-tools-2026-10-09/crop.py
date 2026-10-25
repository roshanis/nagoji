from PIL import Image,ImageDraw;import sys
im=Image.open(sys.argv[1]).convert('RGB');x0,y0,x1,y1=map(int,sys.argv[2].split(','));s=int(sys.argv[4])
c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s));d=ImageDraw.Draw(c)
step=int(sys.argv[5])
for x in range((x0//step+1)*step,x1,step): d.line([((x-x0)*s,0),((x-x0)*s,c.size[1])],fill=(0,255,0)); d.text(((x-x0)*s+2,2),str(x),fill=(0,255,0))
for y in range((y0//step+1)*step,y1,step): d.line([(0,(y-y0)*s),(c.size[0],(y-y0)*s)],fill=(0,255,0)); d.text((2,(y-y0)*s+2),str(y),fill=(0,255,0))
c.save(sys.argv[3])
