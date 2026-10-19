"""Subtitles for "demo v1", timed to the original narration pauses and on-screen cues.

python3 subs_demo.py ../output/demo_v1.srt
"""
import sys
cues = [
 (0.05, 2.80, "Hello everyone, this is Group 14,\nTeam Sweet Potatoes."),
 (2.87, 5.40, "Our project focuses on how to enable"),
 (5.40, 9.60, "international residents to participate\nin local government decisions."),
 (10.55, 13.90, "During our investigation,\nwe found five problems."),
 (14.51, 18.90, "First, residents find policy terminology\nhard to understand,"),
 (18.90, 22.80, "and they lose confidence\nwhen expressing their opinions."),
 (23.37, 28.90, "Second, it's hard to attend\nin-person discussions with a busy daily life."),
 (29.60, 34.60, "Third, topics that don't feel\npersonally relevant get less attention."),
 (35.29, 39.60, "Fourth, residents get stuck\nfinding the right department."),
 (41.92, 45.35, "Lastly, newer residents\nrely on social media,"),
 (45.35, 50.20, "but official information is mostly\nshared through physical channels."),
 # Jason: each line lands with its label on the persona card
 (50.86, 52.45, "Meet Jason."),
 (52.60, 55.95, "He's from Taiwan, and he's 34 years old."),
 (56.10, 59.55, "He moved to Melbourne eight years ago,\nand he has a dog."),
 (59.70, 62.20, "He's a full-time employee as well."),
 (62.35, 65.70, "He doesn't follow council decisions closely."),
 (65.95, 69.45, "But when something affects him,"),
 (69.60, 73.60, "he runs into the same problems\nwe mentioned before."),
 (73.74, 75.95, "So, we introduce HearHere:"),
 (76.10, 79.25, "a street pillar paired with a mobile app,"),
 (79.35, 82.10, "with a customised AI helper inside."),
 (82.40, 85.10, "Let's see what Jason can do with HearHere."),
 # Park walk: one sentence per cue with breathing room, using the quiet stretch after 119 s
 (85.40, 89.00, "On his way to the park,\nJason passes a HearHere pillar."),
 (89.35, 93.15, "He taps the screen and finds\nthe dog park issue nearby."),
 (93.50, 97.35, "It's shown in Traditional Chinese,\nwith difficult terms explained."),
 (97.70, 100.60, "Then he speaks to the AI helper in Mandarin."),
 (100.95, 105.90, "It turns his words into a clear English\ncomment and names the responsible department."),
 (106.25, 110.25, "Jason checks it before sending it.\nHis voice is never recorded."),
 (110.60, 114.85, "He taps his phone on the NFC pad,\nand the issue moves to the app."),
 (115.20, 117.60, "The pillar keeps nothing."),
 (117.95, 122.60, "In the app, he can follow\neach stage through to the result."),
 (128.90, 133.00, "He can also share it on Instagram,\nso his neighbours can join in."),
 (134.62, 136.15, "And if he has more questions,"),
 (136.25, 139.60, "he can ask Spud in the app,\nin his own language."),
 (143.77, 147.85, "With HearHere, Jason can understand\nthe policy in his own language,"),
 (147.95, 151.90, "find the right department,\nand know his opinion has been received,"),
 (152.00, 155.20, "all without attending a meeting."),
]
# Ending: limitations / future work, then the tagline as the list fades (~169.5).
def spread(lines, a, b, gap=0.08):
    w = [len(t) + 12 for t in lines]
    span = b - a - gap * (len(lines) - 1)
    for txt, wi in zip(lines, w):
        d = span * wi / sum(w); cues.append((a, a + d, txt)); a += d + gap
spread(["But HearHere has limits:",
        "users may not feel comfortable\nspeaking in public,",
        "the translation may not be accurate,",
        "and we don't know how councils will react.",
        "In the future, we'll test comfort,\ntranslation accuracy,",
        "access without smartphones,\nand how councils respond."], 155.45, 169.35)
spread(["HearHere: the street pillar\nfor understanding local decisions.",
        "Speak here. Be heard!"], 169.5, 174.35)
def ts(x):
    ms = round(x * 1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
out = []
for i, (s, e, txt) in enumerate(cues, 1):
    out.append(f"{i}\n{ts(s)} --> {ts(e)}\n{txt}\n")
open(sys.argv[1], "w").write("\n".join(out))
for s, e, txt in cues:
    n = len(txt.replace("\n", " ")); print(f"{s:7.2f} {e-s:4.2f}s {n/(e-s):4.1f}cps  {txt.replace(chr(10),' / ')}")
    assert max(len(l) for l in txt.split("\n")) <= 46, txt
