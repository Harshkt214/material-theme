// usage: node render_video.js <duration_s> [fps] [onlyTimesCsv]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const dir = __dirname, dur = +process.argv[2], fps = +(process.argv[3] || 30);
  const only = process.argv[4] ? process.argv[4].split(',').map(Number) : null;
  const out = path.join(dir, only ? 'snap' : 'vframes'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'video.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  fs.writeFileSync(path.join(dir, 'sfx.json'), JSON.stringify(await p.evaluate(() => window.sfxList)));
  const times = only || Array.from({ length: Math.ceil(dur * fps) }, (_, i) => i / fps);
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => window.seek(t), times[i]);
    await p.screenshot({ path: path.join(out, only ? `s_${times[i].toFixed(2)}.png` : `f${String(i).padStart(5, '0')}.jpg`), ...(only ? {type:'png'} : {type:'jpeg', quality:95}) });
  }
  await b.close();
})();
