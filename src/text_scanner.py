import json
import re
from pathlib import Path

from wolern.src.utils import STANDART_VOCABULARY_PATH, STANDART_UNCHECKED_PATH
from wolern.src.vocabulary import get_vocabulary, add_word_to_vocabulary


# Logic for reading and analyzing text files


def load_text(file_path,load_limit):
    if file_path.suffix == ".txt":
        return load_txt_file(file_path,load_limit)
    elif file_path.suffix == ".docx":
        return load_docx(file_path)
    elif file_path.suffix == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError("Unsupported file type.")

def load_txt_file(file_path,load_limit=0):
    vocabulary = load_vocabulary(STANDART_VOCABULARY_PATH)
    text = load_text_from_file(file_path)
    unknown_words = list(find_unknown_words(text,vocabulary))

    if len(unknown_words) > load_limit != 0:
        to_vocabulary,rest = unknown_words[:load_limit],unknown_words[load_limit:]
        for word in to_vocabulary:
            add_word_to_vocabulary(word)
        save_unknown_unchecked_words(rest,STANDART_UNCHECKED_PATH)
    else:
        for word in unknown_words:
            add_word_to_vocabulary(word)

def load_docx(file_path):
    pass

def load_pdf(file_path):
    pass


def load_vocabulary(path):
    """Load vocabulary from JSON file and return set of known words."""
    vocabulary = get_vocabulary(path)
    return set(vocabulary.keys())

def load_text_from_file(file_path):
    """Load and clean text from a .txt file."""
    text = file_path.read_text(encoding="utf-8").lower()
    words = re.findall(r'\b[a-z]+\b', text)
    return set(words)

def find_unknown_words(words_in_text, known_words):
    """Compare text words with known words."""
    return words_in_text-known_words

def save_unknown_unchecked_words(words,path_to):
    path_to.parent.mkdir(parents=True, exist_ok=True)

    with path_to.open("w", encoding="utf-8") as f:
        json.dump(list(words), f, ensure_ascii=False, indent=2)

    print(f"Saved {len(words)} words into {path_to}")
