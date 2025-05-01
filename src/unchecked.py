import json
import os.path
from pathlib import Path

from wolern.src.utils import STANDART_UNCHECKED_PATH, PATH_TO_WEIRD_WORDS_VOCABULARY


_cache_unchecked_words = json.loads(STANDART_UNCHECKED_PATH.read_text(encoding='utf-8'))

if os.path.exists(PATH_TO_WEIRD_WORDS_VOCABULARY):
    _cache_weird_words = json.loads(PATH_TO_WEIRD_WORDS_VOCABULARY.read_text(encoding="utf-8"))
else:
    _cache_weird_words = {}

def get_weirds_word():
    return _cache_weird_words

def update_weirds_word(word,warnings):
    _cache_weird_words[word] = {"warnings": warnings}
    with PATH_TO_WEIRD_WORDS_VOCABULARY.open("w", encoding="utf-8") as f:
        json.dump(_cache_weird_words, f, ensure_ascii=False, indent=2)

    print(f"✅ Word '{word}' moved to weird vocabulary.")

def get_unchecked_words_list_with_frequencies():
    return _cache_unchecked_words

def get_unsorted_list_of_new_words(vocabulary):
    # unsorted_dict = get_unchecked_words_list_with_frequencies()
    res = []
    for word in get_list_of_new_words(vocabulary):
        res.append([word,])
    #     unsorted_dict[word]['frequency'] = float(word['frequency'])
    # return [[word,freq] for word,freq in unsorted_dict.items()]

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
