from gtts import gTTS
import pyttsx3,time
from pathlib import Path

AUDIO_DIR = Path("../data/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def _filename(word: str, suffix: str) -> Path:
    return AUDIO_DIR / f"{word.lower()}_{suffix}.mp3"

def generate_audio(word: str) -> Path:
    gt_file = _filename(word, "gt")  # data/audio/focus_gt.mp3
    try:
        gTTS(text=word, lang="pl").save(gt_file.as_posix())
        time.sleep(1)
        return gt_file               # ✅ success with gTTS
    except Exception:
        # gTTS failed → fallback
        pytt_file = _filename(word, "pytt")
        engine = pyttsx3.init()
        engine.save_to_file(word, pytt_file.as_posix())
        engine.runAndWait()          # actually synthesize
        return pytt_file


def get_audio_path(word: str) -> Path:
    for suffix in ("gt", "pytt"):         # look for gTTS first
        f = _filename(word, suffix)       # data/audio/focus_gt.mp3, then …_pytt.mp3
        if f.exists():
            return f                      # found existing file → use it
    return generate_audio(word)

def get_list_of_audio_files(pattern="*_gt.mp3"):
    return sorted(AUDIO_DIR.glob(pattern))

def sync_audio_files():
    """
    Regenerates gTTS files for any word that currently has only a
    pyttsx3 fallback.  Looks at file suffixes (_gt.mp3 / _pytt.mp3)
    inside AUDIO_DIR.
    """
    gtts   = {p.stem.rsplit('_', 1)[0] for p in AUDIO_DIR.glob("*_gt.mp3")}
    pyttsx = {p.stem.rsplit('_', 1)[0] for p in AUDIO_DIR.glob("*_pytt.mp3")}

    missing_in_gtts = pyttsx - gtts           # words we only have pytt audio for

    for word in missing_in_gtts:
        print(f"[sync] Upgrading '{word}' from pyttsx3 to gTTS …")
        generate_audio(word)                  # this will try gTTS again


