from sqlalchemy import create_engine
from backend.src.database.database import Base, sessionmaker
from sqlalchemy.orm import Session
import pytest
import backend.src.core.word as word_module
from backend.src.database.crud.words import add_word
from backend.src.services.user_word_status_service import get_user_word_status_by_vocabulary_word_id
from backend.src.database.models import UserWordStatus, UserHiddenTranslations
from backend.src.database.crud.user_hidden_translations import create_hidden_translation

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

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    from backend.src.database.models import Users
    test_user = Users(clerk_id="test_clerk_id", email="test@example.com")
    db_session.add(test_user)
    db_session.commit()
    return test_user

@pytest.fixture
def test_vocabulary(db_session, test_user):
    """Create a test vocabulary for the test user."""
    from backend.src.database.models import Vocabularies
    test_vocabulary = Vocabularies(name="Test Vocabulary", user_id=test_user.id)
    db_session.add(test_vocabulary)
    db_session.commit()
    return test_vocabulary

@pytest.fixture
def test_vocabulary_word(db_session, test_vocabulary, test_word):
    """Create a test vocabulary word linking the test word to the test vocabulary."""
    from backend.src.database.models import VocabularyWords
    test_vocab_word = VocabularyWords(
        vocabulary_id=test_vocabulary.vocabulary_id,
        word_id=test_word.id
    )
    db_session.add(test_vocab_word)
    db_session.commit()
    return test_vocab_word

class TestHiddenInfo:
    def test_hidden_translation(self, db_session, test_user, test_vocabulary, test_vocabulary_word):

        # Create UserWordStatus
        user_word_status = UserWordStatus(
            vocabulary_word_id=test_vocabulary_word.vocabulary_word_id,
            status="learning"
        )
        db_session.add(user_word_status)
        db_session.commit()

        # Create UserHiddenTranslations
        hidden_translation = create_hidden_translation(
            db_session,
            user_word_status_id=user_word_status.user_word_status_id,
            translation_id=1  # Assuming translation ID 1 exists
        )

        assert hidden_translation.user_word_status_id == user_word_status.user_word_status_id
        assert hidden_translation.translation_id == 1


    def test_get_full
