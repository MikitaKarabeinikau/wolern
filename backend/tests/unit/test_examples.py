import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Words
from backend.src.database.crud.examples import create_example, get_examples_by_word_id

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


def test_create_example(db_session):
    """Test creating an example for a word."""
    # Create a word
    word = Words(word="example", language="english")
    db_session.add(word)
    db_session.commit()

    # Create an example
    example = create_example(
        db_session, word_id=word.id, part_of_speech="noun", example="This is an example sentence."
    )

    # Verify the example
    assert example is not None
    assert example.word_id == word.id
    assert example.part_of_speech == "noun"
    assert example.example == "This is an example sentence."


def test_get_examples_by_word_id(db_session):
    """Test retrieving examples by word ID."""
    # Create a word
    word = Words(word="example", language="english")
    db_session.add(word)
    db_session.commit()

    # Create multiple examples
    create_example(db_session, word_id=word.id, part_of_speech="noun", example="First example.")
    create_example(db_session, word_id=word.id, part_of_speech="noun", example="Second example.")

    # Retrieve examples
    examples = get_examples_by_word_id(db_session, word_id=word.id)

    # Verify the examples
    assert len(examples) == 2
    assert examples[0].example == "First example."
    assert examples[1].example == "Second example."
