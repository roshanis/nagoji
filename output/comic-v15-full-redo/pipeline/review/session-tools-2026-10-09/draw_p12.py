from PIL import Image,ImageDraw;import json,sys
im=Image.open(sys.argv[1]).convert('RGB');W,H=im.size;d=ImageDraw.Draw(im)
for f in json.loads(sys.argv[2]):
    d.ellipse([f['x']*W-f['r']*H,f['y']*H-f['r']*H,f['x']*W+f['r']*H,f['y']*H+f['r']*H],outline=(255,0,0),width=max(3,H//200))
im.save(sys.argv[3])
