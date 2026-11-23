const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'frames.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  for (let i = 1; i <= 11; i++) {
    await p.evaluate(n => window.show(n), i);
    await p.waitForTimeout(80);
    await p.screenshot({ path: path.join(dir, 'frames', `f${String(i).padStart(2, '0')}.png`) });
  }
  await b.close();
})();
