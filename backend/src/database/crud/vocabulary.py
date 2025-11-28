from sqlalchemy.orm import Session
from .. import models
import logging
from src.config import settings
from typing import Optional, List

logger = logging.getLogger(__name__)

def create_vocabulary(db:Session, user_id: int , name: str)-> models.Vocabulary:
    """Create a new vocabulary list for a user."""
    try:
        if get_number_of_vocabularies_by_user(db, user_id) >= settings.MAX_VOCABULARIES_PER_USER:
            raise ValueError(f"User with id '{user_id}' has reached the maximum number of vocabularies.")
        
        db_vocabulary = models.Vocabulary(
            user_id=user_id,
            name=name
        )
        db.add(db_vocabulary)
        logger.info(f"Vocabulary '{name}' for user_id '{user_id}' added to session.")
        db.commit()
        db.refresh(db_vocabulary)
        
        logger.info(f"Successfully created vocabulary '{name}' for user_id '{user_id}'.")

        return db_vocabulary
    except Exception as e:
        logger.error(f"Error creating vocabulary '{name}' for user_id '{user_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_vocabulary_by_vocabulary_id(db: Session, vocabulary_id: int) -> Optional[models.Vocabulary]:
    """Get vocabulary by ID."""
    try:
        return db.query(models.Vocabulary).filter(
            models.Vocabulary.vocabulary_id == vocabulary_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting vocabulary: {e}", exc_info=True)
        raise

def get_number_of_vocabularies_by_user(db: Session, user_id: int) -> int:
    """Get the number of vocabulary lists for a specific user."""
    try:
        count = db.query(models.Vocabulary).filter(models.Vocabulary.user_id == user_id).count()
        logger.info(f"User_id '{user_id}' has {count} vocabularies.")
        return count
    except Exception as e:
        logger.error(f"Error getting number of vocabularies for user_id '{user_id}': {e}", exc_info=True)
        raise
    
def update_vocabulary_name(db: Session, user_id: int, vocabulary_id: int, new_name: str) -> Optional[models.Vocabulary]:
    """Update the name of a vocabulary list."""
    try:
        vocabulary = db.query(models.Vocabulary).filter(models.Vocabulary.vocabulary_id == vocabulary_id).first()
        if not vocabulary:
            logger.warning(f"Vocabulary with id '{vocabulary_id}' not found.")
            return None

        if user_id is not None and vocabulary.user_id != user_id:
            raise PermissionError(f"User {user_id} does not own vocabulary {vocabulary_id}")

        vocabulary.name = new_name
        db.commit()
        db.refresh(vocabulary)
        logger.info(f"Vocabulary id '{vocabulary_id}' name updated to '{new_name}'.")
        return vocabulary
    except PermissionError:
        raise
    except Exception as e:
        logger.error(f"Error updating vocabulary id '{vocabulary_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_vocabulary_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Vocabulary]:
    """Get all vocabulary lists for a specific user with pagination."""
    try:
        vocabularies = db.query(models.Vocabulary).filter(
            models.Vocabulary.user_id == user_id
        ).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(vocabularies)} vocabularies for user_id '{user_id}'.")
        return vocabularies
    except Exception as e:
        logger.error(f"Error getting vocabularies for user_id '{user_id}': {e}", exc_info=True)
        raise
    
def delete_vocabulary(db: Session, user_id: int, vocabulary_id: int) -> bool:
    """Delete a vocabulary list."""
    try:
        vocabulary = db.query(models.Vocabulary).filter(models.Vocabulary.vocabulary_id == vocabulary_id).first()
        if not vocabulary:
            logger.warning(f"Vocabulary with id '{vocabulary_id}' not found.")
            return False
        if user_id is not None and vocabulary.user_id != user_id:
            raise PermissionError(f"User {user_id} does not own vocabulary {vocabulary_id}")
      
        db.delete(vocabulary)
        db.commit()
        logger.info(f"Vocabulary id '{vocabulary_id}' deleted.")
        return True
    except PermissionError:
        raise
    except Exception as e:
        logger.error(f"Error deleting vocabulary id '{vocabulary_id}': {e}", exc_info=True)
        db.rollback()
        raise