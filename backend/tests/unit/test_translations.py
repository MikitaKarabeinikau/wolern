"""
Unit tests for Translations CRUD operations.

Tests translation creation, retrieval, and relationships with words.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Words
from backend.src.database.crud.translations import (
    create_translation,
    get_translations_by_word_id,
    get_translation_by_id,
    get_translations_by_language,
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


class TestTranslationsModel:
    """Test suite for Translations model and CRUD operations."""

    def test_create_translation(self, db_session):
        """Test creating a translation for a word."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a translation
        translation = create_translation(
            db_session, word_id=word.id, language="french", translation="chat"
        )

        # Verify the translation
        assert translation is not None
        assert translation.word_id == word.id
        assert translation.language == "french"
        assert translation.translation == "chat"
        assert translation.id is not None

    def test_create_translation_lowercase_language(self, db_session):
        """Test that language is automatically converted to lowercase."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a translation with uppercase language
        translation = create_translation(
            db_session, word_id=word.id, language="FRENCH", translation="chat"
        )

        # Verify the language is lowercase
        assert translation.language == "french"

    def test_get_translations_by_word_id(self, db_session):
        """Test retrieving translations by word ID."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create multiple translations
        create_translation(db_session, word_id=word.id, language="french", translation="chat")
        create_translation(db_session, word_id=word.id, language="spanish", translation="gato")
        create_translation(db_session, word_id=word.id, language="german", translation="katze")

        # Retrieve translations
        translations = get_translations_by_word_id(db_session, word_id=word.id)

        # Verify the translations
        assert len(translations) == 3
        languages = [t.language for t in translations]
        assert "french" in languages
        assert "spanish" in languages
        assert "german" in languages

    def test_get_translation_by_id(self, db_session):
        """Test retrieving a translation by its ID."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a translation
        translation = create_translation(
            db_session, word_id=word.id, language="french", translation="chat"
        )

        # Retrieve the translation by ID
        retrieved_translation = get_translation_by_id(db_session, id=translation.id)

        # Verify the retrieved translation
        assert retrieved_translation is not None
        assert retrieved_translation.id == translation.id
        assert retrieved_translation.language == "french"
        assert retrieved_translation.translation == "chat"
        assert retrieved_translation.word_id == word.id

    def test_get_translation_by_id_not_found(self, db_session):
        """Test retrieving a translation by an invalid ID."""
        # Attempt to retrieve a translation with a non-existent ID
        retrieved_translation = get_translation_by_id(db_session, id=999)

        # Verify the result
        assert retrieved_translation is None

    def test_get_translations_by_language(self, db_session):
        """Test retrieving all translations for a specific language."""
        # Create multiple words
        word1 = Words(word="cat", language="english")
        word2 = Words(word="dog", language="english")
        word3 = Words(word="bird", language="english")
        db_session.add_all([word1, word2, word3])
        db_session.commit()

        # Create translations in French
        create_translation(db_session, word_id=word1.id, language="french", translation="chat")
        create_translation(db_session, word_id=word2.id, language="french", translation="chien")
        create_translation(db_session, word_id=word3.id, language="spanish", translation="pájaro")

        # Retrieve French translations
        french_translations = get_translations_by_language(db_session, language="french")

        # Verify the translations
        assert len(french_translations) == 2
        french_words = [t.translation for t in french_translations]
        assert "chat" in french_words
        assert "chien" in french_words

    def test_duplicate_translation_same_language(self, db_session):
        """Test that duplicate translations in
        the same language cannot be created for the same word."""

        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create the first translation
        translation1 = create_translation(
            db_session, word_id=word.id, language="french", translation="chat"
        )

        # Verify the first translation was created
        assert translation1.translation == "chat"

        # Return the existing translation when trying to create a duplicate
        translation2 = create_translation(
            db_session, word_id=word.id, language="french", translation="chat"
        )
        assert translation2.id == translation1.id
        assert translation2.translation == translation1.translation
        assert translation2.word_id == translation1.word_id

    def test_multiple_translations_different_languages(self, db_session):
        """Test that a word can have translations in multiple languages."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create translations in different languages
        translation1 = create_translation(
            db_session, word_id=word.id, language="french", translation="chat"
        )
        translation2 = create_translation(
            db_session, word_id=word.id, language="spanish", translation="gato"
        )
        translation3 = create_translation(
            db_session, word_id=word.id, language="german", translation="katze"
        )

        # Verify all translations exist
        assert translation1.language == "french"
        assert translation2.language == "spanish"
        assert translation3.language == "german"

    def test_translation_word_relationship(self, db_session):
        """Test the relationship between translations and words."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Create translations
        create_translation(db_session, word_id=word.id, language="french", translation="chat")
        create_translation(db_session, word_id=word.id, language="spanish", translation="gato")

        # Refresh the word to load relationships
        db_session.refresh(word)

        # Verify the relationship
        assert len(word.translations) == 2
        languages = [t.language for t in word.translations]
        assert "french" in languages
        assert "spanish" in languages

    def test_empty_translation_validation(self, db_session):
        """Test that empty translations are not allowed."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Attempt to create a translation with an empty string
        with pytest.raises(ValueError, match="Translation cannot be empty"):
            create_translation(db_session, word_id=word.id, language="french", translation="")

        # Attempt to create a translation with whitespace only
        with pytest.raises(ValueError, match="Translation cannot be empty"):
            create_translation(db_session, word_id=word.id, language="french", translation="   ")

    def test_empty_language_validation(self, db_session):
        """Test that empty language is not allowed."""
        # Create a word
        word = Words(word="cat", language="english")
        db_session.add(word)
        db_session.commit()

        # Attempt to create a translation with an empty language
        with pytest.raises(ValueError, match="Language cannot be empty"):
            create_translation(db_session, word_id=word.id, language="", translation="chat")
