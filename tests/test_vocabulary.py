from pathlib import Path

import pytest
from src.vocabulary import *

@pytest.fixture
def vocabulary():
    return Vocabulary()

def test_add_word_to_vocabulary_None_argument(vocabulary):
    with pytest.raises(ValueError,match="Word could not be a None"):
        vocabulary.add_word_to_vocabulary(None,Path(__file__).resolve().parent)

def  test_add_word_to_vocabulary_short_word_error(vocabulary):
    with pytest.raises(ValueError,match="LENGTH OF WORD COULD NOT BE LESS OR EQUALE 1 "):
        vocabulary.add_word_to_vocabulary('a',Path(__file__).resolve().parent)
def test_set_vocabulary_dir(vocabulary):
    assert vocabulary.set_vocabulary_dir() == VOCABULARY_DIR_PATH/vocabulary.owner

def test_delete_vocabulary(vocabulary):
    vocabulary.add_new_vocabulary('test_vocabulary')
    assert vocabulary.is_vocabulary_exit('test_vocabulary') == True
    vocabulary.delete_vocabulary('test_vocabulary')
    assert vocabulary.is_vocabulary_exit('test_vocabulary') == False

if __name__ == "__main__":
    Vocabulary('known').add_word_to_vocabulary('house')
    manager = Vocabulary_Manager()
    print(manager.collection)
