/**
 * npm run vo — create the final voiceover, one mp3 per scene, with ElevenLabs TTS.
 *
 * Credit safety:
 *  - Only runs in FINAL mode (draft mode never calls ElevenLabs).
 *  - Only generates a scene when public/vo/<id>.mp3 is missing or its voiceText changed
 *    (sha256 of voiceText stored in vo-cache.json).
 *  - Prints characters + estimated credits BEFORE any call.
 *  - Asks for confirmation if one run exceeds FIXED.credits.confirmAbove (500).
 *
 * Flags:
 *   --dry-run        print the estimate only, never call the API
 *   --force <id>     regenerate one scene even if cached (repeatable)
 */
import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { createInterface } from "node:readline/promises";
import { config as loadEnv } from "dotenv";
import { config, FIXED } from "../config";
import { validateConfig, voPath } from "../src/validate";

type CacheEntry = { voiceTextSha256: string; chars: number; voiceId: string; modelId: string; generatedAt: string };
type Cache = Record<string, CacheEntry>;

const ROOT = process.cwd();
const CACHE_FILE = join(ROOT, "vo-cache.json");

const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const forced = new Set<string>();
args.forEach((a, i) => {
  if (a === "--force" && args[i + 1]) forced.add(args[i + 1]);
});

const sha256 = (s: string) => createHash("sha256").update(s, "utf8").digest("hex");

const readCache = (): Cache => (existsSync(CACHE_FILE) ? JSON.parse(readFileSync(CACHE_FILE, "utf8")) : {});
const writeCache = (c: Cache) => writeFileSync(CACHE_FILE, JSON.stringify(c, null, 2) + "\n");

const main = async () => {
  validateConfig(config);

  if (config.mode !== "final") {
    console.log('config.mode is "draft" — ElevenLabs is not called in draft mode.');
    console.log('When the script is frozen, set mode: "final" in config.ts and run `npm run vo` again.');
    process.exit(1);
  }

  const { voiceId, modelId, voiceSettings, outputFormat } = FIXED.voice;
  const perChar = FIXED.credits.perCharByModel[modelId] ?? 1;
  const cache = readCache();

  for (const id of forced) {
    if (!config.scenes.some((s) => s.id === id)) throw new Error(`--force: no scene with id "${id}"`);
  }

  // Decide what needs generating.
  const todo: { id: string; text: string; reason: string }[] = [];
  for (const s of config.scenes) {
    const file = join(ROOT, "public", voPath("final", s.id));
    const hash = sha256(s.voiceText);
    const entry = cache[s.id];
    let reason: string | null = null;
    if (forced.has(s.id)) reason = "forced";
    else if (!existsSync(file)) reason = "audio missing";
    else if (!entry || entry.voiceTextSha256 !== hash) reason = "voiceText changed";
    if (reason) todo.push({ id: s.id, text: s.voiceText, reason });
  }

  const totalScriptChars = config.scenes.reduce((a, s) => a + s.voiceText.length, 0);

  console.log(`Model: ${modelId} (~${perChar} credit/char)`);
  console.log(`Whole script: ${totalScriptChars} characters across ${config.scenes.length} scenes.`);
  for (const s of config.scenes) {
    const t = todo.find((x) => x.id === s.id);
    console.log(`  ${t ? "GENERATE" : "cached  "}  ${s.id.padEnd(12)} ${String(s.voiceText.length).padStart(4)} chars${t ? `  (${t.reason})` : ""}`);
  }

  if (todo.length === 0) {
    console.log("Nothing to generate — 0 credits. All scenes are cached.");
    return;
  }

  const chars = todo.reduce((a, t) => a + t.text.length, 0);
  const credits = Math.ceil(chars * perChar);
  console.log(`\nThis run: ${chars} characters ≈ ${credits} credits.`);

  if (totalScriptChars > FIXED.credits.typicalMaxChars) {
    console.log(
      `\nWARNING: the script is ${totalScriptChars} characters. A 10-second ad is usually 150-200. ` +
        "It will likely run longer than 10 s and cost more than expected. Consider trimming voiceText.",
    );
  }

  if (dryRun) {
    console.log("\n--dry-run: no API calls made.");
    return;
  }

  if (voiceId.startsWith("REPLACE_")) {
    throw new Error("Set FIXED.voice.voiceId in config.ts to your ElevenLabs voice ID first.");
  }

  loadEnv();
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) throw new Error("ELEVENLABS_API_KEY is not set. Put it in .env (see .env.example).");

  if (credits > FIXED.credits.confirmAbove) {
    if (!process.stdin.isTTY) {
      throw new Error(`Run would cost ~${credits} credits (> ${FIXED.credits.confirmAbove}). Re-run in an interactive terminal to confirm.`);
    }
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    const answer = await rl.question(
      `\nThis run exceeds ${FIXED.credits.confirmAbove} credits (~${credits}). Type "yes" to continue: `,
    );
    rl.close();
    if (answer.trim().toLowerCase() !== "yes") {
      console.log("Cancelled. No credits spent.");
      process.exit(1);
    }
  }

  mkdirSync(join(ROOT, "public", "vo"), { recursive: true });

  for (const t of todo) {
    process.stdout.write(`Generating ${t.id} ... `);
    const url = `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}?output_format=${outputFormat}`;
    const res = await fetch(url, {
      method: "POST",
      headers: { "xi-api-key": apiKey, "Content-Type": "application/json", Accept: "audio/mpeg" },
      body: JSON.stringify({ text: t.text, model_id: modelId, voice_settings: voiceSettings }),
    });
    if (!res.ok) {
      const body = (await res.text()).slice(0, 500);
      throw new Error(`ElevenLabs error ${res.status} for "${t.id}": ${body}`);
    }
    const buf = Buffer.from(await res.arrayBuffer());
    writeFileSync(join(ROOT, "public", voPath("final", t.id)), buf);
    // Save the cache after every scene so a later failure never causes a paid retake.
    cache[t.id] = {
      voiceTextSha256: sha256(t.text),
      chars: t.text.length,
      voiceId,
      modelId,
      generatedAt: new Date().toISOString(),
    };
    writeCache(cache);
    console.log(`done (${(buf.length / 1024).toFixed(0)} KB)`);
  }

  console.log(`\nDone. Generated ${todo.length} file(s) in public/vo/.`);
};

main().catch((e) => {
  console.error(`\n${e instanceof Error ? e.message : e}`);
  process.exit(1);
});
