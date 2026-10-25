from PIL import Image,ImageDraw;import json,sys
im=Image.open(sys.argv[1]).convert('RGB');W,H=im.size;d=ImageDraw.Draw(im)
fs=json.loads(sys.argv[2])
for f in fs:
    d.ellipse([f['x']*W-f['r']*H,f['y']*H-f['r']*H,f['x']*W+f['r']*H,f['y']*H+f['r']*H],outline=(255,0,0),width=max(3,H//300))
im.save(sys.argv[3]+'.png')
for i,f in enumerate(fs):
    cx,cy,r=f['x']*W,f['y']*H,f['r']*H
    b=[int(cx-2*r),int(cy-2*r),int(cx+2*r),int(cy+2*r)]
    c=im.crop(b); s=480/c.width; c=c.resize((480,int(c.height*s))); c.save(sys.argv[3]+f'-z{i}.png')
