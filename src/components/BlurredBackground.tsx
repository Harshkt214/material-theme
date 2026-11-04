import { AbsoluteFill, Img, OffthreadVideo, staticFile } from "remotion";
import { FIXED } from "../../config";
import { isVideo } from "../media";

/** The scene clip scaled to fill the frame and heavily blurred. */
export const BlurredBackground: React.FC<{ src: string }> = ({ src }) => {
  const style: React.CSSProperties = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    // Scale up so the blur never shows soft edges.
    transform: "scale(1.25)",
    filter: `blur(${FIXED.layout.backgroundBlurPx}px)`,
  };
  return (
    <AbsoluteFill style={{ backgroundColor: "#000", overflow: "hidden" }}>
      {isVideo(src) ? (
        <OffthreadVideo src={staticFile(src)} muted style={style} />
      ) : (
        <Img src={staticFile(src)} style={style} />
      )}
      <AbsoluteFill style={{ backgroundColor: FIXED.colors.backgroundDim }} />
    </AbsoluteFill>
  );
};
