"""
Unit tests for Synonyms CRUD operations.

Tests synonym creation, retrieval, and relationships with words.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Words
from backend.src.database.crud.synonyms import (
    create_synonym,
    get_synonyms_by_word_id,
    get_synonym_by_id,
)

# Create a test database URL
TEST_DATABASE_URL = "postgresql+psycopg2://woler_test_user:password@localhost/test_db"

# Create a test engine and session
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


class TestSynonymsModel:
    """Test suite for Synonyms model and CRUD operations."""

    def test_create_synonym(self, db_session):
        """Test creating a synonym for a word."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a synonym
        synonym = create_synonym(db_session, word_id=word.id, synonym="joyful")

        # Verify the synonym
        assert synonym is not None
        assert synonym.word_id == word.id
        assert synonym.synonym == "joyful"
        assert synonym.id is not None

    def test_create_synonym_lowercase(self, db_session):
        """Test that synonyms are automatically converted to lowercase."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a synonym with uppercase letters
        synonym = create_synonym(db_session, word_id=word.id, synonym="JOYFUL")

        # Verify the synonym is lowercase
        assert synonym.synonym == "joyful"

    def test_get_synonyms_by_word_id(self, db_session):
        """Test retrieving synonyms by word ID."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Create multiple synonyms
        create_synonym(db_session, word_id=word.id, synonym="joyful")
        create_synonym(db_session, word_id=word.id, synonym="cheerful")
        create_synonym(db_session, word_id=word.id, synonym="delighted")

        # Retrieve synonyms
        synonyms = get_synonyms_by_word_id(db_session, word_id=word.id)

        # Verify the synonyms
        assert len(synonyms) == 3
        synonym_words = [syn.synonym for syn in synonyms]
        assert "joyful" in synonym_words
        assert "cheerful" in synonym_words
        assert "delighted" in synonym_words

    def test_get_synonym_by_id(self, db_session):
        """Test retrieving a synonym by its ID."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a synonym
        synonym = create_synonym(db_session, word_id=word.id, synonym="joyful")

        # Retrieve the synonym by ID
        retrieved_synonym = get_synonym_by_id(db_session, id=synonym.id)

        # Verify the retrieved synonym
        assert retrieved_synonym is not None
        assert retrieved_synonym.id == synonym.id
        assert retrieved_synonym.synonym == "joyful"
        assert retrieved_synonym.word_id == word.id

    def test_get_synonym_by_id_not_found(self, db_session):
        """Test retrieving a synonym by an invalid ID."""
        # Attempt to retrieve a synonym with a non-existent ID
        retrieved_synonym = get_synonym_by_id(db_session, id=999)

        # Verify the result
        assert retrieved_synonym is None

    def test_duplicate_synonyms_for_same_word(self, db_session):
        """Test that duplicate synonyms cannot be created for the same word."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Create the first synonym
        synonym1 = create_synonym(db_session, word_id=word.id, synonym="joyful")

        # Verify the first synonym was created
        assert synonym1.synonym == "joyful"

        # Return the existing synonym when trying to create a duplicate
        synonym2 = create_synonym(db_session, word_id=word.id, synonym="joyful")
        assert synonym2.id == synonym1.id
        assert synonym2.synonym == synonym1.synonym
        assert synonym2.word_id == synonym1.word_id

    def test_multiple_words_same_synonym(self, db_session):
        """Test that multiple words can have the same synonym."""
        # Create two words
        word1 = Words(word="happy", language="english")
        word2 = Words(word="glad", language="english")
        db_session.add_all([word1, word2])
        db_session.commit()

        # Create the same synonym for both words
        synonym1 = create_synonym(db_session, word_id=word1.id, synonym="joyful")
        synonym2 = create_synonym(db_session, word_id=word2.id, synonym="joyful")

        # Verify both synonyms exist
        assert synonym1.synonym == "joyful"
        assert synonym2.synonym == "joyful"
        assert synonym1.word_id == word1.id
        assert synonym2.word_id == word2.id
        assert synonym1.id != synonym2.id

    def test_synonym_word_relationship(self, db_session):
        """Test the relationship between synonyms and words."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Create synonyms
        create_synonym(db_session, word_id=word.id, synonym="joyful")
        create_synonym(db_session, word_id=word.id, synonym="cheerful")

        # Refresh the word to load relationships
        db_session.refresh(word)

        # Verify the relationship
        assert len(word.synonyms) == 2
        synonym_words = [syn.synonym for syn in word.synonyms]
        assert "joyful" in synonym_words
        assert "cheerful" in synonym_words

    def test_empty_synonym_validation(self, db_session):
        """Test that empty synonyms are not allowed."""
        # Create a word
        word = Words(word="happy", language="english")
        db_session.add(word)
        db_session.commit()

        # Attempt to create a synonym with an empty string
        with pytest.raises(ValueError, match="Synonym cannot be empty"):
            create_synonym(db_session, word_id=word.id, synonym="")

        # Attempt to create a synonym with whitespace only
        with pytest.raises(ValueError, match="Synonym cannot be empty"):
            create_synonym(db_session, word_id=word.id, synonym="   ")
