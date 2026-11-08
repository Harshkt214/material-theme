// Builds Instagram highlight covers (1080x1920) + a profile preview, Signal File style.
// Run: NODE_PATH=$(npm root -g) node build.js <this folder>
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const dir = process.argv[2];
const fontCss = `
@font-face{font-family:"PF";font-weight:800;src:url("../fonts/playfair-display-latin-800-normal.woff2")}
@font-face{font-family:"Mono";font-weight:700;src:url("../fonts/ibm-plex-mono-latin-700-normal.woff2")}
@font-face{font-family:"Baloo";font-weight:800;src:url("../fonts/baloo-2-latin-800-normal.woff2")}
html,body{margin:0}`;

// icon drawings inside a 400x400 box
const icons = {
  start: { color: "#26d07c", label: "START", svg: `<circle cx="200" cy="200" r="150" fill="none" stroke="#26d07c" stroke-width="22"/><path d="M170 130 L285 200 L170 270 Z" fill="#26d07c"/>` },
  free: { color: "#ffc94a", label: "FREE FILES", svg: `<path d="M110 60 H250 L310 120 V340 H110 Z" fill="none" stroke="#ffc94a" stroke-width="22" stroke-linejoin="round"/><path d="M250 60 V120 H310" fill="none" stroke="#ffc94a" stroke-width="22" stroke-linejoin="round"/><path d="M210 160 V280 M160 235 L210 285 L260 235" fill="none" stroke="#ffc94a" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>` },
  cases: { color: "#ff4d5e", label: "CASE FILES", svg: `<path d="M60 110 H170 L200 145 H340 V320 H60 Z" fill="none" stroke="#ff4d5e" stroke-width="22" stroke-linejoin="round"/><text x="200" y="285" text-anchor="middle" font-family="Mono" font-weight="700" font-size="110" fill="#ff4d5e">#</text>` },
  wyckoff: { color: "#ff8a3d", label: "WYCKOFF", svg: `<g stroke="#ff8a3d" stroke-width="16" stroke-linecap="round"><line x1="110" y1="120" x2="110" y2="330"/><line x1="200" y1="80" x2="200" y2="290"/><line x1="290" y1="50" x2="290" y2="230"/></g><rect x="80" y="170" width="60" height="120" rx="10" fill="#ff8a3d"/><rect x="170" y="120" width="60" height="130" rx="10" fill="#ff8a3d"/><rect x="260" y="80" width="60" height="110" rx="10" fill="#ff8a3d"/>` },
  rules: { color: "#26d07c", label: "RULES", svg: `<rect x="80" y="60" width="240" height="290" rx="26" fill="none" stroke="#26d07c" stroke-width="22"/><g stroke="#26d07c" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M115 135 l20 20 l35 -40"/><path d="M115 215 l20 20 l35 -40"/><path d="M115 295 l20 20 l35 -40"/></g><g stroke="#26d07c" stroke-width="18" stroke-linecap="round"><line x1="200" y1="140" x2="285" y2="140"/><line x1="200" y1="220" x2="285" y2="220"/><line x1="200" y1="300" x2="285" y2="300"/></g>` },
};

const cover = (k) => `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}
body{width:1080px;height:1920px;background:radial-gradient(60% 35% at 50% 50%, #1a2440, #0b0f1a 70%);display:flex;align-items:center;justify-content:center}
.ring{width:720px;height:720px;border-radius:50%;border:4px solid rgba(238,241,248,.14);background:rgba(27,36,64,.55);display:flex;align-items:center;justify-content:center;box-shadow:0 0 120px ${icons[k].color}33}
</style></head><body><div class="ring"><svg width="420" height="420" viewBox="0 0 400 400">${icons[k].svg}</svg></div></body></html>`;

const bio = ["🧠 Pehle dimaag, phir chart", "📊 Trading psychology Hindi mein, SEBI data ke saath", "📒 Free Trading Journal 👇", "⚠️ Educational only, not advice"];
const preview = () => `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}
body{width:1080px;background:#000;color:#f5f5f5;font-family:Inter,sans-serif;padding:50px 44px;box-sizing:border-box}
.top{display:flex;align-items:center;gap:56px}.pp{width:220px;height:220px;border-radius:50%;overflow:hidden;border:4px solid #262626}
.stats{display:flex;gap:60px;font-size:30px;text-align:center}.stats b{display:block;font-size:40px}
.name{font-weight:700;font-size:34px;margin-top:30px}.cat{color:#a8a8a8;font-size:30px;margin-top:6px}
.bio{font-size:32px;line-height:1.45;margin-top:10px;white-space:pre-line}.link{color:#e0f1ff;font-size:30px;margin-top:8px}
.btns{display:flex;gap:16px;margin-top:30px}.btn{flex:1;background:#262626;border-radius:16px;text-align:center;font-weight:700;font-size:30px;padding:20px 0}
.hl{display:flex;gap:34px;margin-top:44px}.h{text-align:center;font-size:24px;width:150px}.h .c{width:146px;height:146px;border-radius:50%;border:4px solid #3a3a3a;overflow:hidden;margin-bottom:12px;background-size:cover;background-position:center}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:44px -44px 0}.grid div{aspect-ratio:9/16;background-size:cover;background-position:center}
.note{font-family:Mono;font-size:22px;color:#777;margin-top:24px;text-align:center}
</style></head><body>
<div class="top"><div class="pp"><img src="../final/tw-profile-1080.png" style="width:100%"></div>
<div class="stats"><div><b>80</b>posts</div><div><b>—</b>followers</div><div><b>—</b>following</div></div></div>
<div class="name">Trading Psychology Hindi | Wizaard</div><div class="cat">Education</div>
<div class="bio">${bio.join("\n")}</div><div class="link">🔗 superprofile.bio/… (freebie link)</div>
<div class="btns"><div class="btn">Follow</div><div class="btn">Message</div></div>
<div class="hl">${Object.keys(icons).map((k) => `<div class="h"><div class="c" style="background-image:url('covers/hl-${k}.png')"></div>${icons[k].label}</div>`).join("")}</div>
<div class="grid">${[1, 2, 3, 4, 5, 6].map((i) => `<div style="background-image:url('thumbs/t${i}.jpg')"></div>`).join("")}</div>
<div class="note">PREVIEW ONLY · @thetradingwizaard · not a real screenshot</div>
</body></html>`;

(async () => {
  fs.mkdirSync(path.join(dir, "covers"), { recursive: true });
  const b = await chromium.launch();
  for (const k of Object.keys(icons)) {
    const f = path.join(dir, `_c_${k}.html`); fs.writeFileSync(f, cover(k));
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
    await p.goto("file://" + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(dir, "covers", `hl-${k}.png`) }); await p.close(); fs.unlinkSync(f);
  }
  const f = path.join(dir, "_preview.html"); fs.writeFileSync(f, preview());
  const p = await b.newPage({ viewport: { width: 1080, height: 1400 } });
  await p.goto("file://" + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(dir, "profile-preview.png"), fullPage: true }); fs.unlinkSync(f);
  await b.close(); console.log("done");
})();
