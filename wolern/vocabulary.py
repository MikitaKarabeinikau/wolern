# Main entry point for the program
import nltk

from wolern.sound_manager import generate_audio, get_audio_path
from wolern.utils import current_datetime
from nltk.corpus import wordnet
import requests
from wolern.utils import convert_pos,initial_repeat_time
from wolern.utils import POS_TAG_MAP

path = '../data/word_list.json'

def get_word_input():
    word = input("Enter the English word").strip().lower()
    return word

def get_synonyms_from_nltk(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().replace('_',' ') !=word:
                synonyms.add(lemma.name().replace('_', ' '))

    return list(synonyms)

def get_synonyms_datamuse(word):
    try:
        response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
        if response.status_code == 200:
            return [item['word'] for item in response.json()]
        else:
            print(f"[Datamuse] Error: Status {response.status_code}")
    except Exception as e:
        print(f"[Datamuse] Request failed: {e}")
    return []


def get_synonyms(word):
    synonyms_from_nltk = get_synonyms_from_nltk(word)

    synonyms_from_datamuse = get_synonyms_datamuse(word)
    filtered_synonyms = synonyms_filter(synonyms_from_nltk,synonyms_from_datamuse,word)
    return filtered_synonyms

#todo
def synonyms_filter(synonyms_arr1,synonyms_arr2,original_word):
    return []

def get_parts_of_speech(word):
    pos_tags = set()
    for synset in wordnet.synsets(word):
        pos_tags.add(convert_pos(synset.pos()))
    return list(pos_tags)

def get_definitions_by_pos(word):
    definitions = {}

    for synset in wordnet.synsets(word):
        pos = synset.pos()
        readable_pos = POS_TAG_MAP.get(pos, pos)

        if readable_pos not in definitions:
            definitions[readable_pos] = []

        definition = synset.definition()
        if definition not in definitions[readable_pos]:
            definitions[readable_pos].append(definition)

    return definitions

def get_examples_from_wordnet(word):
    examples = set()
    for syn in wordnet.synsets(word):
        for ex in syn.examples():
            examples.add(ex)
    return list(examples)

def get_tags_from_wordnet(word):
    tags = set()
    for syn in wordnet.synsets(word):
        lexname = syn.lexname()  # e.g., 'noun.food', 'noun.animal'
        main_tag = lexname.split('.')[-1]
        tags.add(main_tag)
        # tags.add(lexname)
    return list(tags)

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