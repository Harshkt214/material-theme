from PIL import Image, ImageDraw, ImageFont
ts=['0.00','3.40','5.60','9.00','13.50','19.50','22.80','30.50','36.50','41.60','44.50','51.20','54.20']
labels=["1 Hook: red candle pe SELL, SL hit","2 Hook (contd)","3 'Ye luck nahi tha' + 40 sec",
"4 Master Candle","5 High-Low = Box","6 4+ candles andar (1-2-3-4)","7 Jaldbaazi = SL hit",
"8 Breakout body 60%+ upar","9 Confirm -> BUY, SL box ke neeche","10 Wick = Trap vs Body = Breakout",
"11 Callback: wo SELL box ke andar tha","12 Cheat sheet (save)","13 SUBSCRIBE end card"]
cols,tw=5,380; th=int(tw*1920/1080); pad,lab,top=24,90,110
W=cols*tw+(cols+1)*pad; rows=-(-len(ts)//cols); H=top+rows*(th+lab+pad)+pad
im=Image.new('RGB',(W,H),'#0b0f1a'); d=ImageDraw.Draw(im)
fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; fn='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
d.text((pad,36),"Master Candle Breakout · Wizaard Explainer · storyboard v1 (timings estimated, ~54 s)",font=ImageFont.truetype(fb,32),fill='#ffc94a')
for i,t in enumerate(ts):
    r,c=divmod(i,cols); x=pad+c*(tw+pad); y=top+r*(th+lab+pad)
    im.paste(Image.open(f'snap/s_{t}.png').convert('RGB').resize((tw,th),Image.LANCZOS),(x,y))
    d.text((x,y+th+8),f"{float(t):.1f}s",font=ImageFont.truetype(fb,26),fill='#26d07c')
    d.text((x,y+th+44),labels[i],font=ImageFont.truetype(fn,20),fill='#f4f6fb')
im.save('storyboard/storyboard-v1.png'); print(im.size)
