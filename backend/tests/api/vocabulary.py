import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from backend.src.database.database import Base, get_db
from backend.src.database import models
from backend.src.api.dependencies import get_current_user
from backend.src.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+psycopg2://woler_test_user:password@localhost/test_db"

# Create test engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Set up and tear down the test database session."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = models.Users(id=1, clerk_id="test_user_123", username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_2(db_session):
    """Create a second test user."""
    user = models.Users(id=2, clerk_id="test_user_456", username="testuser2", email="test2@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_vocabulary(db_session, test_user):
    """Create a test vocabulary."""
    vocabulary = models.Vocabulary(vocabulary_id=1, user_id=test_user.id, name="Work Vocabulary")
    db_session.add(vocabulary)
    db_session.commit()
    db_session.refresh(vocabulary)
    return vocabulary


@pytest.fixture
def test_vocabulary_with_words(db_session, test_user):
    """Create a test vocabulary with words."""
    vocabulary = models.Vocabulary(vocabulary_id=2, user_id=test_user.id, name="Travel Vocabulary")
    db_session.add(vocabulary)
    db_session.commit()
    db_session.refresh(vocabulary)
    return vocabulary


@pytest.fixture
def client(db_session):
    """Create a test client with overridden dependencies."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def mock_get_current_user(user_id: int):
    """Helper to mock the current user dependency."""
    def _mock():
        return {"id": user_id, "clerk_id": f"test_user_{user_id}"}
    return _mock


class TestGetVocabularyById:
    """Test GET /vocabularies/{vocabulary_id} endpoint."""

    def test_get_vocabulary_by_id_success(self, client, test_vocabulary, test_user):
        """Test successfully retrieving a vocabulary by ID."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)

        response = client.get(f"/vocabularies/{test_vocabulary.vocabulary_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "vocabulary" in data
        assert data["vocabulary"]["vocabulary_id"] == test_vocabulary.vocabulary_id
        assert data["vocabulary"]["name"] == "Work Vocabulary"
        assert data["vocabulary"]["user_id"] == test_user.id
        assert "created_at" in data["vocabulary"]
        assert "word_count" in data["vocabulary"]

    def test_get_vocabulary_by_id_with_word_count(self, client, test_vocabulary_with_words, test_user, db_session):
        """Test retrieving a vocabulary includes correct word count."""
        # Add some words to the vocabulary
        word1 = models.Words(word="hello", language="english")
        word2 = models.Words(word="goodbye", language="english")
        db_session.add_all([word1, word2])
        db_session.commit()

        vocab_word1 = models.VocabularyWords(vocabulary_id=test_vocabulary_with_words.vocabulary_id, word_id=word1.id)
        vocab_word2 = models.VocabularyWords(vocabulary_id=test_vocabulary_with_words.vocabulary_id, word_id=word2.id)
        db_session.add_all([vocab_word1, vocab_word2])
        db_session.commit()

        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)

        response = client.get(f"/vocabularies/{test_vocabulary_with_words.vocabulary_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["vocabulary"]["word_count"] == 2

    def test_get_vocabulary_by_id_not_found(self, client, test_user):
        """Test retrieving a non-existent vocabulary returns 404."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)

        non_existent_id = 99999
        response = client.get(f"/vocabularies/{non_existent_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert str(non_existent_id) in data["detail"]

    def test_get_vocabulary_by_id_unauthorized_user(self, client, test_vocabulary, test_user_2):
        """Test user cannot retrieve another user's vocabulary."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user_2.id)

        response = client.get(f"/vocabularies/{test_vocabulary.vocabulary_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data

    def test_get_vocabulary_by_id_invalid_id_format(self, client, test_user):
        """Test retrieving vocabulary with invalid ID format."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)

        response = client.get("/vocabularies/invalid_id")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_vocabulary_by_id_without_authentication(self, client, test_vocabulary):
        """Test retrieving vocabulary without authentication fails."""
        # Don't override get_current_user, simulating no auth
        app.dependency_overrides.clear()

        response = client.get(f"/vocabularies/{test_vocabulary.vocabulary_id}")

        # Should return 401 or 403 depending on your auth implementation
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    @patch("backend.src.database.crud.vocabulary.get_vocabulary_by_vocabulary_id")
    def test_get_vocabulary_by_id_database_error(self, mock_get_vocab, client, test_user):
        """Test database error handling returns 500."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)
        mock_get_vocab.side_effect = Exception("Database connection error")

        response = client.get("/vocabularies/1")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "detail" in data
        assert "Failed to retrieve vocabulary" in data["detail"]

    def test_get_vocabulary_by_id_zero_id(self, client, test_user):
        """Test retrieving vocabulary with ID 0."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)

        response = client.get("/vocabularies/0")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_vocabulary_by_id_negative_id(self, client, test_user):
        """Test retrieving vocabulary with negative ID."""
        app.dependency_overrides[get_current_user] = mock_get_current_user(test_user.id)

        response = client.get("/vocabularies/-1")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
