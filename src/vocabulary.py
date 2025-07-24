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
from src.sound_manager import generate_audio, get_audio_path
from src.unchecked import update_weirds_word
from src.utils import current_datetime, parse_time_to_str, initial_repeat_time, STANDART_VOCABULARY_PATH, \
    STANDART_UNCHECKED_PATH, VOCABULARY_DIR_PATH
from src.fetchers import *

CEFR_CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "cache" / "cefr_cache.json"
_cache_unchecked_words = json.loads(STANDART_UNCHECKED_PATH.read_text(encoding='utf-8'))
_cefr_cache = json.loads(CEFR_CACHE_PATH.read_text(encoding="utf-8"))




class Vocabulary():
    def __init__(self,owner='scoobykot'):
        self.owner = owner
        self.dir = self.set_vocabulary_dir()
        self.collection = self.load_all_vocabularies()

    def set_vocabulary_dir(self):
        if os.path.isdir(VOCABULARY_DIR_PATH/self.owner):
            return VOCABULARY_DIR_PATH/self.owner
        else:
            os.mkdir(VOCABULARY_DIR_PATH/self.owner)
            print(f'[INFO] New dir {VOCABULARY_DIR_PATH/self.owner} was created!')
            return VOCABULARY_DIR_PATH/self.owner
    def load_all_vocabularies(self):
        pass

    def show_all_vocabularies():
        vocabularies = os.listdir(Path(__file__).resolve().parent.parent / "data" / "vocabularies")
        print('\n'.join(list(vocabularies)))
        return vocabularies


def pop_word_from_vocabulary(word, vocabulary_name):
    vocabulary = get_vocabulary(vocabulary_name)
    if vocabulary_name != STANDART_UNCHECKED_PATH:
        deleted_word_data = vocabulary.pop(word, None)
        with open(vocabulary_name, 'w', encoding='utf-8') as fl:
            json.dump(vocabulary, fl, ensure_ascii=False, indent=2)
        print(f'Word : {word} was deleted. {vocabulary_name} is rewrote.')
        return deleted_word_data
    else:
        vocabulary.remove(word)
        with open(vocabulary_name, 'w', encoding='utf-8') as fl:
            json.dump(vocabulary, fl, ensure_ascii=False, indent=2)
        print(f'Word : {word} was deleted. {vocabulary_name} is rewrote.')
        return word


def get_vocabulary(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    else:
        print(f'[INFO] File {path} does not exist!\n'
              f'Opened empty vocabulary.')
        return {}


def get_cefr_level(word):
    return _cefr_cache.get(word.lower(), "UNKNOWN")


def word_in_vocabulary(word, vocabulary):
    return True if word in vocabulary.keys() else False


def get_word_input():
    word = input("Enter the English word").strip().lower()
    return word

def is_word_in_vocabulary(word,vocabulary_file_path = Path(__file__).resolve().parent.parent/'data'/'vocabularies'/'vocabulary.json'):
    #What if file_path will be uncorrect? Should I raise Error or new dict is enough?
    #Could new dict make bugs in future ?
    if word is None:
        raise ValueError('Word should not be None')
    if len(word) <=1:
        raise ValueError('Word should have more symbols then 1')
    vocabulary = get_vocabulary(vocabulary_file_path)
    return True if word in vocabulary.keys() else False

def add_word_to_vocabulary(word, vocabulary_path, learning_stage=0):
    if word == None:
        raise ValueError(f'Word could not be a None')
    elif len(word) <= 1:
        raise ValueError(f'LENGTH OF WORD COULD NOT BE LESS OR EQUALE 1 ')
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
        "translation": get_translation_from_cache(word),
        "synonyms": synonyms,
        "definition": definitions if definitions else [],
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
        'frequency': frequency

    }
    warnings = find_warnings(word)

    if len(warnings) != 0:
        update_weirds_word(word['word'], warnings)
    else:
        vocabulary[word["word"]] = word
        with vocabulary_path.open("w", encoding="utf-8") as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=2)
        print(f"✅ Word '{word}' added to vocabulary.")


def find_warnings(word_data):
    """
    Inspect word data for missing or suspicious fields.
    Returns a list of warning messages.
    """

    warnings = []

    if not word_data.get("translation"):
        warnings.append("Missing translation")
    if not word_data.get("synonyms"):
        warnings.append("No synonyms found")
    if not word_data.get("definition"):
        warnings.append("No definitions available")
    if not word_data.get("examples"):
        warnings.append("No example sentences")
    if not word_data.get("part_of_speech"):
        warnings.append("Missing part of speech")
    if not word_data.get("frequency"):
        warnings.append("Missing frequency")
    if not word_data.get("level"):
        warnings.append("No CEFR level found")

    return warnings


def get_list_of_words(vocabulary):
    return list(vocabulary.keys())


def show_vocabulary(vocabulary):
    if isinstance(vocabulary, dict):
        return '\n'.join(list(vocabulary.keys()))
    elif isinstance(vocabulary, list):
        return '\n'.join(list(vocabulary))


def remove_word_from_vocabulary(word, vocabulary):
    pass


def update_word(word, vocabulary):
    pass


def update_learning_stage(word, stage, vocabulary, path_to):
    with path_to.open("w", encoding="utf-8") as f:
        vocabulary[word]['learning_stage'] = stage
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)


def reset_vocabulary_file():
    pass
