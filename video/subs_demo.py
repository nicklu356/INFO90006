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
 (45.35, 50.20, "but official information is mostly\ndistributed through physical channels."),
 (50.86, 52.00, "Meet Jason."),
 (52.19, 55.90, "He moved from Taiwan eight years ago."),
 (56.01, 61.90, "He works full time, and he has a dog."),
 (62.77, 67.70, "Like most of the people we interviewed,\nhe doesn't follow council decisions closely."),
 (68.10, 72.20, "But when something affects him,\nhe runs into the same problems."),
 (73.74, 75.95, "So, we introduce HearHere:"),
 (76.10, 79.25, "a street pillar paired with a mobile app,"),
 (79.35, 82.10, "with a customised AI helper inside."),
 (82.75, 85.20, "Let's see what Jason can do with HearHere."),
 (85.39, 89.00, "On his way to the park,\nJason passes a HearHere pillar."),
 (89.33, 92.85, "He taps the screen and finds\nthe dog park issue nearby."),
 (93.09, 97.10, "It's shown in Traditional Chinese,\nwith difficult terms explained."),
 (97.39, 100.10, "Then he speaks to the AI helper in Mandarin."),
 (100.40, 103.05, "It turns his words into\na clear English comment"),
 (103.10, 105.45, "and names the responsible department."),
 (105.71, 107.55, "Jason checks it before sending."),
 (107.65, 109.90, "His voice is never recorded."),
 (110.57, 114.75, "He taps his phone on the NFC pad,\nand the issue moves to the app."),
 (114.85, 116.55, "The pillar keeps nothing."),
 (116.69, 120.60, "In the app, he can follow\nevery stage through to the outcome."),
 (128.90, 133.00, "He can also share it on Instagram,\nso his neighbours can join in."),
 (134.62, 136.15, "And if he has more questions,"),
 (136.25, 139.60, "he can ask Spud in the app,\nin his own language."),
 (143.77, 147.85, "With HearHere, Jason can understand\nthe policy in his own language,"),
 (147.95, 151.90, "find the right department,\nand know his opinion has been received,"),
 (152.00, 155.20, "all without attending a meeting."),
]
# Ending: shortened limitations / future work, then the tagline from the moment the list fades (169.8).
def spread(lines, a, b, gap=0.08):
    w = [len(t) + 12 for t in lines]
    span = b - a - gap * (len(lines) - 1)
    for txt, wi in zip(lines, w):
        d = span * wi / sum(w); cues.append((a, a + d, txt)); a += d + gap
spread(["But HearHere has limits:",
        "speaking in public may feel uncomfortable,",
        "and AI translation can make mistakes.",
        "Next, we'll test comfort,\ntranslation accuracy,",
        "access without smartphones,\nand how councils respond."], 155.5, 169.65)
spread(["HearHere: the street pillar\nfor understanding local decisions.",
        "Speak here. Be heard!"], 169.8, 174.35)
def ts(x):
    ms = round(x * 1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
out = []
for i, (s, e, txt) in enumerate(cues, 1):
    out.append(f"{i}\n{ts(s)} --> {ts(e)}\n{txt}\n")
open(sys.argv[1], "w").write("\n".join(out))
for s, e, txt in cues:
    n = len(txt.replace("\n", " ")); print(f"{s:7.2f} {e-s:4.2f}s {n/(e-s):4.1f}cps  {txt.replace(chr(10),' / ')}")
    assert max(len(l) for l in txt.split("\n")) <= 46, txt
