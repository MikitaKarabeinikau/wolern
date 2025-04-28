"""
utils.py is meant for small, reusable helper functions that are not specific to business logic.

Date formatting is a general-purpose helper — you will probably want to reuse this for:

    Logging when words were added.

    Debug messages.

    File naming (if you use timestamps).

    Displaying last update time in GUI.

"""
from pathlib import Path

STANDART_VOCABULARY_PATH = Path(__file__).resolve().parent.parent / 'data' / 'vocabularies' / 'vocabulary.json'
STANDART_UNCHECKED_PATH = Path(__file__).resolve().parent.parent / 'data' / 'vocabularies' / 'unchecked.json'
from time import gmtime,strftime
from datetime import datetime,timedelta


# CEFR progression scale
CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

#Could be expand in future
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
    0: "New word – not yet reviewed",
    1: "Recognized – seen once or twice",
    2: "Familiar – answered correctly once",
    3: "Learned – answered correctly multiple times",
    4: "Mastered – reviewed over time, rarely forgotten",
    5: "Archived – fully known, rarely shown unless reset"
}

def current_datetime():
    return datetime.utcnow()

def parse_time_to_str(time):
    return time.strftime("%d-%m-%Y %H:%M:%S")

def initial_repeat_time():
    return datetime.utcnow() + timedelta(minutes=5)

def change_repeat_time(minutes,time=None):
    if time is None:
        time = datetime.utcnow()
    return time + timedelta(minutes=minutes)

def parse_str_to_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%d-%m-%Y %H:%M:%S")

def convert_pos(tag):
    return POS_TAG_MAP.get(tag, "unknown")