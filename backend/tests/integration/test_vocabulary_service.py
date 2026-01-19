import pytest
from schemas.word import WordCreate, WordWithFullDataResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from backend.src.database.models import Users, Vocabulary, Words, VocabularyWords
from backend.src.services.vocabulary_service import add_new_vocabulary_word, delete_word_from_vocabulary_secure, get_all_words_in_vocabulary_with_data
from backend.src.database import models
from backend.src.core.word import Word
import backend.src.core.word as word

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

    def test_delete_word_from_vocabulary_secure_raises_error_for_nonexistent_word(self, db_session, test_user, test_vocabulary):
        """Test that deleting a non-existent word from a vocabulary raises an error."""
        with pytest.raises(ValueError) as excinfo:
            delete_word_from_vocabulary_secure(
                db=db_session,
                vocabulary_id=test_vocabulary.vocabulary_id,
                word_id=9999  # Non-existent word ID
            )
        assert "Word not found in the specified vocabulary." in str(excinfo.value)

    def test_delete_word_from_vocabulary_secure_deletes_word(self, db_session, test_user, test_vocabulary, test_word, test_vocabulary_word):
        """Test that deleting a word from a vocabulary works correctly."""
        delete_word_from_vocabulary_secure(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id,
            word_id=test_word.id
        )

        # Verify the vocabulary word was deleted
        vocab_word = (
            db_session.query(VocabularyWords)
            .filter_by(vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
            .first()
        )
        assert vocab_word is None

    def test_check_existens_of_word_status_after_deletion(self, db_session, test_user, test_vocabulary, test_word, test_vocabulary_word):
        """Test that the user word status is deleted when a word is removed from a vocabulary."""
        delete_word_from_vocabulary_secure(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id,
            word_id=test_word.id
        )

        # Verify the user word status was deleted
        user_word_status = (
            db_session.query(models.UserWordStatus)
            .filter_by(vocabulary_word_id=test_vocabulary_word.id)
            .first()
        )
        assert user_word_status is None

    def test_create_vocabulary_word_secure_success(self, db_session, test_user, test_vocabulary, test_word):
        """Test successfully creating a vocabulary word with security check."""
        from backend.src.services.vocabulary_service import create_vocabulary_word_secure

        vocab_word = create_vocabulary_word_secure(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id,
            word=test_word
        )

        assert vocab_word is not None
        assert vocab_word.vocabulary_id == test_vocabulary.vocabulary_id
        assert vocab_word.word_id == test_word.id

    def test_create_vocabulary_word_secure_invalid_vocabulary(self, db_session, test_word):
        """Test that creating a vocabulary word with invalid vocabulary raises error."""
        from backend.src.services.vocabulary_service import create_vocabulary_word_secure

        with pytest.raises(ValueError) as excinfo:
            create_vocabulary_word_secure(
                db=db_session,
                vocabulary_id=9999,
                word=test_word
            )
        assert "Vocabulary does not belong to any user." in str(excinfo.value)

    def test_get_all_vocabulary_words_by_vocabulary_id_empty(self, db_session, test_user, test_vocabulary):
        """Test getting vocabulary words from an empty vocabulary."""
        from backend.src.services.vocabulary_service import get_all_vocabulary_words_by_vocabulary_id

        vocab_words = get_all_vocabulary_words_by_vocabulary_id(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id
        )

        assert vocab_words == []

    def test_get_all_vocabulary_words_by_vocabulary_id_multiple_words(self, db_session, test_user, test_vocabulary):
        """Test getting multiple vocabulary words from a vocabulary."""
        from backend.src.services.vocabulary_service import get_all_vocabulary_words_by_vocabulary_id

        word1 = Words(id=10, word="cat", language="english")
        word2 = Words(id=11, word="dog", language="english")
        word3 = Words(id=12, word="bird", language="english")
        db_session.add_all([word1, word2, word3])
        db_session.commit()

        vocab_word1 = VocabularyWords(vocabulary_id=test_vocabulary.vocabulary_id, word_id=word1.id)
        vocab_word2 = VocabularyWords(vocabulary_id=test_vocabulary.vocabulary_id, word_id=word2.id)
        vocab_word3 = VocabularyWords(vocabulary_id=test_vocabulary.vocabulary_id, word_id=word3.id)
        db_session.add_all([vocab_word1, vocab_word2, vocab_word3])
        db_session.commit()

        vocab_words = get_all_vocabulary_words_by_vocabulary_id(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id
        )

        assert len(vocab_words) == 3
        word_ids = [vw.word_id for vw in vocab_words]
        assert word1.id in word_ids
        assert word2.id in word_ids
        assert word3.id in word_ids

    def test_get_all_words_in_vocabulary_with_data_empty_vocabulary(self, db_session, test_user, test_vocabulary):
        """Test getting word data from an empty vocabulary returns empty dict."""
        words_data = get_all_words_in_vocabulary_with_data(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id
        )

        assert words_data == {}

    def test_delete_word_from_vocabulary_secure_invalid_vocabulary(self, db_session, test_word):
        """Test that deleting a word from invalid vocabulary raises error."""
        with pytest.raises(ValueError) as excinfo:
            delete_word_from_vocabulary_secure(
                db=db_session,
                vocabulary_id=9999,
                word_id=test_word.id
            )
        assert "Vocabulary does not belong to any user." in str(excinfo.value)

    def test_add_new_vocabulary_word_with_missing_fields(self, db_session, test_vocabulary):
        """Test adding a word with minimal/missing optional fields."""
        word_minimal = word.Word(
            word="test",
            language="english",
            translation={},
            synonyms=[],
            definition={},
            examples={},
            part_of_speech=[],
            date_added="2024-01-01",
            tags=[],
            frequency=0.0,
            warnings=[]
        )

        vocabulary_word = add_new_vocabulary_word(
            db=db_session,
            word=word_minimal,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        assert vocabulary_word is not None
        base_word = db_session.query(Words).filter_by(word="test").first()
        assert base_word is not None

    def test_get_all_words_in_vocabulary_with_data(self, db_session, test_user, test_vocabulary):
        word_1 = word.Word(word="cat",
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
        word_2 = word.Word(word="bird",
                          language="english",
                          translation={"russian": ["птица"]},
                          synonyms=["avian"],
                          definition={"noun": ["a warm-blooded egg-laying vertebrate"]},
                          examples={"noun": ["The bird sang a song."]},
                          part_of_speech=["noun"],
                          date_added="2024-01-02",
                          tags=["animal"],
                          frequency=0.345,
                          warnings=["common"])
        vocab_word_1 = add_new_vocabulary_word(
            db=db_session,
            word=word_1,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )
        vocab_word_2 = add_new_vocabulary_word(
            db=db_session,
            word=word_2,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )
        words_with_data = get_all_words_in_vocabulary_with_data(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        assert len(words_with_data) == 2
        assert "cat" in words_with_data
        assert "bird" in words_with_data

        # Test cat data
        cat_data = words_with_data["cat"]
        assert cat_data["word"] == "cat"
        assert cat_data["language"] == "english"

        # Translations are returned as a list of objects
        assert isinstance(cat_data["translations"], list)
        assert len(cat_data["translations"]) > 0
        russian_translation = next((t for t in cat_data["translations"] if t["language"] == "russian"), None)
        assert russian_translation is not None
        assert russian_translation["translation"] == "кот"

        # Synonyms are a list of synonym objects
        assert isinstance(cat_data["synonyms"], list)
        assert len(cat_data["synonyms"]) > 0
        assert cat_data["synonyms"][0]["synonym"] == "feline"

        # Definitions are a list of definition objects
        assert isinstance(cat_data["definitions"], list)
        assert len(cat_data["definitions"]) > 0
        noun_definition = next((d for d in cat_data["definitions"] if d["part_of_speech"] == "noun"), None)
        assert noun_definition is not None
        assert noun_definition["definition"] == "a small domesticated carnivorous mammal"

        # Examples are a list of example objects
        assert isinstance(cat_data["examples"], list)
        assert len(cat_data["examples"]) > 0
        noun_example = next((e for e in cat_data["examples"] if e["part_of_speech"] == "noun"), None)
        assert noun_example is not None
        assert noun_example["example"] == "The cat sat on the mat."

        # Tags are a list of tag objects - extract the tag field
        assert isinstance(cat_data["tags"], list)
        assert len(cat_data["tags"]) > 0
        tag_values = [t["tag"] for t in cat_data["tags"]]
        assert "animal" in tag_values

        assert cat_data["frequency"] == 0.456

        # Warnings are a list of warning objects
        assert isinstance(cat_data["warnings"], list)
        assert len(cat_data["warnings"]) > 0
        assert cat_data["warnings"][0]["warning_message"] == "common"

        # Test bird data
        bird_data = words_with_data["bird"]
        assert bird_data["word"] == "bird"
        assert bird_data["language"] == "english"

        russian_translation_bird = next((t for t in bird_data["translations"] if t["language"] == "russian"), None)
        assert russian_translation_bird is not None
        assert russian_translation_bird["translation"] == "птица"

        assert len(bird_data["synonyms"]) > 0
        assert bird_data["synonyms"][0]["synonym"] == "avian"

        assert len(bird_data["definitions"]) > 0
        assert len(bird_data["examples"]) > 0

        # Extract tag values for bird
        bird_tag_values = [t["tag"] for t in bird_data["tags"]]
        assert "animal" in bird_tag_values

        assert bird_data["frequency"] == 0.345

    def test_get_all_words_in_vocabulary_with_multiple_data(self, db_session, test_user, test_vocabulary):
        """Test getting words with multiple translations, definitions, examples, and tags."""
        word_1 = word.Word(
            word="run",
            language="english",
            translation={
                "russian": ["бегать", "убегать"],
                "polish": ["biegać"]
            },
            synonyms=["sprint", "jog", "dash"],
            definition={
                "verb": [
                    "move at a speed faster than a walk",
                    "be in charge of; manage",
                    "operate or function"
                ],
                "noun": [
                    "an act or spell of running",
                    "a continuous stretch or period"
                ]
            },
            examples={
                "verb": [
                    "He runs a successful business.",
                    "The engine runs smoothly."
                ],
                "noun": [
                    "I went for a morning run.",
                    "The play had a long run on Broadway."
                ]
            },
            part_of_speech=["verb", "noun"],
            date_added="2024-01-01",
            tags=["common", "sports", "business", "movement"],
            frequency=0.89,
            warnings=["irregular verb", "multiple meanings"]
        )

        word_2 = word.Word(
            word="book",
            language="english",
            translation={
                "russian": ["книга", "заказывать"],
                "polish": ["książka", "rezerwować"]
            },
            synonyms=["volume", "tome", "publication", "reserve"],
            definition={
                "noun": [
                    "a written or printed work consisting of pages",
                    "a set of tickets or stamps bound together"
                ],
                "verb": [
                    "reserve accommodation, a ticket, etc.",
                    "make an official record of"
                ]
            },
            examples={
                "noun": [
                    "I read a fascinating book last night.",
                    "He bought a book of stamps.",
                    "She keeps a book of all expenses."
                ],
                "verb": [
                    "I need to book a hotel for next week.",
                    "The officer booked him for speeding."
                ]
            },
            part_of_speech=["noun", "verb"],
            date_added="2024-01-02",
            tags=["common", "education", "travel", "literature"],
            frequency=0.92,
            warnings=["noun-verb confusion", "common"]
        )

        vocab_word_1 = add_new_vocabulary_word(
            db=db_session,
            word=word_1,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )
        vocab_word_2 = add_new_vocabulary_word(
            db=db_session,
            word=word_2,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        words_with_data = get_all_words_in_vocabulary_with_data(
            db=db_session,
            vocabulary_id=test_vocabulary.vocabulary_id,
        )

        assert len(words_with_data) == 2
        assert "run" in words_with_data
        assert "book" in words_with_data

        # Test run data with multiple translations
        run_data = words_with_data["run"]
        assert run_data["word"] == "run"
        assert run_data["language"] == "english"

        # Check multiple translations
        assert isinstance(run_data["translations"], list)
        assert len(run_data["translations"]) == 3  # russian, spanish, french

        russian_trans = next((t for t in run_data["translations"] if t["language"] == "russian"), None)
        assert russian_trans is not None
        assert russian_trans["translation"] in ["бегать", "убегать"]

        polish_trans = next((t for t in run_data["translations"] if t["language"] == "polish"), None)
        assert polish_trans is not None
        assert polish_trans["translation"] == "biegać"


        # Check multiple synonyms
        assert isinstance(run_data["synonyms"], list)
        assert len(run_data["synonyms"]) == 3
        synonym_values = [s["synonym"] for s in run_data["synonyms"]]
        assert "sprint" in synonym_values
        assert "jog" in synonym_values
        assert "dash" in synonym_values

        # Check multiple definitions for different parts of speech
        assert isinstance(run_data["definitions"], list)
        assert len(run_data["definitions"]) >= 5  # 3 verb + 2 noun definitions

        verb_definitions = [d for d in run_data["definitions"] if d["part_of_speech"] == "verb"]
        assert len(verb_definitions) == 3
        verb_def_texts = [d["definition"] for d in verb_definitions]
        assert "move at a speed faster than a walk" in verb_def_texts
        assert "be in charge of; manage" in verb_def_texts
        assert "operate or function" in verb_def_texts

        noun_definitions = [d for d in run_data["definitions"] if d["part_of_speech"] == "noun"]
        assert len(noun_definitions) == 2
        noun_def_texts = [d["definition"] for d in noun_definitions]
        assert "an act or spell of running" in noun_def_texts
        assert "a continuous stretch or period" in noun_def_texts

        # Check multiple examples for different parts of speech
        assert isinstance(run_data["examples"], list)
        assert len(run_data["examples"]) >= 4

        verb_examples = [e for e in run_data["examples"] if e["part_of_speech"] == "verb"]
        assert len(verb_examples) == 2
        verb_example_texts = [e["example"] for e in verb_examples]
        assert "He runs a successful business." in verb_example_texts
        assert "The engine runs smoothly." in verb_example_texts

        noun_examples = [e for e in run_data["examples"] if e["part_of_speech"] == "noun"]
        assert len(noun_examples) == 2
        noun_example_texts = [e["example"] for e in noun_examples]
        assert "I went for a morning run." in noun_example_texts
        assert "The play had a long run on Broadway." in noun_example_texts

        # Check multiple tags
        assert isinstance(run_data["tags"], list)
        assert len(run_data["tags"]) == 4
        tag_values = [t["tag"] for t in run_data["tags"]]
        assert "common" in tag_values
        assert "sports" in tag_values
        assert "business" in tag_values
        assert "movement" in tag_values

        assert run_data["frequency"] == 0.89

        # Check multiple warnings
        assert isinstance(run_data["warnings"], list)
        assert len(run_data["warnings"]) == 2
        warning_messages = [w["warning_message"] for w in run_data["warnings"]]
        assert "irregular verb" in warning_messages
        assert "multiple meanings" in warning_messages

        # Test book data with multiple translations and definitions
        book_data = words_with_data["book"]
        assert book_data["word"] == "book"
        assert book_data["language"] == "english"

        # Check multiple translations for book
        assert isinstance(book_data["translations"], list)
        assert len(book_data["translations"]) == 4  # russian, polish

        russian_book_trans = next((t for t in book_data["translations"] if t["language"] == "russian"), None)
        assert russian_book_trans is not None
        assert russian_book_trans["translation"] in ["книга", "заказывать"]

        polish_book_trans = next((t for t in book_data["translations"] if t["language"] == "polish"), None)
        assert polish_book_trans is not None
        assert polish_book_trans["translation"] in ["książka", "rezerwować"]


        # Check multiple synonyms for book
        assert len(book_data["synonyms"]) == 4
        book_synonym_values = [s["synonym"] for s in book_data["synonyms"]]
        assert "volume" in book_synonym_values
        assert "tome" in book_synonym_values
        assert "publication" in book_synonym_values
        assert "reserve" in book_synonym_values

        # Check multiple definitions for book
        assert len(book_data["definitions"]) >= 4  # 2 noun + 2 verb definitions

        book_noun_definitions = [d for d in book_data["definitions"] if d["part_of_speech"] == "noun"]
        assert len(book_noun_definitions) == 2

        book_verb_definitions = [d for d in book_data["definitions"] if d["part_of_speech"] == "verb"]
        assert len(book_verb_definitions) == 2

        # Check multiple examples for book
        assert len(book_data["examples"]) >= 5  # 3 noun + 2 verb examples

        book_noun_examples = [e for e in book_data["examples"] if e["part_of_speech"] == "noun"]
        assert len(book_noun_examples) == 3

        book_verb_examples = [e for e in book_data["examples"] if e["part_of_speech"] == "verb"]
        assert len(book_verb_examples) == 2

        # Check multiple tags for book
        assert len(book_data["tags"]) == 4
        book_tag_values = [t["tag"] for t in book_data["tags"]]
        assert "common" in book_tag_values
        assert "education" in book_tag_values
        assert "travel" in book_tag_values
        assert "literature" in book_tag_values

        assert book_data["frequency"] == 0.92

        # Check multiple warnings for book
        assert len(book_data["warnings"]) == 2
        book_warning_messages = [w["warning_message"] for w in book_data["warnings"]]
        assert "noun-verb confusion" in book_warning_messages
        assert "common" in book_warning_messages
