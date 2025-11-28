import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.models import Base, Words, Users, Vocabulary, VocabularyWords, Exercise, UserExercises

# Create a test database URL (PostgreSQL in-memory database)
TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/test_db"

# Create a test engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest fixture to set up and tear down the database
@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

# Test the Words model
def test_create_word(db_session):
    """Test creating a word."""
    word = Words(
        word="example",
        language="english",
        audio_url="http://example.com/audio.mp3",
        frequency=0.5,
    )
    db_session.add(word)
    db_session.commit()

    # Query the word
    result = db_session.query(Words).filter(Words.word == "example").first()
    assert result is not None
    assert result.word == "example"
    assert result.language == "english"
    assert result.audio_url == "http://example.com/audio.mp3"
    assert result.frequency == 0.5

# Test the Users model
def test_create_user(db_session):
    """Test creating a user."""
    user = Users(
        clerk_id="clerk123",
        username="testuser",
        email="testuser@example.com",
        role="user",
        native_language="english",
        preferred_language="spanish",
    )
    db_session.add(user)
    db_session.commit()

    # Query the user
    result = db_session.query(Users).filter(Users.clerk_id == "clerk123").first()
    assert result is not None
    assert result.username == "testuser"
    assert result.email == "testuser@example.com"
    assert result.role == "user"
    assert result.native_language == "english"
    assert result.preferred_language == "spanish"

# Test the Vocabulary model
def test_create_vocabulary(db_session):
    """Test creating a vocabulary."""
    user = Users(
        clerk_id="clerk123",
        username="testuser",
        email="testuser@example.com",
    )
    db_session.add(user)
    db_session.commit()

    vocabulary = Vocabulary(
        name="Test Vocabulary",
        user_id=user.id,
    )
    db_session.add(vocabulary)
    db_session.commit()

    # Query the vocabulary
    result = db_session.query(Vocabulary).filter(Vocabulary.name == "Test Vocabulary").first()
    assert result is not None
    assert result.name == "Test Vocabulary"
    assert result.user_id == user.id

# Test the VocabularyWords model
def test_create_vocabulary_word(db_session):
    """Test adding a word to a vocabulary."""
    user = Users(
        clerk_id="clerk123",
        username="testuser",
        email="testuser@example.com",
    )
    db_session.add(user)
    db_session.commit()

    vocabulary = Vocabulary(
        name="Test Vocabulary",
        user_id=user.id,
    )
    db_session.add(vocabulary)
    db_session.commit()

    word = Words(
        word="example",
        language="english",
    )
    db_session.add(word)
    db_session.commit()

    vocab_word = VocabularyWords(
        vocabulary_id=vocabulary.vocabulary_id,
        word_id=word.id,
    )
    db_session.add(vocab_word)
    db_session.commit()

    # Query the vocabulary word
    result = db_session.query(VocabularyWords).filter(VocabularyWords.vocabulary_id == vocabulary.vocabulary_id).first()
    assert result is not None
    assert result.vocabulary_id == vocabulary.vocabulary_id
    assert result.word_id == word.id

# Test the UserExercises model
def test_create_user_exercise(db_session):
    """Test creating a user exercise."""
    user = Users(
        clerk_id="clerk123",
        username="testuser",
        email="testuser@example.com",
    )
    db_session.add(user)
    db_session.commit()

    word = Words(
        word="example",
        language="english",
    )
    db_session.add(word)
    db_session.commit()

    exercise = Exercise(
        word_id=word.id,
        difficulty="medium",
        part_of_speech="noun",
        question="What is the meaning of 'example'?",
        explanation="An example is a representative form or pattern.",
        hints={"hint1": "Think of a sample."},
    )
    db_session.add(exercise)
    db_session.commit()

    user_exercise = UserExercises(
        user_id=user.id,
        exercise_id=exercise.id,
        word_id=word.id,
    )
    db_session.add(user_exercise)
    db_session.commit()

    # Query the user exercise
    result = db_session.query(UserExercises).filter(UserExercises.user_id == user.id).first()
    assert result is not None
    assert result.user_id == user.id
    assert result.exercise_id == exercise.id
    assert result.word_id == word.id