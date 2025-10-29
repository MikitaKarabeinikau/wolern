from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from openai import BaseModel
from sqlalchemy.orm import Session
from backend.src.database import models
from backend.src.database.database import get_database
from backend.src.database.models import User_Quiz_Progress
from backend.src.database.quiz import get_quiz_words, increase_correct_answers, increase_correct_answers_in_a_row, increase_learning_stage, increase_wrong_answers, increase_wrong_answers_in_a_row,reset_correct_answers_in_a_row, reset_wrong_answers_in_a_row
from backend.utils import authenticate_and_get_user_details
from backend.src.database.translations import get_translations_for_quiz
from backend.src.database.definitions import get_definitions_for_quiz
from backend.src.database.examples import get_examples_for_quiz
from backend.src.database.synonyms import get_synonyms_for_quiz
from backend.src.database.quiz import get_quiz_progress

import logging

class SetNextReviewDateRequest(BaseModel):
    new_date: str

router = APIRouter()
logger = logging.getLogger(__name__)

@router.put("/quiz/word/{word_id}/set_next_review_date")
async def set_next_review_date(request: Request, word_id: int, body: SetNextReviewDateRequest, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        # Parse the ISO 8601 date string into a Python datetime object
        try:
            new_date = datetime.fromisoformat(body.new_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")

        word = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.word_id == word_id, models.User_Quiz_Progress.user_id == clerk_id).first()

        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        # Update the database with the parsed datetime object
        word.time_to_repeat = new_date
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

@router.get("/quiz/generate")
async def generate_quiz(request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    words = get_quiz_words(db, clerk_id)
    if not words:
        raise HTTPException(status_code=404, detail="No quiz words found")
    return {"words": words}


@router.get("/quiz/word/translations")
async def get_word_translations(request: Request, db: Session = Depends(get_database)):
    # Logic to get translations for a quiz word
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    translations = get_translations_for_quiz(db, clerk_id)

    if not translations:
        raise HTTPException(status_code=404, detail="No translations found for the quiz words")
    return {"translations": translations}

@router.get("/quiz/word/definitions")
async def get_word_definitions(request: Request, db: Session = Depends(get_database)):
    # Logic to get definitions for a quiz word
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    definitions = get_definitions_for_quiz(db, clerk_id)

    if not definitions:
        raise HTTPException(status_code=404, detail="No definitions found for the quiz words")
    return {"definitions": definitions}

@router.get("/quiz/word/examples")
async def get_word_examples(request: Request, db: Session = Depends(get_database)):
    # Logic to get examples for a quiz word
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    examples = get_examples_for_quiz(db, clerk_id)

    if not examples:
        raise HTTPException(status_code=404, detail="No examples found for the quiz words")
    return {"examples": examples}

@router.get("/quiz/word/synonyms")
async def get_word_synonyms(request: Request, db: Session = Depends(get_database)):
    # Logic to get synonyms for a quiz word
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    synonyms = get_synonyms_for_quiz(db, clerk_id)

    if not synonyms:
        raise HTTPException(status_code=404, detail="No synonyms found for the quiz words")
    return {"synonyms": synonyms}   

@router.get("/quiz/data")
async def get_quiz_data(request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    if not clerk_id:
        raise HTTPException(status_code=401, detail="Unauthorized: Missing clerk_id")

    data = get_quiz_progress(db, clerk_id)

    if not data:
        raise HTTPException(status_code=404, detail="No quiz progress found for the user")

    return {"progress": data}

@router.put("/quiz/words/{word_id}/correct-answers")
async def update_correct_answers(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = increase_correct_answers(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/wrong-answers")
async def update_wrong_answers(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = increase_wrong_answers(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/correct-answers-row/increase")
async def update_correct_answers_in_a_row(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = increase_correct_answers_in_a_row(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/wrong-answers-row/increase")
async def update_wrong_answers_in_a_row(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = increase_wrong_answers_in_a_row(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/learning-stage/increase")
async def update_learning_stage(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = increase_learning_stage(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/correct-answers-row/reset")
async def reset_correct_answers(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = reset_correct_answers_in_a_row(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/wrong-answers-row/reset")
async def reset_wrong_answers(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = reset_wrong_answers_in_a_row(db, clerk_id, word_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}

@router.put("/quiz/words/{word_id}/learning-stage/decrease")
async def decrease_learning_stage(word_id: int, request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).first()
    if progress and progress.learning_stage > 0:
        progress.learning_stage -= 1
        db.commit()
    else:
        progress = None
    if not progress:
        raise HTTPException(status_code=404, detail="Quiz progress not found")

    return {"progress": progress}