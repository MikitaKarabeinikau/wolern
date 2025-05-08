"""
Audio file utilities.

This module provides functionality for generating, retrieving, and managing .mp3 audio files
for given words, leveraging Google Text-to-Speech (gTTS) with a pyttsx3 fallback.

Key Functions
-------------
_filename : Construct standardized .mp3 filenames within the AUDIO_DIR.
generate_audio : Synthesize speech to .mp3 using gTTS or fallback to pyttsx3.
get_audio_path : Locate an existing audio file or generate one if missing.
get_list_of_audio_files : List audio files in AUDIO_DIR matching a glob pattern.
sync_audio_files : Regenerate gTTS audio for words only present as pyttsx3 fallbacks.

Dependencies
------------
- gTTS
- pyttsx3
- pathlib
- time
- wolern.src.utils.AUDIO_DIR
"""
import time
from pathlib import Path
from gtts import gTTS
import pyttsx3


from requests import RequestException

from wolern.src.utils import AUDIO_DIR


def _filename(word: str, suffix: str) -> Path:
    """
    Construct an .mp3 file path by combining the provided word and suffix.

    Parameters:
        word (str): The base word to include in the filename (will be stripped and lowercased).
        suffix (str): The suffix to append to the filename (e.g., 'gt' for gTTS output or 'pytt' for pyttsx3 fallback).

    Returns:
        Path: A Path object pointing to the generated .mp3 file within AUDIO_DIR.
    """
    normalized_word = word.strip().lower()
    filename = f"{normalized_word}_{suffix}.mp3"
    return AUDIO_DIR / filename


def generate_audio(word: str) -> Path:
    """
    Generate an audio file for the given word using Google Text-to-Speech (gTTS),
    falling back to pyttsx3 if gTTS fails.

    Parameters:
        word (str): The text to synthesize into speech.

    Returns:
        Path: The Path to the synthesized .mp3 audio file. The file suffix will be 'gt'
            if generated via gTTS, or 'pytt' if falling back to pyttsx3.
    """
    # Attempt synthesis with gTTS
    gt_file = _filename(word, "gt")
    try:
        gTTS(text=word, lang="en").save(gt_file.as_posix())
        time.sleep(1)
        return gt_file
    except RequestException:
        # Fallback to pyttsx3 if gTTS fails
        pytt_file = _filename(word, "pytt")
        engine = pyttsx3.init()
        engine.save_to_file(word, pytt_file.as_posix())
        engine.runAndWait()
        return pytt_file


def get_audio_path(word: str) -> Path:
    """
    Locate an existing audio file for the given word or generate one if missing.

    Parameters:
        word (str): The text for which to retrieve or create audio.

    Returns:
        Path: The Path to the existing or newly generated .mp3 audio file.
    """
    for suffix in ("gt", "pytt"):  # look for gTTS first
        f = _filename(word, suffix)
        if f.exists():
            return f  # found existing file → use it
    return generate_audio(word)


def get_list_of_audio_files(pattern: str = "*_gt.mp3") -> list[Path]:
    """
    Retrieve a sorted list of existing audio files matching the provided pattern.

    Parameters:
        pattern (str): A glob pattern to match filenames within AUDIO_DIR (default: '*_gt.mp3').

    Returns:
        list[Path]: A sorted list of Path objects for files matching the pattern.
    """
    return sorted(AUDIO_DIR.glob(pattern))


def sync_audio_files() -> None:
    """
    Regenerate gTTS audio for words that have only a pyttsx3 fallback.

    Scans AUDIO_DIR for '_gt.mp3' and '_pytt.mp3' files; for each word found only in
    pyttsx3 ('_pytt.mp3'), regenerates its audio via gTTS.

    Parameters:
            None

    Returns:
            None
    """
    # Collect sets of words with each suffix
    gtts = {p.stem.rsplit("_", 1)[0] for p in AUDIO_DIR.glob("*_gt.mp3")}
    pyttsx = {p.stem.rsplit("_", 1)[0] for p in AUDIO_DIR.glob("*_pytt.mp3")}

    # Identify words missing gTTS audio
    missing_in_gtts = pyttsx - gtts

    # Regenerate gTTS audio for missing words
    for word in missing_in_gtts:
        print(f"[sync] Upgrading '{word}' from pyttsx3 to gTTS …")
        generate_audio(word)  # this will attempt gTTS and fallback if necessary
