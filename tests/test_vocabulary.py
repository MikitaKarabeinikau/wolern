import pytest

from wolern.src.utils import UNCHECKED_PATH, VOCABULARY_PATH
from wolern.src.vocabulary import delete_word_from_vocabulary


if __name__ == '__main__':
    print(delete_word_from_vocabulary("browning",UNCHECKED_PATH))
    print(delete_word_from_vocabulary("duties",VOCABULARY_PATH))

@pytest.fixture
def 