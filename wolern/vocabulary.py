# Main entry point for the program

from wolern.wolern.utils import current_datetime
from nltk.corpus import wordnet
import requests
"""
{
  "word": "example",
  "translation": {
    "ru": "пример",
    "pl": "przykład"
  },
  "synonyms": ["sample", "instance", "case"],
  "definition": "A representative form or pattern.",
  "examples": [
    "This is a good example of clean code.",
    "For example, water freezes at 0°C."
  ],
  "part_of_speech": "noun",
  "source_text": "my_english_article.txt",
  "date_added": "20-04-2025 14:30:00",
  "last_reviewed": "20-04-2025 15:00:00",
  "review_count": 3,
  "learning_stage": 2,
  "time_to_repeat": "22-04-2025 16:00:00",
  "notes": "",
  "level": "B1",
  "tags": ["general", "daily"],
  "audio_url": null,
  "known": false
}
"""

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
    s1 = get_synonyms_from_nltk(word)

    s2 = get_synonyms_datamuse(word)

    return s1,s2



def add_word_to_vocabulary(word,source_text):
    source_text = source_text
    added_date = current_datetime()

    part_of_speech = None
    definitions = None
    synonyms = None
    translation = None
    example = None
    level = None

    review_count = None
    last_reviewed = None
    learning_stage = None
    time_to_repeat = None

    audio_url = None

    known = None
    tags = None

    word = {
        "word": word,
        "translation": translation,
        "synonyms": [],
        "definition": definitions if definitions else [] ,
        "examples": [example] if example else [],
        "part_of_speech": part_of_speech,
        "source_text": source_text,
        "date_added": added_date,
        "last_reviewed": last_reviewed,
        "review_count": review_count,
        "learning_stage": learning_stage,
        "time_to_repeat": time_to_repeat,
        "notes": "",
        "level": level,
        "tags": tags if tags else [],
        "audio_url": audio_url,
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