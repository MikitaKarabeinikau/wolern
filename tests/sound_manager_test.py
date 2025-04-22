
from wolern.sound_manager import generate_audio, get_audio_path, sync_audio_files

sync_audio_files()
if __name__ == "__main__":
    print(generate_audio("focus"))
    print(generate_audio("joy"))
    sync_audio_files()