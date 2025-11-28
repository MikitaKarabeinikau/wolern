from sqlalchemy.orm import Session
from src.database import models
from src.database.crud import (
    user_examples,
    user_definitions,
    user_synonyms,
    user_tags,
    user_translations
)
from .auth import (
    verify_user_owns_example,
    verify_user_owns_definition,
    verify_user_owns_synonym,
    verify_user_owns_tag,
    verify_user_owns_translation,
    OwnershipVerificationError
)
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# USER EXAMPLES - Secure Operations
# ============================================================================

def create_user_example_secure(
    db: Session,
    user_word_status_id: int,
    user_id: int,
    part_of_speech: str,
    example: str
) -> models.UserExamples:
    """
    Create a user example with ownership verification.
    
    Verifies that the user owns the word status before creating.
    """
    from .auth import verify_user_owns_word_status
    
    try:
        # Verify ownership
        verify_user_owns_word_status(db, user_word_status_id, user_id)
        
        # Create via CRUD
        return user_examples.create_user_example(
            db=db,
            user_word_status_id=user_word_status_id,
            part_of_speech=part_of_speech,
            example=example
        )
        
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to create example for word_status {user_word_status_id}")
        raise
    except Exception as e:
        logger.error(f"Error creating user example: {e}", exc_info=True)
        raise


def update_user_example_secure(
    db: Session,
    example_id: int,
    user_id: int,
    new_example: str
) -> models.UserExamples:
    """
    Update a user example with ownership verification.
    
    Raises OwnershipVerificationError if user doesn't own the example.
    """
    try:
        # Verify ownership
        verify_user_owns_example(db, example_id, user_id)
        
        # Update via CRUD
        return user_examples.update_user_example(
            db=db,
            id=example_id,
            new_example=new_example,
        )
        
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update example {example_id}")
        raise
    except Exception as e:
        logger.error(f"Error updating user example: {e}", exc_info=True)
        raise


def delete_user_example_secure(
    db: Session,
    example_id: int,
    user_id: int
) -> bool:
    """
    Delete a user example with ownership verification.
    
    Raises OwnershipVerificationError if user doesn't own the example.
    """
    try:
        # Verify ownership
        verify_user_owns_example(db, example_id, user_id)
        
        # Delete via CRUD
        return user_examples.delete_user_example(db=db, id=example_id)
        
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete example {example_id}")
        raise
    except Exception as e:
        logger.error(f"Error deleting user example: {e}", exc_info=True)
        raise


# ============================================================================
# USER DEFINITIONS - Secure Operations
# ============================================================================

def update_user_definition_secure(
    db: Session,
    definition_id: int,
    user_id: int,
    new_definition: str
) -> models.UserDefinitions:
    """Update a user definition with ownership verification."""
    try:
        verify_user_owns_definition(db, definition_id,user_id)
        return user_definitions.update_user_definition(db, definition_id, new_definition)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update definition {definition_id}")
        raise


def delete_user_definition_secure(
    db: Session,
    id: int,
    user_id: int
) -> bool:
    """Delete a user definition with ownership verification."""
    try:
        verify_user_owns_definition(db, id, user_id)
        return user_definitions.delete_user_definition(db, id)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete definition {id}")
        raise


# ============================================================================
# USER SYNONYMS - Secure Operations
# ============================================================================

def update_user_synonym_secure(
    db: Session,
    synonym_id: int,
    user_id: int,
    new_synonym: str
) -> models.UserSynonyms:
    """Update a user synonym with ownership verification."""
    try:
        verify_user_owns_synonym(db, synonym_id, user_id)
        return user_synonyms.update_user_synonym(db, synonym_id, new_synonym)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update synonym {synonym_id}")
        raise


def delete_user_synonym_secure(
    db: Session,
    synonym_id: int,
    user_id: int
) -> bool:
    """Delete a user synonym with ownership verification."""
    try:
        verify_user_owns_synonym(db, synonym_id, user_id)
        return user_synonyms.delete_user_synonym(db, synonym_id)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete synonym {synonym_id}")
        raise


# ============================================================================
# USER TAGS - Secure Operations
# ============================================================================

def update_user_tag_secure(
    db: Session,
    tag_id: int,
    user_id: int,
    new_tag: str
) -> models.UserTags:
    """Update a user tag with ownership verification."""
    try:
        verify_user_owns_tag(db, tag_id, user_id)
        return user_tags.update_user_tag(db, tag_id, new_tag)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update tag {tag_id}")
        raise


def delete_user_tag_secure(
    db: Session,
    tag_id: int,
    user_id: int
) -> bool:
    """Delete a user tag with ownership verification."""
    try:
        verify_user_owns_tag(db, tag_id, user_id)
        return user_tags.delete_user_tag(db, tag_id)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete tag {tag_id}")
        raise


# ============================================================================
# USER TRANSLATIONS - Secure Operations
# ============================================================================

def update_user_translation_secure(
    db: Session,
    translation_id: int,
    user_id: int,
    new_translation: str
) -> models.UserTranslations:
    """Update a user translation with ownership verification."""
    try:
        verify_user_owns_translation(db, translation_id, user_id)
        return user_translations.update_user_translation(db, translation_id, new_translation)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update translation {translation_id}")
        raise


def delete_user_translation_secure(
    db: Session,
    translation_id: int,
    user_id: int
) -> bool:
    """Delete a user translation with ownership verification."""
    try:
        verify_user_owns_translation(db, translation_id, user_id)
        return user_translations.delete_user_translation(db, translation_id)
    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete translation {translation_id}")
        raise