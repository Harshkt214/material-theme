// Render index.html → renders/<name>.mp4 without the hyperframes CLI.
// Video: seek the GSAP timeline frame by frame in Playwright, pipe PNGs to ffmpeg.
// Audio: every <audio class="clip"> is placed at data-start (trimmed to data-duration,
// scaled by data-volume), mixed, then loudnorm to -14 LUFS / -1.5 dBTP.
// Usage (from any dir with playwright available): node render.cjs [outName]
const { chromium } = require("playwright");
const { spawn, execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const dir = __dirname;
const FPS = 30;
const name = process.argv[2] || path.basename(dir);
fs.mkdirSync(path.join(dir, "renders"), { recursive: true });
const silent = path.join(dir, "renders", ".video.mp4");
const out = path.join(dir, "renders", name + ".mp4");

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto("file://" + path.join(dir, "index.html"), { waitUntil: "domcontentloaded" });
  await p.waitForTimeout(2500);
  const { dur, clips } = await p.evaluate(() => {
    const root = document.getElementById("root");
    const clips = [...document.querySelectorAll("audio.clip")].map((a) => ({
      src: a.getAttribute("src"), start: +a.dataset.start, dur: a.dataset.duration ? +a.dataset.duration : null, vol: a.dataset.volume ? +a.dataset.volume : 1,
    }));
    return { dur: +root.dataset.duration, clips };
  });
  const frames = Math.round(dur * FPS);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", silent], { stdio: ["pipe", "inherit", "inherit"] });
  for (let i = 0; i < frames; i++) {
    await p.evaluate((t) => { window.__timelines.main.seek(t, false); }, i / FPS);
    const buf = await p.screenshot({ type: "png" });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % 150 === 0) console.log(`frame ${i}/${frames}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
  await b.close();

  // Audio mix
  const args = ["-y", "-loglevel", "error", "-i", silent];
  const filters = [];
  clips.forEach((c, i) => {
    args.push("-i", path.join(dir, c.src));
    const trim = c.dur ? `atrim=0:${c.dur},` : "";
    const ms = Math.round(c.start * 1000);
    filters.push(`[${i + 1}:a]${trim}volume=${c.vol},adelay=${ms}|${ms},aformat=channel_layouts=stereo[a${i}]`);
  });
  if (clips.length) {
    filters.push(`${clips.map((_, i) => `[a${i}]`).join("")}amix=inputs=${clips.length}:normalize=0,apad,atrim=0:${dur},loudnorm=I=-14:TP=-1.5:LRA=11[aout]`);
    args.push("-filter_complex", filters.join(";"), "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", out);
  } else {
    args.push("-c", "copy", out);
  }
  execFileSync("ffmpeg", args, { stdio: "inherit" });
  fs.unlinkSync(silent);
  console.log("done", out);
})();
