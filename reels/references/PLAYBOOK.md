# Reel Editing Playbook

## Reference breakdown — "Before the edit / After the magic" (FINAL RESULT panel only), learned 2026-11-03

Measured: 15.2 s, 30 fps, integrated −14 LUFS, LRA 2.2 LU (music runs wall-to-wall with no silences). Scene-score cuts at 0.13, 2.87, 3.73, 4.17, 4.43 and 9.37 s. Most beats change by type and overlay rather than by a hard cut.

- **Hook (0–1 s):** frame 0 already shows a small white line ("TIRED OF…") and a giant red condensed word that slams in letter by letter, over a strong red glow. The claim (the pain) is on screen before the face says anything.
- **Pacing:** a new visual beat every ~1.5–2.5 s (giant word, card row, chart, phone, CTA), so about 7 beats in 15 s. The average "shot" (new graphic state) runs ~1.9 s.
- **Text system:** a 2-tier stack. A small Inter-style caps line sits above. Under it, ONE giant condensed word (Bebas/League-Gothic style) fills about 90 % of the frame width and slams from scale ≈1.8 to 1.0 with overshoot, a 2–3-frame shake and a coloured outer glow. The colour follows the emotion: red = denied / danger, grey-white = neutral, green = help / fix, yellow = rebuild, lime = CTA. Words sometimes sit behind the subject's head for depth.
- **Pop-up cards:** rounded dark cards with a 1-word label and an icon. They pop in one by one (scale + motion blur, ~0.3 s apart), arranged in a row in the lower third, and each one lands on its spoken word.
- **Warning icons:** yellow ⚠ triangles flank the giant word on "danger" lines and bounce in on either side.
- **Phone mockup:** a hand-held phone rises from the bottom showing an app screen (score gauge with a number counting up and coloured bars). The gauge needle and the number animate.
- **Animated bars / lists:** stacked pill tags ("LATE PAYMENTS", "COLLECTIONS"…) slide in one under another.
- **Cursor click on CTA:** an arrow cursor flies in and clicks the giant CTA word or button, with a press-scale.
- **Transitions:** whip / zoom-blur push between beats (heavy motion blur for 2–3 frames). The brief asks for a white flash on every scene change, so we use a 3–4-frame white flash plus a whoosh.
- **Layout:** text in the upper third, subject in the centre, cards in the lower third. Everything stays above the IG caption zone.
- **Grade:** deep blacks, high contrast, crushed shadows, saturated accent colour, slight vignette, dark-green / black background.
- **Music style:** a continuous upbeat cinematic/trap-pop bed, loud (~−14 LUFS total), and a steady pulse with no drops.
- **SFX style:** a sub-impact on each slam word, quick whooshes on pushes, small UI pops on cards, a click on the CTA.

## Safe zones (IG 1080×1920)
- Nothing in the top 168 px. All words and graphics sit in the band y 168–1330. Below 1330 there is only texture. Keep x within 60–940 (right action rail).

## Learned rules
- 2026-11-03: Frame 0 = the hook: a small line plus the giant word already on screen and readable. Never start black. — why: reference style, first-second retention.
- 2026-11-03: Every line = a small caps line on top plus ONE giant condensed slam word (scale 1.8→1.0 with back-overshoot, 3-frame shake, coloured glow). The word matches the spoken line. — why: reference text system.
- 2026-11-03: The giant word's colour follows the emotion (cyan calm, red fear/loss, amber FOMO/greed, green rules/win). — why: reference colour-per-emotion.
- 2026-11-03: A new visual beat every 1.5–2.5 s. Never hold one static graphic longer than ~3 s. — why: reference pacing (~1.9 s avg).
- 2026-11-03: White flash (3–4 frames) plus a whoosh on every scene change, and the cut lands in the voice pause. — why: brief + reference push transitions.
- 2026-11-03: Cards pop in one by one, each on its spoken word, with a pop SFX. Warning ⚠ icons on danger lines. — why: reference card rows.
- 2026-11-03: SFX map: impact on every slam word, whoosh on scene changes, pop on cards, tick on checklist items, click on the CTA. — why: brief + reference SFX style.
- 2026-11-03: Time scenes from `ffmpeg silencedetect` (n=-30dB d=0.25, then -38dB d=0.1 for word gaps). Whisper drifts on Hinglish TTS, so use it only to confirm the wording. — why: whisper drifted 2+ s after 12 s in this reel.
- 2026-11-03: Vary the layout from scene to scene (text-top/graphic-bottom, then flip to graphic-top/text-bottom) while colours, fonts and voice stay fixed. — why: creator wants a fixed brand with varied patterns.
- 2026-11-03: Research claims keep the "research kehti hai" framing and say "lagbhag / ~", never an exact invented number. — why: truth rules.
- 2026-11-03: If a licence-checked sound can't be downloaded (host blocked) or its licence is unclear, synthesize it locally and list it as "self-generated, original". — why: licence rule; the cdn.freesound.org download was blocked.

- 2026-11-03: Master the assets before applying the mix gains: voice file loudnorm to −16 LUFS, music bed file to −20 LUFS, then voice 100 % / bed 43 %, so the bed sits ~11 dB under the voice (final ≈ −13 LUFS, peak ≤ −2 dBFS). — why: a peak-normalized bed at 43 % came out louder than the voice.
- 2026-11-03: Vendor GSAP into `assets/vendor/` (from `npm pack gsap`). The render can't fetch cdn.jsdelivr.net in this environment. — why: the render failed on the CDN script.

## Saved styles
- SLAM WORD: League Gothic, 300–360 px, scale 1.8→1.0 `back.out(2.2)` over 0.32 s, then a 3-frame x/y shake (±10 px), and a text-shadow glow in the emotion colour (0 0 30px + 0 0 80px).
- KICKER LINE: Inter 900, 44–52 px caps, letter-spacing 0.06em, white at 85 %, rises 30 px and fades in 0.2 s before the slam.
- POP CARD: dark panel #10151D, 2 px emotion-coloured border, radius 28, icon + 1–2 words, scale 0.4→1 `back.out(2.5)` with blur 12→0, one by one.
- WARNING ICON: amber ⚠ triangle (SVG) that bounces in at scale 0→1.2→1 and wiggles ±8° on the danger word.
- CANDLE CHART: SVG candles that draw in left to right (staggered 0.04 s): a green rally (FOMO) or red crash (fear), plus a price line.
- EMOTION GAUGE: a semicircle arc with green → amber → red stops, the needle swings with an overshoot to the danger zone, and the label counts up.
- BARS COMPARE: two horizontal bars that grow from 0, labelled "1x" and "~2x" in green and red, with the label ticking up as it grows.
- TRAP LOOP: 3 cards on a dashed ring with a rotating arrow head, popping in order.
- PHONE CHECKLIST: rounded phone frame (radius 70, notch), list rows with tick circles filling green one by one, plus a tick SFX.
- CTA CLICK: a green pill button. An arrow cursor glides in, the button press-scales 1→0.92→1 with a ring ripple, and a click SFX plays.
- WHITE FLASH: full-frame #fff, opacity 0→0.9→0 over 4 frames, centred on the cut.
