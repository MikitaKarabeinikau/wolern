from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
from backend.src.config import settings
logger = logging.getLogger(__name__)


def create_example(db: Session,word_id: int, part_of_speech: str, example:str) -> models.Examples:
    """Create a new example for a definition."""
    try:
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word with id '{word_id}' does not exist.")
        
        existing_example = db.query(models.Examples).filter(
            models.Examples.word_id == word_id,
            models.Examples.part_of_speech == part_of_speech,
            models.Examples.example == example
        ).first()
        if existing_example:
            logger.info(f"Example already exists for word_id '{word_id}', part_of_speech '{part_of_speech}'.")
            return existing_example

        db_example = models.Examples(
            word_id=word_id,
            part_of_speech=part_of_speech,
            example=example
        )
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        
        logger.info(f"Successfully created example for part_of_speech '{part_of_speech}'.")

        return db_example
    except Exception as e:
        logger.error(f"Error creating example for part_of_speech '{part_of_speech}': {e}", exc_info=True)
        db.rollback()
        raise

def get_examples_by_word_id(db: Session, word_id: int) -> list[models.Examples]:
    """Get all examples for a specific word by its ID."""
    try:
        examples = db.query(models.Examples).filter(
            models.Examples.word_id == word_id
        ).all()
        logger.info(f"Retrieved {len(examples)} examples for word_id '{word_id}'.")
        return examples
    except Exception as e:
        logger.error(f"Error getting examples for word_id '{word_id}': {e}", exc_info=True)
        raise

def get_examples_by_part_of_speech(db: Session, part_of_speech: str) -> list[models.Examples]:
    """Get all examples for a specific part of speech."""
    try:
        examples = db.query(models.Examples).filter(models.Examples.part_of_speech == part_of_speech).all()
        logger.info(f"Retrieved {len(examples)} examples for part_of_speech '{part_of_speech}'.")
        return examples
    except Exception as e:
        logger.error(f"Error getting examples for part_of_speech '{part_of_speech}': {e}", exc_info=True)
        raise

def get_example_by_id(db: Session, id: int) -> models.Examples:
    """Get an example by its ID."""
    try:
        example = db.query(models.Examples).filter(models.Examples.id == id).one()
        logger.info(f"Example with id '{id}' retrieved successfully.")
        return example
    except NoResultFound:
        logger.warning(f"Example with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting example with id '{id}': {e}", exc_info=True)
        raise
