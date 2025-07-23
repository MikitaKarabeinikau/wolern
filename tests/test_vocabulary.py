from pathlib import Path

import pytest
from src.vocabulary import add_word_to_vocabulary


if __name__ == '__main__':
    add_word_to_vocabulary("dog", Path(__file__).resolve().parent.parent/'tests'/'data'/'test_vocabulary.json')

