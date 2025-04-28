"""
Host all functions that:
• build the word dict (add_word_to_vocabulary, build_word_entry)
• load/save JSON (load_vocabulary, save_vocabulary)
• update stats (update_learning_stage, update_repeat_time).

"""
import nltk
from pathlib import Path
import json
from wolern.src.sound_manager import generate_audio, get_audio_path
from wolern.src.utils import current_datetime, parse_time_to_str
from wolern.src.fetchers import *

VOCABULARY_PATH = Path(__file__).resolve().parent.parent / "data" / "vocabulary.json"
CEFR_CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "cefr_cache.json"

_cefr_cache = json.loads(CEFR_CACHE_PATH.read_text(encoding="utf-8"))

def get_vocabulary(path=VOCABULARY_PATH):
    if VOCABULARY_PATH.exists():
        return json.loads(VOCABULARY_PATH.read_text(encoding="utf-8"))
    else:
        return {}

vocab = get_vocabulary()

def get_cefr_level(word):
    return _cefr_cache.get(word.lower(),"UNKNOWN")

def word_in_vocabulary(word,vocabulary):
    return True if word in vocabulary.keys() else False

def get_word_input():
    word = input("Enter the English word").strip().lower()
    return word


def add_word_to_vocabulary(word,vocabulary=vocab):
    if word in vocab.keys():
        print(f'Word : {word} already in vocabulary')
        return
    added_date = parse_time_to_str(current_datetime())

    part_of_speech = get_parts_of_speech(word)
    definitions = get_definitions_by_pos(word)
    synonyms = get_synonyms(word)
    translation = get_translation(word)
    examples = get_examples_from_wordnet(word)
    level = get_cefr_level(word)

    review_count = 0
    last_reviewed = parse_time_to_str(current_datetime())
    learning_stage = 0
    time_to_repeat = parse_time_to_str(initial_repeat_time())

    audio_url = generate_audio(word)

    known = False
    tags = get_tags_from_wordnet(word)

    word = {
        "word": word.lower(),
        "translation": get_transtaltion_from_cache(word),
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
        "audio_url": str(get_audio_path(word)),
        "known": known
    }
    vocab[word["word"]] = word
    VOCABULARY_PATH.write_text(json.dumps(vocab,ensure_ascii=False,indent=2),encoding="utf-8")



def show_vocabulary_list(vocabulary):
    return '\n'.join(list(vocabulary.keys()))

def remove_word_from_vocabulary():
    pass

def update_word():

    pass

def is_word(word):
    pass

def reset_vocabulary_file():
    pass