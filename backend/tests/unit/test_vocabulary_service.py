from unittest.mock import Mock, patch
import pytest
from backend.src.services import vocabulary_service
from backend.src.core.word import Word
from backend.src.database import models

class TestVocabularyServiceUnit:
    def setup_method(self):
        self.mock_db = Mock()
        self.mock_word = Word(
            word="cat",
            language="english",
            translation={"russian": ["кот"]},
            synonyms=["feline"],
            definition={"noun": ["a small animal"]},
            examples={"noun": ["The cat sat."]},
            part_of_speech=["noun"],
            frequency=0.1,
            date_added="2024-01-01",
            tags=["animal"]
        )

    @patch("backend.src.services.vocabulary_service.add_word")
    @patch("backend.src.services.vocabulary_service.create_vocabulary_word")
    def test_add_new_vocabulary_word_creates_new_word_and_vocab_word(self, mock_create_vocab_word, mock_add_word):
        # Setup: word does not exist
        self.mock_db.query.return_value.filter.return_value.first.side_effect = [None, None]
        mock_new_word = Mock(spec=models.Words, id=1)
        mock_add_word.return_value = mock_new_word
        mock_vocab_word = Mock(spec=models.VocabularyWords, id=2)
        mock_create_vocab_word.return_value = mock_vocab_word

        result = vocabulary_service.add_new_vocabulary_word(self.mock_db, self.mock_word, vocabulary_id=10)
        assert result == mock_vocab_word
        mock_add_word.assert_called_once_with(self.mock_db, self.mock_word)
        mock_create_vocab_word.assert_called_once_with(self.mock_db, 10, 1)

    @patch("backend.src.services.vocabulary_service.create_vocabulary_word")
    def test_add_new_vocabulary_word_existing_word_and_vocab_word(self, mock_create_vocab_word):
        # Setup: word and vocab word exist
        mock_existing_word = Mock(spec=models.Words, id=1)
        mock_existing_vocab_word = Mock(spec=models.VocabularyWords, id=2)
        self.mock_db.query.return_value.filter.return_value.first.side_effect = [mock_existing_word, mock_existing_vocab_word]

        result = vocabulary_service.add_new_vocabulary_word(self.mock_db, self.mock_word, vocabulary_id=10)
        assert result == mock_existing_vocab_word
        mock_create_vocab_word.assert_not_called()

    @patch("backend.src.services.vocabulary_service.create_vocabulary_word")
    @patch("backend.src.services.vocabulary_service.get_user_by_vocabulary_id")
    @patch("backend.src.services.vocabulary_service.get_preferred_language_by_user_id")
    def test_create_vocabulary_word_secure_success(self, mock_get_pref_lang, mock_get_user_by_vocab_id, mock_create_vocab_word):
        mock_user = Mock(id=5)
        mock_get_user_by_vocab_id.return_value = mock_user
        mock_get_pref_lang.return_value = "english"
        mock_word = Mock(spec=models.Words, id=1)
        mock_vocab_word = Mock(spec=models.VocabularyWords, id=2)
        mock_create_vocab_word.return_value = mock_vocab_word

        result = vocabulary_service.create_vocabulary_word_secure(self.mock_db, vocabulary_id=10, word=mock_word)
        assert result == mock_vocab_word
        mock_get_user_by_vocab_id.assert_called_once_with(self.mock_db, 10)
        mock_get_pref_lang.assert_called_once_with(self.mock_db, 5)
        mock_create_vocab_word.assert_called_once_with(self.mock_db, 10, 1)

    @patch("backend.src.services.vocabulary_service.get_user_by_vocabulary_id")
    def test_create_vocabulary_word_secure_no_user(self, mock_get_user_by_vocab_id):
        mock_get_user_by_vocab_id.return_value = None
        mock_word = Mock(spec=models.Words, id=1)
        with pytest.raises(ValueError):
            vocabulary_service.create_vocabulary_word_secure(self.mock_db, vocabulary_id=10, word=mock_word)
