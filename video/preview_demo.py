"""Music bed + combined preview for "demo v1".

Music (Kevin MacLeod, incompetech.com, CC BY 4.0) goes in video/music/:
  Wallpaper.mp3       0:00 -> HearHere reveal (problem + persona)
  Life of Riley.mp3   HearHere reveal -> end

python3 preview_demo.py
  -> ../output/demo_v1_music.m4a     music bed only (separate stem)
  -> ../output/demo_v1_preview.mp4   720p preview: video + SFX + music + burned-in subtitles
Run sfx_demo.py first (needs ../output/demo_v1_sfx.flac). Without the music files the
preview is made with SFX only.
"""
import pathlib, subprocess

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / "output"
MUSIC = ROOT / "music"
SRC = OUT / "demo_v1_silent.webm"
SFX = OUT / "demo_v1_sfx.flac"
SRT = OUT / "demo_v1.srt"
DUR = 174.37
SWITCH = 73.6           # HearHere reveal whoosh at 73.8
MUSIC_LUFS = -21        # bed level; SFX sit on top of it


def ff(*args):
    subprocess.check_call(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *map(str, args)])


def music_bed(path):
    a, b = MUSIC / "Wallpaper.mp3", MUSIC / "Life of Riley.mp3"
    rest = DUR - SWITCH
    graph = (
        f"[0:a]atrim=0:{SWITCH + 1.2},asetpts=PTS-STARTPTS,afade=t=in:d=1.0,afade=t=out:st={SWITCH - 0.4}:d=1.6[a];"
        f"[1:a]atrim=0:{rest},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={rest - 3.5}:d=3.5,"
        f"adelay={int(SWITCH * 1000)}:all=1[b];"
        f"[a][b]amix=inputs=2:duration=longest:normalize=0,aresample=48000,"
        f"loudnorm=I={MUSIC_LUFS}:TP=-2:LRA=11,atrim=0:{DUR}[m]"
    )
    ff("-i", a, "-i", b, "-filter_complex", graph, "-map", "[m]", "-ac", "2", "-ar", 48000, "-c:a", "aac", "-b:a", "192k", path)


def main():
    have_music = all((MUSIC / f).exists() for f in ("Wallpaper.mp3", "Life of Riley.mp3"))
    inputs = ["-i", SRC, "-i", SFX]
    if have_music:
        bed = OUT / "demo_v1_music.m4a"
        music_bed(bed)
        inputs += ["-i", bed]
        amix = "[1:a]volume=3dB[s];[s][2:a]amix=inputs=2:duration=first:normalize=0,"
    else:
        print("music files not found in video/music/ - preview has SFX only")
        amix = "[1:a]"
    style = "FontName=DejaVu Sans,FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H60000000,BorderStyle=3,Outline=3,Shadow=0,MarginV=20"
    graph = (f"[0:v]scale=1280:720,subtitles={SRT.name}:force_style='{style}'[v];"
             f"{amix}loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    subprocess.check_call(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *map(str, inputs), "-filter_complex", graph,
                           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "26",
                           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", "demo_v1_preview.mp4"], cwd=OUT)
    print("preview:", OUT / "demo_v1_preview.mp4")


if __name__ == "__main__":
    main()
