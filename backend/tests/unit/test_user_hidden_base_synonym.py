import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from backend.src.database.crud.user_hidden_base_synonym import (
    create_hidden_synonym,
    get_hidden_synonyms_by_user_word_status_id,
    delete_from_hidden_synonym,
)
from backend.src.database.models import UserHiddenBaseSynonym


class TestUserHiddenBaseSynonym:
    """Unit tests for user_hidden_base_synonym CRUD operations."""

    def test_create_hidden_synonym_success(self):
        """Test successfully creating a hidden synonym."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1
        synonym_id = 10

        hidden_synonym = create_hidden_synonym(mock_db, user_word_status_id, synonym_id)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert hidden_synonym.user_word_status_id == user_word_status_id
        assert hidden_synonym.synonym_id == synonym_id

    def test_create_hidden_synonym_error_rollback(self):
        """Test that error during creation triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_db.commit.side_effect = Exception("Database error")

        with pytest.raises(Exception) as excinfo:
            create_hidden_synonym(mock_db, 1, 10)

        assert "Database error" in str(excinfo.value)
        mock_db.rollback.assert_called_once()

    def test_get_hidden_synonyms_by_user_word_status_id_success(self):
        """Test retrieving hidden synonyms for a user word status."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1

        mock_syn1 = UserHiddenBaseSynonym(id=1, user_word_status_id=1, synonym_id=10)
        mock_syn2 = UserHiddenBaseSynonym(id=2, user_word_status_id=1, synonym_id=20)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_syn1, mock_syn2]

        hidden_synonyms = get_hidden_synonyms_by_user_word_status_id(mock_db, user_word_status_id)

        assert len(hidden_synonyms) == 2
        assert hidden_synonyms[0].synonym_id == 10
        assert hidden_synonyms[1].synonym_id == 20

    def test_get_hidden_synonyms_by_user_word_status_id_empty(self):
        """Test retrieving hidden synonyms when none exist."""
        mock_db = Mock(spec=Session)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []

        hidden_synonyms = get_hidden_synonyms_by_user_word_status_id(mock_db, 1)

        assert len(hidden_synonyms) == 0

    def test_delete_from_hidden_synonym_success(self):
        """Test successfully deleting a hidden synonym."""
        mock_db = Mock(spec=Session)
        hidden_synonym_id = 1

        mock_synonym = UserHiddenBaseSynonym(id=hidden_synonym_id, user_word_status_id=1, synonym_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_synonym

        delete_from_hidden_synonym(mock_db, hidden_synonym_id)

        mock_db.delete.assert_called_once_with(mock_synonym)
        mock_db.commit.assert_called_once()

    def test_delete_from_hidden_synonym_error_rollback(self):
        """Test that error during deletion triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_synonym = UserHiddenBaseSynonym(id=1, user_word_status_id=1, synonym_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_synonym
        mock_db.delete.side_effect = Exception("Delete error")

        with pytest.raises(Exception):
            delete_from_hidden_synonym(mock_db, 1)

        mock_db.rollback.assert_called_once()