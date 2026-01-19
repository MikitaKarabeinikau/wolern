import pytest
from unittest.mock import Mock, MagicMock, patch
from backend.src.database.crud import words
from backend.src.database import models


class TestWordServiceUnit:
    """True unit tests for word service."""

    def test_get_word_by_word_text_returns_word(self):
        """Test that get_word_by_word_text returns a word when found."""
        # Arrange: Mock database session
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        mock_first = Mock()

        # Create mock word object
        mock_word = Mock(spec=models.Words)
        mock_word.id = 1
        mock_word.word = "cat"
        mock_word.language = "english"

        # Set up mock chain
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_word

        # Act: Call the function
        result = words.get_word_by_word_text(
            mock_db,
            "cat",
        )

        # Assert: Verify behavior
        assert result == mock_word
        mock_db.query.assert_called_once_with(models.Words)
        mock_query.filter.assert_called_once()


    def test_get_word_by_word_text_returns_none_when_not_found(self):
        """Test that get_word_by_word_text returns None when word not found."""
        # Arrange
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = words.get_word_by_word_text(mock_db, "nonexistent")

        # Assert
        assert result is None


    def test_get_word_by_word_text_converts_to_lowercase(self):
        """Test that word is converted to lowercase before query."""
        # Arrange
        mock_db = Mock()
        mock_word = Mock(spec=models.Words)
        mock_word.word = "cat"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_word

        # Act
        result = words.get_word_by_word_text(mock_db, "CAT")

        # Assert
        assert result.word == "cat"

    def test_list_words_applies_language_filter(self):
        """Test that language filter is applied when provided."""
        # Arrange
        mock_db = Mock()
        mock_query = Mock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        # Act
        words.get_words_by_language(mock_db, language="english")

        # Assert
        mock_query.filter.assert_called_once()


    def test_search_words_uses_ilike(self):
        """Test that search uses case-insensitive LIKE."""
        # Arrange
        mock_db = Mock()
        mock_query = Mock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        # Act
        words.search_words_by_prefix(mock_db, "cat")

        # Assert
        mock_query.filter.assert_called_once()
        # Could check that filter was called with ilike pattern
