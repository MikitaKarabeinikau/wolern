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
def test_is_word_in_vocabulary_False():
    assert is_word_in_vocabulary('mod',Path(__file__).resolve().parent.parent/'tests'/'data'/'test_vocabulary.json') == False

def test_is_word_in_vocabulary_None():
    with pytest.raises(ValueError,match="Word should not be None"):
        assert is_word_in_vocabulary(None,Path(__file__).resolve().parent.parent/'tests'/'data'/'test_vocabulary.json') == False

def test_is_word_in_vocabulary_TO_SHORT_WORD():
    with pytest.raises(ValueError,match='Word should have more symbols then 1'):
        assert is_word_in_vocabulary('b',Path(__file__).resolve().parent.parent/'tests'/'data'/'test_vocabulary.json') == False
@pytest.fixture
def vocabulary():
    return Vocabulary()
def test_set_vocabulary_dir(vocabulary):
    assert vocabulary.set_vocabulary_dir() == VOCABULARY_DIR_PATH/vocabulary.owner

def test_delete_vocabulary(vocabulary):
    vocabulary.add_new_vocabulary('test_vocabulary')
    assert vocabulary.is_vocabulary_exit('test_vocabulary') == True
    vocabulary.delete_vocabulary('test_vocabulary')
    assert vocabulary.is_vocabulary_exit('test_vocabulary') == False

if __name__ == "__main__":
    vocabulary = Vocabulary()
    vocabulary.add_word_to_vocabulary('home','known')
    vocabulary.add_word_to_vocabulary('frog','known')
    vocabulary.delete_word_from_vocabulary('home','known')
