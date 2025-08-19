import pytest
from unittest.mock import patch
import quiz
from vocabulary import Vocabulary

vocabulary_obj = Vocabulary('test')
test_word = vocabulary_obj.vocabulary['voices']


@patch('builtins.input', side_effect=['voices', 'VoIces', '       vOICEs', '                 Voices         '])
def test_correct_answer(mock_input):
    assert quiz.check_answer(test_word) == (['_', '_', '_', '_', '_', '_'], ['_', '_', '_', '_', '_', '_'])
    assert quiz.check_answer(test_word) == (['_', '_', '_', '_', '_', '_'], ['_', '_', '_', '_', '_', '_'])
    assert quiz.check_answer(test_word) == (['_', '_', '_', '_', '_', '_'], ['_', '_', '_', '_', '_', '_'])
    assert quiz.check_answer(test_word) == (['_', '_', '_', '_', '_', '_'], ['_', '_', '_', '_', '_', '_'])


test_word = vocabulary_obj.vocabulary['voices']['word']


@patch('builtins.input', side_effect=['Socces', 'T', 'Animations'])
def test_uncorrect_answer(mock_input):
    assert quiz.check_answer(test_word) == (['V', '_', 'I', '_', '_', '_'], ['S', '_', 'C', '_', '_', '_'])
    assert quiz.check_answer(test_word) == (['V', 'O', 'I', 'C', 'E', 'S'], ['T', '*', '*', '*', '*', '*'])
    assert quiz.check_answer(test_word) == (['V', 'O', '_', 'C', 'E', 'S', '*', '*', '*', '*'], ['A', 'N', '_', 'M', 'A', 'T', 'I', 'O', 'N', 'S'])
