from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Words
from backend.src.database.words import get_word_id_by_word, get_all_words_from_db, delete_word_by_id_from_db, add_word
from backend.schemas import AddWordRequest
from backend.src.core.word import Word
import logging
import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

class SetNextReviewDateRequest(BaseModel):
    new_date: str

@router.post("/user/words")
async def add_new_word(request: Request, word_request: AddWordRequest, db: Session = Depends(get_database)):
    
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        new_word = Word(word=word_request.word)
        add_word(db, new_word, clerk_id)
        logger.info(f"Word '{new_word.word}' added successfully by user '{clerk_id}'.")
        return {"success": True, "message": "Word added successfully"}
    
    except HTTPException as http_exc:  
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add word: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to add word: " + str(e))

@router.put("/words/vocabulary/{new_vocabulary}/{id}")
async def change_word_vocabulary(id: int, new_vocabulary: str, request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        word = db.query(Words).filter(Words.id == id, Words.added_by_user_id == clerk_id).first()

        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        word.vocabulary = new_vocabulary
        db.commit()
        logger.info(f"Vocabulary for word with ID '{id}' updated to '{new_vocabulary}' by user '{clerk_id}'.")
        return True
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update vocabulary for word with ID '{id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update vocabulary: " + str(e))


@router.get("/user/words/{word}")
async def get_word_id(request: Request, word: str, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        clerk_id = user_details["user_id"]
        word_id = await get_word_id_by_word(db, word)
        if word_id is None:
            raise HTTPException(status_code=404, detail="Word not found")
        logger.info(f"Retrieved word ID '{word_id}' for word '{word}' by user '{clerk_id}'.")
        return {"word": word, "word_id": word_id}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  
    except Exception as e:
        logger.error(f"Failed to retrieve word ID: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve word ID: " + str(e))


@router.get("/user/words")
async def get_all_words(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        clerk_id = user_details["user_id"]
        words = get_all_words_from_db(db, clerk_id)
        logger.info(f"Retrieved all words for user '{clerk_id}'.")
        return {"words": words}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail) 
    except Exception as e:
        logger.error(f"Failed to retrieve words: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve words: " + str(e))

@router.put("/quiz/word/{word_id}/set_next_review_date")
async def set_next_review_date(request: Request, word_id: int, body: SetNextReviewDateRequest, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        # Parse the ISO 8601 date string into a Python datetime object
        try:
            new_date = datetime.datetime.fromisoformat(body.new_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")

        word = db.query(Words).filter(Words.id == word_id, Words.added_by_user_id == clerk_id).first()

        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        # Update the database with the parsed datetime object
        word.time_to_reapet = new_date
        db.commit()
        logger.info(f"Next review date for word with ID '{word_id}' set to '{new_date}' by user '{clerk_id}'.")
        return {"success": True, "message": f"Next review date set to {new_date}"}
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to set next review date for word with ID '{word_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to set next review date: " + str(e))
    
@router.put("/words/{word_id}/wrong-answers")
async def change_wrong_answers_count(request: Request, word_id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        increase_wrong_count(db, word_id, clerk_id)
        logger.info(f"Wrong answers count for word with ID '{word_id}' incremented by user '{clerk_id}'.")
        
        return True
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to increment wrong answers count for word with ID '{word_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to increment wrong answers count: " + str(e))

@router.put("/words/{word_id}/correct-answers")
async def change_correct_answers_count(request: Request, word_id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        increase_correct_count(db, word_id, clerk_id)
        logger.info(f"Correct answers count for word with ID '{word_id}' incremented by user '{clerk_id}'.")
        
        return True
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to increment correct answers count for word with ID '{word_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to increment correct answers count: " + str(e))

@router.put("/words/{word_id}/vocabulary/to_learn")
async def change_word_vocabulary(request: Request, word_id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        word = db.query(Words).filter(Words.id == word_id, Words.added_by_user_id == clerk_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")
        word.vocabulary = 'learning'
        db.commit()
        logger.info(f"Vocabulary for word with ID '{word_id}' changed to 'learning' by user '{clerk_id}'.")
        return True

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update vocabulary for word with ID '{word_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update vocabulary: " + str(e))

@router.delete("/user/words/{word_id}",status_code=204)
async def delete_word_by_id(request: Request, word_id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_word_by_id_from_db(db=db, word_id=word_id, clerk_id=clerk_id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Word not found or user does not have permission.")
        logger.info(f"Word with ID '{word_id}' deleted successfully by user '{clerk_id}'.")
        return None
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete word: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")