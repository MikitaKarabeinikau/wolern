import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Words
from backend.src.database.crud.definitions import (
    create_definition,
    get_definitions_by_word_id,
    get_definition_by_id,
)

# Create a test database URL
TEST_DATABASE_URL = "postgresql+psycopg2://woler_test_user:password@localhost/test_db"

# Create a test engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Set up and tear down the test database session."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_create_definition(db_session):
    """Test creating a definition for a word."""
    # Create a word
    word = Words(word="example", language="english")
    db_session.add(word)
    db_session.commit()

    # Create a definition
    definition = create_definition(
        db_session,
        word_id=word.id,
        part_of_speech="noun",
        definition="A representative form or pattern.",
    )

    # Verify the definition
    assert definition is not None
    assert definition.word_id == word.id
    assert definition.part_of_speech == "noun"
    assert definition.definition == "A representative form or pattern."


def test_get_definitions_by_word_id(db_session):
    """Test retrieving definitions by word ID."""
    # Create a word
    word = Words(word="example", language="english")
    db_session.add(word)
    db_session.commit()

    # Create multiple definitions
    create_definition(
        db_session,
        word_id=word.id,
        part_of_speech="noun",
        definition="A representative form or pattern.",
    )
    create_definition(
        db_session,
        word_id=word.id,
        part_of_speech="verb",
        definition="To illustrate or demonstrate.",
    )

    # Retrieve definitions
    definitions = get_definitions_by_word_id(db_session, word_id=word.id)

    # Verify the definitions
    assert len(definitions) == 2
    assert definitions[0].part_of_speech == "noun"
    assert definitions[1].part_of_speech == "verb"


def test_get_definition_by_id(db_session):
    """Test retrieving a definition by its ID."""
    # Create a word
    word = Words(word="example", language="english")
    db_session.add(word)
    db_session.commit()

    # Create a definition
    definition = create_definition(
        db_session,
        word_id=word.id,
        part_of_speech="noun",
        definition="A representative form or pattern.",
    )

    # Retrieve the definition by ID
    retrieved_definition = get_definition_by_id(db_session, definition_id=definition.id)

    # Verify the retrieved definition
    assert retrieved_definition is not None
    assert retrieved_definition.id == definition.id
    assert retrieved_definition.definition == "A representative form or pattern."


def test_get_definition_by_id_not_found(db_session):
    """Test retrieving a definition by an invalid ID."""
    # Attempt to retrieve a definition with a non-existent ID
    retrieved_definition = get_definition_by_id(db_session, definition_id=999)

    # Verify the result
    assert retrieved_definition is None
