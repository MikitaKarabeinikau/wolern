import pytest
from schemas.word import WordCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Users, Vocabulary, Words, VocabularyWords
from backend.src.services.vocabulary_service import add_new_vocabulary_word
from database import models
from backend.src.core.word import Word  

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
    user = Users(id=1,clerk_id='test_user', username="test_user", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_word(db_session):
    """Create a test word."""
    word = Words(id=1, word="dog", language="english")
    db_session.add(word)
    db_session.commit()
    return word

@pytest.fixture
def test_vocabulary(db_session, test_user):
    """Create a test vocabulary."""
    vocabulary = Vocabulary(vocabulary_id=1, user_id=test_user.id, name="Test Vocabulary")
    db_session.add(vocabulary)
    db_session.commit()
    return vocabulary

@pytest.fixture
def test_vocabulary_word(db_session, test_vocabulary, test_word):
    """Create a test vocabulary word."""
    vocab_word = VocabularyWords(id=1, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
    db_session.add(vocab_word)
    db_session.commit()
    return vocab_word

class TestVocabularyService:
    """Test suite for the vocabulary service."""

    def check_word_status_created(self, db_session, vocabulary_word_id):
        """Helper method to check if UserWordStatus is created."""
        user_word_status = (
            db_session.query(models.UserWordStatus)
            .filter_by(vocabulary_word_id=vocabulary_word_id)
            .first()
        )
        assert user_word_status is not None, "UserWordStatus was not created."

    def test_add_new_vocabulary_word_creates_new_word(self, db_session, test_vocabulary):
        """Test adding a new vocabulary word that doesn't exist in the base words table."""
        word = Word(word="cat", 
                    language="english",
                    translation={"russian": ["кот"]}, 
                    synonyms=["feline"], 
                    definition={"noun": ["a small domesticated carnivorous mammal"]}, 
                    examples={"noun": ["The cat sat on the mat."]},
                    part_of_speech=["noun"],
                    date_added="2024-01-01", 
                    tags=["animal"],
                    frequency=0.456,
                    warnings=["common"])
        word_dict = word.to_dict()
        
        vocabulary_word = add_new_vocabulary_word(
            db=db_session,
            word=word,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        # Verify the word was added to the base words table
        base_word = db_session.query(Words).filter_by(word=word_dict["word"]).first()
        assert base_word is not None
        assert base_word.word == word_dict["word"]

        # Verify the vocabulary word was added
        vocab_word = db_session.query(VocabularyWords).filter_by(word_id=base_word.id).first()
        assert vocab_word is not None
        assert vocab_word.vocabulary_id == test_vocabulary.vocabulary_id

    def test_add_new_vocabulary_word_existing_word(self, db_session, test_user, test_vocabulary):
        """Test adding a vocabulary word that already exists in the base words table."""
        # Add the word to the base words table
        word = Word(word="cat", 
                          language="english",
                          translation={"russian": ["кот"]}, 
                          synonyms=["feline"], 
                          definition={"noun": ["a small domesticated carnivorous mammal"]}, 
                          examples={"noun": ["The cat sat on the mat."]},
                          part_of_speech=["noun"],
                          date_added="2024-01-01", 
                          tags=["animal"],
                          frequency=0.456,
                          warnings=["common"])
        base_word = Words(word=word.word, language=word.language)
        db_session.add(base_word)
        db_session.commit()

        # Add the vocabulary word
        vocabulary_word = add_new_vocabulary_word(
            db=db_session,
            word=word,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        # Verify the vocabulary word was added
        vocab_word = db_session.query(VocabularyWords).filter_by(word_id=base_word.id).first()
        assert vocab_word is not None
        assert vocab_word.vocabulary_id == test_vocabulary.vocabulary_id

    def test_add_new_vocabulary_word_existing_vocab_word(self, db_session, test_user, test_vocabulary):
        """Test adding a vocabulary word that already exists in the vocabulary."""
        # Add the word to the base words table
        word = Word(word="cat", 
                          language="english",
                          translation={"russian": ["кот"]}, 
                          synonyms=["feline"], 
                          definition={"noun": ["a small domesticated carnivorous mammal"]}, 
                          examples={"noun": ["The cat sat on the mat."]},
                          part_of_speech=["noun"],
                          date_added="2024-01-01", 
                          tags=["animal"],
                          frequency=0.456,
                          warnings=["common"])
        
        base_word = Words(word=word.word, language=word.language)
        db_session.add(base_word)
        db_session.commit()

        # Add the vocabulary word
        vocab_word = VocabularyWords(
            vocabulary_id=test_vocabulary.vocabulary_id,
            word_id=base_word.id,
        )
        db_session.add(vocab_word)
        db_session.commit()

        # Attempt to add the same vocabulary word again
        vocabulary_word = add_new_vocabulary_word(
            db=db_session,
            word=word,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        # Verify the existing vocabulary word was returned
        assert vocabulary_word.vocabulary_id == vocab_word.id

    def test_add_new_vocabulary_word_rollback_on_error(self, db_session, test_user, test_vocabulary):
        """Test rollback when an error occurs during adding a vocabulary word."""
        word = Word(word="cat", 
                          language="english",
                          translation={"russian": ["кот"]}, 
                          synonyms=["feline"], 
                          definition={"noun": ["a small domesticated carnivorous mammal"]}, 
                          examples={"noun": ["The cat sat on the mat."]},
                          part_of_speech=["noun"],
                          date_added="2024-01-01", 
                          tags=["animal"],
                          frequency=0.456,
                          warnings=["common"]).to_dict()

        # Simulate an error by passing an invalid vocabulary ID
        with pytest.raises(Exception):
            add_new_vocabulary_word(
                db=db_session,
                word=word,
                vocabulary_id=999,  # Invalid vocabulary ID
            )

        # Verify the word was not added to the base words table
        base_word = db_session.query(Words).filter_by(word=word["word"]).first()
        assert base_word is None

        # Verify the vocabulary word was not added
        vocab_word = db_session.query(VocabularyWords).filter_by(word_id=999).first()
        assert vocab_word is None

    def test_add_new_vocabulary_word_create_user_word_status(self, db_session, test_user, test_vocabulary):
        """Test that adding a new vocabulary word creates a user word status."""
        word = Word(word="cat", 
                          language="english",
                          translation={"russian": ["кот"]}, 
                          synonyms=["feline"], 
                          definition={"noun": ["a small domesticated carnivorous mammal"]}, 
                          examples={"noun": ["The cat sat on the mat."]},
                          part_of_speech=["noun"],
                          date_added="2024-01-01", 
                          tags=["animal"],
                          frequency=0.456,
                          warnings=["common"])
        vocabulary_word = add_new_vocabulary_word(
            db=db_session,
            word=word,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        # Verify the user word status was created
        user_word_status = (
            db_session.query(models.UserWordStatus)
            .filter_by(vocabulary_word_id=vocabulary_word.id)
            .first()
        )
        assert user_word_status is not None

    def test_add_new_vocabulary_word_create_user_word_status_and_quiz_progress(self, db_session, test_user, test_vocabulary):
        """Test that adding a new vocabulary word creates a user word status and initializes quiz progress."""
        word = Word(word="cat", 
                          language="english",
                          translation={"russian": ["кот"]}, 
                          synonyms=["feline"], 
                          definition={"noun": ["a small domesticated carnivorous mammal"]}, 
                          examples={"noun": ["The cat sat on the mat."]},
                          part_of_speech=["noun"],
                          date_added="2024-01-01", 
                          tags=["animal"],
                          frequency=0.456,
                          warnings=["common"])
        vocabulary_word = add_new_vocabulary_word(
            db=db_session,
            word=word,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        # Verify the user word status was created
        user_word_status = (
            db_session.query(models.UserWordStatus)
            .filter_by(vocabulary_word_id=vocabulary_word.id)
            .first()
        )
        assert user_word_status is not None

        # Verify the quiz progress was initialized
        quiz_progress = (
            db_session.query(models.UserQuizProgress)
            .filter_by(user_word_status_id=user_word_status.id)
            .first()
        )
        assert quiz_progress is not None
        assert quiz_progress.correct == 0
        assert quiz_progress.wrong == 0
        assert quiz_progress.correct_streak == 0
        assert quiz_progress.wrong_streak == 0
        assert quiz_progress.learning_stage == 1