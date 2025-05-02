import json
import os.path
from pathlib import Path

from wolern.src.utils import STANDART_UNCHECKED_PATH, PATH_TO_WEIRD_WORDS_VOCABULARY, STANDART_VOCABULARY_PATH
if not os.path.exists(str(STANDART_UNCHECKED_PATH)):
    with open(STANDART_UNCHECKED_PATH, 'w', encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)
    print(f'{STANDART_UNCHECKED_PATH} file was created.')

_cache_unchecked_words = json.loads(STANDART_UNCHECKED_PATH.read_text(encoding='utf-8'))



if os.path.exists(PATH_TO_WEIRD_WORDS_VOCABULARY):
    _cache_weird_words = json.loads(PATH_TO_WEIRD_WORDS_VOCABULARY.read_text(encoding="utf-8"))
else:
    _cache_weird_words = {}

def get_weirds_word():
    return _cache_weird_words

def get_dict_of_new_words_with_frequency(vocabulary):
    dct = {}
    for word,info in vocabulary.items():
        if info.get('learning_stage',0) == 0:
            dct[word] = info['frequency']
    return dct

def update_weirds_word(word,warnings):
    _cache_weird_words[word] = {"warnings": warnings}
    with PATH_TO_WEIRD_WORDS_VOCABULARY.open("w", encoding="utf-8") as f:
        json.dump(_cache_weird_words, f, ensure_ascii=False, indent=2)

    print(f"✅ Word '{word}' moved to weird vocabulary.")

def get_unchecked_words_dict_with_frequencies():
    type(_cache_unchecked_words)
    return _cache_unchecked_words

def get_unsorted_list_of_new_words(vocabulary):

    unsorted_list = []
    for word,frequency in get_dict_of_new_words_with_frequency(vocabulary).items():
        unsorted_list.append([word,frequency])
    print(len(unsorted_list))
    for word in get_unchecked_words_dict_with_frequencies():
        if word['word'] not in json.loads(STANDART_VOCABULARY_PATH.read_text(encoding='utf-8')).keys():
            unsorted_list.append([word['word'],word['frequency']])
    print(len(unsorted_list))
    return unsorted_list

def save_sorted_unchecked_words():
    pass
def insert_sorted_unchecked_word():
    pass
def get_sorted_unchecked():
    pass
def mark_state_as_updated():
    pass
def shift_next_unchecked_word():
    pass

def send_to_weird_words(word):
    pass
