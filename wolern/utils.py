"""
utils.py is meant for small, reusable helper functions that are not specific to business logic.

Date formatting is a general-purpose helper — you will probably want to reuse this for:

    Logging when words were added.

    Debug messages.

    File naming (if you use timestamps).

    Displaying last update time in GUI.

"""

from time import gmtime,strftime

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
    return strftime("%d-%m-%Y %H:%M:%S",gmtime())

def initial_datetime_to_repeat():
    current = current_datetime()
    when = None

    return when

def convert_pos(tag):
    return POS_TAG_MAP.get(tag, "unknown")