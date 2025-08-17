import pytest
from unittest.mock import patch
import quiz
from vocabulary import Vocabulary


vocabulary_obj = Vocabulary('test')
test_word = vocabulary_obj.vocabulary['voices']

@patch('builtins.input',return_value='voices')
def test_correct_answer(mock_input):
    assert quiz.check_answer(test_word) == (['_', '_', '_', '_', '_', '_'] ,['_', '_', '_', '_', '_', '_'])


