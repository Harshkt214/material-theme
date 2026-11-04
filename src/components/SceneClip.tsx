import { AbsoluteFill, Img, OffthreadVideo, staticFile } from "remotion";
import { FIXED } from "../../config";
import { isVideo } from "../media";

/** The sharp scene clip, centered at its natural aspect ratio. */
export const SceneClip: React.FC<{ src: string }> = ({ src }) => {
  const { top, height, sidePadding } = FIXED.layout.clipBox;
  const style: React.CSSProperties = { width: "100%", height: "100%", objectFit: "contain" };
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top,
          left: sidePadding,
          right: sidePadding,
          height,
        }}
      >
        {isVideo(src) ? (
          <OffthreadVideo src={staticFile(src)} muted style={style} />
        ) : (
          <Img src={staticFile(src)} style={style} />
        )}
      </div>
    </AbsoluteFill>
  );
};
