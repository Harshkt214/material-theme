"""Builds galti.html (2-page A4) from the 10 mistakes below. Text source: Trading Psychology Content Bank,
Season 2 (videos 9-16) + Season 3 videos 19-20 (FOMO, revenge). Render: Playwright page.pdf."""
G = [
 ("Loss mein SL door khiskana", "Loss aversion",
  "Price SL ke paas aaye aur tum SL thoda aur door kar do, \"bas thoda saans lene do\".",
  "SL entry se pehle tay karo aur broker mein lagao. Loss mein SL kabhi door nahi.",
  "Tversky &amp; Kahneman (1992): loss ka dard barabar jeet ki khushi se lagbhag do guna (ek estimate; naye studies kam batate hain)."),
 ("Profit jaldi book, loss hold", "Disposition effect",
  "Journal mein average win chhota aur average loss bada. Profit mein darr, loss mein umeed.",
  "Last 10 trades ka average win vs average loss nikalo. Exit entry se pehle likho.",
  "Odean (1998): log profit wale shares jaldi bechte hain, loss wale pakad kar rakhte hain."),
 ("Averaging down", "Loser mein add karna",
  "Position loss mein hai aur tum \"average kam karne\" ke liye aur kharid lete ho.",
  "Rule likho: loss wali position mein kabhi add nahi. Add sirf profit wali mein, plan se.",
  "Tom Hougaard, <i>Best Loser Wins</i> (2022)."),
 ("Zyada trade, zyada kharcha", "Overconfidence · overtrading",
  "Din ke trades ginti se bahar. Bina setup ke bhi click, \"ek aur try\".",
  "Ek din ki max trade limit tay karo (jaise 3) aur use rules mein likho.",
  "Barber &amp; Odean (2000), ek US study (1991-96): sabse zyada trade karne wale households ko 11.4% saalana mila, market ne 17.9% diya."),
 ("Sirf apne favour ke saboot", "Confirmation bias",
  "Bullish ho to har chart bullish dikhta hai. Ulta signal \"noise\" lagta hai.",
  "Har trade se pehle ek reason likho jo trade ke KHILAAF ho.",
  "Daniel Kahneman, <i>Thinking, Fast and Slow</i> (2011)."),
 ("Last 3 trades se system badalna", "Recency bias",
  "3 loss ke baad perfect setup bhi skip, ya naya indicator dhoondna.",
  "Agle 20 trades ka sample tay karo. Beech mein system mat badlo.",
  "Kahneman (2011); Mark Douglas, <i>Trading in the Zone</i> (2000)."),
 ("\"Mujhe pata tha!\"", "Hindsight bias",
  "Chart ke baad sab obvious lagta hai, aur apni skill zyada lagti hai.",
  "Trade se PEHLE plan likho. Baad mein plan se compare karo, yaad se nahi.",
  "Kahneman (2011)."),
 ("\"Bas mera paisa wapas aa jaaye\"", "Loss mein risk lena · hope",
  "Break-even ka intezaar. Loss badhta hai par position band nahi hoti.",
  "Har open loss par poocho: \"Ye trade aaj naya hota to leta?\" Nahi = band karo.",
  "Kahneman (2011); Hougaard (2022)."),
 ("Bhaagti candle ke peeche bhaagna", "FOMO",
  "Breakout nikal gaya, tum top par kood gaye. Late entry, bada SL.",
  "Rule: candle bhaag gayi to chase nahi. Pullback ka wait, ya agla setup.",
  "Jared Tendler, <i>The Mental Game of Trading</i> (2021)."),
 ("Market se badla", "Revenge trading",
  "Loss ke turant baad naya trade, aksar bade size mein, gusse mein.",
  "Har loss ke baad 15 minute screen band. Daily max loss pe din khatam.",
  "Tendler (2021)."),
]
card = lambda i, g: f'''<div class="g box"><div class="top"><div class="n">{i}</div><div class="tt"><div class="name">{g[0]}</div><div class="bias">{g[1]}</div></div><div class="me"><i></i>maine bhi ki</div></div>
<div class="cols"><div><b class="p">KAISE PEHCHANO</b>{g[2]}</div><div><b class="f">FIX</b>{g[3]}</div></div><div class="src">Source: {g[4]}</div></div>'''
pages = []
for p in range(2):
    cards = "".join(card(p*5+i+1, G[p*5+i]) for i in range(5))
    if p == 0:
        band = '''<div class="band" style="padding-bottom:7mm"><img class="logo" src="../../brand/final/tw-icon.svg">
<div class="kicker">FREE PDF · KEYWORD GALTI · DIMAAG VS MARKET</div>
<h1>Raju ki <span style="color:#ff4d5e">10 Galtiyan</span></h1>
<div class="sub"><span class="raju">R</span>Raju har naya retail trader hai. Shayad tum bhi. Har galti ka asli naam, kaise pehchano, aur fix. Jo galti tumne bhi ki hai, uska dabba tick karo.</div></div>'''
    else:
        band = '''<div class="band" style="padding-bottom:6mm"><img class="logo" src="../../brand/final/tw-icon.svg">
<div class="kicker">RAJU KI 10 GALTIYAN · PAGE 2</div><h1 style="font-size:22pt">Galti <span style="color:#ff4d5e">6 se 10</span></h1></div>'''
    extra = '' if p == 0 else '''<div class="score"><div class="punch">Tumhara score: ____ / 10</div><p>Jitne tick, utni galtiyan pakdi gayi. Sabse badi wali chuno aur sirf usi ka fix is hafte lagao. Ek galti, ek hafta.</p></div>'''
    pages.append(f'''<section class="page">{band}<div class="body" style="padding-top:4mm">{cards}{extra}</div>
<div class="foot"><span><b>@thetradingwizaard</b> · Raju ki 10 Galtiyan · page {p+1}/2</span><span>Educational only, not advice</span></div></section>''')
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Raju ki 10 Galtiyan</title>
<link rel="stylesheet" href="../_shared/pdf.css"><style>
.raju{{display:inline-flex;align-items:center;justify-content:center;width:7mm;height:7mm;border-radius:50%;background:#ff8a3d;color:#0b0f1a;font-family:B;font-size:12pt;margin-right:2mm;vertical-align:middle}}
.g{{padding:3mm 4mm 2.4mm;margin-bottom:2.8mm}}
.top{{display:flex;align-items:center;gap:3mm}}
.n{{flex:none;width:9mm;height:9mm;border-radius:2mm;background:#0b0f1a;color:#ff4d5e;font-family:B;font-size:13pt;display:flex;align-items:center;justify-content:center}}
.tt{{flex:1}}.name{{font-weight:800;font-size:11.5pt}}
.bias{{font-family:M;font-size:7.5pt;letter-spacing:.08em;color:#ff8a3d;text-transform:uppercase}}
.me{{display:flex;align-items:center;gap:1.5mm;font-family:M;font-size:7pt;color:var(--mute)}}
.me i{{width:5mm;height:5mm;border:1.6px solid #ff4d5e;border-radius:1mm;display:inline-block}}
.cols{{display:flex;gap:4mm;margin-top:2mm;font-size:8.8pt;line-height:1.42}}
.cols>div{{flex:1}}
.cols b{{display:block;font-family:M;font-size:7pt;letter-spacing:.1em;margin-bottom:.6mm}}
.cols .p{{color:#d63447}}.cols .f{{color:#178a52}}
.g .src{{margin-top:1.6mm;border-top:1px dashed var(--line);padding-top:1.2mm}}
.score{{margin-top:3mm;background:#0b0f1a;color:#eef1f8;border-radius:3mm;padding:3.5mm 5mm}}
.score .punch{{color:#ffc94a}}.score p{{margin:1mm 0 0;font-size:9pt;color:#c9cfdd}}
</style></head><body>{"".join(pages)}</body></html>'''
open("galti.html", "w").write(html)
print("ok")
