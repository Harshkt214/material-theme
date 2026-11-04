import { Composition, staticFile, type CalculateMetadataFunction } from "remotion";
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { Ad } from "./Ad";
import { config, FIXED } from "../config";
import { validateConfig, voPath, captionPath } from "./validate";
import { computeLineStartsMs } from "./captionTiming";
import type { AdProps, CaptionFile, ResolvedScene } from "./types";

const { fps, width, height, endCardSeconds } = FIXED.video;

const loadCaptions = async (path: string): Promise<CaptionFile | null> => {
  try {
    const res = await fetch(staticFile(path));
    if (!res.ok) return null;
    return (await res.json()) as CaptionFile;
  } catch {
    return null;
  }
};

/**
 * Measures every scene's audio and sets the total duration.
 * This only reads local files — it never calls ElevenLabs.
 */
const calculateMetadata: CalculateMetadataFunction<AdProps> = async () => {
  validateConfig(config);

  const scenes: ResolvedScene[] = [];
  for (const scene of config.scenes) {
    const audioPath = voPath(config.mode, scene.id);
    let seconds: number;
    let audio: string | null = audioPath;
    try {
      seconds = await getAudioDurationInSeconds(staticFile(audioPath));
    } catch {
      if (config.mode === "final") {
        throw new Error(
          `FINAL mode: public/${audioPath} is missing. Run \`npm run vo\` first (rendering never calls ElevenLabs).`,
        );
      }
      // Draft without audio: silence, length estimated from the voice text.
      audio = null;
      seconds = Math.max(
        FIXED.draft.minSceneSeconds,
        scene.voiceText.length / FIXED.draft.charsPerSecond,
      );
    }

    const durationInFrames = Math.max(1, Math.ceil(seconds * fps));
    const captions = audio ? await loadCaptions(captionPath(config.mode, scene.id)) : null;
    if (config.mode === "final" && !captions) {
      console.warn(`No captions for "${scene.id}" — run \`npm run captions\`. Using evenly spaced lines.`);
    }
    const lineStartsMs = computeLineStartsMs(
      scene.caption,
      (durationInFrames / fps) * 1000,
      captions?.words ?? null,
    );
    scenes.push({ ...scene, audio, durationInFrames, lineStartsMs });
  }

  const total = scenes.reduce((a, s) => a + s.durationInFrames, 0) + Math.round(endCardSeconds * fps);

  return {
    durationInFrames: total,
    props: { mode: config.mode, scenes, endCard: config.endCard, music: config.music },
  };
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Ad"
    component={Ad}
    width={width}
    height={height}
    fps={fps}
    durationInFrames={fps * 10}
    defaultProps={{ mode: config.mode, scenes: [], endCard: config.endCard, music: config.music }}
    calculateMetadata={calculateMetadata}
  />
);
