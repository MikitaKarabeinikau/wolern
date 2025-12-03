from typing import Optional
from sqlalchemy.orm import Session
from backend.src.database import models
from backend.src.database.crud import (
    user_examples,
    user_definitions,
    user_synonyms,
    user_tags,
    user_translations,
)
from .auth import (
    verify_user_owns_example,
    verify_user_owns_definition,
    verify_user_owns_synonym,
    verify_user_owns_tag,
    verify_user_owns_translation,
    OwnershipVerificationError,
)
import logging

logger = logging.getLogger(__name__)


# Custom exception for not found errors
class NotFoundError(Exception):
    """Raised when a resource is not found."""

    pass


# ============================================================================
# USER EXAMPLES - Secure Operations
# ============================================================================


def create_user_example_secure(
    db: Session, user_word_status_id: int, user_id: int, part_of_speech: str, example: str
) -> models.UserExamples:
    """Create a user example with ownership verification."""
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)

        return user_examples.create_user_example(
            db=db,
            user_word_status_id=user_word_status_id,
            part_of_speech=part_of_speech,
            example=example,
        )

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to create example for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error creating user example: {e}", exc_info=True)
        raise


def get_user_example_secure(db: Session, example_id: int, user_id: int) -> models.UserExamples:
    """Get a user example with ownership verification."""
    try:
        verify_user_owns_example(db, example_id, user_id)
        example = user_examples.get_user_example_by_id(db, example_id)

        if not example:
            raise NotFoundError(f"Example {example_id} not found")

        return example

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to access example {example_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user example: {e}", exc_info=True)
        raise


def get_user_examples_by_word_status_secure(
    db: Session, user_word_status_id: int, user_id: int
) -> list[models.UserExamples]:
    """Get all examples for a word status with ownership verification."""
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)
        return user_examples.get_examples_by_word_status(db, user_word_status_id)

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to access examples for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error retrieving examples: {e}", exc_info=True)
        raise


def update_user_example_secure(
    db: Session,
    example_id: int,
    user_id: int,
    part_of_speech: Optional[str] = None,
    example: Optional[str] = None,
) -> models.UserExamples:
    """Update a user example with ownership verification."""
    try:
        verify_user_owns_example(db, example_id, user_id)

        updated = user_examples.update_user_example(
            db=db, id=example_id, part_of_speech=part_of_speech, new_example=example
        )

        if not updated:
            raise NotFoundError(f"Example {example_id} not found")

        return updated

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update example {example_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error updating user example: {e}", exc_info=True)
        raise


def delete_user_example_secure(db: Session, example_id: int, user_id: int) -> bool:
    """Delete a user example with ownership verification."""
    try:
        verify_user_owns_example(db, example_id, user_id)

        success = user_examples.delete_user_example(db=db, id=example_id)

        if not success:
            raise NotFoundError(f"Example {example_id} not found")

        return success

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete example {example_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting user example: {e}", exc_info=True)
        raise


# ============================================================================
# USER DEFINITIONS - Secure Operations
# ============================================================================


def create_user_definition_secure(
    db: Session, user_word_status_id: int, user_id: int, part_of_speech: str, definition: str
) -> models.UserDefinitions:
    """Create a user definition with ownership verification."""
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)

        return user_definitions.create_user_definition(
            db=db,
            user_word_status_id=user_word_status_id,
            part_of_speech=part_of_speech,
            definition=definition,
        )

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to create definition for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error creating user definition: {e}", exc_info=True)
        raise


def get_user_definition_secure(
    db: Session, definition_id: int, user_id: int
) -> models.UserDefinitions:
    """Get a user definition with ownership verification."""
    try:
        verify_user_owns_definition(db, definition_id, user_id)
        return user_definitions.get_user_definition_by_id(db, definition_id)

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to access definition {definition_id}")
        raise
    except Exception as e:
        logger.error(f"Error retrieving user definition: {e}", exc_info=True)
        raise


def update_user_definition_secure(
    db: Session,
    definition_id: int,
    user_id: int,
    part_of_speech: Optional[str] = None,
    definition: Optional[str] = None,
) -> models.UserDefinitions:
    """Update a user definition with ownership verification."""
    try:
        verify_user_owns_definition(db, definition_id, user_id)

        return user_definitions.update_user_definition(
            db=db, definition_id=definition_id, part_of_speech=part_of_speech, definition=definition
        )

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update definition {definition_id}")
        raise
    except Exception as e:
        logger.error(f"Error updating user definition: {e}", exc_info=True)
        raise


def delete_user_definition_secure(db: Session, definition_id: int, user_id: int) -> bool:
    """Delete a user definition with ownership verification."""
    try:
        verify_user_owns_definition(db, definition_id, user_id)
        return user_definitions.delete_user_definition(db, definition_id)

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete definition {definition_id}")
        raise
    except Exception as e:
        logger.error(f"Error deleting user definition: {e}", exc_info=True)
        raise


def get_definitions_for_word_status_secure(
    db: Session, user_word_status_id: int, user_id: int
) -> list[models.UserDefinitions]:
    """Get all definitions for a word status with ownership verification."""
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)
        return user_definitions.get_user_definitions_by_user_word_status_id(db, user_word_status_id)

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to access definitions for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error retrieving definitions: {e}", exc_info=True)
        raise


# ============================================================================
# USER SYNONYMS - Secure Operations
# ============================================================================


def create_user_synonym_secure(
    db: Session, user_word_status_id: int, user_id: int, synonym: str
) -> models.UserSynonyms:
    """
    Create a user synonym with ownership verification.

    Args:
        db: Database session
        user_word_status_id: Word status ID to attach synonym to
        user_id: User ID (for ownership verification)
        synonym: The synonym text

    Returns:
        Created UserSynonyms object

    Raises:
        OwnershipVerificationError: If user doesn't own word status
    """
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)

        return user_synonyms.create_user_synonym(
            db=db, user_word_status_id=user_word_status_id, synonym=synonym
        )

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to create synonym for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error creating user synonym: {e}", exc_info=True)
        raise


def get_user_synonym_secure(db: Session, synonym_id: int, user_id: int) -> models.UserSynonyms:
    """
    Get a user synonym with ownership verification.

    Args:
        db: Database session
        synonym_id: Synonym ID to retrieve
        user_id: User ID (for ownership verification)

    Returns:
        UserSynonyms object

    Raises:
        OwnershipVerificationError: If user doesn't own synonym
        NotFoundError: If synonym doesn't exist
    """
    try:
        verify_user_owns_synonym(db, synonym_id, user_id)
        synonym = user_synonyms.get_user_synonym_by_id(db, synonym_id)

        if not synonym:
            raise NotFoundError(f"Synonym {synonym_id} not found")

        return synonym

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to access synonym {synonym_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user synonym: {e}", exc_info=True)
        raise


def list_user_synonyms_by_word_status_secure(
    db: Session, user_word_status_id: int, user_id: int
) -> list[models.UserSynonyms]:
    """
    Get all synonyms for a word status with ownership verification.

    Args:
        db: Database session
        user_word_status_id: Word status ID
        user_id: User ID (for ownership verification)

    Returns:
        List of UserSynonyms objects

    Raises:
        OwnershipVerificationError: If user doesn't own word status
    """
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)
        return user_synonyms.get_synonyms_by_word_status(db, user_word_status_id)

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to access synonyms for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error retrieving synonyms: {e}", exc_info=True)
        raise


def update_user_synonym_secure(
    db: Session, synonym_id: int, user_id: int, synonym: str
) -> models.UserSynonyms:
    """
    Update a user synonym with ownership verification.

    Args:
        db: Database session
        synonym_id: Synonym ID to update
        user_id: User ID (for ownership verification)
        synonym: New synonym text

    Returns:
        Updated UserSynonyms object

    Raises:
        OwnershipVerificationError: If user doesn't own synonym
        NotFoundError: If synonym doesn't exist
    """
    try:
        verify_user_owns_synonym(db, synonym_id, user_id)

        updated = user_synonyms.update_user_synonym(db, synonym_id, synonym)

        if not updated:
            raise NotFoundError(f"Synonym {synonym_id} not found")

        return updated

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update synonym {synonym_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error updating user synonym: {e}", exc_info=True)
        raise


def delete_user_synonym_secure(db: Session, synonym_id: int, user_id: int) -> bool:
    """
    Delete a user synonym with ownership verification.

    Args:
        db: Database session
        synonym_id: Synonym ID to delete
        user_id: User ID (for ownership verification)

    Returns:
        True if deleted successfully

    Raises:
        OwnershipVerificationError: If user doesn't own synonym
        NotFoundError: If synonym doesn't exist
    """
    try:
        verify_user_owns_synonym(db, synonym_id, user_id)

        success = user_synonyms.delete_user_synonym(db, synonym_id)

        if not success:
            raise NotFoundError(f"Synonym {synonym_id} not found")

        return success

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete synonym {synonym_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting user synonym: {e}", exc_info=True)
        raise


# ============================================================================
# USER TAGS - Secure Operations
# ============================================================================
def create_user_tag_secure(
    db: Session, user_word_status_id: int, user_id: int, tag: str
) -> models.UserTags:
    """
    Create a user tag with ownership verification.

    Args:
        db: Database session
        user_word_status_id: Word status ID to attach tag to
        user_id: User ID (for ownership verification)
        tag: The tag text

    Returns:
        Created UserTags object

    Raises:
        OwnershipVerificationError: If user doesn't own word status
    """
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)

        return user_tags.create_user_tag(db=db, user_word_status_id=user_word_status_id, tag=tag)

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to create tag for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error creating user tag: {e}", exc_info=True)
        raise


def get_user_tag_secure(db: Session, tag_id: int, user_id: int) -> models.UserTags:
    """
    Get a user tag with ownership verification.

    Args:
        db: Database session
        tag_id: Tag ID to retrieve
        user_id: User ID (for ownership verification)

    Returns:
        UserTags object

    Raises:
        OwnershipVerificationError: If user doesn't own tag
        NotFoundError: If tag doesn't exist
    """
    try:
        verify_user_owns_tag(db, tag_id, user_id)
        tag = user_tags.get_user_tag_by_id(db, tag_id)

        if not tag:
            raise NotFoundError(f"Tag {tag_id} not found")

        return tag

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to access tag {tag_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user tag: {e}", exc_info=True)
        raise


def list_user_tags_by_word_status_secure(
    db: Session, user_word_status_id: int, user_id: int
) -> list[models.UserTags]:
    """
    Get all tags for a word status with ownership verification.

    Args:
        db: Database session
        user_word_status_id: Word status ID
        user_id: User ID (for ownership verification)

    Returns:
        List of UserTags objects

    Raises:
        OwnershipVerificationError: If user doesn't own word status
    """
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)
        return user_tags.get_user_definitions_by_user_word_status_id(db, user_word_status_id)

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to access tags for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error retrieving tags: {e}", exc_info=True)
        raise


def update_user_tag_secure(db: Session, tag_id: int, user_id: int, tag: str) -> models.UserTags:
    """
    Update a user tag with ownership verification.

    Args:
        db: Database session
        tag_id: Tag ID to update
        user_id: User ID (for ownership verification)
        tag: New tag text

    Returns:
        Updated UserTags object

    Raises:
        OwnershipVerificationError: If user doesn't own tag
        NotFoundError: If tag doesn't exist
    """
    try:
        verify_user_owns_tag(db, tag_id, user_id)

        updated = user_tags.update_user_tag(db, tag_id, tag)

        if not updated:
            raise NotFoundError(f"Tag {tag_id} not found")

        return updated

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update tag {tag_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error updating user tag: {e}", exc_info=True)
        raise


def delete_user_tag_secure(db: Session, tag_id: int, user_id: int) -> bool:
    """
    Delete a user tag with ownership verification.

    Args:
        db: Database session
        tag_id: Tag ID to delete
        user_id: User ID (for ownership verification)

    Returns:
        True if deleted successfully

    Raises:
        OwnershipVerificationError: If user doesn't own tag
        NotFoundError: If tag doesn't exist
    """
    try:
        verify_user_owns_tag(db, tag_id, user_id)

        success = user_tags.delete_user_tag(db, tag_id)

        if not success:
            raise NotFoundError(f"Tag {tag_id} not found")

        return success

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete tag {tag_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting user tag: {e}", exc_info=True)
        raise


# ============================================================================
# USER TRANSLATIONS - Secure Operations
# ============================================================================


def create_user_translation_secure(
    db: Session, user_word_status_id: int, user_id: int, language: str, translation: str
) -> models.UserTranslations:
    """
    Create a user translation with ownership verification.

    Args:
        db: Database session
        user_word_status_id: Word status ID to attach translation to
        user_id: User ID (for ownership verification)
        language: Language of the translation
        translation: The translated text

    Returns:
        Created UserTranslations object

    Raises:
        OwnershipVerificationError: If user doesn't own word status
    """
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)

        return user_translations.create_user_translation(
            db=db,
            user_word_status_id=user_word_status_id,
            language=language,
            translation=translation,
        )

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to create translation for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error creating user translation: {e}", exc_info=True)
        raise


def get_user_translation_secure(
    db: Session, translation_id: int, user_id: int
) -> models.UserTranslations:
    """
    Get a user translation with ownership verification.

    Args:
        db: Database session
        translation_id: Translation ID to retrieve
        user_id: User ID (for ownership verification)

    Returns:
        UserTranslations object

    Raises:
        OwnershipVerificationError: If user doesn't own translation
        NotFoundError: If translation doesn't exist
    """
    try:
        verify_user_owns_translation(db, translation_id, user_id)
        translation = user_translations.get_user_translation_by_id(db, translation_id)

        if not translation:
            raise NotFoundError(f"Translation {translation_id} not found")

        return translation

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to access translation {translation_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user translation: {e}", exc_info=True)
        raise


def list_user_translations_by_word_status_secure(
    db: Session, user_word_status_id: int, user_id: int
) -> list[models.UserTranslations]:
    """
    Get all translations for a word status with ownership verification.

    Args:
        db: Database session
        user_word_status_id: Word status ID
        user_id: User ID (for ownership verification)

    Returns:
        List of UserTranslations objects

    Raises:
        OwnershipVerificationError: If user doesn't own word status
    """
    from .auth import verify_user_owns_word_status

    try:
        verify_user_owns_word_status(db, user_word_status_id, user_id)
        return user_translations.get_translations_by_word_status(db, user_word_status_id)

    except OwnershipVerificationError:
        logger.warning(
            f"User {user_id} attempted to access translations for word_status {user_word_status_id}"
        )
        raise
    except Exception as e:
        logger.error(f"Error retrieving translations: {e}", exc_info=True)
        raise


def update_user_translation_secure(
    db: Session,
    translation_id: int,
    user_id: int,
    language: Optional[str] = None,
    translation: Optional[str] = None,
) -> models.UserTranslations:
    """
    Update a user translation with ownership verification.

    Args:
        db: Database session
        translation_id: Translation ID to update
        user_id: User ID (for ownership verification)
        language: New language (optional)
        translation: New translation text (optional)

    Returns:
        Updated UserTranslations object

    Raises:
        OwnershipVerificationError: If user doesn't own translation
        NotFoundError: If translation doesn't exist
    """
    try:
        verify_user_owns_translation(db, translation_id, user_id)

        updated = user_translations.update_user_translation(
            db=db, translation_id=translation_id, language=language, translation=translation
        )

        if not updated:
            raise NotFoundError(f"Translation {translation_id} not found")

        return updated

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to update translation {translation_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error updating user translation: {e}", exc_info=True)
        raise


def delete_user_translation_secure(db: Session, translation_id: int, user_id: int) -> bool:
    """
    Delete a user translation with ownership verification.

    Args:
        db: Database session
        translation_id: Translation ID to delete
        user_id: User ID (for ownership verification)

    Returns:
        True if deleted successfully

    Raises:
        OwnershipVerificationError: If user doesn't own translation
        NotFoundError: If translation doesn't exist
    """
    try:
        verify_user_owns_translation(db, translation_id, user_id)

        success = user_translations.delete_user_translation(db, translation_id)

        if not success:
            raise NotFoundError(f"Translation {translation_id} not found")

        return success

    except OwnershipVerificationError:
        logger.warning(f"User {user_id} attempted to delete translation {translation_id}")
        raise
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting user translation: {e}", exc_info=True)
        raise
