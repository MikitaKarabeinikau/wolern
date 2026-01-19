import pytest
from backend.src.services.vocabulary_service import create_vocabulary_word_secure
from sqlalchemy import create_engine
from backend.src.services.word_service import get_full_word_data_by_word, is_word_in_user_vocabularies
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
def test_word_1(db_session):
    word_data = word_module.Word(
        word="dog",
        language="english",
        translation={"russian": ["собака"]},
        synonyms=["canine", "puppy"],
        definition={"noun": ["a domesticated carnivorous mammal"]},
        examples={"noun": ["The dog barked loudly."]},
        part_of_speech=["noun"],
        frequency=0.2,
        date_added="2024-01-01",
        tags=["animal", "pet"],
    )
    word = add_word(db_session, word_data)
    db_session.add(word)
    db_session.commit()
    return word

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
    user = models.Users(
        clerk_id="test_clerk_id",
        username="testuser",
        email="testuser@example.com"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_vocabulary(db_session, test_user, test_word):
    """Create a test vocabulary for the user."""
    vocabulary = models.Vocabulary(
        user_id=test_user.id,
        name="Test Vocabulary",
    )
    db_session.add(vocabulary)
    db_session.commit()

    vocab_word = models.VocabularyWords(
        vocabulary_id=vocabulary. vocabulary_id,
        word_id=test_word.id
    )
    db_session.add(vocab_word)
    db_session.commit()
    return vocabulary

@pytest.fixture
def test_vocabulary_word(db_session, test_vocabulary, test_word):
    """Create a test vocabulary word linking the vocabulary and word."""
    vocab_word = models.VocabularyWords(
        vocabulary_id=test_vocabulary.vocabulary_id,
        word_id=test_word.id
    )
    db_session.add(vocab_word)
    db_session.commit()
    return vocab_word

class TestWordService:
    def test_get_full_word_data_by_word(self, db_session, test_word):

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

class TestIsWordInUserVocabularies:
    def test_is_word_in_user_vocabularies_found(self, db_session, test_user, test_word,test_vocabulary):

        # Act
        result = is_word_in_user_vocabularies(db_session, test_user.id, test_word.id)
        print(result)

        # Assert
        assert result is True

    def test_is_word_in_user_vocabularies_not_found(self, db_session, test_user, test_word_1):

        # Act
        result = is_word_in_user_vocabularies(db_session, test_user.id, test_word_1.id)

        print(result)
        # Assert
        assert result is False

    def test_is_word_in_user_vocabularies_no_user(self, db_session, test_word):

        # Act
        result = is_word_in_user_vocabularies(db_session, 9999, test_word.id)

        # Assert
        assert result is False

    def test_get_vocabulary_names_by_word_id(self, db_session, test_user, test_word, test_vocabulary):

        from backend.src.services.word_service import get_user_vocabularies_names_by_word_id

        # Act
        result = get_user_vocabularies_names_by_word_id(db_session, test_user.id, test_word.id)

        # Assert
        assert len(result) == 1
        assert result[0] == "Test Vocabulary"

    def test_several_vocabularies_have_word(self, db_session, test_user, test_word, test_vocabulary):

        from backend.src.services.word_service import get_user_vocabularies_names_by_word_id

        # Arrange
        vocabulary2 = models.Vocabulary(
            user_id=test_user.id,
            name="Second Vocabulary",
        )
        db_session.add(vocabulary2)
        db_session.commit()

        vocab_word2 = models.VocabularyWords(
            vocabulary_id=vocabulary2.vocabulary_id,
            word_id=test_word.id
        )
        db_session.add(vocab_word2)
        db_session.commit()

        # Act
        result = get_user_vocabularies_names_by_word_id(db_session, test_user.id, test_word.id)

        # Assert
        assert len(result) == 2
        assert "Test Vocabulary" in result
        assert "Second Vocabulary" in result

    def test_get_word_relations_with_user_vocabularies(self, db_session, test_user, test_word, test_vocabulary):

        from backend.src.services.word_service import get_word_relations_with_user_vocabularies

        vocabulary2 = models.Vocabulary(
            user_id=test_user.id,
            name="Second Vocabulary",
        )
        db_session.add(vocabulary2)
        db_session.commit()

        vocab_word2 = models.VocabularyWords(
            vocabulary_id=vocabulary2.vocabulary_id,
            word_id=test_word.id
        )
        db_session.add(vocab_word2)
        db_session.commit()

        # Act
        result = get_word_relations_with_user_vocabularies(db_session, test_user.id, test_word.id)

        # Assert
        assert result["word_id"] == test_word.id
        assert result["word"] == test_word.word
        assert result["vocabulary_count"] == 2
        assert len(result["vocabulary_names"]) == 2
        assert "Test Vocabulary" in result["vocabulary_names"]
        assert "Second Vocabulary" in result["vocabulary_names"]
        assert set(result["vocabulary_names"]) == {"Test Vocabulary", "Second Vocabulary"}

    def test_change_vocabulary(self, db_session, test_user, test_word, test_vocabulary):

        from backend.src.services.word_service import change_vocabulary
        from backend.src.database.crud.vocabulary_words import get_vocabulary_word_by_vocab_and_word_id

        # Arrange
        new_vocabulary = models.Vocabulary(
            user_id=test_user.id,
            name="New Vocabulary",
        )
        db_session.add(new_vocabulary)
        db_session.commit()

        # Act
        change_vocabulary(db_session, test_word.id, new_vocabulary.vocabulary_id, test_vocabulary.vocabulary_id)

        # Assert
        old_vocab_word = get_vocabulary_word_by_vocab_and_word_id(db_session, test_vocabulary.vocabulary_id, test_word.id)
        new_vocab_word = get_vocabulary_word_by_vocab_and_word_id(db_session, new_vocabulary.vocabulary_id, test_word.id)

        assert old_vocab_word is None
        assert new_vocab_word is not None
        assert new_vocab_word.word_id == test_word.id
        assert new_vocab_word.vocabulary_id == new_vocabulary.vocabulary_id
