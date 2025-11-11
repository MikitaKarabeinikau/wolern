from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Words, Translation
from backend.src.database.translations import get_word_translations_from_db, get_all_translations_for_user_from_db, delete_translation_by_id,get_translation_by_id, update_translation_by_id,add_translation
from backend.schemas import TranslationResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/user/words/{word_id}/{language}/translations/{new_translation}")
async def create_translation(
    request: Request,
    word_id: int,
    language: str,
    translation: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        word = db.query(Words).filter(Words.id == word_id, Words.added_by_user_id == clerk_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found or access denied.")
        
        add_translation(db, word_id, language, translation)

        logger.info(f"New translation created for word '{word.id}' by user '{clerk_id}'.")
        return {"message": "Translation created successfully."}
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create translation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create translation: " + str(e))

@router.get("/user/{word}/translations")
async def get_word_translations(request: Request, word: str, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        clerk_id = user_details["user_id"]
        translations = get_word_translations_from_db(db, word, clerk_id)
        logger.info(f"Translations data for word '{word}' and user '{clerk_id}': {translations}")
        return {"translations": translations}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)
    except Exception as e:
        logger.error(f"Failed to retrieve translations for word '{word}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve translations: " + str(e))
   
 
@router.get("/user/words/translations/all", response_model=TranslationResponse)
async def get_all_translations_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        all_translations = get_all_translations_for_user_from_db(db, clerk_id)
        logger.info(f"Retrieved all translations for user '{clerk_id}'.")
        return {"translations": all_translations}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)
    
    except Exception as e:
        logger.error(f"Failed to retrieve all translations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve translations: " + str(e))


@router.put("/user/words/translations/{id}", status_code=204)
async def update_translation(
    request: Request,
    id: int,
    translation: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_translation = get_translation_by_id(db, id)
        if not existing_translation:
            raise HTTPException(status_code=404, detail="Translation not found")
        
        word = db.query(Words).filter(Words.id == existing_translation.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        updated_translation = update_translation_by_id(db, id, translation, word.id)
        db.commit()
        logger.info(f"Translation with ID '{id}' updated by user '{clerk_id}'.")
        return updated_translation

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update translation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update translation: " + str(e))
    

@router.delete("/user/words/translations/{id}",status_code=204)
async def delete_translation(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_translation = get_translation_by_id(db, id)
        if not existing_translation:
            raise HTTPException(status_code=404, detail="Translation not found")
        
        word = db.query(Words).filter(Words.id == existing_translation.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        was_deleted = delete_translation_by_id(db=db, clerk_id=clerk_id, translation_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Translation not found or user does not have permission.")
        logger.info(f"Translation with ID '{id}' deleted by user '{clerk_id}'.")
        return was_deleted

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete translation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")