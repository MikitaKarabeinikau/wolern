import json
import os.path
from pathlib import Path

from wolern.src.utils import STANDART_UNCHECKED_PATH, PATH_TO_WEIRD_WORDS_VOCABULARY, STANDART_VOCABULARY_PATH, \
    STANDART_SORTED_UNCHECKED_PATH

_cache_unchecked_words = json.loads(STANDART_UNCHECKED_PATH.read_text(encoding='utf-8'))



if os.path.exists(PATH_TO_WEIRD_WORDS_VOCABULARY):
    _cache_weird_words = json.loads(PATH_TO_WEIRD_WORDS_VOCABULARY.read_text(encoding="utf-8"))
else:
    _cache_weird_words = {}

if os.path.exists(STANDART_SORTED_UNCHECKED_PATH):
    _cache_sorted_unchecked_words = json.loads(STANDART_SORTED_UNCHECKED_PATH.read_text(encoding="utf-8"))
else:
    _cache_sorted_unchecked_words = {}

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

def sort_unchecked_by_frequency(vocabulary):
    unsorted_list = get_unsorted_list_of_new_words(vocabulary)
    sorted_list = _cache_sorted_unchecked_words
    for word in unsorted_list:
        index = binary_search_insert_index(word,sorted_list,0,len(sorted_list))
        sorted_list.insert(index,word)
        delete_from_unchecked(word[0])
    return sorted_list

def delete_from_unchecked(word):
    if word in _cache_unchecked_words:
        del _cache_unchecked_words[word]
        print(f"✅ Deleted '{word}' from unchecked cache.")
    else:
        print(f"⚠️ Word '{word}' not found in unchecked cache.")


def binary_search_insert_index(target, sorted_list, low, high):
    """
    Find the correct index to insert `target` into `sorted_list` (sorted by frequency).

    Parameters:
    - target (tuple): (word, frequency) you want to insert
    - sorted_list (list of tuples): [(word, freq), ...]
    - low (int): lower index to start from
    - high (int): upper index (exclusive)

    Returns:
    - int: index to insert the target
    """
    target_freq = target[1]

    if low >= high:
        return low

    mid = (low + high) // 2
    mid_freq = sorted_list[mid][1]

    if target_freq < mid_freq:
        return binary_search_insert_index(target, sorted_list, low, mid)
    else:
        return binary_search_insert_index(target, sorted_list, mid + 1, high)



def save_sorted_unchecked_words(vocabulary):
    data = sort_unchecked_by_frequency(vocabulary)
    with open(STANDART_SORTED_UNCHECKED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_sorted_unchecked():

    return _cache_sorted_unchecked_words


