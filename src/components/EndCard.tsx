import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { FIXED } from "../../config";
import { fontFamily } from "../fonts";
import type { EndCard as EndCardData } from "../types";

const InstagramIcon: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2}>
    <rect x="3" y="3" width="18" height="18" rx="5" />
    <circle cx="12" cy="12" r="4" />
    <circle cx="17.5" cy="6.5" r="1" fill={color} stroke="none" />
  </svg>
);

const XIcon: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2.4} strokeLinecap="round">
    <path d="M4 4 L20 20 M20 4 L4 20" />
  </svg>
);

/** White end card: logo, product image, tagline and two social handles. */
export const EndCard: React.FC<{ data: EndCardData }> = ({ data }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c = FIXED.colors;
  const pop = spring({ frame, fps, config: { damping: 14 } });
  const fade = (from: number) =>
    interpolate(frame, [from, from + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: c.endCardBackground,
        alignItems: "center",
        justifyContent: "center",
        fontFamily,
        color: c.endCardText,
        opacity: fade(0),
      }}
    >
      <Img src={staticFile(data.logo)} style={{ position: "absolute", top: 170, height: 150, objectFit: "contain" }} />
      <Img
        src={staticFile(data.productImage)}
        style={{
          width: 760,
          height: 860,
          objectFit: "contain",
          marginTop: -40,
          transform: `scale(${0.9 + 0.1 * pop})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: 430,
          left: 80,
          right: 80,
          textAlign: "center",
          fontSize: 68,
          fontWeight: 800,
          lineHeight: 1.15,
          opacity: fade(4),
        }}
      >
        {data.tagline}
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 220,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 22,
          fontSize: 46,
          fontWeight: 600,
          color: c.endCardMuted,
          opacity: fade(8),
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <InstagramIcon size={46} color={c.endCardMuted} />
          {data.instagram}
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <XIcon size={40} color={c.endCardMuted} />
          {data.x}
        </div>
      </div>
    </AbsoluteFill>
  );
};
