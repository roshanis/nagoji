from PIL import Image,ImageDraw;import sys
im=Image.open(sys.argv[1]).convert('RGB')
x0,y0,x1,y1=map(int,sys.argv[2].split(','));s=int(sys.argv[3]);step=int(sys.argv[5]) if len(sys.argv)>5 else 10
c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.LANCZOS);d=ImageDraw.Draw(c)
for x in range((x0//step+1)*step,x1,step):
    d.line([((x-x0)*s,0),((x-x0)*s,c.height)],fill=(0,255,255) if x%50 else (255,0,255),width=1)
    if x%50==0: d.text(((x-x0)*s+2,2),str(x),fill=(255,0,255))
for y in range((y0//step+1)*step,y1,step):
    d.line([(0,(y-y0)*s),(c.width,(y-y0)*s)],fill=(0,255,255) if y%50 else (255,0,255),width=1)
    if y%50==0: d.text((2,(y-y0)*s+2),str(y),fill=(255,0,255))
c.save(sys.argv[4])
