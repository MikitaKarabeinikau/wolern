import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from backend.src.database.crud.user_hidden_base_example import (
    create_hidden_example,
    get_hidden_examples_by_user_word_status_id,
    delete_from_hidden_example,
)
from backend.src.database.models import UserHiddenBaseExample


class TestUserHiddenBaseExample:
    """Unit tests for user_hidden_base_example CRUD operations."""

    def test_create_hidden_example_success(self):
        """Test successfully creating a hidden example."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1
        example_id = 10

        hidden_example = create_hidden_example(mock_db, user_word_status_id, example_id)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert hidden_example.user_word_status_id == user_word_status_id
        assert hidden_example.example_id == example_id

    def test_create_hidden_example_error_rollback(self):
        """Test that error during creation triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_db.commit.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            create_hidden_example(mock_db, 1, 10)

        mock_db.rollback.assert_called_once()

    def test_get_hidden_examples_by_user_word_status_id_success(self):
        """Test retrieving hidden examples for a user word status."""
        mock_db = Mock(spec=Session)
        user_word_status_id = 1

        mock_ex1 = UserHiddenBaseExample(id=1, user_word_status_id=1, example_id=10)
        mock_ex2 = UserHiddenBaseExample(id=2, user_word_status_id=1, example_id=20)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_ex1, mock_ex2]

        hidden_examples = get_hidden_examples_by_user_word_status_id(mock_db, user_word_status_id)

        assert len(hidden_examples) == 2
        assert hidden_examples[0].example_id == 10
        assert hidden_examples[1].example_id == 20

    def test_delete_from_hidden_example_success(self):
        """Test successfully deleting a hidden example."""
        mock_db = Mock(spec=Session)
        hidden_example_id = 1

        mock_example = UserHiddenBaseExample(id=hidden_example_id, user_word_status_id=1, example_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_example

        delete_from_hidden_example(mock_db, hidden_example_id)

        mock_db.delete.assert_called_once_with(mock_example)
        mock_db.commit.assert_called_once()

    def test_delete_from_hidden_example_error_rollback(self):
        """Test that error during deletion triggers rollback."""
        mock_db = Mock(spec=Session)
        mock_example = UserHiddenBaseExample(id=1, user_word_status_id=1, example_id=10)

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.one.return_value = mock_example
        mock_db.delete.side_effect = Exception("Delete error")

        with pytest.raises(Exception):
            delete_from_hidden_example(mock_db, 1)

        mock_db.rollback.assert_called_once()