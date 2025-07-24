from src.word import get_word_from_vocabulary
from src.utils import TEST_VOCABULARY

def test_get_word_from_vocabulary_IN():
    assert get_word_from_vocabulary("dog",TEST_VOCABULARY)



if __name__ == "__main__":
    get_word_from_vocabulary("dog",TEST_VOCABULARY)
