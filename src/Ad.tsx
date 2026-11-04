import { AbsoluteFill, Audio, interpolate, Sequence, staticFile, useVideoConfig } from "remotion";
import { FIXED } from "../config";
import { BlurredBackground } from "./components/BlurredBackground";
import { SceneClip } from "./components/SceneClip";
import { Caption } from "./components/Caption";
import { EndCard } from "./components/EndCard";
import type { AdProps } from "./types";

/**
 * Main composition. Pure rendering of local files — no network calls to ElevenLabs.
 * Timeline: scene 1 .. scene N (each as long as its voice audio), then the end card.
 */
export const Ad: React.FC<AdProps> = ({ scenes, endCard, music }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const a = FIXED.audio;
  const endCardFrames = Math.round(FIXED.video.endCardSeconds * fps);
  const fadeOut = Math.round(fps * 0.5);

  let from = 0;
  const timed = scenes.map((s) => {
    const start = from;
    from += s.durationInFrames;
    return { ...s, start };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {timed.map((s) => (
        <Sequence key={s.id} from={s.start} durationInFrames={s.durationInFrames} name={s.id}>
          <BlurredBackground src={s.src} />
          <SceneClip src={s.src} />
          <Caption caption={s.caption} lineStartsMs={s.lineStartsMs} />
          {s.audio ? <Audio src={staticFile(s.audio)} volume={a.voiceVolume} /> : null}
          {s.sfx ? <Audio src={staticFile(s.sfx)} volume={a.sfxVolume} /> : null}
        </Sequence>
      ))}

      <Sequence from={from} durationInFrames={endCardFrames} name="end-card">
        <EndCard data={endCard} />
        {endCard.sfx ? <Audio src={staticFile(endCard.sfx)} volume={a.sfxVolume} /> : null}
      </Sequence>

      {music ? (
        <Audio
          src={staticFile(music)}
          loop
          volume={(f) =>
            a.musicVolume *
            interpolate(f, [durationInFrames - fadeOut, durationInFrames], [1, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          }
        />
      ) : null}
    </AbsoluteFill>
  );
};
