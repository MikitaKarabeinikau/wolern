from wolern.src.text_scanner import load_txt_file, save_unknown_unchecked_words, load_text
from wolern.src.vocabulary import get_vocabulary
from pathlib import Path

PATH_TO_TEST_TEXT = Path(__file__).resolve().parent / "data" / "text_for_scanner_test.txt"
PATH_TO_TEST_VOCABULARY = Path(__file__).resolve().parent / "data" / 'test_vocabulary.json'
PATH_TO_TEST_UNCHECKED = Path(__file__).resolve().parent / "data" / 'unchecked.json'

if __name__ == "__main__":
    # print(len(load_text_file(PATH_TO_TEST_TEXT)))
    load_text(PATH_TO_TEST_TEXT,10)
