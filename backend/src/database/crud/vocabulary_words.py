from database.crud.user_word_status import create_user_word_status
from sqlalchemy.orm import Session
from backend.src.database import models
import logging
from typing import List

logger = logging.getLogger(__name__)


def create_vocabulary_word(db: Session, vocabulary_id: int, word_id: int) -> models.VocabularyWords:
    """Add a word to a vocabulary."""
    try:
        # Verify vocabulary exists
        vocabulary = (
            db.query(models.Vocabulary)
            .filter(models.Vocabulary.vocabulary_id == vocabulary_id)
            .first()
        )

        if not vocabulary:
            raise ValueError(f"Vocabulary ID {vocabulary_id} does not exist")

        # Verify word exists
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word ID {word_id} does not exist")

        # Check if already exists
        existing = (
            db.query(models.VocabularyWords)
            .filter(
                models.VocabularyWords.vocabulary_id == vocabulary_id,
                models.VocabularyWords.word_id == word_id,
            )
            .first()
        )

        if existing:
            logger.info(f"Word ID {word_id} already in vocabulary ID {vocabulary_id}")
            return existing

        # Create entry
        new_word = models.VocabularyWords(vocabulary_id=vocabulary_id, word_id=word_id)
        db.add(new_word)
        db.flush()

        #Create user word status
        new_status_id = create_user_word_status(db, vocabulary_word_id=new_word.id)
        db.add(new_status_id)
        db.commit()
        db.refresh(new_word)

        logger.info(f"Added word ID {word_id} to vocabulary ID {vocabulary_id}")
        return new_word

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error adding word to vocabulary: {e}", exc_info=True)
        db.rollback()
        raise


def get_vocabulary_words(
    db: Session, vocabulary_id: int, skip: int = 0, limit: int = 100
) -> List[models.VocabularyWords]:
    """Get words in a vocabulary with pagination."""
    try:
        return (
            db.query(models.VocabularyWords)
            .filter(models.VocabularyWords.vocabulary_id == vocabulary_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as e:
        logger.error(f"Error getting vocabulary words: {e}", exc_info=True)
        raise


def delete_vocabulary_word(db: Session, vocabulary_word_id: int) -> bool:
    """Delete a vocabulary word entry by its ID."""
    try:
        word_entry = (
            db.query(models.VocabularyWords)
            .filter(models.VocabularyWords.id == vocabulary_word_id)
            .first()
        )

        if not word_entry:
            return False

        db.delete(word_entry)
        db.commit()
        logger.info(f"Deleted vocabulary word entry ID {vocabulary_word_id}")
        return True

    except Exception as e:
        logger.error(f"Error deleting vocabulary word: {e}", exc_info=True)
        db.rollback()
        raise


def remove_word_from_vocabulary(db: Session, vocabulary_id: int, word_id: int) -> bool:
    """Remove a specific word from a vocabulary."""
    try:
        entry = (
            db.query(models.VocabularyWords)
            .filter(
                models.VocabularyWords.vocabulary_id == vocabulary_id,
                models.VocabularyWords.word_id == word_id,
            )
            .first()
        )

        if not entry:
            return False

        db.delete(entry)
        db.commit()
        logger.info(f"Removed word ID {word_id} from vocabulary ID {vocabulary_id}")
        return True

    except Exception as e:
        logger.error(f"Error removing word from vocabulary: {e}", exc_info=True)
        db.rollback()
        raise


def is_word_in_vocabulary(db: Session, vocabulary_id: int, word_id: int) -> bool:
    """Check if a word exists in a vocabulary."""
    try:
        return (
            db.query(models.VocabularyWords)
            .filter(
                models.VocabularyWords.vocabulary_id == vocabulary_id,
                models.VocabularyWords.word_id == word_id,
            )
            .first()
            is not None
        )
    except Exception as e:
        logger.error(f"Error checking word in vocabulary: {e}", exc_info=True)
        raise


def count_vocabulary_words(db: Session, vocabulary_id: int) -> int:
    """Count words in a vocabulary."""
    try:
        return (
            db.query(models.VocabularyWords)
            .filter(models.VocabularyWords.vocabulary_id == vocabulary_id)
            .count()
        )
    except Exception as e:
        logger.error(f"Error counting vocabulary words: {e}", exc_info=True)
        raise
