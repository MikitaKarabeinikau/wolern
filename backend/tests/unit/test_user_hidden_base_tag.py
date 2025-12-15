import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from backend.src.database.crud.user_hidden_base_tag import (
    create_hidden_tag,
    get_hidden_tags_by_user_word_status_id,
    delete_from_hidden_tag,
)
from backend.src.database.models import UserHiddenBaseTag


class TestUserHiddenBaseTag:
    """Unit tests for user_hidden_base_tag CRUD operations."""

    def test_create_hidden_tag_success(self):
        """Test successfully creating a hidden tag."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1
        tag_id = 10

        hidden_tag = create_hidden_tag(mock_db, user_word_status_id, tag_id)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert hidden_tag.user_word_status_id == user_word_status_id
        assert hidden_tag.tag_id == tag_id

    def test_create_hidden_tag_error_rollback(self):
        """Test that error during creation triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_db.commit.side_effect = Exception("Database error")

        with pytest.raises(Exception) as excinfo:
            create_hidden_tag(mock_db, 1, 10)

        assert "Database error" in str(excinfo.value)
        mock_db.rollback.assert_called_once()

    def test_get_hidden_tags_by_user_word_status_id_success(self):
        """Test retrieving hidden tags for a user word status."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1

        mock_tag1 = UserHiddenBaseTag(id=1, user_word_status_id=1, tag_id=10)
        mock_tag2 = UserHiddenBaseTag(id=2, user_word_status_id=1, tag_id=20)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_tag1, mock_tag2]

        hidden_tags = get_hidden_tags_by_user_word_status_id(mock_db, user_word_status_id)

        assert len(hidden_tags) == 2
        assert hidden_tags[0].tag_id == 10
        assert hidden_tags[1].tag_id == 20
        mock_db.query.assert_called_once_with(UserHiddenBaseTag)

    def test_get_hidden_tags_by_user_word_status_id_empty(self):
        """Test retrieving hidden tags when none exist."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []

        hidden_tags = get_hidden_tags_by_user_word_status_id(mock_db, user_word_status_id)

        assert len(hidden_tags) == 0

    def test_get_hidden_tags_by_user_word_status_id_error(self):
        """Test error handling when retrieving hidden tags."""
        mock_db = Mock(spec=Session)
        mock_db.query.side_effect = Exception("Query error")

        with pytest.raises(Exception) as excinfo:
            get_hidden_tags_by_user_word_status_id(mock_db, 1)

        assert "Query error" in str(excinfo.value)

    def test_delete_from_hidden_tag_success(self):
        """Test successfully deleting a hidden tag."""
        mock_db = Mock(spec=Session)
        hidden_tag_id = 1

        mock_tag = UserHiddenBaseTag(id=hidden_tag_id, user_word_status_id=1, tag_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_tag

        delete_from_hidden_tag(mock_db, hidden_tag_id)

        mock_db.delete.assert_called_once_with(mock_tag)
        mock_db.commit.assert_called_once()

    def test_delete_from_hidden_tag_not_found(self):
        """Test deleting a non-existent hidden tag."""
        mock_db = Mock(spec=Session)
        hidden_tag_id = 999

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.side_effect = Exception("Not found")

        with pytest.raises(Exception) as excinfo:
            delete_from_hidden_tag(mock_db, hidden_tag_id)

        assert "Not found" in str(excinfo.value)
        mock_db.rollback.assert_called_once()

    def test_delete_from_hidden_tag_error_rollback(self):
        """Test that error during deletion triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_tag = UserHiddenBaseTag(id=1, user_word_status_id=1, tag_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_tag
        mock_db.delete.side_effect = Exception("Delete error")

        with pytest.raises(Exception) as excinfo:
            delete_from_hidden_tag(mock_db, 1)

        assert "Delete error" in str(excinfo.value)
        mock_db.rollback.assert_called_once()