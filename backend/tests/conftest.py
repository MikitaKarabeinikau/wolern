import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from src.database.models import Base, Words, User, Vocabulary, VocabularyWords

# Test database URL
TEST_DATABASE_URL = "postgresql://user:password@localhost:5432/test_wolern"

@pytest.fixture(scope="session")
def engine():
    """Create test database engine"""
    # Create test database if it doesn't exist
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)
    
    engine = create_engine(TEST_DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup: Drop all tables after tests
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(engine):
    """Create a new database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    # Rollback transaction after each test
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def sample_word(db_session):
    """Create a sample word for testing"""
    word = Words(
        word="test",
        language="en",
        frequency_rank=100
    )
    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)
    return word

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing"""
    user = User(
        clerk_id="test_clerk_123",
        username="testuser",
        email="test@example.com"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user