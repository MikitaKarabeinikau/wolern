from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def create_definition(
    db: Session, word_id: int, part_of_speech: str, definition: str
) -> models.Definitions:
    """Create a new definition for a word."""
    try:
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word with id '{word_id}' does not exist.")

        existing_definition = (
            db.query(models.Definitions)
            .filter(
                models.Definitions.word_id == word_id,
                models.Definitions.part_of_speech == part_of_speech,
                models.Definitions.definition == definition,
            )
            .first()
        )

        if existing_definition:
            logger.info(
                f"Definition already exists for word_id '{word_id}' \\\
                    , part_of_speech '{part_of_speech}'."
            )
            return existing_definition

        db_definition = models.Definitions(
            word_id=word_id, part_of_speech=part_of_speech, definition=definition
        )
        db.add(db_definition)
        db.commit()
        db.refresh(db_definition)

        logger.info(f"Successfully created definition for word_id '{word_id}'.")

        return db_definition
    except Exception as e:
        logger.error(f"Error creating definition for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise


def get_definitions_by_word_id(db: Session, word_id: int) -> list[models.Definitions]:
    """Get all definitions for a specific word by its ID."""
    try:
        definitions = (
            db.query(models.Definitions).filter(models.Definitions.word_id == word_id).all()
        )
        logger.info(f"Retrieved {len(definitions)} definitions for word_id '{word_id}'.")
        return definitions
    except Exception as e:
        logger.error(f"Error getting definitions for word_id '{word_id}': {e}", exc_info=True)
        raise


def get_definition_by_id(db: Session, definition_id: int) -> models.Definitions:
    """Get a definition by its ID."""
    try:
        definition = (
            db.query(models.Definitions).filter(models.Definitions.id == definition_id).one()
        )
        logger.info(f"Definition with id '{definition_id}' retrieved successfully.")
        return definition
    except NoResultFound:
        logger.warning(f"Definition with id '{definition_id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting definition with id '{definition_id}': {e}", exc_info=True)
        raise
