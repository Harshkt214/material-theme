# UGC product-ad template (Remotion)

10-second vertical (1080x1920, 24fps) UGC-style product ads. Blurred-fill background, sharp centered clip, bold outlined captions, white end card. Per video you only edit `config.ts` and add assets; fonts, colors, layout and voice are fixed.

```bash
npm install
npm run dev        # preview in Remotion Studio
```

## Make a new ad in 4 steps

1. **Content** – put your clips/images in `public/clips/`, logo and product image in `public/brand/`, then edit the top block of `config.ts`: `scenes` (hook → problem → solution → result: `src`, `caption`, `voiceText`) and `endCard`. Use only real, approved copy. Use `\n` in a caption to split it into lines (each line fades in on its own).
2. **Draft** (free) – keep `mode: "draft"` and run `npm run dev`. Scenes use `public/vo-draft/<id>.mp3` if you drop one there (e.g. a phone recording), otherwise silence with an estimated length. Iterate on script, pacing and visuals as long as you like; nothing calls ElevenLabs.
3. **Voice** – when the script is frozen, set `mode: "final"` and run `npm run vo`. It prints characters and estimated credits first, only generates scenes whose audio is missing or whose `voiceText` changed, asks before any run over 500 credits, then makes local Whisper captions timing. (`npm run vo -- --dry-run` shows the cost without spending anything.)
4. **Render** – `npm run render` → `out/ad.mp4`. Each scene lasts exactly as long as its voice file. Rendering only reads local files and never calls ElevenLabs.

## One-time setup

- `cp .env.example .env` and set `ELEVENLABS_API_KEY` (never commit `.env`).
- Set `FIXED.voice.voiceId` in `config.ts` to your ElevenLabs voice. Default model is Flash (`eleven_flash_v2_5`, ~0.5 credit/char); change `FIXED.voice.modelId` if you need another.
- The first `npm run vo` / `npm run captions` builds whisper.cpp and downloads the `base.en` model into `whisper.cpp/` (needs `git`, `make` and a C compiler on macOS/Linux; prebuilt on Windows). After that it's offline and free.

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Remotion Studio preview |
| `npm run vo` | ElevenLabs voice for changed scenes only (final mode), then captions |
| `npm run vo -- --dry-run` | Cost estimate only |
| `npm run vo -- --force <id>` | Regenerate one scene on purpose (costs credits) |
| `npm run captions` | Local Whisper word timings → `public/captions/<mode>/<id>.json` |
| `npm run render` | `out/ad.mp4` |

## How it fits together

- `config.ts` – per-video content (top) + fixed brand settings `FIXED` (bottom).
- `src/Root.tsx` – measures each scene's audio (`getAudioDurationInSeconds`) and sets the total length: sum of scenes + 2 s end card.
- `src/Ad.tsx` – timeline; `src/components/` – `BlurredBackground`, `SceneClip`, `Caption`, `EndCard`.
- Caption **text** always comes from `config.ts`. Whisper is only used for **timing**: each caption line fades in when its first words are spoken. Lines that don't appear in the voice text are spread evenly.
- `vo-cache.json` – sha256 of the `voiceText` each `public/vo/<id>.mp3` was made from. Commit it together with `public/vo/` so you never pay twice.
- Audio mix: voice 100%, music 43%, SFX 60%.
- Sounds and licences: see [`assets-licences.md`](assets-licences.md).
