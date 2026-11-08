"""Builds reels/freebies/<kw>/cover.html (1080x1080) for each freebie. Render with Playwright screenshot 1080x1080.
usage: python3 cover.py <kw>   (kw lowercase)"""
import sys, os, html
C = {
 "rules": dict(kicker="FREE TEMPLATE · PDF (PRINT)", title='Mere Trading <span style="color:#26d07c">Rules</span>', badge="FREE",
   head=["#", "RULE", "EXAMPLE"], rows=[("1","Risk / trade","1% capital"),("5","Max trades","3 / din"),("6","Daily max loss","Band karo"),("8","Averaging down",'<span style="color:#ff4d5e">Kabhi nahi</span>')],
   last="10 dabbe · khud bharo · print karo"),
 "zone": dict(kicker="FREE 1-PAGE PDF · BOOK NOTES", title='Trading in the Zone: <span style="color:#ffc94a">5 Truths</span>', badge="FREE",
   head=["#", "TRUTH", ""], rows=[("1","Kuch bhi ho sakta hai",""),("2","Aage jaanna zaroori nahi",""),("3","Win-loss random bante hain",""),("4","Edge = probability","")],
   last="+ 7 principles · Mark Douglas ki book se"),
 "checklist": dict(kicker="FREE 1-PAGE PDF · TRADE SE PEHLE", title='Pre-Trade <span style="color:#26d07c">Checklist</span>', badge="FREE",
   head=["", "SAWAAL", ""], rows=[("☐","Mera setup hai?",""),("☐","SL tay aur broker mein?",""),("☐","Risk ₹ accept hai?",""),("☐","Gussa / FOMO to nahi?","")],
   last="10 sawaal · 1 bhi Nahi = trade nahi"),
 "review": dict(kicker="FREE TEMPLATE · PDF · HAR SUNDAY", title='Weekly <span style="color:#ffc94a">Review</span>', badge="FREE",
   head=["", "IS HAFTE", ""], rows=[("✓","Best decision",""),("✗",'<span style="color:#ff4d5e">Worst decision</span>',""),("A/C","A-game vs C-game",""),("→",'<span style="color:#26d07c">Agle hafte 1 sudhaar</span>',"")],
   last="4 hafte + mahine ka top 3"),
 "galti": dict(kicker="FREE PDF · BRAIN VS MARKET", title='Raju ki <span style="color:#ff4d5e">10 Galtiyan</span>', badge="FREE",
   head=["#", "GALTI", "FIX"], rows=[("1","Loss mein SL khiskana","SL broker mein"),("2","Profit jaldi, loss hold","Avg win vs loss"),("3","Averaging down","Add nahi"),("4","Overtrading","Max trades")],
   last="Galti · kaise pehchano · fix"),
 "challenge": dict(kicker="FREE FILE · GOOGLE SHEETS / EXCEL", title='20-Trade <span style="color:#ffc94a">Challenge</span>', badge="FREE",
   head=["#", "SETUP SAME?", "R"], rows=[("1","Haan",'<span style="color:#26d07c">+2.0R</span>'),("2","Haan",'<span style="color:#ff4d5e">-1.0R</span>'),("3","Haan",'<span style="color:#ff4d5e">-1.0R</span>'),("…","20 tak","")],
   last="Win rate · Avg R · Total R apne aap"),
 "risk": dict(kicker="FREE FILE · GOOGLE SHEETS / EXCEL", title='Risk + Position <span style="color:#26d07c">Size</span>', badge="FREE",
   head=["", "DAALO", ""], rows=[("₹","Capital · Risk %",""),("→","Entry · Stop loss",""),("=",'<span style="color:#ffc94a">Quantity</span>',""),("=",'<span style="color:#ffc94a">Lots</span>',"")],
   last="+ drawdown recovery table"),
 "routine": dict(kicker="FREE 1-PAGE PDF · MARKET SE PEHLE", title='Pre-Market <span style="color:#26d07c">Routine</span>', badge="10 MIN",
   head=["MIN", "STEP", ""], rows=[("1","Mann ki halat",""),("2","News + events",""),("2","Levels mark karo",""),("1",'<span style="color:#26d07c">Dheemi saans</span>',"")],
   last="8 steps · roz same order"),
}
kw = sys.argv[1]; c = C[kw]
rows = "".join(f'<div class="row"><div>{a}</div><div>{b}</div><div>{d}</div></div>' for a, b, d in c["rows"])
h = c["head"]
out = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(../../brand/fonts/playfair-display-latin-800-normal.woff2)}}
@font-face{{font-family:B;src:url(../../brand/fonts/baloo-2-latin-800-normal.woff2)}}
@font-face{{font-family:M;src:url(../../brand/fonts/ibm-plex-mono-latin-700-normal.woff2)}}
body{{margin:0;width:1080px;height:1080px;background:#0b0f1a;color:#eef1f8;font-family:Inter,sans-serif;position:relative;overflow:hidden}}
.g{{position:absolute;inset:0;background-image:linear-gradient(rgba(238,241,248,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(238,241,248,.05) 2px,transparent 2px);background-size:60px 60px}}
.m{{font-family:M;letter-spacing:.12em;color:#ffc94a;font-size:28px;position:absolute;left:90px;top:90px}}
h1{{font-family:P;font-size:104px;line-height:1.02;margin:0;position:absolute;left:90px;top:145px;width:900px}}
.card{{position:absolute;left:90px;top:480px;width:900px;height:370px;background:rgba(27,36,64,.7);border:2px solid rgba(238,241,248,.14);border-radius:32px;overflow:hidden}}
.row{{display:flex;font-size:32px;font-weight:700;padding:0 36px;height:62px;align-items:center;border-bottom:2px solid rgba(238,241,248,.08)}}
.row div:nth-child(1){{width:90px;color:#8d97ad}}.row div:nth-child(2){{flex:1}}.row div:nth-child(3){{text-align:right}}
.h{{color:#8d97ad;font-family:M;font-size:22px}}
.last{{padding:0 36px;height:58px;display:flex;align-items:center;color:#ffc94a;font-size:28px;font-weight:700}}
.free{{position:absolute;right:90px;top:418px;background:#26d07c;color:#0b0f1a;font-family:B;font-size:44px;padding:4px 30px;border-radius:40px;transform:rotate(-4deg)}}
.foot{{position:absolute;left:90px;right:90px;top:900px;display:flex;align-items:center;gap:24px;font-size:34px;font-weight:800}}
.foot img{{width:90px;height:90px;border-radius:50%}}
.foot span{{margin-left:auto;font-size:22px;font-weight:600;color:#8d97ad}}
</style></head><body><div class="g"></div>
<div class="m">{c["kicker"]}</div>
<h1>{c["title"]}</h1>
<div class="free">{c["badge"]}</div>
<div class="card"><div class="row h"><div>{h[0]}</div><div>{h[1]}</div><div>{h[2]}</div></div>{rows}<div class="last">{c["last"]}</div></div>
<div class="foot"><img src="../../brand/final/tw-icon.svg">@thetradingwizaard<span>Educational only, not advice</span></div>
</body></html>'''
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", kw)
os.makedirs(d, exist_ok=True)
open(os.path.join(d, "cover.html"), "w").write(out)
print("ok", kw)
