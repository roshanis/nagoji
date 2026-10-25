from PIL import Image,ImageDraw;import json,sys
im=Image.open(sys.argv[1]).convert('RGB');W,H=im.size;d=ImageDraw.Draw(im)
for f in json.loads(sys.argv[2]):
    d.ellipse([f['x']*W-f['r']*H,f['y']*H-f['r']*H,f['x']*W+f['r']*H,f['y']*H+f['r']*H],outline=(255,0,0),width=max(3,H//200))
im.save(sys.argv[3])
if len(sys.argv)>4:
    for i,f in enumerate(json.loads(sys.argv[2])):
        cx,cy,r=f['x']*W,f['y']*H,f['r']*H
        im.crop((int(cx-2*r),int(cy-2*r),int(cx+2*r),int(cy+2*r))).resize((600,600)).save(sys.argv[3].replace('.png',f'-z{i}.png'))
