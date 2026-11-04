import type { CaptionWord } from "./types";

/**
 * Caption TEXT always comes from config.ts. Whisper is only used for TIMING:
 * each caption line fades in when its first words are spoken.
 *
 * If a line can't be matched in the transcript (or there is no transcript,
 * e.g. draft mode with silence), lines are spread evenly over the scene.
 */

const norm = (w: string) =>
  w
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^\p{L}\p{N}]+/gu, "");

const wordsOf = (s: string) => s.split(/\s+/).map(norm).filter(Boolean);

export const splitCaptionLines = (caption: string) =>
  caption
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);

export const computeLineStartsMs = (
  caption: string,
  sceneMs: number,
  transcript: CaptionWord[] | null,
): number[] => {
  const lines = splitCaptionLines(caption);
  const n = lines.length;
  const even = lines.map((_, i) => Math.round((i * sceneMs) / Math.max(n, 1) * 0.85));
  if (!transcript || transcript.length === 0) return even;

  const tWords = transcript
    .map((w) => ({ ...w, n: norm(w.text) }))
    .filter((w) => w.n.length > 0);

  const found: (number | null)[] = [];
  let cursor = 0;
  for (const line of lines) {
    const lw = wordsOf(line);
    let hit: number | null = null;
    if (lw.length > 0) {
      // Look for the first 1-2 words of the line, in order, after the previous match.
      for (let k = cursor; k < tWords.length; k++) {
        if (tWords[k].n !== lw[0]) continue;
        if (lw.length > 1 && k + 1 < tWords.length && tWords[k + 1].n !== lw[1]) continue;
        hit = k;
        break;
      }
    }
    if (hit !== null) {
      found.push(tWords[hit].startMs);
      cursor = hit + 1;
    } else {
      found.push(null);
    }
  }

  // First line always shows at the start of the scene.
  found[0] = 0;
  // Fill unmatched lines with the even-spread fallback, keeping order.
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    const v = found[i] ?? even[i];
    out.push(Math.max(v, i > 0 ? out[i - 1] : 0));
  }
  return out;
};
