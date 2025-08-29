"""
This module provides utilities for fetching word data such as
frequencies, CEFR levels, synonyms, and translations.
"""
from pathlib import Path
import json
import csv
import warnings
from typing import List, Iterable
import deepl
import requests
from requests import RequestException
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet
from deep_translator import LingueeTranslator,exceptions

from src.utils import convert_pos, POS_TAG_MAP, CEFR_ORDER, TRANSLATION_CACHE_PATH, \
    PATH_TO_SUBTLEXus, FREQUENCIES_CACHE_PATH, CEFR_VOCABULARY_PROFILE_FILE_PATH, CEFR_OCTANOVAE_VOCABULARY_PROFILE_FILE_PATH, CEFR_CACHE_PATH
_translation_cache: dict[str, dict]
if TRANSLATION_CACHE_PATH.exists():
    _translation_cache = json.loads(TRANSLATION_CACHE_PATH.read_text(encoding="utf-8"))
else:
    _translation_cache = {}



def frequency_exist(word: str) -> bool:
    return word in _frequency_cache


def build_frequency_dict() -> None:
    subtlex = pd.read_excel(PATH_TO_SUBTLEXus)
    frequency_dict = dict(zip(subtlex["Word"].str.lower(), subtlex["SUBTLCD"]))
    with open(FREQUENCIES_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(frequency_dict, f, ensure_ascii=False, indent=2)
    print(f"{FREQUENCIES_CACHE_PATH} file was created.")


if not FREQUENCIES_CACHE_PATH.exists():
    build_frequency_dict()
_frequency_cache = json.loads(FREQUENCIES_CACHE_PATH.read_text(encoding="utf-8"))


def get_frequency(word: str) -> float | None:
    """
    Retrieve the frequency score of a word from the loaded frequency cache.

    Parameters:
        word (str): The word to look up.

    Returns:
        float | None: The frequency value if found; otherwise, None.

    Notes:
        - Logs a message if the word is not found in the frequency cache.
        - Frequency is typically based on corpus data (e.g. SUBTLEX-US).
    """
    frequency = _frequency_cache.get(word)
    if frequency is None:
        print(f"Couldn't find frequency for word '{word}'")
    return frequency


def _save_translation_cache():
    TRANSLATION_CACHE_PATH.write_text(
        json.dumps(_translation_cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def check_translation_in_cache(word: str) -> dict[str, list[str]] | None:
    """
    Check if a translation for the given word is already stored in the local cache.

    Parameters:
        word (str): The English word to look up in the cache.

    Returns:
        dict[str, list[str]] | None: A dictionary with target languages as keys and
        lists of translated words as values, or None if the word is not in the cache.
    """
    return _translation_cache.get(word.lower(), None)


def get_synonyms_from_nltk(word: str) -> List[str]:
    """
    Retrieve a list of synonyms for the given word using NLTK's WordNet.

    Parameters:
        word (str): The word for which to find synonyms.

    Returns:
        List[str]: A list of unique synonyms (with underscores replaced by spaces),
        excluding the original word itself.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().replace("_", " ") != word:
                synonyms.add(lemma.name().replace("_", " "))

    return list(synonyms)


def get_synonyms_datamuse(word: str) -> List[str]:
    if word == "":
        raise ValueError("[ERROR] Word could not be empty")
    """
    Fetch synonyms for a given word using the Datamuse API.

    Parameters:
        word (str): The word to retrieve synonyms for.

    Returns:
        List[str]: A list of synonyms returned by the API. If the request fails
        or the word has no known synonyms, returns an empty list.

    Notes:
        - Makes a GET request to the Datamuse API.
        - Handles network-related errors gracefully using RequestException.
        - An empty result may indicate the word is rare or has no listed synonyms.
    """
    try:
        response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}",timeout=5)
        if response.status_code == 200:
            return [item["word"] for item in response.json()]

        print(f"[Datamuse] Error: Status {response.status_code}")
    except RequestException as e:
        print(f"[Datamuse] Request failed: {e}")
    return []


def replace_part(word: str, left_index: int | None, right_index: int | None) -> str:
    if left_index is None or right_index is None:
        return word
    return word[:left_index] + "..." + word[right_index:]


def get_index_of_similar_part(
    word: str, other_word: str
) -> tuple[int | None, int | None]:
    """
    Find the start and end indices of the longest common substring (length ≥ 3)
    between two words.

    Parameters:
        word (str): The base word.
        other_word (str): The word to compare against.

    Returns:
        tuple[int | None, int | None]: The start and end indices (in `other_word`)
        of the longest similar part, or (None, None) if none found.
    """
    best_start = None
    best_end = None
    max_len = 0

    for i in range(len(word)):
        for j in range(len(other_word)):
            length = 0
            while (
                    i + length < len(word)
                    and j + length < len(other_word)
                    and word[i + length] == other_word[j + length]
            ):
                length += 1
            if length >= 3 and length > max_len:
                best_start = j
                best_end = j + length
                max_len = length

    return best_start, best_end


def hide_similar_parts(word: str, compared_word: list[str]) -> List[str]:
    if word is None or compared_word is None:
        raise ValueError('Could compare with None argument')
    if len(word) < 3 or len(compared_word) < 3:
        return compared_word
    if type(word) is not type('text') or type(compared_word) is not type('text'):
        raise ValueError('Values should be string type')

    start, end = get_index_of_similar_part(word,compared_word)
    if start is None and end is None:
        return compared_word
    transformation = [i for i in compared_word]
    for i in range(start,end):
        transformation[i] = '.'
    return ''.join(transformation)

def get_synonyms(word: str) -> List[str]:
    """
    Retrieve a combined list of synonyms for a word using both NLTK and Datamuse sources.

    Parameters:
        word (str): The word to look up.

    Returns:
        List[str]: A list of unique synonyms gathered from both sources.
    """
    synonyms_from_nltk = get_synonyms_from_nltk(word)
    synonyms_from_datamuse = get_synonyms_datamuse(word)
    filtered_synonyms = synonyms_filter(synonyms_from_nltk, synonyms_from_datamuse)
    return filtered_synonyms


def synonyms_filter(
    synonyms_arr1: List[str], synonyms_arr2: List[str], exclude: str | None = None
) -> List[str]:
    """
    Merge two synonym lists into one unique list and optionally exclude a specific word.

    Parameters:
        synonyms_arr1 (List[str]): First list of synonyms.
        synonyms_arr2 (List[str]): Second list of synonyms.
        exclude (str | None): A word to remove from the result if present (e.g., the original word).

    Returns:
        List[str]: A list of unique synonyms with optional exclusion applied.
    """
    merged = set(synonyms_arr1) | set(synonyms_arr2)
    if exclude:
        merged.discard(exclude)
    return list(merged)


def get_parts_of_speech(word: str) -> List[str]:
    """
    Get all distinct parts of speech associated with a word using WordNet.

    Parameters:
        word (str): The word to analyze.

    Returns:
        List[str]: A list of unique parts of speech (e.g., 'noun', 'verb', 'adj'),
                   mapped using the `convert_pos` utility function.
    """
    pos_tags = set()
    for synset in wordnet.synsets(word):
        pos_tags.add(convert_pos(synset.pos()))
    return list(pos_tags)

def get_cefr_level(word):
    _cefr_cache = json.loads(CEFR_CACHE_PATH.read_text(encoding="utf-8"))
    return _cefr_cache.get(word.lower(), "UNKNOWN")

def get_definitions_by_pos(word):

    definitions = {}

    for synset in wordnet.synsets(word):
        pos = synset.pos()
        readable_pos = POS_TAG_MAP.get(pos, pos)
        if readable_pos not in definitions:
            definitions[readable_pos] = []

        definition = synset.definition()
        if definition not in [item for values in definitions.values() for item in values]:
            definitions[readable_pos].append(definition)
    return definitions


def get_examples_from_wordnet(word: str) -> List[str]:
    """
    Retrieve unique example sentences for a given word from WordNet.

    Parameters:
        word (str): The word to retrieve example sentences for.

    Returns:
        List[str]: A list of unique example sentences using the word.
    """
    examples = set()
    for syn in wordnet.synsets(word):
        for ex in syn.examples():
            examples.add(ex)
    return list(examples)


def get_tags_from_wordnet(word: str) -> List[str]:

    tags = set()
    for syn in wordnet.synsets(word):
        lexname = syn.lexname()  # e.g., 'noun.food', 'noun.animal'
        main_tag = lexname.split(".")[-1]
        tags.add(main_tag)
    return list(tags)


def fetch_cefr_from_evp(word: str) -> str | None:
    """
    Fetch the CEFR level of a word from the English Vocabulary Profile website.

    Parameters:
        word (str): The word to look up.

    Returns:
        str | None: The CEFR level (e.g., 'A1', 'B2') if found, otherwise None.

    Notes:
        - Uses BeautifulSoup to parse the HTML of the EVP page.
        - Suppresses SSL warnings and sets a request timeout.
    """
    url = f"https://vocabulary.englishprofile.org/wordlist/EVP?word={word}"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        badge = soup.select_one("span.label-cefr")
        return badge.text.strip() if badge else None
    except RequestException as e:
        print("[EVP] error:", e)
        return None


def highest_cefr(existing: str | None, new: str) -> str:
    """
    Return the higher CEFR level between two values based on CEFR_ORDER.

    Parameters:
        existing (str | None): An existing CEFR level, or None.
        new (str): A new CEFR level to compare.

    Returns:
        str: The higher (more advanced) CEFR level.
    """
    if existing is None:
        return new
    return new if CEFR_ORDER.index(new) > CEFR_ORDER.index(existing) else existing


def build_cefr_dict(files):
    """
    Build a dictionary mapping words to their highest CEFR level from multiple CSV files.

    Parameters:
        files (Iterable[Path]): A list or iterable of CSV file paths containing
                                'headword' and 'CEFR' columns.

    Returns:
        dict[str, str]: A dictionary where each word is mapped to its highest CEFR level.
    """
    cefr: dict[str, str] = {}
    c = []
    for csv_path in files:
        with csv_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row["headword"].strip().lower()
                level = row["CEFR"].strip().upper()
                if level not in c : c.append(level)
                cefr[word] = c
    return cefr


def get_translation_from_cache(word: str) -> dict[str, list[str]] | None:

    return _translation_cache.get(word)


def get_translation(
    word: str, target_lang: str = "russian"
) -> dict[str, list[str] | None]:

    w = word.lower()

    cached = _translation_cache.get(w)
    if cached and target_lang in cached:
        return {target_lang: cached[target_lang]}

    try:
        translated_words = LingueeTranslator(source="english", target=target_lang).translate(word, return_all=True)
        _translation_cache.setdefault(w, {})[target_lang] = translated_words
        _save_translation_cache()
        return {target_lang: translated_words}
    except exceptions.ElementNotFoundInGetRequest as e:  # Can't narrow to RequestException here due to external lib
        warnings.warn(f"[translation] {word} → {target_lang} failed: {e}")
        _translation_cache.setdefault(w, {})[target_lang] = None
        _save_translation_cache()
        return {target_lang: None}


def cefr_from_csv_to_json():
    """
    Build a CEFR dictionary from CSV files and save it to a JSON file.

    Uses CSV_PATH_1 and CSV_PATH_2 as input sources and stores the combined
    result at CACHE_PATH in a pretty-printed JSON format.

    Returns:
        None

    Side effects:
        - Overwrites the file at CACHE_PATH with the new CEFR data.
    """
    data = build_cefr_dict([CEFR_VOCABULARY_PROFILE_FILE_PATH, CEFR_OCTANOVAE_VOCABULARY_PROFILE_FILE_PATH])
    CEFR_CACHE_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

