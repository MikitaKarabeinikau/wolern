
from wolern.sound_manager import generate_audio, get_audio_path, sync_audio_files

sync_audio_files()
if __name__ == "__main__":
    print(generate_audio("focus"))  # first call → creates *_gt.mp3
    print(get_audio_path("focus"))  # returns same file without regen
    sync_audio_files()