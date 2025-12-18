from database.crud.user_quiz_progress import get_user_quiz_progress_by_id
from sqlalchemy.orm import Session
from backend.src.database import models
import logging
from sqlalchemy.orm.exc import NoResultFound
from backend.src.config import settings
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


def answer_logic(db: Session, answer: bool, user_quiz_progress_id: int) -> models.UserQuizProgress:
    """Update user quiz progress based on whether the answer was correct or not."""
    try:
        user_quiz_progress = get_user_quiz_progress_by_id(db, user_quiz_progress_id)
        user_quiz_progress.last_attempted = datetime.now(timezone.utc)
        if answer:
            user_quiz_progress.correct += 1
            user_quiz_progress.wrong_streak = 0
            user_quiz_progress.correct_streak += 1
            if user_quiz_progress.correct_streak == settings.CORRECT_STREAK_THRESHOLD:
                if user_quiz_progress.learning_stage < 5:
                    user_quiz_progress.learning_stage += 1
                    user_quiz_progress.correct_streak = 1
                    logger.info(f"User quiz progress id '{user_quiz_progress_id}' advanced to learning stage '{user_quiz_progress.learning_stage}'.")
        else:
            user_quiz_progress.wrong += 1
            user_quiz_progress.correct_streak = 0
            user_quiz_progress.wrong_streak += 1
            if user_quiz_progress.wrong_streak == settings.CORRECT_STREAK_THRESHOLD:
                if user_quiz_progress.learning_stage > 1:
                    user_quiz_progress.learning_stage -= 1
                    user_quiz_progress.wrong_streak = 1

        updated_time = set_new_time_to_repeat(db, user_quiz_progress, answer)
        db.commit()
        db.refresh(updated_time)
        return updated_time
    except NoResultFound:
        logger.warning(f"User quiz progress with id '{user_quiz_progress_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error updating user quiz progress for id '{user_quiz_progress_id}': {e}",
            exc_info=True,
        )
        raise

def set_new_time_to_repeat(db:Session, user_quiz_progress:models.UserQuizProgress, answer: bool) -> models.UserQuizProgress:
    """Set a new time to repeat for the user quiz progress."""
    try:
        if answer:
            if user_quiz_progress.correct_streak < settings.CORRECT_STREAK_THRESHOLD:
                streak = user_quiz_progress.correct_streak
            else:
                streak = settings.CORRECT_STREAK_THRESHOLD
        else:
            streak = 0
        learning_stage = user_quiz_progress.learning_stage
        if learning_stage <= 1:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(minutes=new_time)
        elif learning_stage == 2:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(hours=new_time)
        elif learning_stage == 3:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(days=new_time)
        elif learning_stage == 4:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(weeks=new_time)
        else:  # learning_stage == 5
            new_time = settings.REPEAT_INTERVALS[4][0]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(weeks=new_time * streak)
        logger.info(f"Setting new time to repeat for UserQuizProgress ID '{user_quiz_progress.id}' to '{new_repeat_time}' based on learning stage '{learning_stage}' and streak '{streak}'.")
        user_quiz_progress.time_to_repeat = new_repeat_time
        return user_quiz_progress
    except Exception as e:
        logger.error(
            f"Error setting new time to repeat for UserQuizProgress ID '{user_quiz_progress.id}': {e}",
            exc_info=True,
        )
        raise

def get_quiz_by_vocabulary_id(db: Session, vocabulary_id: int, user_id: int) -> models.UserQuizProgress:
    """Retrieve user quiz progress by vocabulary ID and user ID."""
    try:
        user_vocabulary = db.query(models.Vocabulary).filter(
            models.Vocabulary.vocabulary_id == vocabulary_id,
            models.Vocabulary.user_id == user_id
        ).one()
        if not user_vocabulary:
            logger.warning(f"Vocabulary with ID '{vocabulary_id}' not found for user ID '{user_id}'.")
            return None
        user_quiz_progress = db.query(models.UserQuizProgress
                                      ).join(models.UserWordStatus, models.UserQuizProgress.user_word_status_id == models.UserWordStatus.id
                                             ).join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id
                                                    ).join(models.Vocabulary, models.VocabularyWords.vocabulary_id == models.Vocabulary.vocabulary_id
                                                           ).filter(
            models.Vocabulary.vocabulary_id == vocabulary_id,
        ).order_by(models.UserQuizProgress.time_to_repeat.asc()).all()
        quiz_data = []
        for quiz in user_quiz_progress:
            serialized_quiz = {
                "id": quiz.id,
                "correct": quiz.correct,
                "wrong": quiz.wrong,
                "learning_stage": quiz.learning_stage,
                "correct_streak": quiz.correct_streak,
                "wrong_streak": quiz.wrong_streak,
                "last_attempted": quiz.last_attempted,
                "time_to_repeat": quiz.time_to_repeat,
            }
            quiz_data.append(serialized_quiz)

        for i in quiz_data:
            logger.info(f"Retrieved UserQuizProgress: {i}")
        return quiz_data

    except NoResultFound:
        logger.warning(f"User quiz progress not found for vocabulary ID '{vocabulary_id}' and user ID '{user_id}'.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving user quiz progress for vocabulary ID '{vocabulary_id}' and user ID '{user_id}': {e}",
            exc_info=True,
        )
        raise

def get_due_quizzes_for_today(db: Session, vocabulary_id: int, user_id: int) -> list[models.UserQuizProgress]:
    """Retrieve due quizzes for today for a given vocabulary and user."""
    try:
        now = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59, microsecond=999999)
        user_quiz_progress = db.query(models.UserQuizProgress
                                      ).join(models.UserWordStatus, models.UserQuizProgress.user_word_status_id == models.UserWordStatus.id
                                             ).join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id
                                                    ).join(models.Vocabulary, models.VocabularyWords.vocabulary_id == models.Vocabulary.vocabulary_id
                                                           ).filter(
            models.Vocabulary.vocabulary_id == vocabulary_id,
            models.Vocabulary.user_id == user_id,
            models.UserQuizProgress.time_to_repeat <= now
        ).order_by(models.UserQuizProgress.time_to_repeat.asc()).all()
        serialized_quizzes = []
        for quiz in user_quiz_progress:
            serialized_quiz = {
                "id": quiz.id,
                "correct": quiz.correct,
                "wrong": quiz.wrong,
                "learning_stage": quiz.learning_stage,
                "correct_streak": quiz.correct_streak,
                "wrong_streak": quiz.wrong_streak,
                "last_attempted": quiz.last_attempted,
                "time_to_repeat": quiz.time_to_repeat,
            }
            serialized_quizzes.append(serialized_quiz)
        logger.info(f"Retrieved {len(user_quiz_progress)} due quizzes for vocabulary ID '{vocabulary_id}' and user ID '{user_id}'.")
        return serialized_quizzes
    except Exception as e:
        logger.error(
            f"Error retrieving due quizzes for vocabulary ID '{vocabulary_id}' and user ID '{user_id}': {e}",
            exc_info=True,
        )
        raise

def get_first_ten_due_quizzes_for_vocabulary(db: Session, vocabulary_id: int, user_id: int) -> list[models.UserQuizProgress]:
    """Retrieve the first ten quizzes for a given vocabulary and user."""
    try:
        now = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59, microsecond=999999)
        user_quiz_progress = db.query(models.UserQuizProgress
                                      ).join(models.UserWordStatus, models.UserQuizProgress.user_word_status_id == models.UserWordStatus.id
                                             ).join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id
                                                    ).join(models.Vocabulary, models.VocabularyWords.vocabulary_id == models.Vocabulary.vocabulary_id
                                                           ).filter(
            models.Vocabulary.vocabulary_id == vocabulary_id,
            models.Vocabulary.user_id == user_id,
            models.UserQuizProgress.time_to_repeat <= now
        ).order_by(models.UserQuizProgress.id.asc()).limit(10).all()
        serialized_quizzes = []
        for quiz in user_quiz_progress:
            serialized_quiz = {
                "id": quiz.id,
                "correct": quiz.correct,
                "wrong": quiz.wrong,
                "learning_stage": quiz.learning_stage,
                "correct_streak": quiz.correct_streak,
                "wrong_streak": quiz.wrong_streak,
                "last_attempted": quiz.last_attempted,
                "time_to_repeat": quiz.time_to_repeat,
            }
            serialized_quizzes.append(serialized_quiz)
        logger.info(f"Retrieved first ten quizzes for vocabulary ID '{vocabulary_id}' and user ID '{user_id}'.")
        return serialized_quizzes
    except Exception as e:
        logger.error(
            f"Error retrieving first ten quizzes for vocabulary ID '{vocabulary_id}' and user ID '{user_id}': {e}",
            exc_info=True,
        )
        raise

def get_all_quizzes(db:Session, vocabulary_id:int, user_id:int) -> list[models.UserQuizProgress]:
    """Retrieve all quizzes for a given vocabulary and user."""
    try:
        user_quiz_progress = db.query(models.UserQuizProgress
                                      ).join(models.UserWordStatus, models.UserQuizProgress.user_word_status_id == models.UserWordStatus.id
                                             ).join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id
                                                    ).join(models.Vocabulary, models.VocabularyWords.vocabulary_id == models.Vocabulary.vocabulary_id
                                                           ).filter(
            models.Vocabulary.vocabulary_id == vocabulary_id,
            models.Vocabulary.user_id == user_id
        ).order_by(models.UserQuizProgress.id.asc()).limit(10) .all()
        serialized_quizzes = []
        for quiz in user_quiz_progress:
            serialized_quiz = {
                "id": quiz.id,
                "correct": quiz.correct,
                "wrong": quiz.wrong,
                "learning_stage": quiz.learning_stage,
                "correct_streak": quiz.correct_streak,
                "wrong_streak": quiz.wrong_streak,
                "last_attempted": quiz.last_attempted,
                "time_to_repeat": quiz.time_to_repeat,
            }
            serialized_quizzes.append(serialized_quiz)
        logger.info(f"Retrieved all quizzes for vocabulary ID '{vocabulary_id}' and user ID '{user_id}'.")
        return serialized_quizzes
    except Exception as e:
        logger.error(
            f"Error retrieving all quizzes for vocabulary ID '{vocabulary_id}' and user ID '{user_id}': {e}",
            exc_info=True,
        )
        raise
