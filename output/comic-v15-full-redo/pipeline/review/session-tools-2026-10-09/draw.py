from PIL import Image,ImageDraw;import json,sys
im=Image.open(sys.argv[1]).convert('RGB');W,H=im.size;d=ImageDraw.Draw(im)
for f in json.loads(sys.argv[2]):
    d.ellipse([f['x']*W-f['r']*H,f['y']*H-f['r']*H,f['x']*W+f['r']*H,f['y']*H+f['r']*H],outline=(255,0,0),width=max(2,H//400))
if len(sys.argv)>4:
    x0,y0,x1,y1=map(int,sys.argv[4].split(','))
    im=im.crop((x0,y0,x1,y1))
    s=int(sys.argv[5]) if len(sys.argv)>5 else 1
    im=im.resize((im.width*s,im.height*s),Image.LANCZOS)
im.save(sys.argv[3])
