from PIL import Image, ImageDraw, ImageFont
import glob, sys
fr = sorted(glob.glob('frames/f*.png'))
labels = [("0.0s","1 Hook: ₹500 vs ₹3,000"),("3.5s","2 Claim + 40 sec promise"),("5.5s","3 Setup: BUY 200, SL 195"),
 ("9.0s","4 SL hit = sirf ₹500"),("11.0s","5 Bina SL: ₹170, −₹3,000"),("17.0s","6 Reveal: loss ENTRY pe"),
 ("22.0s","7 Psychology: Odean study"),("31.0s","8 Callback: recovery math"),("37.0s","9 2 Rules"),
 ("45.0s","10 Close: plan ka bill"),("49.0s","11 Related video + SUBSCRIBE")]
cols, tw = 4, 420; th = int(tw*1920/1080); pad, lab, top = 24, 90, 110
W = cols*tw + (cols+1)*pad; rows = -(-len(fr)//cols); H = top + rows*(th+lab+pad) + pad
im = Image.new('RGB',(W,H),'#0b0f1a'); d = ImageDraw.Draw(im)
fb = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; fn='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
d.text((pad,36),"S012 Stop Loss Myth · Wizaard Explainer · storyboard v2 (timings estimated, ~53 s)",font=ImageFont.truetype(fb,34),fill='#ffc94a')
for i,f in enumerate(fr):
    r,c = divmod(i,cols); x = pad + c*(tw+pad); y = top + r*(th+lab+pad)
    im.paste(Image.open(f).convert('RGB').resize((tw,th),Image.LANCZOS),(x,y))
    d.text((x,y+th+8),labels[i][0],font=ImageFont.truetype(fb,28),fill='#26d07c')
    d.text((x,y+th+44),labels[i][1],font=ImageFont.truetype(fn,24),fill='#f4f6fb')
im.save('storyboard-v2.png'); print(im.size)
