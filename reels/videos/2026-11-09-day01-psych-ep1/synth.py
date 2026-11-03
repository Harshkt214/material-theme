"""Synthesize original SFX + music bed (no third-party audio). Usage: python3 synth.py <outdir>"""
import sys, wave, numpy as np

SR = 44100
OUT = sys.argv[1]
rng = np.random.default_rng(7)


def lp(x, cutoff):
    """one-pole lowpass; cutoff may be array"""
    c = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def save(name, x, stereo=False):
    x = np.asarray(x, float)
    if not stereo:
        x = np.stack([x, x], 1)
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    d = (x * 32767).astype('<i2')
    with wave.open(f"{OUT}/{name}.wav", 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())


def t(dur):
    return np.arange(int(dur * SR)) / SR

# impact: pitch-dropping sub + noise crack
tt = t(0.9)
f = 40 + 110 * np.exp(-tt * 18)
sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.5)
crack = lp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 30)
save('impact', np.tanh(1.8 * sub + 0.9 * crack))

# whoosh: noise through sweeping lowpass, bell envelope
tt = t(0.5)
env = np.sin(np.pi * tt / 0.5) ** 2
cut = 300 + 5000 * np.sin(np.pi * tt / 0.5) ** 1.5
n = rng.standard_normal(len(tt))
save('whoosh', lp(lp(n, cut), cut) * env)

# pop: fast upward blip
tt = t(0.11)
f = 500 + 900 * (tt / 0.11)
save('pop', np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38) * np.minimum(1, tt * 2000))

# tick: short bright woodblock tick
tt = t(0.06)
tick = (np.sin(2 * np.pi * 1800 * tt) + 0.5 * np.sin(2 * np.pi * 3400 * tt)) * np.exp(-tt * 120)
save('tick', tick)

# click: mouse-like double transient
tt = t(0.12)
cl = np.zeros(len(tt))
for off, amp in ((0.0, 1.0), (0.055, 0.6)):
    i = int(off * SR); seg = np.arange(len(tt) - i) / SR
    cl[i:] += amp * (rng.standard_normal(len(seg)) * np.exp(-seg * 900) + np.sin(2 * np.pi * 2500 * seg) * np.exp(-seg * 400))
save('click', cl)

# flash sting: tiny bright shimmer for the white flash (optional layer)

# ---- music bed: dark half-time trap, 140 bpm, A minor ----
DUR = 24.0
BPM = 140; beat = 60 / BPM
N = int(DUR * SR); mix = np.zeros((N, 2))
chords = [[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]]  # Am F Dm E
roots = [45, 41, 38, 40]
bar = 4 * beat
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
pad = np.zeros(N)
bass = np.zeros(N)
for bi in range(int(DUR / bar) + 1):
    s = int(bi * bar * SR); e = min(N, int((bi + 1) * bar * SR))
    if s >= N: break
    tt = np.arange(e - s) / SR
    ch = chords[bi % 4]
    seg = np.zeros(e - s)
    for m in ch:
        for det in (-0.08, 0.08):
            ph = (mtof(m + det) * tt) % 1
            seg += 2 * ph - 1
    att = np.minimum(1, tt / 0.4) * np.minimum(1, (tt[-1] - tt + 0.05) / 0.3)
    pad[s:e] += seg * att
    # 808 on beat 1 and the "and" of 2
    for off in (0, 1.5 * beat, 2.75 * beat):
        i = s + int(off * SR)
        if i >= e: continue
        L = min(N - i, int(1.1 * SR)); st = np.arange(L) / SR
        f = mtof(roots[bi % 4] - 12) * (1 + 1.5 * np.exp(-st * 40))
        bass[i:i + L] += np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-st * 2.2)
pad = lp(lp(pad, 900), 1400)
drums = np.zeros(N)
step = beat / 2
for k in range(int(DUR / step)):
    i = int(k * step * SR)
    L = min(N - i, int(0.05 * SR)); st = np.arange(L) / SR
    hat = rng.standard_normal(L)
    hat = hat - lp(hat, 7000)  # highpass-ish
    drums[i:i + L] += 0.35 * hat * np.exp(-st * 90) * (1.0 if k % 2 == 0 else 0.6)
    if k % 8 == 4:  # clap on beat 3 (half-time)
        L2 = min(N - i, int(0.25 * SR)); st2 = np.arange(L2) / SR
        cl = lp(rng.standard_normal(L2), 2500)
        drums[i:i + L2] += 1.2 * cl * np.exp(-st2 * 22)
music = 0.55 * pad / (np.max(np.abs(pad)) + 1e-9) + 0.7 * bass / (np.max(np.abs(bass)) + 1e-9) + 0.5 * drums / (np.max(np.abs(drums)) + 1e-9)
# fade in/out
tt = np.arange(N) / SR
music *= np.minimum(1, tt / 0.3) * np.minimum(1, (DUR - tt) / 1.5)
mix[:, 0] = music; mix[:, 1] = np.roll(music, 9)
save('music_bed', np.tanh(1.2 * mix), stereo=True)
print('ok')
