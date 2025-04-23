from nltk.corpus import wordnet
import requests
from wolern.utils import convert_pos,initial_repeat_time
from wolern.utils import POS_TAG_MAP
import requests, warnings
from bs4 import BeautifulSoup
import csv, json
from pathlib import Path
from deep_translator import LingueeTranslator
CEFR_DIR = Path(__file__).resolve().parent.parent / 'data/cefr_sources'
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TRANSLATION_CACHE_PATH = DATA_DIR / "translation_cache.json"
TRANSLATION_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

CSV_PATH_1 = CEFR_DIR / "cefrj-vocabulary-profile-1.5.csv"
CSV_PATH_2 = CEFR_DIR / "cefr_sources/octanove-vocabulary-profile-c1c2-1.0.csv"


CACHE_PATH = DATA_DIR/ "cefr_cache.json"
TRANSLATION_CACHE_PATH = DATA_DIR / "translation_cache.json"
if TRANSLATION_CACHE_PATH.exists():
    _translation_cache: dict[str: dict] = json.loads(TRANSLATION_CACHE_PATH.read_text(encoding="utf-8"))
else:
    _translation_cache = {}


# CEFR progression scale
CEFR_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

def _save_translation_cache():
    TRANSLATION_CACHE_PATH.write_text(
        json.dumps(_translation_cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def check_translation_in_cache(word):
    return _translation_cache.get(word.lower(), None)

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

def highest_cefr(existing, new):
    """Return whichever CEFR is later (higher) in the scale."""
    if existing is None:
        return new
    return new if CEFR_ORDER.index(new) > CEFR_ORDER.index(existing) else existing

def build_cefr_dict(files):
    cefr = {}
    for CSV_PATH in files:
        with CSV_PATH.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word  = row["headword"].strip().lower()
                level = row["CEFR"].strip().upper()
                cefr[word] = highest_cefr(cefr.get(word), level)
    return cefr

def get_transtaltion_from_cache(word):
    return _translation_cache.get(word)

def get_translation(word, target_lang = "russian") -> dict:
    """
        Return {<target_lang>: <translation or None>}
        Caches results in translation_cache.json.
    """
    w = word.lower()

    # 1. quick cache hit
    cached = _translation_cache.get(w)
    if cached and target_lang in cached:
        return {target_lang: cached[target_lang]}

    # 2. try Deep-Translator (Google)
    try:
        translated_words = LingueeTranslator(source="english", target=target_lang).translate(word, return_all=True)
        _translation_cache.setdefault(w, {})[target_lang] = translated_words
        _save_translation_cache()
        return {target_lang: translated_words}
    except Exception as e:
        warnings.warn(f"[translation] {word} → {target_lang} failed: {e}")
        _translation_cache.setdefault(w, {})[target_lang] = None
        _save_translation_cache()
        return {target_lang: None}

def cefr_from_csv_to_json():
    data = build_cefr_dict([CSV_PATH_1, CSV_PATH_2])
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                          encoding="utf-8")




