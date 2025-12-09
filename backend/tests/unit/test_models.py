"""
Unit tests for database models.

Tests all model creation, relationships, constraints, and validations.
Uses SQLite in-memory database for fast, isolated testing.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from backend.src.database.database import Base
from backend.src.database import models

# ============================================================================
# TEST DATABASE SETUP
# ============================================================================

# Use SQLite for fast, isolated tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create database tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Provide a database session for tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_user(db):
    """Create a sample user for tests."""
    user = models.Users(
        username="testuser",
        email="test@example.com",
        clerk_id="clerk_123",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_word(db):
    """Create a sample word for tests."""
    word = models.Words(
        word="cat",
        language="english",
    )
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


@pytest.fixture
def sample_vocabulary(db, sample_user):
    """Create a sample vocabulary for tests."""
    vocabulary = models.Vocabulary(
        user_id=sample_user.id,
        name="Animals Vocabulary",
    )
    db.add(vocabulary)
    db.commit()
    db.refresh(vocabulary)
    return vocabulary


# ============================================================================
# USER MODEL TESTS
# ============================================================================


class TestUserModel:
    """Test User model."""

    def test_create_user_minimal(self, db):
        """Test creating a user with minimal required fields."""
        user = models.Users(username="newuser", email="new@example.com", clerk_id="clerk_123")
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.clerk_id == "clerk_123"
        assert isinstance(user.created_at, datetime)

    def test_create_user_full_fields(self, db):
        """Test creating a user with all fields."""
        user = models.Users(
            username="fulluser",
            email="full@example.com",
            clerk_id="clerk_123",
            preferred_language="english",
            native_language="russian",
            role="user",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.preferred_language == "english"
        assert user.native_language == "russian"
        assert user.role == "user"

    def test_user_unique_username(self, db, sample_user):
        """Test that username must be unique."""
        duplicate_user = models.Users(
            username="testuser",  # Same as sample_user
            email="different@example.com",
            clerk_id="clerk_456",
        )
        db.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_user_unique_email(self, db, sample_user):
        """Test that email must be unique."""
        duplicate_user = models.Users(
            clerk_id="clerk_456",
            username="differentuser",
            email="test@example.com",  # Same as sample_user
        )
        db.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_user_timestamps(self, db):
        """Test that timestamps are set automatically."""
        user = models.Users(
            clerk_id="clerk_123",
            username="timetest",
            email="time@example.com",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.created_at is not None


# ============================================================================
# WORD MODEL TESTS
# ============================================================================


class TestWordModel:
    """Test Words model."""

    def test_create_word_minimal(self, db):
        """Test creating a word with minimal fields."""
        word = models.Words(word="dog", language="english")
        db.add(word)
        db.commit()
        db.refresh(word)

        assert word.id is not None
        assert word.word == "dog"
        assert word.language == "english"
        assert isinstance(word.created_at, datetime)

    def test_create_word_full_fields(self, db):
        """Test creating a word with all fields."""
        word = models.Words(
            word="beautiful",
            language="english",
            audio_url="https://example.com/audio.mp3",
            frequency=0.5,
        )
        db.add(word)
        db.commit()
        db.refresh(word)

        assert word.language == "english"
        assert word.frequency == 0.5

    def test_word_unique_constraint(self, db, sample_word):
        """Test that word must be unique."""
        duplicate_word = models.Words(word="cat")
        db.add(duplicate_word)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_word_case_sensitive(self, db):
        """Test word storage preserves case."""
        word = models.Words(word="Python", language="english")
        db.add(word)
        db.commit()
        db.refresh(word)

        assert word.word == "python"  # Case preserved
        assert word.language == "english"


# ============================================================================
# VOCABULARY MODEL TESTS
# ============================================================================


class TestVocabularyModel:
    """Test Vocabulary model."""

    def test_create_vocabulary(self, db, sample_user):
        """Test creating a vocabulary."""
        vocab = models.Vocabulary(
            user_id=sample_user.id,
            name="My Vocab List",
        )
        db.add(vocab)
        db.commit()
        db.refresh(vocab)

        assert vocab.vocabulary_id is not None
        assert vocab.user_id == sample_user.id
        assert vocab.name == "My Vocab List"

    def test_vocabulary_requires_user(self, db):
        """Test that vocabulary requires a valid user_id."""
        vocab = models.Vocabulary(user_id=99999, name="Test Vocab")  # Non-existent user
        db.add(vocab)

        with pytest.raises(ValueError, match="User with ID 99999 does not exist"):
            db.commit()

    def test_vocabulary_user_relationship(self, db, sample_user):
        """Test vocabulary-user relationship."""
        vocab = models.Vocabulary(user_id=sample_user.id, name="Test Vocab")
        db.add(vocab)
        db.commit()
        db.refresh(vocab)

        # Access relationship
        assert vocab.user.username == sample_user.username


# ============================================================================
# VOCABULARY WORDS (Junction Table) TESTS
# ============================================================================


class TestVocabularyWordsModel:
    """Test VocabularyWords junction table."""

    def test_add_word_to_vocabulary(self, db, sample_vocabulary, sample_word):
        """Test adding a word to a vocabulary."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()
        db.refresh(vocab_word)

        assert vocab_word.id is not None
        assert vocab_word.vocabulary_id == sample_vocabulary.vocabulary_id
        assert vocab_word.word_id == sample_word.id
        assert isinstance(vocab_word.added_at, datetime)

    def test_vocabulary_word_unique_constraint(self, db, sample_vocabulary, sample_word):
        """Test that same word can't be added twice to same vocabulary."""
        vocab_word1 = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word1)
        db.commit()

        # Try to add same word again
        vocab_word2 = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_multiple_words_in_vocabulary(self, db, sample_vocabulary):
        """Test adding multiple words to a vocabulary."""
        words = [
            models.Words(word="cat", language="english"),
            models.Words(word="dog", language="english"),
            models.Words(word="bird", language="english"),
        ]
        db.add_all(words)
        db.commit()

        for word in words:
            vocab_word = models.VocabularyWords(
                vocabulary_id=sample_vocabulary.vocabulary_id, word_id=word.id
            )
            db.add(vocab_word)
        db.commit()

        # Query all words in vocabulary
        count = (
            db.query(models.VocabularyWords)
            .filter_by(vocabulary_id=sample_vocabulary.vocabulary_id)
            .count()
        )

        assert count == 3


# ============================================================================
# USER WORD STATUS TESTS
# ============================================================================


class TestUserWordStatusModel:
    """Test UserWordStatus model."""

    def test_create_word_status(self, db, sample_user, sample_vocabulary, sample_word):
        """Test creating a user word status."""
        # First add word to vocabulary
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()
        db.refresh(vocab_word)

        # Create word status
        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()
        db.refresh(word_status)

        assert word_status.id is not None
        assert word_status.vocabulary_word_id == vocab_word.id
        isinstance(word_status.created_at, datetime)  # Default


# ============================================================================
# USER DEFINITIONS TESTS
# ============================================================================


class TestUserDefinitionsModel:
    """Test UserDefinitions model."""

    def test_create_user_definition(self, db, sample_user, sample_vocabulary, sample_word):
        """Test creating a user definition."""
        # Setup word status
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(vocabulary_word_id=vocab_word.id)
        db.add(word_status)
        db.commit()

        # Create definition
        definition = models.UserDefinitions(
            user_word_status_id=word_status.id,
            part_of_speech="noun",
            definition="A small domesticated carnivorous mammal",
        )
        db.add(definition)
        db.commit()
        db.refresh(definition)

        assert definition.id is not None
        assert definition.user_word_status_id == word_status.id
        assert definition.part_of_speech == "noun"
        assert definition.definition == "A small domesticated carnivorous mammal"

    def test_multiple_definitions_per_word(self, db, sample_user, sample_vocabulary, sample_word):
        """Test adding multiple definitions to same word."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        # Add multiple definitions
        definitions = [
            models.UserDefinitions(
                user_word_status_id=word_status.id, part_of_speech="noun", definition="Definition 1"
            ),
            models.UserDefinitions(
                user_word_status_id=word_status.id, part_of_speech="verb", definition="Definition 2"
            ),
        ]
        db.add_all(definitions)
        db.commit()

        count = (
            db.query(models.UserDefinitions).filter_by(user_word_status_id=word_status.id).count()
        )

        assert count == 2


# ============================================================================
# USER EXAMPLES TESTS
# ============================================================================


class TestUserExamplesModel:
    """Test UserExamples model."""

    def test_create_user_example(self, db, sample_user, sample_vocabulary, sample_word):
        """Test creating a user example."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        example = models.UserExamples(
            user_word_status_id=word_status.id,
            part_of_speech="noun",
            example="The cat sat on the mat",
        )
        db.add(example)
        db.commit()
        db.refresh(example)

        assert example.id is not None
        assert example.example == "The cat sat on the mat"


# ============================================================================
# USER SYNONYMS TESTS
# ============================================================================


class TestUserSynonymsModel:
    """Test UserSynonyms model."""

    def test_create_user_synonym(self, db, sample_user, sample_vocabulary, sample_word):
        """Test creating a user synonym."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        synonym = models.UserSynonyms(user_word_status_id=word_status.id, synonym="feline")
        db.add(synonym)
        db.commit()
        db.refresh(synonym)

        assert synonym.id is not None
        assert synonym.synonym == "feline"


# ============================================================================
# USER TAGS TESTS
# ============================================================================


class TestUserTagsModel:
    """Test UserTags model."""

    def test_create_user_tag(self, db, sample_user, sample_vocabulary, sample_word):
        """Test creating a user tag."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        tag = models.UserTags(user_word_status_id=word_status.id, tag="animals")
        db.add(tag)
        db.commit()
        db.refresh(tag)

        assert tag.id is not None
        assert tag.tag == "animals"

    def test_multiple_tags_per_word(self, db, sample_user, sample_vocabulary, sample_word):
        """Test adding multiple tags to same word."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        tags = [
            models.UserTags(user_word_status_id=word_status.id, tag="animals"),
            models.UserTags(user_word_status_id=word_status.id, tag="pets"),
            models.UserTags(user_word_status_id=word_status.id, tag="mammals"),
        ]
        db.add_all(tags)
        db.commit()

        count = db.query(models.UserTags).filter_by(user_word_status_id=word_status.id).count()

        assert count == 3


# ============================================================================
# USER TRANSLATIONS TESTS
# ============================================================================


class TestUserTranslationsModel:
    """Test UserTranslations model."""

    def test_create_user_translation(self, db, sample_user, sample_vocabulary, sample_word):
        """Test creating a user translation."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        translation = models.UserTranslations(
            user_word_status_id=word_status.id, language="french", translation="chat"
        )
        db.add(translation)
        db.commit()
        db.refresh(translation)

        assert translation.id is not None
        assert translation.language == "french"
        assert translation.translation == "chat"

    def test_multiple_translations_per_word(self, db, sample_user, sample_vocabulary, sample_word):
        """Test adding translations in multiple languages."""
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        translations = [
            models.UserTranslations(
                user_word_status_id=word_status.id, language="french", translation="chat"
            ),
            models.UserTranslations(
                user_word_status_id=word_status.id, language="spanish", translation="gato"
            ),
            models.UserTranslations(
                user_word_status_id=word_status.id, language="german", translation="katze"
            ),
        ]
        db.add_all(translations)
        db.commit()

        count = (
            db.query(models.UserTranslations).filter_by(user_word_status_id=word_status.id).count()
        )

        assert count == 3


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestModelIntegration:
    """Test model relationships and complex scenarios."""

    def test_complete_word_learning_flow(self, db, sample_user, sample_vocabulary, sample_word):
        """Test complete flow: vocabulary → word → status → all content."""
        # 1. Add word to vocabulary
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        # 2. Create word status
        word_status = models.UserWordStatus(
            vocabulary_word_id=vocab_word.id,
        )
        db.add(word_status)
        db.commit()

        # 3. Add definition
        definition = models.UserDefinitions(
            user_word_status_id=word_status.id, part_of_speech="noun", definition="A feline"
        )
        db.add(definition)

        # 4. Add example
        example = models.UserExamples(
            user_word_status_id=word_status.id, part_of_speech="noun", example="The cat meowed"
        )
        db.add(example)

        # 5. Add synonym
        synonym = models.UserSynonyms(user_word_status_id=word_status.id, synonym="feline")
        db.add(synonym)

        # 6. Add tag
        tag = models.UserTags(user_word_status_id=word_status.id, tag="animals")
        db.add(tag)

        # 7. Add translation
        translation = models.UserTranslations(
            user_word_status_id=word_status.id, language="english", translation="cat"
        )
        db.add(translation)

        db.commit()

        # Verify all content exists
        assert (
            db.query(models.UserDefinitions).filter_by(user_word_status_id=word_status.id).count()
            == 1
        )

        assert (
            db.query(models.UserExamples).filter_by(user_word_status_id=word_status.id).count() == 1
        )

        assert (
            db.query(models.UserSynonyms).filter_by(user_word_status_id=word_status.id).count() == 1
        )

        assert db.query(models.UserTags).filter_by(user_word_status_id=word_status.id).count() == 1

        assert (
            db.query(models.UserTranslations).filter_by(user_word_status_id=word_status.id).count()
            == 1
        )

    def test_cascade_delete_vocabulary(self, db, sample_user, sample_vocabulary, sample_word):
        """Test that deleting vocabulary cascades properly."""
        # Add word to vocabulary
        vocab_word = models.VocabularyWords(
            vocabulary_id=sample_vocabulary.vocabulary_id, word_id=sample_word.id
        )
        db.add(vocab_word)
        db.commit()

        vocab_id = sample_vocabulary.vocabulary_id

        # Delete vocabulary
        db.delete(sample_vocabulary)
        db.commit()

        # Verify vocabulary_word is also deleted
        remaining = db.query(models.VocabularyWords).filter_by(vocabulary_id=vocab_id).count()

        assert remaining == 0


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
