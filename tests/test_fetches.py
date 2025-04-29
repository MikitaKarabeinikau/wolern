import json
from dataclasses import replace

from wolern.src.fetchers import get_translation, get_synonyms, get_definitions_by_pos, get_tags_from_wordnet, \
    get_examples_from_wordnet, get_parts_of_speech, replace_part, get_index_of_similar_part, hide_similar_parts, \
    PATH_TO_SUBTLEXus, FREQUENCIES_CACHE_PATH

def check_frequency_on_unique_data():
    frequency = json.loads(FREQUENCIES_CACHE_PATH.read_text(encoding="utf-8"))
    print(len(frequency.values()),len(set(frequency.values())))
def test_get_synonyms():
    word = "focus"
    synonyms = get_synonyms(word)
    print(f"Synonyms for '{word}':\n{synonyms}")

def test_get_part_of_speech():
    word = "focus"
    part_of_speech  = get_parts_of_speech(word)
    print(f'Word: {word} => Part of speech {part_of_speech}')

if __name__ == "__main__":
    # print(get_synonyms('focus'))
    # hide_similar_parts('focus',get_synonyms('focus'))
    # assert replace_part('synonym',2,5) == 'sy...ym'
    # assert get_index_of_similar_part('non','synonym') == (2,5)
    # print(get_examples_from_wordnet('focus'))
    # print(get_frequencies('word'))
    check_frequency_on_unique_data()
