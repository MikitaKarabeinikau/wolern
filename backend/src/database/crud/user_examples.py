from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)

def create_user_example(db:Session,user_word_status_id:int, part_of_speech:str, example:str) -> models.UserExamples:
    """Create a new user example for a definition."""
    try:
        word_status = db.query(models.UserWordStatus).filter(models.UserWordStatus.id == user_word_status_id).first()
        if not word_status:
            raise ValueError(f"UserWordStatus with id '{user_word_status_id}' does not exist.")
        
        existing_example = db.query(models.UserExamples).filter(models.UserExamples.user_word_status_id == user_word_status_id, models.UserExamples.part_of_speech == part_of_speech, models.UserExamples.example == example).first()
        if existing_example:
            logger.warning(f"Example '{example}' for user_word_status_id '{user_word_status_id}' and part_of_speech '{part_of_speech}' already exists.")
            return existing_example

        db_user_example = models.UserExamples(
            user_word_status_id=user_word_status_id,
            part_of_speech=part_of_speech,
            example=example,
        )
        db.add(db_user_example)
        db.commit()
        db.refresh(db_user_example)
        
        logger.info(f"Successfully created user example for user_word_status_id '{user_word_status_id}'.")

        return db_user_example
    except Exception as e:
        logger.error(f"Error creating user example for user_word_status_id '{user_word_status_id}': {e}", exc_info=True)
        db.rollback()
        raise
    
def get_user_examples_by_word_status_id(db:Session,user_word_status_id:int) -> list[models.UserExamples]:
    """Get all user examples for a specific word status by its ID."""
    try:
        user_examples = db.query(models.UserExamples).filter(models.UserExamples.user_word_status_id == user_word_status_id).all()
        logger.info(f"Retrieved {len(user_examples)} user examples for user_word_status_id '{user_word_status_id}'.")
        return user_examples
    except Exception as e:
        logger.error(f"Error getting user examples for user_word_status_id '{user_word_status_id}': {e}", exc_info=True)
        raise
    
def get_user_examples_by_part_of_speech(db:Session, part_of_speech:str) -> list[models.UserExamples]:
    """Get all user examples for a specific definition by its ID."""
    try:
        user_examples = db.query(models.UserExamples).filter(models.UserExamples.part_of_speech == part_of_speech).all()
        logger.info(f"Retrieved {len(user_examples)} user examples for part_of_speech '{part_of_speech}'.")
        return user_examples
    except Exception as e:
        logger.error(f"Error getting user examples for part_of_speech '{part_of_speech}': {e}", exc_info=True)
        raise

def get_user_example_by_id(db:Session, id:int) -> models.UserExamples:
    """Get a user example by its ID."""
    try:
        user_example = db.query(models.UserExamples).filter(models.UserExamples.id == id).one()
        logger.info(f"User example with id '{id}' retrieved successfully.")
        return user_example
    except NoResultFound:
        logger.warning(f"User example with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting user example with id '{id}': {e}", exc_info=True)
        raise
    
def update_user_example(db:Session, id:int, new_example:str) -> models.UserExamples:
    """Update an existing user example."""
    try:
        user_example = db.query(models.UserExamples).filter(models.UserExamples.id == id).one()
        user_example.example = new_example
        db.commit()
        db.refresh(user_example)
        
        logger.info(f"User example with id '{id}' updated successfully.")

        return user_example
    except NoResultFound:
        logger.warning(f"User example with id '{id}' not found for update.")
        return None
    except Exception as e:
        logger.error(f"Error updating user example with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_user_example(db:Session, id:int) -> bool:
    """Delete a user example by its ID."""
    try:
        user_example = db.query(models.UserExamples).filter(models.UserExamples.id == id).one()
        db.delete(user_example)
        db.commit()
        
        logger.info(f"User example with id '{id}' deleted successfully.")

        return True
    except NoResultFound:
        logger.warning(f"User example with id '{id}' not found for deletion.")
        return False
    except Exception as e:
        logger.error(f"Error deleting user example with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise