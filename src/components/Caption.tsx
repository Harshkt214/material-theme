import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { FIXED } from "../../config";
import { fontFamily } from "../fonts";
import { splitCaptionLines } from "../captionTiming";

const FADE_FRAMES = 6;

/** Bold white captions with a black outline. Each line fades in at its own start time. */
export const Caption: React.FC<{ caption: string; lineStartsMs: number[] }> = ({
  caption,
  lineStartsMs,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const lines = splitCaptionLines(caption);
  const f = FIXED.fonts;
  const c = FIXED.colors;

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top: FIXED.layout.captionTop,
          left: 60,
          right: 60,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 6,
          textAlign: "center",
        }}
      >
        {lines.map((line, i) => {
          const start = Math.round(((lineStartsMs[i] ?? 0) / 1000) * fps);
          const t = interpolate(frame, [start, start + FADE_FRAMES], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <div
              key={i}
              style={{
                fontFamily,
                fontWeight: f.captionWeight,
                fontSize: f.captionSize,
                lineHeight: 1.12,
                color: c.captionText,
                WebkitTextStroke: `${f.captionStroke}px ${c.captionStroke}`,
                paintOrder: "stroke fill",
                opacity: t,
                transform: `translateY(${(1 - t) * 14}px)`,
              }}
            >
              {line}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
