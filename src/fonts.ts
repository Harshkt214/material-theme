import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Fixed brand font, bundled locally (public/fonts, SIL OFL 1.1) so every
// render looks identical and works offline.
export const fontFamily = "Montserrat";

loadFont({
  family: fontFamily,
  url: staticFile("fonts/Montserrat-Variable.ttf"),
  weight: "100 900",
  format: "truetype",
});
