"""Original SFX for the Case File style: heartbeat, stamp, shutter, typekey. Usage: python3 synth2.py <outdir>"""
import sys, wave, numpy as np
SR = 44100
OUT = sys.argv[1]
rng = np.random.default_rng(11)


def lp(x, cutoff):
    a = 1 - np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a * (x[i] - s); y[i] = s
    return y


def save(name, x):
    x = np.asarray(x, float); x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    d = (np.stack([x, x], 1) * 32767).astype('<i2')
    with wave.open(f"{OUT}/{name}.wav", 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())


def t(d):
    return np.arange(int(d * SR)) / SR

# heartbeat: lub-dub, low thumps
tt = t(0.9); hb = np.zeros(len(tt))
for off, amp in ((0.0, 1.0), (0.22, 0.7)):
    i = int(off * SR); st = np.arange(len(tt) - i) / SR
    f = 48 + 30 * np.exp(-st * 30)
    hb[i:] += amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-st * 14)
save('heartbeat', np.tanh(2.2 * hb))

# stamp: hard thud + paper slap
tt = t(0.5)
thud = np.sin(2 * np.pi * np.cumsum(70 + 120 * np.exp(-tt * 40)) / SR) * np.exp(-tt * 12)
slap = lp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 45)
save('stamp', np.tanh(1.6 * thud + 1.4 * slap))

# shutter: two mechanical clicks + short noise
tt = t(0.16); sh = np.zeros(len(tt))
for off in (0.0, 0.07):
    i = int(off * SR); st = np.arange(len(tt) - i) / SR
    n = rng.standard_normal(len(st)); n = n - lp(n, 1500)
    sh[i:] += n * np.exp(-st * 140)
save('shutter', sh)

# typekey: short bright key tick
tt = t(0.05)
tk = (rng.standard_normal(len(tt)) - lp(rng.standard_normal(len(tt)), 3000)) * np.exp(-tt * 260) + 0.4 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 200)
save('typekey', tk)
print('ok')
