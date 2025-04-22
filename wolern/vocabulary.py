"""
Host all functions that:
• build the word dict (add_word_to_vocabulary, build_word_entry)
• load/save JSON (load_vocabulary, save_vocabulary)
• update stats (update_learning_stage, update_repeat_time).

"""
import nltk
from fetchers import *

from wolern.sound_manager import generate_audio, get_audio_path
from wolern.utils import current_datetime

path = '../data/word_list.json'

def get_word_input():
    word = input("Enter the English word").strip().lower()
    return word


def add_word_to_vocabulary(word):
    added_date = current_datetime()

    part_of_speech = get_parts_of_speech(word)
    definitions = get_definitions_by_pos(word)
    synonyms = get_synonyms(word)
    translation = None
    examples = get_examples_from_wordnet(word)
    level = None

    review_count = 0
    last_reviewed = current_datetime()
    learning_stage = 0
    time_to_repeat = initial_repeat_time()

    audio_url = generate_audio(word)

    known = False
    tags = get_tags_from_wordnet(word)

    word = {
        "word": word,
        "translation": translation,
        "synonyms": synonyms,
        "definition": definitions if definitions else [] ,
        "examples": [examples] if examples else [],
        "part_of_speech": part_of_speech,
        "date_added": added_date,
        "last_reviewed": last_reviewed,
        "review_count": review_count,
        "learning_stage": learning_stage,
        "time_to_repeat": time_to_repeat,
        "notes": "",
        "level": level,
        "tags": tags if tags else [],
        "audio_url": get_audio_path(word),
        "known": known
    }
    pass

def list_word():
    pass

def remove_word_from_vocabulary():
    pass

def update_word():

    pass

def is_word(word):
    pass

def reset_vocabulary_file():
    pass