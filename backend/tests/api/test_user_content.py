import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.src.api.dependencies import get_current_user

from backend.src.database.database import Base, get_db
from backend.src.database import models
from backend.src.api.v1 import (
    user_definitions,
    user_examples,
    user_synonyms,
    user_tags,
    user_translation,
)

# ============================================================================
# TEST DATABASE SETUP
# ============================================================================

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for tests."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Mock authentication - returns test user
def mock_get_current_user():
    """Mock the get_current_user dependency."""
    return {"id": 1, "username": "testuser", "email": "test@example.com"}


# ============================================================================
# CREATE TEST APP
# ============================================================================

app = FastAPI()

# Include routers
app.include_router(user_definitions.router, prefix="/api/v1")
app.include_router(user_examples.router, prefix="/api/v1")
app.include_router(user_synonyms.router, prefix="/api/v1")
app.include_router(user_tags.router, prefix="/api/v1")
app.include_router(user_translation.router, prefix="/api/v1")

# Override dependencies
app.dependency_overrides[get_db] = override_get_db

# Import and override authentication

app.dependency_overrides[get_current_user] = mock_get_current_user


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create database tables before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Get database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = models.Users(id=1, clerk_id="user_12345", username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_vocabulary(db, test_user):
    """Create a test vocabulary."""
    vocab = models.Vocabulary(user_id=test_user.id, name="Test Vocabulary")
    db.add(vocab)
    db.commit()
    db.refresh(vocab)
    return vocab


@pytest.fixture
def test_word(db):
    """Create a test word."""
    word = models.Words(word="cat", language="english")
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


@pytest.fixture
def test_vocabulary_word(db, test_vocabulary, test_word):
    """Create a vocabulary word entry."""
    vocab_word = models.VocabularyWords(
        vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id
    )
    db.add(vocab_word)
    db.commit()
    db.refresh(vocab_word)
    return vocab_word


@pytest.fixture
def test_word_status(db, test_user, test_vocabulary_word):
    """Create a test user word status."""
    word_status = models.UserWordStatus(
        vocabulary_word_id=test_vocabulary_word.id,
    )
    db.add(word_status)
    db.commit()
    db.refresh(word_status)
    return word_status


# ============================================================================
# TESTS - USER DEFINITIONS
# ============================================================================


class TestUserDefinitions:
    """Test Users Definitions API."""

    def test_create_definition_success(self, client, test_word_status):
        """Test creating a definition."""
        response = client.post(
            "/api/v1/user-definitions",
            json={
                "user_word_status_id": test_word_status.id,
                "part_of_speech": "noun",
                "definition": "A small domesticated carnivorous mammal",
            },
        )

        print(f"Response: {response.json()}")  # Debug
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["definition"]["part_of_speech"] == "noun"

    def test_create_definition_whitespace_validation(self, client, test_word_status):
        """Test whitespace validation."""
        response = client.post(
            "/api/v1/user-definitions",
            json={
                "user_word_status_id": test_word_status.id,
                "part_of_speech": "noun",
                "definition": "   ",  # Only whitespace
            },
        )

        assert response.status_code == 422

    def test_get_definition(self, client, db, test_word_status):
        """Test getting a definition."""
        # Create definition
        definition = models.UserDefinitions(
            user_word_status_id=test_word_status.id, part_of_speech="noun", definition="A feline"
        )
        db.add(definition)
        db.commit()
        db.refresh(definition)

        # Get it
        response = client.get(f"/api/v1/user-definitions/{definition.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["definition"]["id"] == definition.id

    def test_list_definitions(self, client, db, test_word_status):
        """Test listing definitions."""
        # Create 3 definitions
        for i in range(3):
            definition = models.UserDefinitions(
                user_word_status_id=test_word_status.id,
                part_of_speech="noun",
                definition=f"Definition {i}",
            )
            db.add(definition)
        db.commit()

        # List them
        response = client.get(f"/api/v1/user-definitions/word-status/{test_word_status.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert len(data["definitions"]) == 3


# ============================================================================
# TESTS - USER SYNONYMS
# ============================================================================


class TestUserSynonyms:
    """Test Users Synonyms API."""

    def test_create_synonym(self, client, test_word_status):
        """Test creating a synonym."""
        response = client.post(
            "/api/v1/user-synonyms",
            json={"user_word_status_id": test_word_status.id, "synonym": "feline"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["synonym"]["synonym"] == "feline"

    def test_gt_zero_validation(self, client):
        """Test gt=0 validation on user_word_status_id."""
        response = client.post(
            "/api/v1/user-synonyms",
            json={"user_word_status_id": 0, "synonym": "test"},  # Should fail
        )

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "greater_than"
        assert error["ctx"]["gt"] == 0

    def test_negative_id_validation(self, client):
        """Test negative ID is rejected."""
        response = client.post(
            "/api/v1/user-synonyms", json={"user_word_status_id": -5, "synonym": "test"}
        )

        assert response.status_code == 422


# ============================================================================
# TESTS - USER TAGS
# ============================================================================


class TestUserTags:
    """Test Users Tags API."""

    def test_create_tag(self, client, test_word_status):
        """Test creating a tag."""
        response = client.post(
            "/api/v1/user-tags", json={"user_word_status_id": test_word_status.id, "tag": "animals"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["tag"]["tag"] == "animals"

    def test_list_tags_includes_count(self, client, db, test_word_status):
        """Test list response includes count."""
        # Create tags
        for i in range(3):
            tag = models.UserTags(user_word_status_id=test_word_status.id, tag=f"tag{i}")
            db.add(tag)
        db.commit()

        # List
        response = client.get(f"/api/v1/user-tags/word-status/{test_word_status.id}")

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert data["count"] == 3


# ============================================================================
# TESTS - USER TRANSLATIONS
# ============================================================================


class TestUserTranslations:
    """Test Users Translations API."""

    def test_create_translation(self, client, test_word_status):
        """Test creating a translation."""
        response = client.post(
            "/api/v1/user-translations",
            json={
                "user_word_status_id": test_word_status.id,
                "language": "english",
                "translation": "cat",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["translation"]["language"] == "english"
        assert data["translation"]["translation"] == "cat"

    def test_invalid_language(self, client, test_word_status):
        """Test invalid language is rejected."""
        response = client.post(
            "/api/v1/user-translations",
            json={
                "user_word_status_id": test_word_status.id,
                "language": "klingon",  # Not supported
                "translation": "test",
            },
        )

        assert response.status_code == 422


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
