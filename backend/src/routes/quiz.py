from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.src.database.quiz import get_quiz_words
from backend.utils import authenticate_and_get_user_details
from backend.src.database.translations import get_translations_for_quiz
from backend.src.database.definitions import get_definitions_for_quiz
from backend.src.database.examples import get_examples_for_quiz
from backend.src.database.synonyms import get_synonyms_for_quiz

import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/quiz/generate")
async def generate_quiz(request: Request, db: Session = Depends(get_database)):
    # Logic to generate quiz words
    user_details = authenticate_and_get_user_details(request=request)
    clerk_id = user_details["user_id"]

    words = get_quiz_words(db,clerk_id)

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

    