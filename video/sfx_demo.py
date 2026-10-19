"""Strip the original audio from "demo v1" and lay a light SFX track on it.

Reuses the synthesised SFX bank from mix.py (royalty-free by construction), plus a crisp
UI click for screen and button taps (mix.py's "tap" is a low thump that reads as a bin lid).
Event times were picked by hand from the edited demo video.

python3 sfx_demo.py            -> ../output/demo_v1_silent.webm, ../output/demo_v1_sfx.webm, ../output/demo_v1_sfx.flac
"""
import pathlib, subprocess, wave
import numpy as np
from mix import SR, sfx_bank, lufs

ROOT = pathlib.Path(__file__).parent
SRC = ROOT.parent / "demo v1 [JoS5xN0uZOw].webm"
OUT = ROOT.parent / "output"
DUR = 174.41

def ui_click():
    """Short bright click with a softer release tick 28 ms later, like a phone UI tap."""
    n = int(0.07 * SR); t = np.arange(n) / SR
    att = np.minimum(1, t / 0.0005)
    s = att * (np.sin(2 * np.pi * 1800 * t) * np.exp(-t / 0.010) + 0.6 * np.sin(2 * np.pi * 4200 * t) * np.exp(-t / 0.003))
    off = int(0.028 * SR); tt = t[: n - off]
    s[off:] += 0.35 * np.minimum(1, tt / 0.0005) * np.sin(2 * np.pi * 2300 * tt) * np.exp(-tt / 0.006)
    return 0.3 * s / np.abs(s).max()


# (time s, sfx name, gain)
EVENTS = [
    # live-action problem section: one soft whoosh per title / numbered card
    (4.50, "whoosh", 0.6),    # question banner slides in
    (15.85, "whoosh", 0.6),   # 01 Language
    (23.85, "whoosh", 0.6),   # 02 Time
    (29.85, "whoosh", 0.6),   # 03 Relevance
    (35.70, "whoosh", 0.6),   # 04 Communication
    (42.20, "whoosh", 0.6),   # 05 Channels
    # Jason persona
    (50.90, "whoosh", 1.0),   # cut to orange persona card
    (52.70, "pop", 1.0),      # 34 years old
    (57.30, "pop", 1.0),      # 8 years in Melbourne
    (59.00, "pop", 1.0),      # has a dog
    (60.35, "pop", 1.0),      # full-time employee
    (61.70, "whoosh", 0.7),   # labels drop out
    (68.30, "pop", 0.9),      # pain points stack in
    (68.50, "pop", 0.9),
    (68.70, "pop", 0.9),
    # HearHere reveal
    (73.80, "whoosh", 1.0),
    (74.30, "chime", 1.0),
    (74.70, "chirp", 0.9),    # Spud says hello
    (77.40, "pop", 1.0),      # Digital Event News
    (77.60, "pop", 1.0),      # App + AI Helper
    (82.70, "whoosh", 1.0),   # burst closes
    # park walk + kiosk UI
    (85.50, "whoosh", 0.7),   # photo panels slide in
    (87.50, "pop", 1.0),      # post appears
    (87.90, "chirp", 0.8),
    (89.20, "pop", 1.0),      # kiosk screen opens
    (93.30, "click", 0.8),
    (97.60, "click", 0.8),
    (105.10, "click", 0.8),
    # NFC tap + phone
    (110.60, "whoosh", 0.8),  # zoom-in circle
    (111.30, "click", 1.0),   # phone taps the NFC pad
    (111.50, "chime", 0.9),   # comment sent
    (116.70, "whoosh", 0.8),  # phone slides to centre
    (119.07, "click", 0.8),   # track progress
    (124.23, "click", 0.8),   # outcome
    (128.43, "click", 0.8),
    (129.30, "click", 0.8),   # share
    (133.00, "click", 0.8),   # post to Instagram
    (133.15, "pop", 0.8),
    (134.53, "click", 0.8),   # Ask Spud
    (138.97, "click", 0.7),
    (141.37, "click", 0.7),
    # benefits badges
    (142.97, "whoosh", 1.0),
    (146.50, "pop", 1.0),     # Less language barriers
    (148.20, "pop", 1.0),     # Less guessing who to contact
    (149.70, "pop", 1.0),     # Less uncertainty after speaking up
    # In the Future
    (155.40, "whoosh", 0.8),  # cut to street
    (157.60, "whoosh", 0.6),  # dim + title
    (160.20, "pop", 1.0),     # 01
    (162.90, "pop", 1.0),     # 02
    (165.50, "pop", 1.0),     # 03
    (169.80, "whoosh", 0.7),  # list fades out
    # ending: post flies in
    (170.60, "whoosh", 1.0),
    (171.20, "chime", 1.0),
    (171.45, "chirp", 0.9),
]


def main():
    n = int((DUR + 1.5) * SR)
    fx = np.zeros(n)
    bank = sfx_bank()
    bank["click"] = ui_click()
    for t, name, g in EVENTS:
        s = bank[name] * g; a = int(t * SR)
        fx[a:a + len(s)] += s[: max(0, n - a)]
    pre = OUT / "demo_v1_sfx_pre.wav"
    with wave.open(str(pre), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(fx / np.abs(fx).max() * 0.7, -1, 1) * 32767).astype(np.int16).tobytes())
    # SFX-only stems are sparse, so normalise by peak rather than LUFS: peaks at -6 dBFS
    # leave headroom for the music bed that goes under it later.
    stem = OUT / "demo_v1_sfx.flac"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(pre), "-af", f"volume={10 ** (-6 / 20) / 0.7:.4f}",
                           "-ac", "2", "-ar", str(SR), "-t", f"{DUR}", str(stem)])
    pre.unlink()
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(SRC), "-map", "0:v", "-c:v", "copy", "-an",
                           str(OUT / "demo_v1_silent.webm")])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", str(SRC), "-i", str(stem), "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "libopus", "-b:a", "160k", "-shortest", str(OUT / "demo_v1_sfx.webm")])
    f = lufs(stem)
    print(f"{len(EVENTS)} SFX events; stem true peak {f['input_tp']} dBTP")


if __name__ == "__main__":
    main()
