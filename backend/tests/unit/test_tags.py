"""
Unit tests for Tags CRUD operations.

Tests tag creation, retrieval, and relationships with words.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Words
from backend.src.database.crud.tags import create_tag, get_tags_by_word_id, get_tag_by_id

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


class TestTagsModel:
    """Test suite for Tags model and CRUD operations."""

    def test_create_tag(self, db_session):
        """Test creating a tag for a word."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a tag
        tag = create_tag(db_session, word_id=word.id, tag="grammar")

        # Verify the tag
        assert tag is not None
        assert tag.word_id == word.id
        assert tag.tag == "grammar"
        assert tag.id is not None

    def test_create_tag_lowercase(self, db_session):
        """Test that tags are automatically converted to lowercase."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a tag with uppercase letters
        tag = create_tag(db_session, word_id=word.id, tag="GRAMMAR")

        # Verify the tag is lowercase
        assert tag.tag == "grammar"

    def test_get_tags_by_word_id(self, db_session):
        """Test retrieving tags by word ID."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Create multiple tags
        create_tag(db_session, word_id=word.id, tag="grammar")
        create_tag(db_session, word_id=word.id, tag="vocabulary")
        create_tag(db_session, word_id=word.id, tag="beginner")

        # Retrieve tags
        tags = get_tags_by_word_id(db_session, word_id=word.id)

        # Verify the tags
        assert len(tags) == 3
        tag_names = [tag.tag for tag in tags]
        assert "grammar" in tag_names
        assert "vocabulary" in tag_names
        assert "beginner" in tag_names

    def test_get_tag_by_id(self, db_session):
        """Test retrieving a tag by its ID."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Create a tag
        tag = create_tag(db_session, word_id=word.id, tag="grammar")

        # Retrieve the tag by ID
        retrieved_tag = get_tag_by_id(db_session, id=tag.id)

        # Verify the retrieved tag
        assert retrieved_tag is not None
        assert retrieved_tag.id == tag.id
        assert retrieved_tag.tag == "grammar"
        assert retrieved_tag.word_id == word.id

    def test_get_tag_by_id_not_found(self, db_session):
        """Test retrieving a tag by an invalid ID."""
        # Attempt to retrieve a tag with a non-existent ID
        retrieved_tag = get_tag_by_id(db_session, id=999)

        # Verify the result
        assert retrieved_tag is None

    def test_multiple_words_same_tag(self, db_session):
        """Test that multiple words can have the same tag."""
        # Create two words
        word1 = Words(word="example", language="english")
        word2 = Words(word="test", language="english")
        db_session.add_all([word1, word2])
        db_session.commit()

        # Create the same tag for both words
        tag1 = create_tag(db_session, word_id=word1.id, tag="grammar")
        tag2 = create_tag(db_session, word_id=word2.id, tag="grammar")

        # Verify both tags exist
        assert tag1.tag == "grammar"
        assert tag2.tag == "grammar"
        assert tag1.word_id == word1.id
        assert tag2.word_id == word2.id
        assert tag1.id != tag2.id

    def test_tag_word_relationship(self, db_session):
        """Test the relationship between tags and words."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Create tags
        create_tag(db_session, word_id=word.id, tag="grammar")
        create_tag(db_session, word_id=word.id, tag="vocabulary")

        # Refresh the word to load relationships
        db_session.refresh(word)

        # Verify the relationship
        assert len(word.tags) == 2
        tag_names = [tag.tag for tag in word.tags]
        assert "grammar" in tag_names
        assert "vocabulary" in tag_names

    def test_duplicate_tags_for_same_word(self, db_session):
        """Test that duplicate tags cannot be created for the same word."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Create the first tag
        tag1 = create_tag(db_session, word_id=word.id, tag="grammar")

        # Verify the first tag was created
        assert tag1.tag == "grammar"

        # Return the existing tag when trying to create a duplicate
        tag2 = create_tag(db_session, word_id=word.id, tag="grammar")
        assert tag2.id == tag1.id
        assert tag2.tag == tag1.tag
        assert tag2.word_id == tag1.word_id

    def test_empty_tag_validation(self, db_session):
        """Test that empty tags are not allowed."""
        # Create a word
        word = Words(word="example", language="english")
        db_session.add(word)
        db_session.commit()

        # Attempt to create a tag with an empty string
        with pytest.raises((ValueError, Exception)):
            create_tag(db_session, word_id=word.id, tag="")
