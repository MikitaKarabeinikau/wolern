from datetime import datetime, timedelta, timezone
from database import models
from database.crud.vocabulary_words import create_vocabulary_word
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.src.database.database import Base
import backend.src.core.word as word_module
from backend.src.database.crud.words import add_word
from backend.src.services.user_quiz_progress_service import answer_logic, get_due_quizzes_for_today, get_quiz_by_vocabulary_id
from backend.src.services.user_word_status_service import get_user_quiz_progress, get_user_word_status_by_vocabulary_word_id
from backend.src.config import settings

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

@pytest.fixture
def test_word2(db_session):
    """Create a second test word."""
    word_data = word_module.Word(
        word="dog",
        language="english",
        translation={"russian": ["собака"], "polish": ["pies"]},
        synonyms=["canine", "puppy"],
        definition={"noun": ["a domesticated carnivorous mammal"]},
        examples={"noun": ["The dog barked loudly."]},
        part_of_speech=["noun"],
        frequency=0.1,
        date_added="2024-01-02",
        tags=["animal", "pet"],
    )

    word = add_word(db_session, word_data)
    db_session.add(word)
    db_session.commit()
    return word

@pytest.fixture
def test_word3(db_session):
    """Create a third test word."""
    word_data = word_module.Word(
        word="bird",
        language="english",
        translation={"russian": ["птица"], "polish": ["ptak"]},
        synonyms=["avian", "fowl"],
        definition={"noun": ["a warm-blooded egg-laying vertebrate"]},
        examples={"noun": ["The bird sang a beautiful song."]},
        part_of_speech=["noun"],
        frequency=0.1,
        date_added="2024-01-03",
        tags=["animal", "wildlife"],
    )

    word = add_word(db_session, word_data)
    db_session.add(word)
    db_session.commit()
    return word

# ==============================QUIZ PROGRESS TESTS ==============================
class TestUserCorrectAnswer:

    def test_correct_answer_increments_correct_count(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers correctly
        updated_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert updated_progress.correct == 1
        assert updated_progress.wrong == 0
        assert updated_progress.correct_streak == 1
        assert updated_progress.learning_stage == 1  # No change in learning stage

    def test_reset_correct_streak_on_wrong_answer(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers correctly twice
        updated_progress = answer_logic(db_session, True, user_quiz_progress.id)
        updated_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert updated_progress.correct_streak == 2

        # User answers incorrectly
        updated_progress = answer_logic(db_session, False, user_quiz_progress.id)

        assert updated_progress.correct_streak == 0
        assert updated_progress.wrong == 1
        assert updated_progress.wrong_streak == 1

    def test_reset_wrotng_streak_on_correct_answer(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers incorrectly twice
        updated_progress = answer_logic(db_session, False, user_quiz_progress.id)
        updated_progress = answer_logic(db_session, False, user_quiz_progress.id)

        assert updated_progress.wrong_streak == 2

        # User answers correctly
        updated_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert updated_progress.wrong_streak == 0
        assert updated_progress.correct == 1
        assert updated_progress.correct_streak == 1

    def test_learning_stage_increments_on_streak(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers correctly three times to reach the threshold
        for _ in range(5):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 2
        assert user_quiz_progress.correct_streak == 1  # Reset after level up

    def test_learning_stage_decrements_on_wrong_streak(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # First, level up the learning stage to 3
        for _ in range(10):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 3

        # Now, answer incorrectly five times to decrease the learning stage
        for _ in range(5):
            user_quiz_progress = answer_logic(db_session, False, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 2
        assert user_quiz_progress.wrong_streak == 1  # Reset after level down

    def test_no_learning_stage_below_one(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers incorrectly multiple times
        for _ in range(10):
            user_quiz_progress = answer_logic(db_session, False, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 1  # Should not go below 1

    def test_no_learning_stage_above_five(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers correctly multiple times
        for _ in range(35):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 5  # Should not go above 5

    def test_correct_streak_resets_after_level_up(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # User answers correctly to level up
        for _ in range(5):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 2
        assert user_quiz_progress.correct_streak == 1  # Should reset to 1 after level up

    def test_wrong_streak_resets_after_level_down(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # First, level up the learning stage to 3
        for _ in range(10):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 3

        # Now, answer incorrectly to level down
        for _ in range(5):
            user_quiz_progress = answer_logic(db_session, False, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 2
        assert user_quiz_progress.wrong_streak == 1  # Should reset to 1 after level down

    def test_correct_streak_doesnt_reset_after_mastered_level(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # Level up to MASTERED
        for _ in range(25):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 5

        # Continue answering correctly to grow correct streak
        for _ in range(3):
            user_quiz_progress = answer_logic(db_session, True, user_quiz_progress.id)

        assert user_quiz_progress.correct_streak == 12  # Should continue growing

    def test_wrong_streak_doesnt_reset_after_lowest_level(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        # Level up to MASTERED
        for _ in range(10):
            user_quiz_progress = answer_logic(db_session, False, user_quiz_progress.id)

        assert user_quiz_progress.learning_stage == 1
        # Continue answering incorrectly to grow wrong streak
        assert user_quiz_progress.wrong_streak == 10  # Should continue growing

class TestSettingNewTimeToRepeat:
    def test_set_new_time_to_repeat_correct_answer(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        #Initial time to repeat
        initial_time_to_repeat = datetime.now(timezone.utc)


        # User answers correctly
        updated_progress = answer_logic(db_session, True, user_quiz_progress.id)

        expected_minute_increment = settings.REPEAT_INTERVALS[user_quiz_progress.learning_stage][user_quiz_progress.correct_streak]
        updated_progress_time = updated_progress.time_to_repeat.astimezone(timezone.utc).replace(second=0, microsecond=0)
        expected_time = (initial_time_to_repeat + timedelta(minutes=expected_minute_increment)).replace(second=0, microsecond=0)
        assert abs(updated_progress_time - expected_time) <= timedelta(minutes=1)  # Allowing a 1 minute margin for test execution time

    def test_set_new_time_to_repeat_wrong_answer(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )

        #Initial time to repeat
        initial_time_to_repeat = datetime.now(timezone.utc)


        # User answers incorrectly
        updated_progress = answer_logic(db_session, False, user_quiz_progress.id)

        expected_minute_increment = settings.REPEAT_INTERVALS[user_quiz_progress.learning_stage][0]
        updated_progress_time = updated_progress.time_to_repeat.astimezone(timezone.utc).replace(second=0, microsecond=0)
        expected_time = (initial_time_to_repeat + timedelta(minutes=expected_minute_increment)).replace(second=0, microsecond=0)
        assert abs(updated_progress_time - expected_time) <= timedelta(minutes=1)  # Allowing a 1 minute margin for test execution time

    def test_set_new_time_for_each_learning_stage(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words
    ):
        test_vocabulary_word = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=test_vocabulary_word.id)

        user_quiz_progress = get_user_quiz_progress(
            db_session, word_status.id
        )
        for stage in range(1, 5):
            for streak in range(1, 5):
                initial_time_to_repeat = datetime.now(timezone.utc)

                # User answers correctly
                updated_progress = answer_logic(db_session, True, user_quiz_progress.id)

                expected_minute_increment = settings.REPEAT_INTERVALS[stage][streak]


                updated_progress_time = updated_progress.time_to_repeat.astimezone(timezone.utc).replace(second=0, microsecond=0)

                if stage == 1:
                    expected_time = (initial_time_to_repeat + timedelta(minutes=expected_minute_increment)).replace(second=0, microsecond=0)
                elif stage == 2:
                    expected_time = (initial_time_to_repeat + timedelta(hours=expected_minute_increment)).replace(second=0, microsecond=0)
                elif stage == 3:
                    expected_time = (initial_time_to_repeat + timedelta(days=expected_minute_increment)).replace(second=0, microsecond=0)
                elif stage == 4:
                    expected_time = (initial_time_to_repeat + timedelta(weeks=expected_minute_increment)).replace(second=0, microsecond=0)

                print(f"Expected time: {expected_time}")
                print(f"Updated progress time: {updated_progress_time}")
                print(f"Difference: {abs(updated_progress_time - expected_time)}")

                assert updated_progress.learning_stage == stage
                assert updated_progress.correct_streak == streak
                assert abs(updated_progress_time - expected_time) <= timedelta(minutes=1)  # Allowing a 1 minute margin for test execution time


class TestQuizForVocabulary:
    def test_quiz_includes_all_words(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words, test_word2: models.Words, test_word3: models.Words
    ):
        # Add words to vocabulary
        vocab_word1 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        vocab_word2 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word2.id)
        vocab_word3 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word3.id)

        word_status1 = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=vocab_word1.id)
        word_status2 = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=vocab_word2.id)
        word_status3 = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=vocab_word3.id)

        quiz_progress1 = get_user_quiz_progress(db_session, word_status1.id)
        quiz_progress2 = get_user_quiz_progress(db_session, word_status2.id)
        quiz_progress3 = get_user_quiz_progress(db_session, word_status3.id)

        assert quiz_progress1 is not None
        assert quiz_progress2 is not None
        assert quiz_progress3 is not None
    
    def test_get_quiz_by_vocabulary_id(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words,test_user: models.Users, test_word2: models.Words, test_word3: models.Words
    ):
        # Add words to vocabulary
        vocab_word1 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        vocab_word2 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word2.id)
        vocab_word3 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word3.id)

        retrieved_quiz_progress = get_quiz_by_vocabulary_id(db_session, vocabulary_id=test_vocabulary.vocabulary_id, user_id=test_user.id)
        ids = [item["id"] for item in retrieved_quiz_progress]
        print(f"Retrieved quiz progress IDs: {ids}")
        assert retrieved_quiz_progress is not None
        assert ids == [1,2,3]

    def test_get_quiz_by_vocabulary_and_change_time_to_repeat(
        self, db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words,test_user: models.Users, test_word2: models.Words, test_word3: models.Words
    ):
        vocab_word1 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        vocab_word2 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word2.id)
        vocab_word3 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word3.id)

        retrieved_quiz_progress = get_quiz_by_vocabulary_id(db_session, vocabulary_id=test_vocabulary.vocabulary_id, user_id=test_user.id)
        ids = [item["id"] for item in retrieved_quiz_progress]
        print(retrieved_quiz_progress[0])
        print(f"Retrieved quiz progress IDs: {ids}")
        print(f"Time to repeat before answer logic: {retrieved_quiz_progress[0]['time_to_repeat']}")
        answer_logic(db_session, True, ids[0])
        print(f"Time to repeat after answer logic: {retrieved_quiz_progress[0]['time_to_repeat']}")
        updated_quiz_progress = get_quiz_by_vocabulary_id(db_session, vocabulary_id=test_vocabulary.vocabulary_id, user_id=test_user.id)
        updated_ids = [item["id"] for item in updated_quiz_progress]
        print(f"Updated quiz progress IDs: {updated_ids}")
        
        assert updated_ids == [2,3,1]

    def test_get_quiz_by_vocabulary_no_words(
        self, db_session: Session, test_user: models.Users
    ):
        retrieved_quiz_progress = get_quiz_by_vocabulary_id(db_session, vocabulary_id=999, user_id=test_user.id)
        assert retrieved_quiz_progress == None

    def test_get_quiz_for_today(self,db_session: Session, test_vocabulary: models.Vocabulary, test_word: models.Words,test_user: models.Users, test_word2: models.Words, test_word3: models.Words):
        vocab_word1 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word.id)
        vocab_word2 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word2.id)
        vocab_word3 = create_vocabulary_word(db_session, vocabulary_id=test_vocabulary.vocabulary_id, word_id=test_word3.id)
        
        for i in range(15):
            word_status = get_user_word_status_by_vocabulary_word_id(db_session, vocabulary_word_id=vocab_word1.id)
            user_quiz_progress = get_user_quiz_progress(
                db_session, word_status.id
            )
            answer_logic(db_session, True, user_quiz_progress.id)

        retrieved_quiz_progress = get_due_quizzes_for_today(db_session, vocabulary_id=test_vocabulary.vocabulary_id, user_id=test_user.id)
        ids = [item["id"] for item in retrieved_quiz_progress]
        print(f"Retrieved quiz progress IDs: {ids}")

        assert ids == [2,3]