import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from backend.src.database.crud.user_hidden_base_translation import (
    create_hidden_translation,
    get_hidden_translations_by_user_word_status_id,
    delete_from_hidden_translation,
)
from backend.src.database.models import UserHiddenBaseTranslation


class TestUserHiddenBaseTranslation:
    """Unit tests for user_hidden_base_translation CRUD operations."""

    def test_create_hidden_translation_success(self):
        """Test successfully creating a hidden translation."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1
        translation_id = 10

        hidden_translation = create_hidden_translation(mock_db, user_word_status_id, translation_id)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert hidden_translation.user_word_status_id == user_word_status_id
        assert hidden_translation.translation_id == translation_id

    def test_create_hidden_translation_error_rollback(self):
        """Test that error during creation triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_db.commit.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            create_hidden_translation(mock_db, 1, 10)

        mock_db.rollback.assert_called_once()

    def test_get_hidden_translations_by_user_word_status_id_success(self):
        """Test retrieving hidden translations for a user word status."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1

        mock_trans1 = UserHiddenBaseTranslation(id=1, user_word_status_id=1, translation_id=10)
        mock_trans2 = UserHiddenBaseTranslation(id=2, user_word_status_id=1, translation_id=20)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_trans1, mock_trans2]

        hidden_translations = get_hidden_translations_by_user_word_status_id(mock_db, user_word_status_id)

        assert len(hidden_translations) == 2
        assert hidden_translations[0].translation_id == 10
        assert hidden_translations[1].translation_id == 20

    def test_delete_from_hidden_translation_success(self):
        """Test successfully deleting a hidden translation."""
        mock_db = Mock(spec=Session)
        hidden_translation_id = 1

        mock_translation = UserHiddenBaseTranslation(id=hidden_translation_id, user_word_status_id=1, translation_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_translation

        delete_from_hidden_translation(mock_db, hidden_translation_id)

        mock_db.delete.assert_called_once_with(mock_translation)
        mock_db.commit.assert_called_once()

    def test_delete_from_hidden_translation_error_rollback(self):
        """Test that error during deletion triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_translation = UserHiddenBaseTranslation(id=1, user_word_status_id=1, translation_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_translation
        mock_db.delete.side_effect = Exception("Delete error")

        with pytest.raises(Exception):
            delete_from_hidden_translation(mock_db, 1)

        mock_db.rollback.assert_called_once()