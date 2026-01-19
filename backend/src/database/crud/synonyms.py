from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def create_synonym(db: Session, word_id: int, synonym: str) -> models.Synonyms:
    """Create a new synonym for a word."""
    try:
        synonym = synonym.lower()
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word with id '{word_id}' does not exist.")

        existing_synonym = (
            db.query(models.Synonyms)
            .filter(models.Synonyms.word_id == word_id, models.Synonyms.synonym == synonym)
            .first()
        )

        if existing_synonym:
            logger.info(f"Synonym already exists for word_id '{word_id}'.")
            return existing_synonym

        db_synonym = models.Synonyms(word_id=word_id, synonym=synonym)
        db.add(db_synonym)
        db.commit()
        db.refresh(db_synonym)

        logger.info(f"Successfully created synonym for word_id '{word_id}'.")

        return db_synonym
    except Exception as e:
        logger.error(f"Error creating synonym for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise


def get_synonyms_by_word_id(db: Session, word_id: int) -> list[models.Synonyms]:
    """Get all synonyms for a specific word by its ID."""
    try:
        synonyms = db.query(models.Synonyms).filter(models.Synonyms.word_id == word_id).all()
        logger.info(f"Retrieved {len(synonyms)} synonyms for word_id '{word_id}'.")
        return synonyms
    except Exception as e:
        logger.error(f"Error getting synonyms for word_id '{word_id}': {e}", exc_info=True)
        raise


def get_synonym_by_id(db: Session, id: int) -> models.Synonyms:
    """Get a synonym by its ID."""
    try:
        synonym = db.query(models.Synonyms).filter(models.Synonyms.id == id).one()
        logger.info(f"Synonym with id '{id}' retrieved successfully.")
        return synonym
    except NoResultFound:
        logger.warning(f"Synonym with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting synonym with id '{id}': {e}", exc_info=True)
        raise
