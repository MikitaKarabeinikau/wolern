from typing import Optional
from services.auth import OwnershipVerificationError, verify_user_owns_word_status
from services.word_service import get_full_word_data_by_id, get_word_definitions, get_word_examples, get_word_synonyms, get_word_tags, get_word_translations
from sqlalchemy.orm import Session, joinedload
from backend.src.database import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def get_word_learning_stage(db: Session, user_word_status_id: int) -> int:
    """Retrieve the learning stage for a given user word status."""
    try:
        user_quiz_progress = (
            db.query(models.UserQuizProgress)
            .filter(models.UserQuizProgress.user_word_status_id == user_word_status_id)
            .one()
        )
        return user_quiz_progress.learning_stage
    except NoResultFound:
        logger.warning(f"User quiz progress for word status id '{user_word_status_id}' not found.")
        return 0
    except Exception as e:
        logger.error(
            f"Error retrieving learning stage for word status id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise


def get_all_words_by_learning_stage(
    db: Session, user_id: int, learning_stage: int
) -> list[models.UserWordStatus]:
    """Retrieve all user word statuses for a user at a specific learning stage."""
    try:
        word_statuses = (
            db.query(models.UserWordStatus)
            .join(models.UserQuizProgress)
            .filter(
                models.UserWordStatus.user_id == user_id,
                models.UserQuizProgress.learning_stage == learning_stage,
            )
            .all()
        )
        return word_statuses
    except Exception as e:
        logger.error(
            f"Error retrieving word statuses for user id \\\
                '{user_id}' at learning stage '{learning_stage}': {e}",
            exc_info=True,
        )
        raise

def get_user_word_status_by_vocabulary_word_id(db: Session, vocabulary_word_id: int) -> models.UserWordStatus:
    """Retrieve UserWordStatus by vocabulary_word_id."""
    try:
        status = (
            db.query(models.UserWordStatus)
            .filter(models.UserWordStatus.vocabulary_word_id == vocabulary_word_id)
            .one()
        )
        return status
    except NoResultFound:
        logger.warning(f"UserWordStatus for vocabulary_word_id '{vocabulary_word_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving UserWordStatus for vocabulary_word_id '{vocabulary_word_id}': {e}",
            exc_info=True,
        )
        raise

def get_word_id_by_user_word_status_id(db: Session, user_word_status_id: int) -> int:
    """Retrieve word_id associated with a given user_word_status_id."""
    try:
        result = (
            db.query(models.VocabularyWords.word_id)
            .join(models.UserWordStatus, models.VocabularyWords.vocabulary_id == models.UserWordStatus.vocabulary_word_id)
            .filter(models.UserWordStatus.id == user_word_status_id)
            .one()
        )
        return result.word_id
    except NoResultFound:
        logger.warning(f"Word ID for user_word_status_id '{user_word_status_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving word ID for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def get_full_word_data_by_user_word_status_id(db: Session, user_word_status_id: int) -> Optional[models.Words]:
    return db.query(models.Words).options(
            joinedload(models.Words.definitions),
            joinedload(models.Words.examples),
            joinedload(models.Words.synonyms),
            joinedload(models.Words.translations),
            joinedload(models.Words.tags),
            joinedload(models.Words.warnings)
        )

def get_full_user_word_status_by_user_word_status_id(db: Session, user_word_status_id: int) -> Optional[models.UserWordStatus]:
    """Retrieve full UserWordStatus with related Word data by user_word_status_id."""
    try:
        user_word_status = (
            db.query(models.UserWordStatus)
            .options(
                joinedload(models.UserWordStatus.user_definitions),
                joinedload(models.UserWordStatus.user_examples),
                joinedload(models.UserWordStatus.user_synonyms),
                joinedload(models.UserWordStatus.user_translations),
                joinedload(models.UserWordStatus.user_tags),
                joinedload(models.UserWordStatus.user_quiz_progress),
                joinedload(models.UserWordStatus.hidden_base_definitions),
                joinedload(models.UserWordStatus.hidden_base_examples),
                joinedload(models.UserWordStatus.hidden_base_synonyms),
                joinedload(models.UserWordStatus.hidden_base_tags),
                joinedload(models.UserWordStatus.hidden_base_translations)
                )
            .filter(models.UserWordStatus.user_word_status_id == user_word_status_id)
            .one()
        )
        return user_word_status
    except NoResultFound:
        logger.warning(f"UserWordStatus for user_word_status_id '{user_word_status_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving UserWordStatus for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def get_full_user_word_status_by_vocabulary_word_id(db: Session, vocabulary_word_id: int) -> Optional[models.UserWordStatus]:
    """Retrieve full UserWordStatus with related Word data by vocabulary_word_id."""
    try:
        user_word_status = (
            db.query(models.UserWordStatus)
            .options(
                joinedload(models.UserWordStatus.user_definitions),
                joinedload(models.UserWordStatus.user_examples),
                joinedload(models.UserWordStatus.user_synonyms),
                joinedload(models.UserWordStatus.user_translations),
                joinedload(models.UserWordStatus.user_tags),
                joinedload(models.UserWordStatus.user_quiz_progress),
                joinedload(models.UserWordStatus.hidden_base_definitions),
                joinedload(models.UserWordStatus.hidden_base_examples),
                joinedload(models.UserWordStatus.hidden_base_synonyms),
                joinedload(models.UserWordStatus.hidden_base_tags),
                joinedload(models.UserWordStatus.hidden_base_translations)
                )
        )
        return user_word_status
    except NoResultFound:
        logger.warning(f"UserWordStatus for vocabulary_word_id '{vocabulary_word_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving UserWordStatus for vocabulary_word_id '{vocabulary_word_id}': {e}",
            exc_info=True,
        )
        raise

def create_user_hidden_translation_secure(
    db: Session,
    user_word_status_id: int,
    translation_id: int
) -> models.UserHiddenBaseTranslation:
    """Create a UserHiddenBaseTranslations entry securely."""
    try:
        existed_hidden_translation = (
            db.query(models.UserHiddenBaseTranslation)
            .filter(
                models.UserHiddenBaseTranslation.user_word_status_id == user_word_status_id,
                models.UserHiddenBaseTranslation.translation_id == translation_id
            )
            .first()
        )
        if existed_hidden_translation:
            raise ValueError(f"Translation ID '{translation_id}' is already hidden for user_word_status_id '{user_word_status_id}'.")
        word = get_word_translations(db, get_word_id_by_user_word_status_id(db, user_word_status_id))
        translation_ids = [t.id for t in word.translations]
        if translation_id not in translation_ids:
            raise ValueError(f"Translation ID '{translation_id}' does not belong to the word associated with user_word_status_id '{user_word_status_id}'.")
        user_hidden_translation = models.UserHiddenBaseTranslation(
            user_word_status_id=user_word_status_id,
            translation_id=translation_id
        )
        db.add(user_hidden_translation)
        db.commit()
        db.refresh(user_hidden_translation)
        return user_hidden_translation
    except Exception as e:
        logger.error(
            f"Error creating UserHiddenBaseTranslations for user_word_status_id '{user_word_status_id}' and translation_id '{translation_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def delete_user_hidden_translation_secure(
    db: Session,
    user_id: int,
    hidden_translation_id: int
) -> None:
    """Delete a UserHiddenBaseTranslations entry securely."""
    try:
        hidden_translation = (
            db.query(models.UserHiddenBaseTranslation)
            .join(models.UserWordStatus, models.UserHiddenBaseTranslation.user_word_status_id == models.UserWordStatus.id)
            .filter(models.UserHiddenBaseTranslation.id == hidden_translation_id)
            .one()
        )
        verify_user_owns_word_status(db, user_id, hidden_translation.user_word_status_id)
        db.delete(hidden_translation)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting UserHiddenBaseTranslation with ID '{hidden_translation_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def create_user_hidden_definition_secure(
    db: Session,
    user_word_status_id: int,
    definition_id: int
) -> models.UserHiddenBaseDefinition:
    """Create a UserHiddenBaseDefinition entry securely."""
    try:
        existed_hidden_definition = (
            db.query(models.UserHiddenBaseDefinition)
            .filter(
                models.UserHiddenBaseDefinition.user_word_status_id == user_word_status_id,
                models.UserHiddenBaseDefinition.definition_id == definition_id
            )
            .first()
        )
        if existed_hidden_definition:
            raise ValueError(f"Definition ID '{definition_id}' is already hidden for user_word_status_id '{user_word_status_id}'.")
        word = get_word_definitions(db, get_word_id_by_user_word_status_id(db, user_word_status_id))
        definition_ids = [d.id for d in word.definitions]
        if definition_id not in definition_ids:
            raise ValueError(f"Definition ID '{definition_id}' does not belong to the word associated with user_word_status_id '{user_word_status_id}'.")
        user_hidden_definition = models.UserHiddenBaseDefinition(
            user_word_status_id=user_word_status_id,
            definition_id=definition_id
        )
        db.add(user_hidden_definition)
        db.commit()
        db.refresh(user_hidden_definition)
        return user_hidden_definition
    except Exception as e:
        logger.error(
            f"Error creating UserHiddenBaseDefinition for user_word_status_id '{user_word_status_id}' and definition_id '{definition_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def delete_user_hidden_definition_secure(
    db: Session,
    user_id: int,
    hidden_definition_id: int
) -> None:
    """Delete a UserHiddenBaseDefinition entry securely."""
    try:
        hidden_definition = (
            db.query(models.UserHiddenBaseDefinition)
            .join(models.UserWordStatus, models.UserHiddenBaseDefinition.user_word_status_id == models.UserWordStatus.id)
            .filter(models.UserHiddenBaseDefinition.id == hidden_definition_id)
            .one()
        )
        verify_user_owns_word_status(db, user_id, hidden_definition.user_word_status_id)
        db.delete(hidden_definition)
        db.commit()
    except OwnershipVerificationError as e:
        logger.error(
            f"Error deleting UserHiddenBaseDefinition with ID '{hidden_definition_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def create_user_hidden_example_secure(
    db: Session,
    user_word_status_id: int,
    example_id: int
) -> models.UserHiddenBaseExample:
    """Create a UserHiddenBaseExample entry securely."""
    try:
        existed_hidden_example = (
            db.query(models.UserHiddenBaseExample)
            .filter(
                models.UserHiddenBaseExample.user_word_status_id == user_word_status_id,
                models.UserHiddenBaseExample.example_id == example_id
            )
            .first()
        )
        if existed_hidden_example:
            raise ValueError(f"Example ID '{example_id}' is already hidden for user_word_status_id '{user_word_status_id}'.")
        word = get_word_examples(db, get_word_id_by_user_word_status_id(db, user_word_status_id))
        example_ids = [e.id for e in word.examples]
        if example_id not in example_ids:
            raise ValueError(f"Example ID '{example_id}' does not belong to the word associated with user_word_status_id '{user_word_status_id}'.")
        user_hidden_example = models.UserHiddenBaseExample(
            user_word_status_id=user_word_status_id,
            example_id=example_id
        )
        db.add(user_hidden_example)
        db.commit()
        db.refresh(user_hidden_example)
        return user_hidden_example
    except Exception as e:
        logger.error(
            f"Error creating UserHiddenBaseExample for user_word_status_id '{user_word_status_id}' and example_id '{example_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def delete_user_hidden_example_secure(
    db: Session,
    user_id: int,
    hidden_example_id: int
) -> None:
    """Delete a UserHiddenBaseExample entry securely."""
    try:
        hidden_example = (
            db.query(models.UserHiddenBaseExample)
            .join(models.UserWordStatus, models.UserHiddenBaseExample.user_word_status_id == models.UserWordStatus.id)
            .filter(models.UserHiddenBaseExample.id == hidden_example_id)
            .one()
        )
        verify_user_owns_word_status(db, user_id, hidden_example.user_word_status_id)
        db.delete(hidden_example)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting UserHiddenBaseExample with ID '{hidden_example_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def create_user_hidden_synonym_secure(
    db: Session,
    user_word_status_id: int,
    synonym_id: int
) -> models.UserHiddenBaseSynonym:
    """Create a UserHiddenBaseSynonym entry securely."""
    existed_hidden_synonym = db.query(models.UserHiddenBaseSynonym).filter(
        models.UserHiddenBaseSynonym.user_word_status_id == user_word_status_id,
        models.UserHiddenBaseSynonym.synonym_id == synonym_id
    ).first()
    if existed_hidden_synonym:
        raise ValueError(f"Synonym ID '{synonym_id}' is already hidden for user_word_status_id '{user_word_status_id}'.")
    try:
        existed_hidden_synonym = (
            db.query(models.UserHiddenBaseSynonym)
            .filter(
                models.UserHiddenBaseSynonym.user_word_status_id == user_word_status_id,
                models.UserHiddenBaseSynonym.synonym_id == synonym_id
            )
            .first()
        )
        if existed_hidden_synonym:
            raise ValueError(f"Synonym ID '{synonym_id}' is already hidden for user_word_status_id '{user_word_status_id}'.")
        word = get_word_synonyms(db, get_word_id_by_user_word_status_id(db, user_word_status_id))
        synonym_ids = [s.id for s in word.synonyms]
        if synonym_id not in synonym_ids:
            raise ValueError(f"Synonym ID '{synonym_id}' does not belong to the word associated with user_word_status_id '{user_word_status_id}'.")
        user_hidden_synonym = models.UserHiddenBaseSynonym(
            user_word_status_id=user_word_status_id,
            synonym_id=synonym_id
        )
        db.add(user_hidden_synonym)
        db.commit()
        db.refresh(user_hidden_synonym)
        return user_hidden_synonym
    except Exception as e:
        logger.error(
            f"Error creating UserHiddenBaseSynonym for user_word_status_id '{user_word_status_id}' and synonym_id '{synonym_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def delete_user_hidden_synonym_secure(
    db: Session,
    user_id: int,
    hidden_synonym_id: int
) -> None:
    """Delete a UserHiddenBaseSynonym entry securely."""
    try:
        hidden_synonym = (
            db.query(models.UserHiddenBaseSynonym)
            .join(models.UserWordStatus, models.UserHiddenBaseSynonym.user_word_status_id == models.UserWordStatus.id)
            .filter(models.UserHiddenBaseSynonym.id == hidden_synonym_id)
            .one()
        )
        verify_user_owns_word_status(db, user_id, hidden_synonym.user_word_status_id)
        db.delete(hidden_synonym)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting UserHiddenBaseSynonym with ID '{hidden_synonym_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def create_user_hidden_tag_secure(
    db: Session,
    user_word_status_id: int,
    tag_id: int
) -> models.UserHiddenBaseTag:
    """Create a UserHiddenBaseTag entry securely."""
    try:
        existed_hidden_tag = (
            db.query(models.UserHiddenBaseTag)
            .filter(
                models.UserHiddenBaseTag.user_word_status_id == user_word_status_id,
                models.UserHiddenBaseTag.tag_id == tag_id
            )
            .first()
        )
        if existed_hidden_tag:
            raise ValueError(f"Tag ID '{tag_id}' is already hidden for user_word_status_id '{user_word_status_id}'.")
        word = get_word_tags(db, get_word_id_by_user_word_status_id(db, user_word_status_id))
        tag_ids = [t.id for t in word.tags]
        if tag_id not in tag_ids:
            raise ValueError(f"Tag ID '{tag_id}' does not belong to the word associated with user_word_status_id '{user_word_status_id}'.")
        user_hidden_tag = models.UserHiddenBaseTag(
            user_word_status_id=user_word_status_id,
            tag_id=tag_id
        )
        db.add(user_hidden_tag)
        db.commit()
        db.refresh(user_hidden_tag)
        return user_hidden_tag
    except Exception as e:
        logger.error(
            f"Error creating UserHiddenBaseTag for user_word_status_id '{user_word_status_id}' and tag_id '{tag_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def delete_user_hidden_tag_secure(
    db: Session,
    user_id: int,
    hidden_tag_id: int
) -> None:
    """Delete a UserHiddenBaseTag entry securely."""
    try:
        hidden_tag = (
            db.query(models.UserHiddenBaseTag)
            .join(models.UserWordStatus, models.UserHiddenBaseTag.user_word_status_id == models.UserWordStatus.id)
            .filter(models.UserHiddenBaseTag.id == hidden_tag_id)
            .one()
        )
        verify_user_owns_word_status(db, user_id, hidden_tag.user_word_status_id)
        db.delete(hidden_tag)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting UserHiddenBaseTag with ID '{hidden_tag_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def requiered_word_data_with_user_word_status(
    db: Session,
    user_word_status: models.UserWordStatus
) -> models.UserWordStatus:
    """Combine base word data with user-specific word status data."""
    user_data = get_full_user_word_status_by_user_word_status_id(
        db= db,
        user_word_status_id=user_word_status.user_word_status_id)
    base_word_data = get_full_word_data_by_user_word_status_id(
        db= db,
        user_word_status_id=user_word_status.user_word_status_id)
    combine_data = {
        "base_word_data": base_word_data,
        "user_data": user_data
    }
    return combine_data
