from database.crud.user_translations import create_user_translation
from database.crud.vocabulary_words import create_vocabulary_word
import pytest
from services.user_content_service import list_user_synonyms_by_word_status_secure, list_user_translations_by_word_status_secure
from services.user_word_status_service import get_user_word_status_by_vocabulary_word_id
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import Base
from database import models
from backend.src.core.word import Word
import backend.src.services.auth as user_content_service
import backend.src.core.word as word_module
from backend.src.database.crud.words import add_word
import backend.src.services.user_content_service as user_content_service
import backend.src.services.user_word_status_service as user_word_status_service
from backend.src.services.auth import  OwnershipVerificationError
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
    user = models.Users(id=1, clerk_id="testuser", username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_vocabulary(db_session, test_user):
    """Create a test vocabulary."""
    vocabulary = models.Vocabulary(vocabulary_id=1, user_id=test_user.id, name="NEW_WORDS")
    db_session.add(vocabulary)
    db_session.commit()
    return vocabulary

@pytest.fixture
def test_word(db_session):
    """Create a test word."""
    word_data = word_module.Word(
        word="cat",
        language="english",
        translation={"russian": ["кот", "кошка"], "polish": ["kot", "kocia"]},
        synonyms=["feline", "kitty", "pussycat"],
        definition={"noun": ["a small domesticated carnivorous mammal", "a feline animal", "a pet animal"]},
        examples={"noun": ["The cat sat on the mat.", "She has a pet cat.", "Cats are great hunters."]},
        part_of_speech=["noun", "verb"],
        frequency=0.1,
        date_added="2024-01-01",
        tags=["animal", "pet"],
    )

    word = add_word(db_session, word_data)
    db_session.add(word)
    db_session.commit()
    return word

# ====================================USER TRANSLATIONS TEST=========================================
class TestUserTranslations:
    """Test user have a word status after adding a vocabulary word."""

    def test_add_new_vocabulary_word_creates_new_word(self, db_session, test_vocabulary,test_word):
        """Test existens of user_word_status after adding a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)

        # Verify UserWordStatus creation
        user_word_status = (
            db_session.query(models.UserWordStatus)
            .filter_by(vocabulary_word_id=test_vocabulary_word.id)
            .first()
        )
        assert user_word_status is not None, "UserWordStatus was not created."

    def test_add_user_translation_secure(self, db_session, test_vocabulary,test_word,test_user):
        """Test adding a user translation to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Add user translation
        user_translation =create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )
        user_translations = list_user_translations_by_word_status_secure(db = db_session, user_word_status_id=word_status.id, user_id=test_user.id)
        assert any(ut.translation == "котяра" for ut in user_translations), "User translation 'котяра' was not found."

        # Retrieve and verify the user translation

    def test_secure_update_user_translation(self, db_session, test_vocabulary,test_word,test_user):
        """Test secure update of a user translation."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Add user translation
        user_translation = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )

        # Securely update the user translation
        updated_user_translation = user_content_service.update_user_translation_secure(
            db=db_session,
            translation_id=user_translation.id,
            user_id=test_user.id,
            translation="котик"
        )
        # Retrieve and verify the updated user translation
        updated_translation = db_session.query(models.UserTranslations).filter_by(id=user_translation.id).first()
        assert updated_translation.translation == "котик", "User translation was not updated securely."
        assert updated_translation.id == user_translation.id, "User translation ID should remain the same after update."
        assert updated_translation.language == "russian", "User translation language should remain unchanged."

    def test_secure_update_user_translation_language(self, db_session, test_vocabulary,test_word,test_user):
        """Test secure update of a user translation language."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Add user translation
        user_translation = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )
        # Securely update the user translation language
        updated_user_translation = user_content_service.update_user_translation_secure(
            db=db_session,
            translation_id=user_translation.id,
            user_id=test_user.id,
            translation="котяра",
            language="ukrainian"
        )
        # Retrieve and verify the updated user translation
        updated_translation = db_session.query(models.UserTranslations).filter_by(id=user_translation.id).first()
        assert updated_translation.translation == "котяра", "User translation should remain unchanged."
        assert updated_translation.language == "ukrainian", "User translation language was not updated securely."
        assert updated_translation.id == user_translation.id, "User translation ID should remain the same after update."

    def test_secure_update_user_translation_none_fields(self, db_session, test_vocabulary,test_word,test_user):
        """Test secure update of a user translation with no fields provided."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Add user translation
        user_translation = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )

        # Attempt to securely update the user translation with no fields
        with pytest.raises(ValueError):
            user_content_service.update_user_translation_secure(
                db=db_session,
                translation_id=user_translation.id,
                user_id=test_user.id,
            )

    def test_secure_update_user_translation_unauthorized(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user translation by unauthorized user."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Create with correct user
        user_translation = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )
        # Attempt to update with unauthorized user
        with pytest.raises(OwnershipVerificationError):
            user_content_service.update_user_translation_secure(
                db=db_session,
                translation_id=user_translation.id,
                user_id=9999,
                translation="котик"
            )


    def test_list_translations_by_word_status_secure(self, db_session, test_vocabulary,test_word,test_user):
        """Test listing user translations by word status securely."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Add user translations
        translation1 = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )
        translation2 = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="кіт",
            language="ukrainian"
        )

        # List user translations securely
        user_translations = user_content_service.list_user_translations_by_word_status_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id
        )

        assert len(user_translations) == 2, "User translations count mismatch."
        translations_set = {ut.translation for ut in user_translations}
        assert "котяра" in translations_set, "'котяра' translation not found."
        assert "кіт" in translations_set, "'кіт' translation not found."

    def test_secure_delete_user_translation(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user translation."""
        test_vocabulary_word = create_vocabulary_word(
            db_session,
            vocabulary_id=test_vocabulary.vocabulary_id,
            word_id=test_word.id
        )
        word_status = get_user_word_status_by_vocabulary_word_id(
            db_session,
            vocabulary_word_id=test_vocabulary_word.id
        )
        assert word_status is not None, "UserWordStatus was not found."

        # Create translation
        user_translation = create_user_translation(
            db=db_session,
            user_word_status_id=word_status.id,
            translation="котяра",
            language="russian"
        )


        translation_id = user_translation.id  # Save ID before deletion

        # Delete the translation
        user_content_service.delete_user_translation_secure(
            db=db_session,
            translation_id=translation_id,
            user_id=test_user.id
        )

        # Verify deletion using the saved ID
        deleted_translation = db_session.query(models.UserTranslations).filter_by(id=translation_id).first()
        assert deleted_translation is None, "User translation was not deleted securely."

# ==================== USER EXAMPLES TESTS ====================
class TestUserExamples:
    """Test user examples CRUD operations."""

    def test_add_user_example_secure(self, db_session, test_vocabulary, test_user, test_word):
        """Test adding a user example to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )
        user_examples = user_content_service.list_user_examples_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )
        assert any(
            ue.example == "My cat loves to play." for ue in user_examples
        ), "User example 'My cat loves to play.' was not found."

    def test_secure_update_user_example(self, db_session, test_vocabulary,test_word, test_user):
        """Test secure update of a user example."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )

        updated_user_example = user_content_service.update_user_example_secure(
            db=db_session,
            example_id=user_example.id,
            user_id=test_user.id,
            example="My cat enjoys playing.",
        )

        updated_example = db_session.query(models.UserExamples).filter_by(id=user_example.id).first()
        assert updated_example.example == "My cat enjoys playing.", "User example was not updated."

    def test_secure_update_user_example_pos(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user example part of speech."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )

        updated_user_example = user_content_service.update_user_example_secure(
            db=db_session,
            example_id=user_example.id,
            user_id=test_user.id,
            part_of_speech="verb",
        )

        updated = db_session.query(models.UserExamples).filter_by(id=user_example.id).first()
        assert updated.part_of_speech == "verb", "User example part of speech was not updated."

    def test_secure_update_example_and_pos(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user example and part of speech."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)

        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )
        db_session.add(user_example)
        db_session.commit()
        db_session.refresh(user_example)

        updated_user_example = user_content_service.update_user_example_secure(
            db=db_session,
            example_id=user_example.id,
            user_id=test_user.id,
            example="My cat is playing.",
            part_of_speech="verb",
        )

        updated = db_session.query(models.UserExamples).filter_by(id=user_example.id).first()
        assert updated.example == "My cat is playing.", "User example was not updated."
        assert updated.part_of_speech == "verb", "User example part of speech was not updated."

    def test_secure_update_user_example_none_fields(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user example with no fields provided."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)

        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )


        with pytest.raises(ValueError):
            user_content_service.update_user_example_secure(
                db=db_session,
                example_id=user_example.id,
                user_id=test_user.id,
            )

    def test_secure_update_user_example_unauthorized(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user example by unauthorized user."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)

        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )
        with pytest.raises(OwnershipVerificationError):
            user_content_service.update_user_example_secure(
                db=db_session,
                example_id=user_example.id,
                user_id=9999,  # Unauthorized user ID
                example="Updated example",
            )

    def test_list_examples_by_word_status_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test listing user examples by word status securely."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        example1 = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="The cat is sleeping.",
            part_of_speech="noun",
        )
        example2 = user_content_service.create_user_example_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            example="I saw a cat yesterday.",
            part_of_speech="noun",
        )
        db_session.add(example1)
        db_session.add(example2)
        db_session.commit()

        user_examples = user_content_service.list_user_examples_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )

        assert len(user_examples) == 2, "User examples count mismatch."
        examples_set = {ue.example for ue in user_examples}
        assert "The cat is sleeping." in examples_set
        assert "I saw a cat yesterday." in examples_set

    def test_secure_delete_user_example(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user example."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_example = user_content_service.create_user_example_secure(
            db=db_session,
            user_id=test_user.id,
            user_word_status_id=word_status.id,
            example="My cat loves to play.",
            part_of_speech="noun",
        )

        user_content_service.delete_user_example_secure(
            db=db_session, example_id=user_example.id, user_id=test_user.id
        )

        deleted_example = db_session.query(models.UserExamples).filter_by(id=user_example.id).first()
        assert deleted_example is None, "User example was not deleted securely."


# ==================== USER DEFINITIONS TESTS ====================
class TestUserDefinitions:
    """Test user definitions CRUD operations."""

    def test_add_user_definition_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user definition to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)

        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_id=test_user.id,
            user_word_status_id=word_status.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        user_definitions = user_content_service.list_user_definitions_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )
        assert any(
            ud.definition == "A furry domestic animal." for ud in user_definitions
        ), "User definition was not found."

    def test_secure_update_user_definition(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user definition."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_id=test_user.id,
            user_word_status_id=word_status.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        updated_definition = user_content_service.update_user_definition_secure(
            db=db_session,
            definition_id=user_definition.id,
            user_id=test_user.id,
            definition="A small furry pet.",
        )

        updated = db_session.query(models.UserDefinitions).filter_by(id=user_definition.id).first()
        assert updated.definition == "A small furry pet.", "User definition was not updated."
        assert updated.part_of_speech == "noun", "User definition part of speech should remain unchanged."

    def test_secure_update_user_definition_pos(self, db_session, test_vocabulary,test_word, test_user):
        """Test secure update of a user definition part of speech."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        updated_definition = user_content_service.update_user_definition_secure(
            db=db_session,
            definition_id=user_definition.id,
            user_id=test_user.id,
            part_of_speech="verb",
        )

        updated = db_session.query(models.UserDefinitions).filter_by(id=user_definition.id).first()
        assert updated.part_of_speech == "verb", "User definition part of speech was not updated."
        assert updated.definition == "A furry domestic animal.", "User definition should remain unchanged."

    def test_secure_update_definition_and_pos(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user definition and part of speech."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        updated_definition = user_content_service.update_user_definition_secure(
            db=db_session,
            definition_id=user_definition.id,
            user_id=test_user.id,
            definition="A small furry pet.",
            part_of_speech="verb",
        )

        updated = db_session.query(models.UserDefinitions).filter_by(id=user_definition.id).first()
        assert updated.definition == "A small furry pet.", "User definition was not updated."
        assert updated.part_of_speech == "verb", "User definition part of speech was not updated."

    def test_secure_update_user_definition_none_fields(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user definition with no fields provided."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        with pytest.raises(ValueError):
            user_content_service.update_user_definition_secure(
                db=db_session,
                definition_id=user_definition.id,
                user_id=test_user.id,
            )

    def test_secure_update_user_definition_unauthorized(self, db_session, test_vocabulary, test_word, test_user):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        """Test secure update of a user definition by unauthorized user."""
        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        with pytest.raises(OwnershipVerificationError):
            user_content_service.update_user_definition_secure(
                db=db_session,
                definition_id=user_definition.id,
                user_id=9999,
                definition="Updated definition",
            )

    def test_list_definitions_by_word_status_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test listing user definitions by word status securely."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        definition1 = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )
        definition2 = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A small pet with whiskers.",
            part_of_speech="noun",
        )

        user_definitions = user_content_service.list_user_definitions_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )

        assert len(user_definitions) == 2, "User definitions count mismatch."
        definitions_set = {ud.definition for ud in user_definitions}
        assert "A furry domestic animal." in definitions_set
        assert "A small pet with whiskers." in definitions_set

    def test_secure_delete_user_definition(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user definition."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_definition = user_content_service.create_user_definition_secure(
            db=db_session,
            user_word_status_id=word_status.id,
            user_id=test_user.id,
            definition="A furry domestic animal.",
            part_of_speech="noun",
        )

        user_content_service.delete_user_definition_secure(
            db=db_session, definition_id=user_definition.id, user_id=test_user.id
        )

        deleted_definition = (
            db_session.query(models.UserDefinitions).filter_by(id=user_definition.id).first()
        )
        assert deleted_definition is None, "User definition was not deleted securely."


# ==================== USER TAGS TESTS ====================
class TestUserTags:
    """Test user tags CRUD operations."""

    def test_add_user_tag_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user tag to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_tag = user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )
        user_tags = user_content_service.list_user_tags_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )
        assert any(ut.tag == "favorite" for ut in user_tags), "User tag 'favorite' was not found."

    def test_secure_update_user_tag(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user tag."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_tag = user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )
        updated_tag = user_content_service.update_user_tag_secure(
            db=db_session, tag_id=user_tag.id, user_id=test_user.id, tag="important"
        )

        updated = db_session.query(models.UserTags).filter_by(id=user_tag.id).first()
        assert updated.tag == "important", "User tag was not updated."

    def test_secure_update_user_tag_empty(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user tag with no fields provided."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_tag = user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )

        with pytest.raises(ValueError):
            user_content_service.update_user_tag_secure(
                db=db_session, tag_id=user_tag.id, user_id=test_user.id, tag=""
            )

    def test_secure_update_user_tag_unauthorized(self, db_session, test_vocabulary, test_word,test_user):
        """Test secure update of a user tag by unauthorized user."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_tag = user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )
        db_session.add(user_tag)
        db_session.commit()
        db_session.refresh(user_tag)

        with pytest.raises(OwnershipVerificationError):
            user_content_service.update_user_tag_secure(
                db=db_session, tag_id=user_tag.id, user_id=9999, tag="Updated tag"
            )

    def test_list_tags_by_word_status_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test listing user tags by word status securely."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        tag1 = user_content_service.create_user_tag_secure(db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite")
        tag2 = user_content_service.create_user_tag_secure(db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="difficult")
        db_session.add(tag1)
        db_session.add(tag2)
        db_session.commit()

        user_tags = user_content_service.list_user_tags_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )

        assert len(user_tags) == 2, "User tags count mismatch."
        tags_set = {ut.tag for ut in user_tags}
        assert "favorite" in tags_set
        assert "difficult" in tags_set

    def test_secure_delete_user_tag(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user tag."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_tag = user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )

        user_content_service.delete_user_tag_secure(
            db=db_session, tag_id=user_tag.id, user_id=test_user.id
        )

        deleted_tag = db_session.query(models.UserTags).filter_by(id=user_tag.id).first()
        assert deleted_tag is None, "User tag was not deleted securely."


# ==================== USER SYNONYMS TESTS ====================
class TestUserSynonyms:
    """Test user synonyms CRUD operations."""

    def test_add_user_synonym_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user synonym to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_synonym = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )

        user_synonyms = list_user_synonyms_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )
        assert any(
            us.synonym == "kitten" for us in user_synonyms
        ), "User synonym 'kitten' was not found."

    def test_secure_update_user_synonym(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user synonym."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        user_synonym = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )
        updated_synonym = user_content_service.update_user_synonym_secure(
            db=db_session, synonym_id=user_synonym.id, user_id=test_user.id, synonym="kitty"
        )
        updated = db_session.query(models.UserSynonyms).filter_by(id=user_synonym.id).first()
        assert updated.synonym == "kitty", "User synonym was not updated."

    def test_secure_update_user_synonym_unauthorized(self, db_session, test_vocabulary, test_word,test_user):
        """Test secure update of a user synonym by unauthorized user."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        db_session.add(test_vocabulary_word)
        db_session.commit()
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_synonym = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )

        with pytest.raises(OwnershipVerificationError):
            user_content_service.update_user_synonym_secure(
                db=db_session, synonym_id=user_synonym.id, user_id=9999, synonym="Updated synonym"
            )

    def test_secure_update_user_synonym_empty(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure update of a user synonym with no fields provided."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."

        user_synonym = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )

        with pytest.raises(ValueError):
            user_content_service.update_user_synonym_secure(
                db=db_session, synonym_id=user_synonym.id, user_id=test_user.id, synonym=""
            )

    def test_list_synonyms_by_word_status_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test listing user synonyms by word status securely."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert word_status is not None, "UserWordStatus was not found."
        synonym1 = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )
        synonym2 = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="feline"
        )
        user_synonyms = user_content_service.list_user_synonyms_by_word_status_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id
        )

        assert len(user_synonyms) == 2, "User synonyms count mismatch."
        synonyms_set = {us.synonym for us in user_synonyms}
        assert "kitten" in synonyms_set
        assert "feline" in synonyms_set

    def test_secure_delete_user_synonym(self, db_session, test_vocabulary, test_user, test_word):
        """Test secure deletion of a user synonym."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        test_word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)
        assert test_word_status is not None, "UserWordStatus was not found."

        user_synonym = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=test_word_status.id, user_id=test_user.id, synonym="kitten"
        )

        user_content_service.delete_user_synonym_secure(
            db=db_session, synonym_id=user_synonym.id, user_id=test_user.id
        )

        deleted_synonym = db_session.query(models.UserSynonyms).filter_by(id=user_synonym.id).first()
        assert deleted_synonym is None, "User synonym was not deleted securely."

class TestUserHiddenDefinitions:
    """Test user hidden definitions CRUD operations."""

    def test_add_user_hidden_definition_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user hidden element to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

    def test_add_existed_user_hidden_definition_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden element to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_definition_secure(
                db=db_session, user_word_status_id=word_status.id, definition_id=1
            )

    def test_add_unexisted_definition_user_hidden_definition_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden element to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_definition_secure(
                db=db_session, user_word_status_id=word_status.id, definition_id=9999
            )


    def test_delete_user_hidden_definition_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden element."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )

        user_word_status_service.delete_user_hidden_definition_secure(
            db=db_session, hidden_definition_id=user_hidden_element.id, user_id=test_user.id
        )

        deleted_hidden_element = db_session.query(models.UserHiddenBaseDefinition).filter_by(id=user_hidden_element.id).first()
        assert deleted_hidden_element is None, "User hidden element was not deleted securely."

    def test_delete_user_hidden_definition_secure_unauthorized(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden element by unauthorized user."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )

        with pytest.raises(ValueError):
            user_word_status_service.delete_user_hidden_definition_secure(
                db=db_session, hidden_definition_id=user_hidden_element.id, user_id=9999
            )

class TestUserHiddenTranslations:
    """Test user hidden translations CRUD operations."""
    def test_add_user_hidden_translation_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user hidden translation to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_translation_secure(
            db=db_session, user_word_status_id=word_status.id, translation_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

    def test_add_existed_user_hidden_translation_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden translation to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_translation_secure(
            db=db_session, user_word_status_id=word_status.id, translation_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_translation_secure(
                db=db_session, user_word_status_id=word_status.id, translation_id=1
            )

    def test_add_unexisted_translation_user_hidden_translation_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden translation to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_translation_secure(
                db=db_session, user_word_status_id=word_status.id, translation_id=9999
            )

    def test_delete_user_hidden_translation_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden translation."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_translation_secure(
            db=db_session, user_word_status_id=word_status.id, translation_id=1
        )

        user_word_status_service.delete_user_hidden_translation_secure(
            db=db_session, hidden_translation_id=user_hidden_element.id, user_id=test_user.id
        )

        deleted_hidden_element = db_session.query(models.UserHiddenBaseTranslation).filter_by(id=user_hidden_element.id).first()
        assert deleted_hidden_element is None, "User hidden element was not deleted securely."

class TestUserHiddenSynonyms:
    """Test user hidden synonyms CRUD operations."""
    def test_add_user_hidden_synonym_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user hidden synonym to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, synonym_id=1
        )
        assert user_hidden_element is not None, "User hidden element was not created."

    def test_add_existed_user_hidden_synonym_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden synonym to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, synonym_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_synonym_secure(
                db=db_session, user_word_status_id=word_status.id, synonym_id=1
            )

    def test_add_unexisted_synonym_user_hidden_synonym_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden synonym to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_synonym_secure(
                db=db_session, user_word_status_id=word_status.id, synonym_id=9999
            )

    def test_delete_user_hidden_synonym_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden synonym."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, synonym_id=1
        )

        user_word_status_service.delete_user_hidden_synonym_secure(
            db=db_session, hidden_synonym_id=user_hidden_element.id, user_id=test_user.id
        )

        deleted_hidden_element = db_session.query(models.UserHiddenBaseSynonym).filter_by(id=user_hidden_element.id).first()
        assert deleted_hidden_element is None, "User hidden element was not deleted securely."

class TestUserHiddenExamples:
    """Test user hidden examples CRUD operations."""
    def test_add_user_hidden_example_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user hidden example to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_example_secure(
            db=db_session, user_word_status_id=word_status.id, example_id=1
        )
        assert user_hidden_element is not None, "User hidden element was not created."

    def test_add_existed_user_hidden_example_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden example to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_example_secure(
            db=db_session, user_word_status_id=word_status.id, example_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_example_secure(
                db=db_session, user_word_status_id=word_status.id, example_id=1
            )

    def test_add_unexisted_example_user_hidden_example_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden example to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_example_secure(
                db=db_session, user_word_status_id=word_status.id, example_id=9999
            )

    def test_delete_user_hidden_example_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden example."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_example_secure(
            db=db_session, user_word_status_id=word_status.id, example_id=1
        )

        user_word_status_service.delete_user_hidden_example_secure(
            db=db_session, hidden_example_id=user_hidden_element.id, user_id=test_user.id
        )

        deleted_hidden_element = db_session.query(models.UserHiddenBaseExample).filter_by(id=user_hidden_element.id).first()
        assert deleted_hidden_element is None, "User hidden element was not deleted securely."

class TestUserHiddenTags:
    """Test user hidden tags CRUD operations."""
    def test_add_user_hidden_tag_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding a user hidden tag to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )
        assert user_hidden_element is not None, "User hidden element was not created."

    def test_add_existed_user_hidden_tag_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden tag to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )

        assert user_hidden_element is not None, "User hidden element was not created."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_tag_secure(
                db=db_session, user_word_status_id=word_status.id, tag_id=1
            )

    def test_add_unexisted_tag_user_hidden_tag_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test adding an existed user hidden tag to a vocabulary word."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        with pytest.raises(ValueError):
            user_word_status_service.create_user_hidden_tag_secure(
                db=db_session, user_word_status_id=word_status.id, tag_id=9999
            )

    def test_delete_user_hidden_tag_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden tag."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )

        user_word_status_service.delete_user_hidden_tag_secure(
            db=db_session, hidden_tag_id=user_hidden_element.id, user_id=test_user.id
        )

        deleted_hidden_element = db_session.query(models.UserHiddenBaseTag).filter_by(id=user_hidden_element.id).first()
        assert deleted_hidden_element is None, "User hidden element was not deleted securely."

    def test_delete_user_hidden_tag_secure_unauthorized(self, db_session, test_vocabulary, test_word, test_user):
        """Test secure deletion of a user hidden tag by unauthorized user."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_hidden_element = user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )

        with pytest.raises(ValueError):
            user_word_status_service.delete_user_hidden_tag_secure(
                db=db_session, hidden_tag_id=user_hidden_element.id, user_id=9999
            )

class TestUserWordStatusContainAllHiddenElementsAndUserData:
    """Test that UserWordStatus contains all hidden elements relations."""
    def test_user_word_status_contains_all_hidden_elements(self, db_session, test_vocabulary, test_word, test_user):
        """Test that UserWordStatus contains all hidden elements relations."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        hidden_definition = user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )
        hidden_translation = user_word_status_service.create_user_hidden_translation_secure(
            db=db_session, user_word_status_id=word_status.id, translation_id=1
        )
        hidden_synonym = user_word_status_service.create_user_hidden_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, synonym_id=1
        )
        hidden_example = user_word_status_service.create_user_hidden_example_secure(
            db=db_session, user_word_status_id=word_status.id, example_id=1
        )
        hidden_tag = user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )

        fetched_word_status = db_session.query(models.UserWordStatus).filter_by(id=word_status.id).first()
        print(fetched_word_status)
        assert len(fetched_word_status.hidden_base_definitions) == 1, "Hidden definitions count mismatch."
        assert len(fetched_word_status.hidden_base_translations) == 1, "Hidden translations count mismatch."
        assert len(fetched_word_status.hidden_base_synonyms) == 1, "Hidden synonyms count mismatch."
        assert len(fetched_word_status.hidden_base_examples) == 1, "Hidden examples count mismatch."
        assert len(fetched_word_status.hidden_base_tags) == 1, "Hidden tags count mismatch."

    def test_user_word_status_contains_user_data(self, db_session, test_vocabulary, test_word, test_user):
        """Test that UserWordStatus contains user data relations."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        user_tag = user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )
        user_synonym = user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )
        user_definition = user_content_service.create_user_definition_secure(
            db=db_session, user_word_status_id=word_status.id,part_of_speech="noun", user_id=test_user.id, definition="A small cat"
        )
        user_translation = user_content_service.create_user_translation_secure(
            db=db_session, user_word_status_id=word_status.id,language="russian", user_id=test_user.id, translation="котенок"
        )
        user_example = user_content_service.create_user_example_secure(
            db=db_session, user_word_status_id=word_status.id,part_of_speech="noun", user_id=test_user.id, example="The kitten is playing."
        )


        fetched_word_status = db_session.query(models.UserWordStatus).filter_by(id=word_status.id).first()
        print(fetched_word_status)
        assert len(fetched_word_status.user_tags) == 1, "User tags count mismatch."
        assert len(fetched_word_status.user_synonyms) == 1, "User synonyms count mismatch."
        assert len(fetched_word_status.user_definitions) == 1, "User definitions count mismatch."
        assert len(fetched_word_status.user_translations) == 1, "User translations count mismatch."
        assert len(fetched_word_status.user_examples) == 1, "User examples count mismatch."

    def test_user_word_status_contain_all_data(self, db_session, test_vocabulary, test_word, test_user):
        """Test that UserWordStatus contains all hidden elements and user data relations."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Create hidden elements
        user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )
        user_word_status_service.create_user_hidden_translation_secure(
            db=db_session, user_word_status_id=word_status.id, translation_id=1
        )
        user_word_status_service.create_user_hidden_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, synonym_id=1
        )
        user_word_status_service.create_user_hidden_example_secure(
            db=db_session, user_word_status_id=word_status.id, example_id=1
        )
        user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )

        # Create user data
        user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )
        user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )
        user_content_service.create_user_definition_secure(
            db=db_session, user_word_status_id=word_status.id,part_of_speech="noun", user_id=test_user.id, definition="A small cat"
        )
        user_content_service.create_user_translation_secure(
            db=db_session, user_word_status_id=word_status.id,language="russian", user_id=test_user.id, translation="котенок"
        )
        user_content_service.create_user_example_secure(
            db=db_session, user_word_status_id=word_status.id,part_of_speech="noun", user_id=test_user.id, example="The kitten is playing."
        )

        fetched_word_status = db_session.query(models.UserWordStatus).filter_by(id=word_status.id).first()
        print(fetched_word_status)
        assert len(fetched_word_status.hidden_base_definitions) == 1, "Hidden definitions count mismatch."
        assert len(fetched_word_status.hidden_base_translations) == 1, "Hidden translations count mismatch."
        assert len(fetched_word_status.hidden_base_synonyms) == 1   , "Hidden synonyms count mismatch."
        assert len(fetched_word_status.hidden_base_examples) == 1, "Hidden examples count mismatch."
        assert len(fetched_word_status.hidden_base_tags) == 1, "Hidden tags count mismatch."
        assert len(fetched_word_status.user_tags) == 1, "User tags count mismatch."
        assert len(fetched_word_status.user_synonyms) == 1, "User synonyms count mismatch."
        assert len(fetched_word_status.user_definitions) == 1, "User definitions count mismatch."
        assert len(fetched_word_status.user_translations) == 1, "User translations count mismatch."
        assert len(fetched_word_status.user_examples) == 1, "User examples count mismatch."
        assert fetched_word_status.user_quiz_progress is not None, "User quiz progress is missing."

class TestGettingFullWordData:
    """Test getting full word data including hidden elements and user data."""
    def test_get_full_word_data_secure(self, db_session, test_vocabulary, test_word, test_user):
        """Test getting full word data securely."""
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        assert word_status is not None, "UserWordStatus was not found."

        # Create hidden elements
        user_word_status_service.create_user_hidden_definition_secure(
            db=db_session, user_word_status_id=word_status.id, definition_id=1
        )
        user_word_status_service.create_user_hidden_translation_secure(
            db=db_session, user_word_status_id=word_status.id, translation_id=1
        )
        user_word_status_service.create_user_hidden_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, synonym_id=1
        )
        user_word_status_service.create_user_hidden_example_secure(
            db=db_session, user_word_status_id=word_status.id, example_id=1
        )
        user_word_status_service.create_user_hidden_tag_secure(
            db=db_session, user_word_status_id=word_status.id, tag_id=1
        )

        # Create user data
        user_content_service.create_user_tag_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, tag="favorite"
        )
        user_content_service.create_user_synonym_secure(
            db=db_session, user_word_status_id=word_status.id, user_id=test_user.id, synonym="kitten"
        )
        user_content_service.create_user_definition_secure(
            db=db_session, user_word_status_id=word_status.id,part_of_speech="noun", user_id=test_user.id, definition="A small cat"
        )
        user_content_service.create_user_translation_secure(
            db=db_session, user_word_status_id=word_status.id,language="russian", user_id=test_user.id, translation="котенок"
        )
        user_content_service.create_user_example_secure(
            db=db_session, user_word_status_id=word_status.id,part_of_speech="noun", user_id=test_user.id, example="The kitten is playing."
        )

        full_word_data = user_word_status_service.requiered_word_data_with_user_word_status(
            db=db_session, user_word_status_id=word_status.id, word_id=test_word.id)

        assert full_word_data is not None, "Full word data was not retrieved."
        assert len(full_word_data["user_data"]['hidden_base_definitions']) == 1, "Hidden definitions count mismatch."
        assert len(full_word_data["user_data"]['hidden_base_translations']) == 1, "Hidden translations count mismatch."
        assert len(full_word_data["user_data"]['hidden_base_synonyms']) == 1   , "Hidden synonyms count mismatch."
        assert len(full_word_data["user_data"]['hidden_base_examples']) == 1, "Hidden examples count mismatch."
        assert len(full_word_data["user_data"]['hidden_base_tags']) == 1, "Hidden tags count mismatch."
        assert len(full_word_data["user_data"]['user_tags']) == 1, "User tags count mismatch."
        assert len(full_word_data["user_data"]['user_synonyms']) == 1, "User synonyms count mismatch."
        assert len(full_word_data["user_data"]['user_definitions']) == 1, "User definitions count mismatch."
        assert len(full_word_data["user_data"]['user_translations']) == 1, "User translations count mismatch."
        assert len(full_word_data["user_data"]['user_examples']) == 1, "User examples count mismatch."
        assert full_word_data["base_word_data"] is not None, "Base word data is missing."
        assert full_word_data["base_word_data"]['word'] == test_word.word, "Base word data mismatch."
        assert full_word_data["user_data"]["user_quiz_progress"] is not None, "User quiz progress is missing."
        assert full_word_data["user_data"]["user_quiz_progress"]['learning_stage'] == 1, "User quiz progress mismatch."


        definitions = full_word_data["base_word_data"]['definitions']
        assert isinstance(definitions, list), "Definitions should be a list"
        assert len(definitions) >= 3, "Should have at least 3 definitions"

        # Get noun definitions
        noun_definitions = [d for d in definitions if d.get('part_of_speech') == 'noun']
        assert len(noun_definitions) == 3, "Should have 3 noun definitions"

        # Check the definition texts
        definition_texts = [d.get('definition') for d in noun_definitions]
        assert "a small domesticated carnivorous mammal" in definition_texts
        assert "a feline animal" in definition_texts
        assert "a pet animal" in definition_texts
