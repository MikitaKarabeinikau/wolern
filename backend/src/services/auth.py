from sqlalchemy.orm import Session
from backend.src.database import models
import logging

logger = logging.getLogger(__name__)


class OwnershipVerificationError(Exception):
    """Raised when ownership verification fails."""
    pass


def verify_user_owns_word_status(
    db: Session, 
    user_word_status_id: int, 
    user_id: int
) -> models.UserWordStatus:
    """
    Verify that a user owns a specific word status.
    
    Args:
        db: Database session
        user_word_status_id: ID of the word status
        user_id: ID of the user to verify
        
    Returns:
        The UserWordStatus object if verified
        
    Raises:
        ValueError: If word status doesn't exist
        OwnershipVerificationError: If user doesn't own the word status
    """
    try:
        # Get word status
        word_status = db.query(models.UserWordStatus).filter(
            models.UserWordStatus.id == user_word_status_id
        ).first()
        
        if not word_status:
            raise ValueError(f"UserWordStatus with id {user_word_status_id} not found")
        
        # Get vocabulary word
        vocab_word = db.query(models.VocabularyWords).filter(
            models.VocabularyWords.id == word_status.vocabulary_word_id
        ).first()
        
        if not vocab_word:
            raise ValueError(f"VocabularyWord not found for word status {user_word_status_id}")
        
        # Get vocabulary
        vocabulary = db.query(models.Vocabulary).filter(
            models.Vocabulary.vocabulary_id == vocab_word.vocabulary_id
        ).first()
        
        if not vocabulary:
            raise ValueError(f"Vocabulary not found")
        
        # Verify ownership
        if vocabulary.user_id != user_id:
            logger.warning(
                f"User {user_id} attempted to access word_status {user_word_status_id} "
                f"owned by user {vocabulary.user_id}"
            )
            raise OwnershipVerificationError(
                f"User {user_id} does not own this word status"
            )
        
        logger.info(f"Ownership verified: user {user_id} owns word_status {user_word_status_id}")
        return word_status
        
    except (ValueError, OwnershipVerificationError):
        raise
    except Exception as e:
        logger.error(f"Error verifying ownership: {e}", exc_info=True)
        raise


def verify_user_owns_example(
    db: Session,
    example_id: int,
    user_id: int
) -> models.UserExamples:
    """
    Verify that a user owns a specific example.
    
    Returns the example if verified, raises OwnershipVerificationError otherwise.
    """
    try:
        # Get example
        example = db.query(models.UserExamples).filter(
            models.UserExamples.id == example_id
        ).first()
        
        if not example:
            raise ValueError(f"Example with id {example_id} not found")
        
        # Verify ownership through word status
        verify_user_owns_word_status(db, example.user_word_status_id, user_id)
        
        return example
        
    except (ValueError, OwnershipVerificationError):
        raise
    except Exception as e:
        logger.error(f"Error verifying example ownership: {e}", exc_info=True)
        raise


def verify_user_owns_definition(
    db: Session,
    definition_id: int,
    user_id: int
) -> models.UserDefinitions:
    """Verify that a user owns a specific definition."""
    try:
        definition = db.query(models.UserDefinitions).filter(
            models.UserDefinitions.id == definition_id
        ).first()
        
        if not definition:
            raise ValueError(f"Definition with id {definition_id} not found")
        
        verify_user_owns_word_status(db, definition.user_word_status_id, user_id)
        
        return definition
        
    except (ValueError, OwnershipVerificationError):
        raise
    except Exception as e:
        logger.error(f"Error verifying definition ownership: {e}", exc_info=True)
        raise


def verify_user_owns_synonym(
    db: Session,
    synonym_id: int,
    user_id: int
) -> models.UserSynonyms:
    """Verify that a user owns a specific synonym."""
    try:
        synonym = db.query(models.UserSynonyms).filter(
            models.UserSynonyms.id == synonym_id
        ).first()
        
        if not synonym:
            raise ValueError(f"Synonym with id {synonym_id} not found")
        
        verify_user_owns_word_status(db, synonym.user_word_status_id, user_id)
        
        return synonym
        
    except (ValueError, OwnershipVerificationError):
        raise
    except Exception as e:
        logger.error(f"Error verifying synonym ownership: {e}", exc_info=True)
        raise


def verify_user_owns_tag(
    db: Session,
    tag_id: int,
    user_id: int
) -> models.UserTags:
    """Verify that a user owns a specific tag."""
    try:
        tag = db.query(models.UserTags).filter(
            models.UserTags.id == tag_id
        ).first()
        
        if not tag:
            raise ValueError(f"Tag with id {tag_id} not found")
        
        verify_user_owns_word_status(db, tag.user_word_status_id, user_id)
        
        return tag
        
    except (ValueError, OwnershipVerificationError):
        raise
    except Exception as e:
        logger.error(f"Error verifying tag ownership: {e}", exc_info=True)
        raise


def verify_user_owns_translation(
    db: Session,
    translation_id: int,
    user_id: int
) -> models.UserTranslations:
    """Verify that a user owns a specific translation."""
    try:
        translation = db.query(models.UserTranslations).filter(
            models.UserTranslations.id == translation_id
        ).first()
        
        if not translation:
            raise ValueError(f"Translation with id {translation_id} not found")
        
        verify_user_owns_word_status(db, translation.user_word_status_id, user_id)
        
        return translation
        
    except (ValueError, OwnershipVerificationError):
        raise
    except Exception as e:
        logger.error(f"Error verifying translation ownership: {e}", exc_info=True)
        raise

