"""Subtitles for the recorded narration (INFO90006.mp3, 2:58).

Times are the speech segments found by Silero VAD; the wording is what was actually said
(checked with Whisper base.en and small.en), written out with the script's spelling.
A segment holding two cues is split by text length.

python3 subs_narration.py ../output/INFO90006.srt
"""
import sys

# (speech start, speech end, [cue text, ...])
SEGMENTS = [
    (0.76, 3.24, ["Hello everyone! This is Group 14."]),
    (4.02, 10.31, ["Our project focuses on how to enable residents",
                   "to participate in local government decisions."]),
    (11.03, 14.31, ["During our investigation,\nwe found five problems."]),
    (15.22, 19.30, ["First, residents find policy terminology\nhard to understand,"]),
    (19.86, 23.01, ["and they lose confidence\nwhen expressing their opinions."]),
    (24.06, 28.84, ["Second, it's hard to attend\nin-person discussions with a busy daily life."]),
    (30.23, 34.41, ["Third, topics that don't feel\npersonally relevant get less attention."]),
    (36.25, 39.43, ["Fourth, residents get stuck\nfinding the right department."]),
    (42.23, 45.61, ["Lastly, newer residents\nrely on social media,"]),
    (45.94, 49.86, ["but official information is mostly\nshared through physical channels."]),
    (51.06, 51.81, ["Meet Jason."]),
    (52.73, 55.62, ["He's from Taiwan, and he's 34 years old."]),
    (56.28, 59.33, ["He moved to Melbourne eight years ago,\nand he has a dog."]),
    (59.99, 61.73, ["He's a full-time employee as well."]),
    (62.81, 65.35, ["He doesn't follow council decisions closely."]),
    (66.33, 67.81, ["But when something affects him,"]),
    (69.69, 72.42, ["he runs into the same problems\nwe mentioned before."]),
    (73.91, 75.94, ["So, we introduce HearHere:"]),
    (76.38, 79.05, ["a street pillar paired with a mobile app,"]),
    (79.45, 81.89, ["with a customised AI helper inside."]),
    (82.84, 85.09, ["Let's see what Jason can do with HearHere."]),
    (85.82, 89.19, ["On his way to the park,\nJason passes a HearHere pillar."]),
    (89.98, 93.22, ["He taps the screen and finds\nthe dog park issue nearby."]),
    (93.94, 97.67, ["It's shown in Traditional Chinese,\nwith difficult terms explained."]),
    (98.26, 100.68, ["Then he speaks to the AI helper in Mandarin."]),
    (101.30, 105.80, ["It turns his words into a clear English\ncomment and names the responsible department."]),
    (106.74, 110.60, ["Jason checks it before sending it.\nHis voice is never recorded."]),
    (111.26, 115.43, ["He taps his phone on the NFC pad,\nand the issue moves to the app."]),
    (116.38, 117.57, ["The pillar keeps nothing."]),
    (118.55, 122.18, ["In the app, he can follow\neach stage through to the result."]),
    (129.88, 133.73, ["He can also share it on Instagram,\nso his neighbours can join in."]),
    (135.64, 137.35, ["And if he has more questions,"]),
    (137.62, 140.93, ["he can ask Spud in the app,\nin his own language."]),
    (144.70, 152.42, ["With HearHere, Jason can understand\nthe policy in his own language,",
                      "find the right department,\nand know his opinion has been received,"]),
    (153.02, 154.60, ["all without attending a meeting."]),
    (155.51, 157.22, ["But HearHere has limits:"]),
    (157.69, 160.61, ["users may not feel comfortable\nspeaking in public,"]),
    (161.05, 163.08, ["how accurate the translation is,"]),
    (163.32, 164.74, ["and how will the council react."]),
    (165.46, 168.39, ["These will all be tested\nin the future to improve."]),
    (170.17, 174.12, ["HearHere: the street pillar\nfor understanding local decisions."]),
    (174.62, 176.39, ["Speak here. Be heard!"]),
]
HOLD, GAP, MIN = 0.5, 0.1, 1.2   # linger after speech, gap before the next cue, shortest cue


def build():
    cues = []
    for s, e, texts in SEGMENTS:
        w = [len(t) for t in texts]
        a = s
        for t, wi in zip(texts, w):
            b = a + (e - s) * wi / sum(w)
            cues.append([a, b, t]); a = b
    for i, c in enumerate(cues):
        nxt = cues[i + 1][0] - GAP if i + 1 < len(cues) else c[1] + HOLD
        if c[1] < nxt:   # only hold past the end of speech where the next cue leaves room
            c[1] = min(max(c[1] + HOLD, c[0] + MIN), nxt)
    return cues


def ts(x):
    ms = round(x * 1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def main():
    cues = build()
    with open(sys.argv[1], "w") as f:
        f.write("\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)))
    for a, b, t in cues:
        assert max(len(l) for l in t.split("\n")) <= 46, t
        print(f"{a:7.2f} {b - a:4.2f}s {len(t) / (b - a):4.1f}cps  {t.replace(chr(10), ' / ')}")


if __name__ == "__main__":
    main()
