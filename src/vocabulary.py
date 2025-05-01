"""
Host all functions that:
• build the word dict (add_word_to_vocabulary, build_word_entry)
• load/save JSON (load_vocabulary, save_vocabulary)
• update stats (update_learning_stage, update_repeat_time).

"""
import os

import nltk
from pathlib import Path
import json
from wolern.src.sound_manager import generate_audio, get_audio_path
from wolern.src.utils import current_datetime, parse_time_to_str, STANDART_VOCABULARY_PATH, STANDART_UNCHECKED_PATH
from wolern.src.fetchers import *

CEFR_CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "cache" / "cefr_cache.json"
_cache_unchecked_words = json.loads(STANDART_UNCHECKED_PATH.read_text(encoding='utf-8'))
_cefr_cache = json.loads(CEFR_CACHE_PATH.read_text(encoding="utf-8"))

def show_all_vocabularies():
    """List all vocabulary files."""
    vocabulary = os.listdir(Path(__file__).resolve().parent.parent / "data" /"vocabularies")
    print('\n'.join(list(vocabulary)))
    return vocabulary

def pop_word_from_vocabulary(word, vocabulary_name):
    vocabulary = get_vocabulary(vocabulary_name)  # 1. Load vocab from file
    if vocabulary_name != STANDART_UNCHECKED_PATH:
        deleted_word_data = vocabulary.pop(word, None) # 2. Remove word if exists
        with open(vocabulary_name, 'w', encoding='utf-8') as fl: # 3. Save updated vocab
            json.dump(vocabulary, fl, ensure_ascii=False, indent=2)
        print(f'Word : {word} was deleted. {vocabulary_name} is rewrote.')
        return deleted_word_data
    else:
        vocabulary.remove(word)  # 2. Remove word if exists
        with open(vocabulary_name, 'w', encoding='utf-8') as fl:  # 3. Save updated vocab
            json.dump(vocabulary, fl, ensure_ascii=False, indent=2)
        print(f'Word : {word} was deleted. {vocabulary_name} is rewrote.')
        return word

def get_unchecked_words_list():
    return list(_cache_unchecked_words)


def get_vocabulary(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    else:
        return {}

def get_list_of_new_words(vocabulary):

    words = [word for word in vocabulary.keys() if vocabulary[word]['learning_stage'] == 0]
    return list(words)

def get_cefr_level(word):
    return _cefr_cache.get(word.lower(),"UNKNOWN")

def word_in_vocabulary(word,vocabulary):
    return True if word in vocabulary.keys() else False

def get_word_input():
    word = input("Enter the English word").strip().lower()
    return word

def add_word_to_vocabulary(word,vocabulary_path,learning_stage=0):
    vocabulary = get_vocabulary(vocabulary_path)
    if word in vocabulary.keys():
        print(f'Word : {word} already in vocabulary')
        return
    added_date = parse_time_to_str(current_datetime())

    part_of_speech = get_parts_of_speech(word)
    definitions = get_definitions_by_pos(word)
    synonyms = get_synonyms(word)
    translation = get_translation(word)
    examples = get_examples_from_wordnet(word)
    level = get_cefr_level(word)
    frequency = get_frequency(word)

    review_count = 0
    last_reviewed = parse_time_to_str(current_datetime())
    learning_stage = learning_stage
    time_to_repeat = parse_time_to_str(initial_repeat_time())

    audio_url = generate_audio(word)

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
        "audio_url": str(get_audio_path(word))
    }


    vocabulary[word["word"]] = word
    with vocabulary_path.open("w", encoding="utf-8") as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)

    print(f"✅ Word '{word}' added to vocabulary.")

def get_list_of_words(vocabulary):
    return list(vocabulary.keys())

def show_vocabulary(vocabulary):
    if isinstance(vocabulary,dict):
        return '\n'.join(list(vocabulary.keys()))
    elif isinstance(vocabulary,list):
        return '\n'.join(list(vocabulary))

def remove_word_from_vocabulary():
    pass

def update_word():

    pass


def reset_vocabulary_file():
    pass