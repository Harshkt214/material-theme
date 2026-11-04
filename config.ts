import type { AdConfig } from "./src/types";

/* =====================================================================
 * PER-VIDEO CONTENT — edit this block (and add assets) for each new ad.
 * Paths are relative to public/.
 *
 * Rule: captions and voiceText must only contain real, approved copy.
 * Never put invented claims, numbers or testimonials here.
 * ===================================================================== */
export const config: AdConfig = {
  // "draft": free preview, uses public/vo-draft/<id>.mp3 or silence. Never calls ElevenLabs.
  // "final": uses public/vo/<id>.mp3 created by `npm run vo`.
  mode: "draft",

  // hook -> problem -> solution -> result. Each scene lasts as long as its audio.
  scenes: [
    {
      id: "hook",
      src: "clips/hook.mp4",
      caption: "[HOOK]\nreplace in config.ts",
      voiceText: "Placeholder hook line. Replace this text in config dot t s.",
    },
    {
      id: "problem",
      src: "clips/problem.png",
      caption: "[PROBLEM]\nreplace in config.ts",
      voiceText: "Placeholder problem line goes here.",
    },
    {
      id: "solution",
      src: "clips/solution.mp4",
      caption: "[SOLUTION]\nreplace in config.ts",
      voiceText: "Placeholder solution line goes here.",
    },
    {
      id: "result",
      src: "clips/result.png",
      caption: "[RESULT]\nreplace in config.ts",
      voiceText: "Placeholder result line goes here.",
    },
  ],

  endCard: {
    logo: "brand/logo.svg",
    productImage: "brand/product.svg",
    tagline: "Your tagline here",
    instagram: "@yourbrand",
    x: "@yourbrand",
  },

  music: "music/placeholder-pad.mp3",
};

/* =====================================================================
 * FIXED BRAND SETTINGS — identical across every video. Do not change
 * per video; change only if the whole brand style changes.
 * ===================================================================== */
export const FIXED = {
  video: { width: 1080, height: 1920, fps: 24, endCardSeconds: 2 },
  fonts: {
    // Loaded from Google Fonts via @remotion/google-fonts (see src/fonts.ts).
    caption: "Montserrat",
    captionWeight: 900,
    captionSize: 78,
    captionStroke: 14,
    endCard: "Montserrat",
  },
  colors: {
    captionText: "#FFFFFF",
    captionStroke: "#000000",
    endCardBackground: "#FFFFFF",
    endCardText: "#111111",
    endCardMuted: "#555555",
    backgroundDim: "rgba(0,0,0,0.25)",
  },
  layout: {
    // Caption block top edge (px from top) and the box the scene clip is centered in.
    captionTop: 230,
    clipBox: { top: 560, height: 1100, sidePadding: 0 },
    backgroundBlurPx: 60,
  },
  audio: {
    voiceVolume: 1.0,
    musicVolume: 0.43,
    sfxVolume: 0.6,
  },
  voice: {
    // ElevenLabs voice used for every ad. Set once (find the ID in ElevenLabs > Voices).
    voiceId: "REPLACE_WITH_ELEVENLABS_VOICE_ID",
    // Flash is the default (about 0.5 credits per character).
    modelId: "eleven_flash_v2_5",
    voiceSettings: { stability: 0.5, similarity_boost: 0.75, style: 0, use_speaker_boost: true },
    outputFormat: "mp3_44100_128",
  },
  draft: {
    // Used to estimate a scene's length when no draft audio exists (silence).
    charsPerSecond: 15,
    minSceneSeconds: 1.2,
  },
  credits: {
    // Credits charged per character, by model. Unknown models fall back to 1.0.
    perCharByModel: {
      eleven_flash_v2_5: 0.5,
      eleven_flash_v2: 0.5,
      eleven_turbo_v2_5: 0.5,
      eleven_turbo_v2: 0.5,
      eleven_multilingual_v2: 1,
      eleven_v3: 1,
    } as Record<string, number>,
    // Ask for confirmation above this many credits in one run.
    confirmAbove: 500,
    // A 10 s ad is ~150-200 characters. Warn above this.
    typicalMaxChars: 250,
  },
  whisper: {
    version: "1.5.5",
    model: "base.en" as const,
    folder: "whisper.cpp",
  },
} as const;
