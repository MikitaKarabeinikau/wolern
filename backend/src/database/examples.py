from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def add_example_with_part_of_speech(db: Session, word_id: int, example_sentence: str, part_of_speech: str):
    """Add a new example with part of speech."""
    try:
        new_example = models.Example(
            word_id=word_id,
            example_sentence=example_sentence,
            part_of_speech=part_of_speech,
        )
        db.add(new_example)
        db.commit()
        db.refresh(new_example)
        logger.info(f"Added new example for word ID '{word_id}' with part of speech '{part_of_speech}'.")
        return new_example
    except Exception as e:
        logger.error(f"Error adding example for word ID '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def add_example(db: Session, example_sentence: str, word_id: int):
    """Add a new example."""
    try:
        db_example = models.Example(example_sentence=example_sentence, word_id=word_id)
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        logger.info(f"Example created for word_id '{word_id}'.")
        return db_example
    except Exception as e:
        logger.error(f"Error creating example for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_examples_for_quiz(db: Session, clerk_id: str):
    """Get all examples for quiz words for a specific user."""
    try:
        examples = (
            db.query(models.Example)
            .join(models.Words)
            .filter(
                models.Words.added_by_user_id == clerk_id,
                (models.Words.vocabulary == "learning") | (models.Words.vocabulary == "unknown")
            )
            .all()
        )
        if not examples:
            logger.info(f"No examples found for quiz words for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(examples)} examples for quiz words for user '{clerk_id}'.")
        return examples
    except Exception as e:
        logger.error(f"Error getting examples for quiz words for user '{clerk_id}': {e}", exc_info=True)
        raise

def get_examples_by_word(db: Session, word: str, clerk_id: str):
    """Get all examples associated with a word for a specific user."""
    try:
        examples = (
            db.query(models.Example)
            .join(models.Words)
            .filter(
                models.Words.word == word.strip(),
                models.Words.added_by_user_id == clerk_id,
            )
            .all()
        )
        if not examples:
            logger.info(f"No examples found for word '{word}' and user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(examples)} examples for word '{word}' and user '{clerk_id}'.")
        return examples
    except Exception as e:
        logger.error(
            f"Error getting examples for word '{word}' and user '{clerk_id}': {e}",
            exc_info=True,
        )
        raise

def get_example_by_id(db: Session, example_id: int):
    """Get a example by its ID."""
    try:
        example = db.query(models.Example).filter(models.Example.id == example_id).first()
        if not example:
            logger.warning(f"Example with ID '{example_id}' not found.")
            return None
        logger.info(f"Fetching example with ID: {example_id}")
        return example
    except Exception as e:
        logger.error(f"Error getting example with ID '{example_id}': {e}", exc_info=True)
        raise

def get_all_examples_for_user_from_db(db: Session, clerk_id: str):
    """Get all examples for a specific user."""
    try:
        examples = db.query(models.Example).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()
        return examples
    except Exception as e:
        logger.error(f"Error getting examples for user with clerk_id {clerk_id}: {e}", exc_info=True)
        raise

def update_example_by_id(db: Session, example_id: int, new_example: str, word_id: int):
    """Update a example by its ID."""
    try:
        example_to_update = get_example_by_id(db, example_id)
        if not example_to_update:
            logger.warning(f"Example with ID '{example_id}' not found.")
            return None

        example_to_update.example_sentence = new_example
        example_to_update.word_id = word_id
        db.commit()
        db.refresh(example_to_update)
        logger.info(f"Example with ID '{example_id}' updated successfully.")
        return example_to_update
    except Exception as e:
        logger.error(f"Error updating example with ID '{example_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_example_by_id(db: Session, clerk_id: str, example_id: int):
    """Delete a example by its ID, ensuring the user has permission."""
    try:
        to_delete = (
            db.query(models.Example)
            .join(models.Words)
            .filter(
                models.Example.id == example_id,
                models.Words.added_by_user_id == clerk_id,
            )
            .first()
        )
        if not to_delete:
            logger.warning(f"No example found or user does not have permission to delete it.")
            return False

        db.delete(to_delete)
        db.commit()
        logger.info(f"Example with ID '{example_id}' deleted successfully.")
        return True  # Indicate successful deletion
    except Exception as e:
        logger.error(f"Error deleting example with ID '{example_id}': {e}", exc_info=True)
        db.rollback()
        raise