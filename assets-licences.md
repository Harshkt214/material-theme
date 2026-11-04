# Asset licences

Every file in `public/` that we did not make ourselves needs a row here **before** it goes into a video.

Rules:
- Allowed: **CC0**, **Public Domain**, **CC BY** (add credit where the licence requires it), or a licence that clearly allows commercial use in ads.
- Not allowed: **NC** (non-commercial), **ND** (no derivatives), "personal use only", or any file whose licence is unclear.
- Sources: Openverse (https://openverse.org, filter: *Use commercially* + *Modify or adapt*) and the earshot sound bank.
- ElevenLabs is **voiceover only**. Never use it for SFX, music, images, video or speech-to-text.

| File (in `public/`) | What | Source URL | Author | Licence | Credit needed? | Added |
|---|---|---|---|---|---|---|
| `fonts/Montserrat-Variable.ttf` | Brand font | https://github.com/google/fonts/tree/main/ofl/montserrat | The Montserrat Project Authors | SIL OFL 1.1 (`fonts/OFL.txt`) | No (keep OFL.txt with the font) | 2026-11-04 |
| `music/placeholder-pad.mp3` | Placeholder music (sine-wave chord) | Generated locally with ffmpeg | — (self-made) | Own work | No | 2026-11-04 |
| `clips/hook.mp4`, `clips/solution.mp4`, `clips/problem.png`, `clips/result.png` | Placeholder clips (test pattern / gradients) | Generated locally with ffmpeg | — (self-made) | Own work | No | 2026-11-04 |
| `brand/logo.svg`, `brand/product.svg` | Placeholder logo / product | Hand-written SVG | — (self-made) | Own work | No | 2026-11-04 |
| `vo/*.mp3` | Voiceover | ElevenLabs TTS (`npm run vo`) | — | ElevenLabs terms for your plan | No | per video |

## How to add a sound (SFX or music)

1. **Find it** on Openverse (audio tab, filters *Use commercially* + *Modify or adapt*) or the earshot sound bank. Open the file's own page and read the licence there. If it says NC, ND, or nothing clear: skip it.
2. **Download** it into `public/sfx/` (effects) or `public/music/` (music). Use a short, clear name, e.g. `sfx/whoosh-01.mp3`.
3. **Log it** by adding a row to the table above: file, source URL (the file's page, not a search page), author, licence, whether credit is needed, date.
4. **Use it** in `config.ts`:
   - Music bed: `music: "music/your-track.mp3"` (mixed at 43%, looped, fades out at the end).
   - Effect on a scene: add `sfx: "sfx/whoosh-01.mp3"` to that scene (plays when the scene starts, at 60%).
   - Effect on the end card: add `sfx: "sfx/pop-01.mp3"` to `endCard`.
5. If the licence requires credit (CC BY), put the credit in the post caption/description when you publish.
