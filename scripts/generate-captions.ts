/**
 * npm run captions — word timings from the voice audio with LOCAL whisper.cpp.
 *
 * Caption TEXT still comes only from config.ts; Whisper only tells us WHEN each
 * caption line is spoken so it can fade in on time.
 *
 * Uses public/vo/<id>.mp3 in final mode (public/vo-draft/<id>.mp3 in draft mode).
 * Writes public/captions/<mode>/<id>.json. Skips scenes whose audio hasn't changed.
 * Free and offline after the first run (whisper.cpp + model are downloaded once).
 */
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { downloadWhisperModel, installWhisperCpp, toCaptions, transcribe } from "@remotion/install-whisper-cpp";
import { config, FIXED } from "../config";
import { captionPath, validateConfig, voPath } from "../src/validate";
import type { CaptionFile } from "../src/types";

const ROOT = process.cwd();
const sha256File = (p: string) => createHash("sha256").update(readFileSync(p)).digest("hex");

const toWav16k = (input: string, output: string) => {
  // Remotion ships its own ffmpeg, so no system install is needed.
  execFileSync("npx", ["remotion", "ffmpeg", "-y", "-loglevel", "error", "-i", input, "-ar", "16000", "-ac", "1", output], {
    stdio: "inherit",
    shell: process.platform === "win32",
  });
};

const main = async () => {
  validateConfig(config);
  const mode = config.mode;

  const pending: { id: string; audio: string; hash: string; out: string }[] = [];
  for (const s of config.scenes) {
    const rel = voPath(mode, s.id);
    const audio = join(ROOT, "public", rel);
    if (!existsSync(audio)) {
      if (mode === "final") throw new Error(`public/${rel} is missing. Run \`npm run vo\` first.`);
      console.log(`skip ${s.id}: no draft audio (captions will be evenly spaced)`);
      continue;
    }
    const out = join(ROOT, "public", captionPath(mode, s.id));
    const hash = sha256File(audio);
    if (existsSync(out)) {
      const prev = JSON.parse(readFileSync(out, "utf8")) as CaptionFile;
      if (prev.audioSha256 === hash) {
        console.log(`cached ${s.id}`);
        continue;
      }
    }
    pending.push({ id: s.id, audio, hash, out });
  }

  if (pending.length === 0) {
    console.log("Captions up to date.");
    return;
  }

  const whisperPath = resolve(ROOT, FIXED.whisper.folder);
  await installWhisperCpp({ to: whisperPath, version: FIXED.whisper.version, printOutput: true });
  await downloadWhisperModel({ model: FIXED.whisper.model, folder: whisperPath, printOutput: true });

  const tmp = join(ROOT, ".tmp-whisper");
  mkdirSync(tmp, { recursive: true });
  mkdirSync(join(ROOT, "public", "captions", mode), { recursive: true });

  try {
    for (const p of pending) {
      process.stdout.write(`Transcribing ${p.id} ... `);
      const wav = join(tmp, `${p.id}.wav`);
      toWav16k(p.audio, wav);
      const result = await transcribe({
        inputPath: wav,
        whisperPath,
        whisperCppVersion: FIXED.whisper.version,
        model: FIXED.whisper.model,
        tokenLevelTimestamps: true,
        splitOnWord: true,
        printOutput: false,
      });
      const { captions } = toCaptions({ whisperCppOutput: result });
      const file: CaptionFile = {
        sceneId: p.id,
        audioFile: voPath(mode, p.id),
        audioSha256: p.hash,
        words: captions.map((c) => ({ text: c.text.trim(), startMs: c.startMs, endMs: c.endMs })),
      };
      writeFileSync(p.out, JSON.stringify(file, null, 2) + "\n");
      console.log(`done (${file.words.length} words)`);
    }
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
};

main().catch((e) => {
  console.error(`\n${e instanceof Error ? e.message : e}`);
  process.exit(1);
});
