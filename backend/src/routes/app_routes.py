from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Dict, Optional
from backend.src.database import models
from ..database.database import (
    get_user_by_clerk_id,
    create_user, get_user_by_username,
    get_user_by_id,
    get_user_vocabulary,
    SessionLocal
)
from ..database.schema import TranslationResponse, Translation, SynonymResponse, Synonym, DefinitionResponse, Definition, ExampleResponse, Example, TagResponse, Tag, WarningResponse, Warning

from backend.utils import authenticate_and_get_user_details
import json
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
import os 
from svix.webhooks import Webhook
from backend.src.core.word import Word
from backend.src.database.database import (
                        get_database,
                        add_word, 
                        get_all_words_from_db, 
                        get_word_id_by_word,
                        get_word_translations_from_db,  
                        get_all_translations_for_user_from_db,
                        get_all_tags_for_user_from_db,
                        get_all_warnings_for_user_from_db,
                        get_all_definitions_for_user_from_db,
                        get_all_examples_for_user_from_db,
                        get_all_synonyms_for_user_from_db)

router = APIRouter()

class WebhookPayload(BaseModel):
    data: dict
    object: str
    type: str


class UserCreateRequest(BaseModel):
    clerk_user_id: str
    username: str = None
    email: str

class AddWordRequest(BaseModel):
    word: str
    
@router.post("/clerk")
async def handle_user_created(request: Request, db: Session = Depends(get_database)):
    # Get raw body for signature verification
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    body = await request.body()
    payload = body.decode('utf-8')
    headers = dict(request.headers)



    try:
        webhook = Webhook(webhook_secret)
        webhook.verify(payload, headers)

        data = json.loads(payload)
        if data.get("type") == "user.created":
            clerk_user_id = data["data"]["id"]
            email_addresses = data["data"].get("email_addresses", [])
            email = email_addresses[0].get("email_address") if email_addresses else None

            try:
                existing_usuer = db.query(models.Users).filter(models.Users.clerk_id == clerk_user_id).first()
                if existing_usuer:
                    return {"success": True, "message": "User already exists"}

                new_user = models.Users(
                    clerk_id=clerk_user_id,
                    username = None,
                    email=email,
                    created_at=datetime.utcnow()
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return {"success": True, "message": "User created successfully"}
            except IntegrityError:
                # This handles the unlikely case where the user.created event is sent twice
                # and another check might be needed, but the first check should prevent it.
                return {"success": True, "message": "User creation conflict, assuming already created"}
            except Exception as e:
                if db:
                    db.rollback()
            # Log the error for debugging purposes
                raise HTTPException(status_code=500, detail=f"Database error on user creation: {e}")
        
        user_data = data.get("data", {})
        user_id = user_data.get("id")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

        
    return {"success": True, "message": f"Event type {payload['type']} handled"}
        
            

@router.get("/users/")
async def get_users(db: Session = Depends(get_database)):
    users = db.query(models.Users).all()
    return {"users": users}


@router.get("/my-vocabulary")
async def my_vocabulary(request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request = request)
    user_id = user_details["user_id"]

    my_vocabulary = get_user_vocabulary(db, user_id=user_id)
    return {"vocabulary": my_vocabulary}

@router.post("/user/words")
async def add_new_word(request: Request, word_request: AddWordRequest, db: Session = Depends(get_database)):
    
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        new_word = Word(word=word_request.word)
        print("adding wprd:",new_word)
        add_word(db, new_word, clerk_id)
        return {"success": True, "message": "Word added successfully"}
    
    except HTTPException as http_exc:  
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to add word: " + str(e))

@router.get("/user/words/{word}")
async def get_word_id(request: Request, word: str, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        clerk_id = user_details["user_id"]
        word_id = await get_word_id_by_word(db, word)
        if word_id is None:
            raise HTTPException(status_code=404, detail="Word not found")
        return {"word": word, "word_id": word_id}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve word ID: " + str(e))

@router.get("/user/words")
async def get_all_words(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        clerk_id = user_details["user_id"]
        words = get_all_words_from_db(db, clerk_id)
        return {"words": words}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve words: " + str(e))

@router.get("/user/{word}/translations")
async def get_word_translations(request: Request, word: str):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        clerk_id = user_details["user_id"]
        data = get_word_translations_from_db(word, clerk_id)
        print("Translations data:", data)  # Debug log
        return data
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve translations: " + str(e))
    
@router.get("/user/words/translations/all", response_model=TranslationResponse)
async def get_all_translations_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Translation objects from the DB
        all_translations = get_all_translations_for_user_from_db(db, clerk_id)
        
        # FastAPI will use the response_model to correctly format this
        return {"translations": all_translations}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve translations: " + str(e))
    
@router.get("/user/words/synonyms/all", response_model=SynonymResponse)
async def get_all_synonyms_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Synonym objects from the DB
        all_synonyms = get_all_synonyms_for_user_from_db(db, clerk_id)
        
        # FastAPI will use the response_model to correctly format this
        return {"synonyms": all_synonyms}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve synonyms: " + str(e))
    
@router.get("/user/words/definitions/all", response_model=DefinitionResponse)
async def get_all_definitions_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Definition objects from the DB
        all_definitions = get_all_definitions_for_user_from_db(db, clerk_id)
        
        # FastAPI will use the response_model to correctly format this
        return {"definitions": all_definitions}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve definitions: " + str(e))
    
@router.get("/user/words/examples/all", response_model=ExampleResponse)
async def get_all_examples_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Example objects from the DB
        all_examples = get_all_examples_for_user_from_db(db, clerk_id)
        
        # FastAPI will use the response_model to correctly format this
        return {"examples": all_examples}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve examples: " + str(e))
    
@router.get("/user/words/tags/all", response_model=TagResponse)
async def get_all_tags_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Tag objects from the DB
        all_tags = get_all_tags_for_user_from_db(db, clerk_id)
        
        # FastAPI will use the response_model to correctly format this
        return {"tags": all_tags}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve tags: " + str(e))

@router.get("/user/words/warnings/all", response_model=WarningResponse)
async def get_all_warnings_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Warning objects from the DB
        all_warnings = get_all_warnings_for_user_from_db(db, clerk_id)
        
        # FastAPI will use the response_model to correctly format this
        return {"warnings": all_warnings}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve warnings: " + str(e))

