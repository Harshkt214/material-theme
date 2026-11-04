// Shared types for config.ts, the Remotion composition and the scripts.

export type Mode = "draft" | "final";

export type Scene = {
  /** Unique, file-safe id (a-z, 0-9, - and _). Audio files are named after it: vo/<id>.mp3 */
  id: string;
  /** Clip or image inside public/, e.g. "clips/hook.mp4" or "clips/result.jpg" */
  src: string;
  /** On-screen caption. Each "\n" starts a new line; every line fades in on its own. */
  caption: string;
  /** Exactly what the voice says. This is the only text sent to ElevenLabs. */
  voiceText: string;
  /** Optional licence-free sound effect inside public/, played when the scene starts. Log it in assets-licences.md. */
  sfx?: string;
};

export type EndCard = {
  logo: string;
  productImage: string;
  tagline: string;
  instagram: string;
  x: string;
  /** Optional licence-free sound effect played when the end card appears. */
  sfx?: string;
};

export type AdConfig = {
  mode: Mode;
  scenes: Scene[];
  endCard: EndCard;
  /** Licence-free music bed inside public/. Mixed at FIXED.audio.musicVolume. */
  music: string;
};

/** Word timings produced by scripts/generate-captions.ts (local Whisper). */
export type CaptionWord = { text: string; startMs: number; endMs: number };
export type CaptionFile = {
  sceneId: string;
  audioFile: string;
  audioSha256: string;
  words: CaptionWord[];
};

/** Everything the composition needs after calculateMetadata has measured the audio. */
export type ResolvedScene = Scene & {
  durationInFrames: number;
  /** Audio path inside public/, or null when a draft scene has no audio (silent, estimated length). */
  audio: string | null;
  /** Start time of each caption line in ms from scene start. */
  lineStartsMs: number[];
};

export type AdProps = {
  mode: Mode;
  scenes: ResolvedScene[];
  endCard: EndCard;
  music: string;
};
