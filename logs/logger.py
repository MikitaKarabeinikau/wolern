from functools import wraps
from pathlib import Path

PATH_TO_LOGGER_FILE = Path(__file__).resolve().parent /'data' / 'activity.log'

def log_add_word(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        word = args[0] if args else "unknown"
        print(f"[LOG] Adding word to vocabulary: {word}")
        result = func(*args, **kwargs)
        print(f"[LOG] Word '{word}' added successfully.\n")
        return result
    return wrapper