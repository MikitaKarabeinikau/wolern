

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

    except Exception as e:
        logger.error(f"Error hiding translation id {translation_id} for UserWordStatus id {user_word_status_id}: {e}", exc_info=True)
        db.rollback()
        raise
