

from sqlalchemy.orm import Session
from backend.src.database import models

import logging
logger = logging.getLogger(__name__)

def hidde_base_translation(db:Session, translation_id:int, user_word_status_id:int):
    # Check if translation id for that word exist
    try:
        hidden_translation = (db.query(models.UserWordStatus)
                                .join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id)
                                .join(models.Words, models.VocabularyWords.word_id == models.Words.id)
                                .join(models.Translations, models.Words.id == models.Translations.word_id)).filter(
                                    models.Translations.id == translation_id,
                                    models.UserWordStatus.id == user_word_status_id
                                ).first()

        if not hidden_translation:
            logger.warning(f"Translation with id {translation_id} not found for UserWordStatus id {user_word_status_id}.")
            raise ValueError("Translation not found for the given UserWordStatus.")

        new_hidden_info = models.UserHiddenBaseTranslation(user_word_status_id=user_word_status_id, translation_id=translation_id)
        db.add(new_hidden_info)
        db.commit()
        db.refresh(new_hidden_info)
        logger.info(f"Successfully hid translation id {translation_id} for UserWordStatus id {user_word_status_id}.")
        return new_hidden_info
    except Exception as e:
        logger.error(f"Error hiding translation id {translation_id} for UserWordStatus id {user_word_status_id}: {e}", exc_info=True)
        db.rollback()
        raise

def hidde_base_example(db:Session, example_id:int, user_word_status_id:int):
    # Check if example id for that word exist
    try:
        hidden_example = (db.query(models.UserWordStatus)
                                .join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id)
                                .join(models.Words, models.VocabularyWords.word_id == models.Words.id)
                                .join(models.Examples, models.Words.id == models.Examples.word_id)).filter(
                                    models.Examples.id == example_id,
                                    models.UserWordStatus.id == user_word_status_id
                                ).first()

        if not hidden_example:
            logger.warning(f"Example with id {example_id} not found for UserWordStatus id {user_word_status_id}.")
            raise ValueError("Example not found for the given UserWordStatus.")

        new_hidden_info = models.UserHiddenBaseExample(user_word_status_id=user_word_status_id, example_id=example_id)
        db.add(new_hidden_info)
        db.commit()
        db.refresh(new_hidden_info)
        logger.info(f"Successfully hid example id {example_id} for UserWordStatus id {user_word_status_id}.")
        return new_hidden_info
    except Exception as e:
        logger.error(f"Error hiding example id {example_id} for UserWordStatus id {user_word_status_id}: {e}", exc_info=True)
        db.rollback()
        raise

def hidde_base_tag(db:Session, tag_id:int, user_word_status_id:int):
    # Check if tag id for that word exist
    try:
        hidden_tag = (db.query(models.UserWordStatus)
                                .join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id)
                                .join(models.Words, models.VocabularyWords.word_id == models.Words.id)
                                .join(models.Tags, models.Words.id == models.Tags.word_id)).filter(
                                    models.Tags.id == tag_id,
                                    models.UserWordStatus.id == user_word_status_id
                                ).first()

        if not hidden_tag:
            logger.warning(f"Tag with id {tag_id} not found for UserWordStatus id {user_word_status_id}.")
            raise ValueError("Tag not found for the given UserWordStatus.")

        new_hidden_info = models.UserHiddenBaseTag(user_word_status_id=user_word_status_id, tag_id=tag_id)
        db.add(new_hidden_info)
        db.commit()
        db.refresh(new_hidden_info)
        logger.info(f"Successfully hid tag id {tag_id} for UserWordStatus id {user_word_status_id}.")
        return new_hidden_info
    except Exception as e:
        logger.error(f"Error hiding tag id {tag_id} for UserWordStatus id {user_word_status_id}: {e}", exc_info=True)
        db.rollback()
        raise

def hidde_base_definition(db:Session, definition_id:int, user_word_status_id:int):
    # Check if definition id for that word exist
    try:
        hidden_definition = (db.query(models.UserWordStatus)
                                .join(models.VocabularyWords, models.UserWordStatus.vocabulary_word_id == models.VocabularyWords.id)
                                .join(models.Words, models.VocabularyWords.word_id == models.Words.id)
                                .join(models.Definitions, models.Words.id == models.Definitions.word_id)).filter(
                                    models.Definitions.id == definition_id,
                                    models.UserWordStatus.id == user_word_status_id
                                ).first()

        if not hidden_definition:
            logger.warning(f"Definition with id {definition_id} not found for UserWordStatus id {user_word_status_id}.")
            raise ValueError("Definition not found for the given UserWordStatus.")

        new_hidden_info = models.UserHiddenBaseDefinition(user_word_status_id=user_word_status_id, definition_id=definition_id)
        db.add(new_hidden_info)
        db.commit()
        db.refresh(new_hidden_info)
        logger.info(f"Successfully hid definition id {definition_id} for UserWordStatus id {user_word_status_id}.")
        return new_hidden_info
    except Exception as e:
        logger.error(f"Error hiding definition id {definition_id} for UserWordStatus id {user_word_status_id}: {e}", exc_info=True)
        db.rollback()
        raise
