
from nltk.corpus import wordnet
import requests
from wolern.utils import convert_pos,initial_repeat_time
from wolern.utils import POS_TAG_MAP
import requests, warnings
from bs4 import BeautifulSoup


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

def fetch_cefr_from_evp(word):
    url = f"https://vocabulary.englishprofile.org/wordlist/EVP?word={word}"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")        # hide InsecureRequestWarning
            r = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        badge = soup.select_one("span.label-cefr")
        return badge.text.strip() if badge else None
    except Exception as e:
        print("[EVP] error:", e)
        return None
