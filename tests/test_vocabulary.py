from pathlib import Path

import pytest
from src.vocabulary import *
def test_add_word_to_vocabulary_None_argument():
    with pytest.raises(ValueError,match="Word could not be a None"):
        add_word_to_vocabulary(None,Path(__file__).resolve().parent)

def  test_add_word_to_vocabulary_short_word_error():
    with pytest.raises(ValueError,match="LENGTH OF WORD COULD NOT BE LESS OR EQUALE 1 "):
        add_word_to_vocabulary('a',Path(__file__).resolve().parent)

def test_is_word_in_vocabulary_True():
    assert is_word_in_vocabulary('dog',Path(__file__).resolve().parent.parent/'tests'/'data'/'test_vocabulary.json') == True

if __name__ == '__main__':
    test_add_word_to_vocabulary_None_argument()
    test_add_word_to_vocabulary_short_word_error()
    test_is_word_in_vocabulary_True()


