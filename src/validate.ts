import type { AdConfig } from "./types";

const ID_RE = /^[a-z0-9_-]+$/;

/** Throws a readable error if config.ts is malformed. Used by the composition and the scripts. */
export const validateConfig = (config: AdConfig): void => {
  if (config.mode !== "draft" && config.mode !== "final") {
    throw new Error(`config.mode must be "draft" or "final", got "${config.mode}"`);
  }
  if (config.scenes.length === 0) {
    throw new Error("config.scenes is empty");
  }
  const seen = new Set<string>();
  for (const s of config.scenes) {
    if (!ID_RE.test(s.id)) {
      throw new Error(`Scene id "${s.id}" must only use a-z, 0-9, "-" and "_" (it becomes a filename).`);
    }
    if (seen.has(s.id)) throw new Error(`Duplicate scene id "${s.id}"`);
    seen.add(s.id);
    if (!s.voiceText.trim()) throw new Error(`Scene "${s.id}" has empty voiceText`);
    if (!s.src.trim()) throw new Error(`Scene "${s.id}" has empty src`);
  }
};

export const voPath = (mode: AdConfig["mode"], id: string) =>
  mode === "final" ? `vo/${id}.mp3` : `vo-draft/${id}.mp3`;

export const captionPath = (mode: AdConfig["mode"], id: string) => `captions/${mode}/${id}.json`;
