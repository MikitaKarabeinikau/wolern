import pytest
from sqlalchemy import create_engine
from backend.src.services.word_service import get_full_word_data_by_word
from backend.src.database import models
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.crud.words import add_word
import backend.src.core.word as word_module

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
def test_word(db_session):
    """Create a test word."""
    word_data = word_module.Word(
        word="cat",
        language="english",
        translation={"russian": ["кот", "кошка"]},
        synonyms=["feline", "kitty"],
        definition={"noun": ["a small domesticated carnivorous mammal", "a feline animal"]},
        examples={"noun": ["The cat sat on the mat.", "She has a pet cat."]},
        part_of_speech=["noun", "verb"],
        frequency=0.1,
        date_added="2024-01-01",
        tags=["animal", "pet"],
    )

    word = add_word(db_session, word_data)
    db_session.add(word)
    db_session.commit()
    return word

class TestWordService:
    def test_get_full_word_data_by_word(self, db_session, test_word):
        # Arrange
        word = test_word

        # Act
        result = get_full_word_data_by_word(db_session, "cat")

        # Assert
        assert result is not None
        assert result.word == "cat"
        assert len(result.definitions) == 2
        assert len(result.examples) == 2
        assert len(result.synonyms) == 2
        assert len(result.translations) == 2
        assert len(result.tags) == 2
        assert 'кот' in [t.translation for t in result.translations]
        assert 'кошка' in [t.translation for t in result.translations]
        assert 'feline' in [s.synonym for s in result.synonyms]
        assert 'kitty' in [s.synonym for s in result.synonyms]
        assert 'a small domesticated carnivorous mammal' in [d.definition for d in result.definitions]
        assert 'a feline animal' in [d.definition for d in result.definitions]
        assert 'The cat sat on the mat.' in [e.example for e in result.examples]
        assert 'She has a pet cat.' in [e.example for e in result.examples]
