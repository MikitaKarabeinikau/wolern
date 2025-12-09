import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Users, Vocabulary, Words
from backend.src.services.vocabulary_service import add_new_vocabulary_word
from backend.src.database import models
from backend.src.core.word import Word
from backend.src.database.crud.words import (
    add_word,
    get_all_words_from_db,
    get_word_id_by_word,
)

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
    user = Users(id=1, username="testuser", email="testuser@example.com")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_vocabulary(db_session, test_user):
    """Create a test vocabulary."""
    vocabulary = Vocabulary(id=1, user_id=test_user.id, name="Test Vocabulary")
    db_session.add(vocabulary)
    db_session.commit()
    return vocabulary


class TestVocabularyService:
    """Test suite for the vocabulary service."""

    def test_add_word_with_full_info(self, db_session):
        """Test adding a new vocabulary word that doesn't exist in the base words table."""
        word = Word(
            word="cat",
            language="english",
            translation={"russian": ["кот", "кошка"]},
            synonyms=["feline", "kitty"],
            definition={
                "noun": ["a small domesticated carnivorous mammal", "a feline animal"]
            },
            examples={"noun": ["The cat sat on the mat.", "She has a pet cat."]},
            part_of_speech=["noun", "verb"],
            date_added="2024-01-01",
            tags=["animal", "pet"],
            frequency=0.456,
            warnings=["common"],
        )

        add_word(db=db_session, word=word)

        all_words = get_all_words_from_db(db_session)
        print(all_words)
        assert any(
            w.word == "cat" for w in all_words
        ), "Word 'cat' was not added to the database."

        cat_id = get_word_id_by_word(db_session, "cat")

        assert cat_id is not None, "Word ID for 'cat' should not be None."
        assert cat_id == 1, f"Expected word ID to be 1, got {cat_id}."

        cat_translations = (
            db_session.query(models.Translations)
            .filter(models.Translations.word_id == cat_id)
            .all()
        )
        assert (
            len(cat_translations) == 2
        ), f"Expected 2 translations for 'cat', got {len(cat_translations)}."
        translation_texts = [t.translation for t in cat_translations]
        assert "кот" in translation_texts, "'кот' translation not found for 'cat'."
        assert "кошка" in translation_texts, "'кошка' translation not found for 'cat'."

        cat_definitions = (
            db_session.query(models.Definitions)
            .filter(models.Definitions.word_id == cat_id)
            .all()
        )
        assert (
            len(cat_definitions) == 2
        ), f"Expected 2 definitions for 'cat', got {len(cat_definitions)}."
        definition_texts = [d.definition for d in cat_definitions]
        assert (
            "a small domesticated carnivorous mammal" in definition_texts
        ), "Expected definition not found for 'cat'."
        assert (
            "a feline animal" in definition_texts
        ), "Expected definition not found for 'cat'."

        cat_examples = (
            db_session.query(models.Examples)
            .filter(models.Examples.word_id == cat_id)
            .all()
        )
        assert (
            len(cat_examples) == 2
        ), f"Expected 2 examples for 'cat', got {len(cat_examples)}."
        example_texts = [e.example for e in cat_examples]
        print(example_texts)
        assert (
            "The cat sat on the mat." in example_texts
        ), "Expected example not found for 'cat'."
        assert (
            "She has a pet cat." in example_texts
        ), "Expected example not found for 'cat'."

        cat_synonyms = (
            db_session.query(models.Synonyms)
            .filter(models.Synonyms.word_id == cat_id)
            .all()
        )
        assert (
            len(cat_synonyms) == 2
        ), f"Expected 2 synonyms for 'cat', got {len(cat_synonyms)}."
        synonym_texts = [s.synonym for s in cat_synonyms]
        assert "feline" in synonym_texts, "'feline' synonym not found for 'cat'."
        assert "kitty" in synonym_texts, "'kitty' synonym not found for 'cat'."

        cat_tags = (
            db_session.query(models.Tags).filter(models.Tags.word_id == cat_id).all()
        )
        assert len(cat_tags) == 2, f"Expected 2 tags for 'cat', got {len(cat_tags)}."
        tag_texts = [t.tag for t in cat_tags]
        assert "animal" in tag_texts, "'animal' tag not found for 'cat'."
        assert "pet" in tag_texts, "'pet' tag not found for 'cat'."
