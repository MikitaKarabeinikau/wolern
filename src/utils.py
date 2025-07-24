"""
utils.py is meant for small, reusable helper functions that are not specific to business logic.

Date formatting is a general-purpose helper — you will probably want to reuse this for:

    Logging when words were added.

    Debug messages.

    File naming (if you use timestamps).

    Displaying last update time in GUI.

"""
from pathlib import Path

CEFR_CACHE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'cache' / 'cefr_cache.json'
CEFR_VOCABULARY_PROFILE_FILE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'source' / 'cefr_sources' / 'cefrj-vocabulary-profile-1.5.csv'
CEFR_OCTANOVAE_VOCABULARY_PROFILE_FILE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'source' / 'cefr_sources' / 'octanove-vocabulary-profile-c1c2-1.0.csv'
PATH_TO_SUBTLEXus = Path(__file__).resolve().parent.parent / 'data' / 'source' / 'frequencies_source' / 'SUBTLEXusfrequencyabove1.xls'
FREQUENCIES_CACHE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'cache' / 'frequency_cache.json'
TRANSLATION_CACHE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'cache' / 'translation_cache.json'
STANDART_VOCABULARY_PATH = Path(__file__).resolve().parent.parent / 'data' / 'vocabularies' / 'vocabulary.json'
STANDART_UNCHECKED_PATH = Path(__file__).resolve().parent.parent / 'data' / 'vocabularies' / 'unchecked.json'
PATH_TO_WEIRD_WORDS_VOCABULARY = Path(__file__).resolve().parent.parent / 'data' / 'vocabularies' / 'weird_words.json'
STANDART_SORTED_UNCHECKED_PATH = Path(
    __file__).resolve().parent.parent / "data" / "vocabularies" / "sorted_unchecked.json"
STANDART_AUDIO_FILES_DIR = Path(__file__).resolve().parent.parent / 'data' / 'cache' / 'audio'
TEST_VOCABULARY = Path(__file__).resolve().parent.parent / 'tests' / 'data' / 'test_vocabulary.json'
VOCABULARY_DIR_PATH = Path(__file__).resolve().parent.parent / 'data'/ 'vocabularies'
from datetime import datetime, timedelta

# CEFR progression scale
CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

POS_TAG_MAP = {
    'n': 'noun',
    'v': 'verb',
    'a': 'adjective',
    's': 'adjective satellite',
    'r': 'adverb',
    'NN': 'noun',
    'VB': 'verb',
    'JJ': 'adjective',
    'RB': 'adverb'
}

LEARNING_STAGE_DESCRIPTION = {
    "NEW WORD": "New word – not yet reviewed",
    "RECOGNIZED": "Recognized – seen once or twice",
    "FAMILIAR": "Familiar – answered correctly once",
    "LEARNED": "Learned – answered correctly multiple times",
    "MASTERED": "Mastered – reviewed over time, rarely forgotten",
    "ARCHIVED": "Archived – fully known, rarely shown unless reset"
}


def current_datetime():
    return datetime.utcnow()


def parse_time_to_str(time):
    return time.strftime("%d-%m-%Y %H:%M:%S")


def initial_repeat_time():
    return datetime.utcnow() + timedelta(minutes=5)


def change_repeat_time(minutes, time=None):
    if time is None:
        time = datetime.utcnow()
    return time + timedelta(minutes=minutes)


def parse_str_to_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%d-%m-%Y %H:%M:%S")


def convert_pos(tag):
    return POS_TAG_MAP.get(tag, "unknown")
