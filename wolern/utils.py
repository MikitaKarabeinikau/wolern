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

def current_datetime():
    return strftime("%d-%m-%Y %H:%M:%S",gmtime())

def convert_pos(tag):
    return POS_TAG_MAP.get(tag, "unknown")