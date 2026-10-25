from PIL import Image
import sys
im=Image.open(sys.argv[1]);x0,y0,x1,y1=map(int,sys.argv[2:6]);s=float(sys.argv[6])
c=im.crop((x0,y0,x1,y1));c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS);c.save(sys.argv[7])
