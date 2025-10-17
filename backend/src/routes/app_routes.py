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
from fastapi import Body
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
                        get_all_synonyms_for_user_from_db,
                        get_definition_by_id,
                        delete_definition_by_id,
                        update_definition_by_id,
                        delete_word_by_id_from_db,
                        delete_example_by_id, 
                        get_example_by_id,
                        update_example_by_id,
                        delete_translation_by_id,
                        delete_tags_by_id,
                        delete_synonym_by_id,
                        update_synonym_by_id,
                        delete_warning_by_id,
                        update_warning_by_id,
                        get_warning_by_id)

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

@router.delete("/user/words/definitions/{id}",status_code=204)
async def delete_definition(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_definition_by_id(db=db, clerk_id=clerk_id, definition_id=id)

        if not was_deleted:
            # This path is taken if the item wasn't found.
            raise HTTPException(status_code=404, detail="Definition not found or user does not have permission.")
        
        # If was_deleted is True, the commit was successful. We can safely return.
        # A 204 response should not have a body.
        return None

    except HTTPException as http_exc:
        # If our own HTTPException is raised, just re-raise it.
        raise http_exc
    except Exception as e:
        # For any other unexpected errors, return a 500.
        # We avoid db.rollback() here as the state of the transaction is uncertain.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")
        
        db.delete(definition)
        db.commit()
        return {"success": True, "message": "Definition deleted successfully"}
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to delete definition: " + str(e))
    

@router.delete("/user/words/examples/{id}",status_code=204)
def delete_example(request: Request, id: int, db: Session = Depends(get_database)):
    print("Delete example called with id:", id)
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_example_by_id(db=db, clerk_id=clerk_id, example_id=id)

        if not was_deleted:
            # This path is taken if the item wasn't found.
            raise HTTPException(status_code=404, detail="Example not found or user does not have permission.")
        return None
    except HTTPException as http_exc:
        # If our own HTTPException is raised, just re-raise it.
        raise http_exc
    except Exception as e:
        # For any other unexpected errors, return a 500.
        # We avoid db.rollback() here as the state of the transaction is uncertain.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")

    
@router.delete("/user/words/{word_id}",status_code=204)
async def delete_word_by_id(request: Request, word_id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_word_by_id_from_db(db=db, word_id=word_id, clerk_id=clerk_id)

        if not was_deleted:
            # This path is taken if the item wasn't found.
            raise HTTPException(status_code=404, detail="Word not found or user does not have permission.")
        
        # If was_deleted is True, the commit was successful. We can safely return.
        # A 204 response should not have a body.
        return None
    except HTTPException as http_exc:
        # If our own HTTPException is raised, just re-raise it.
        raise http_exc
    except Exception as e:
        # For any other unexpected errors, return a 500.
        # We avoid db.rollback() here as the state of the transaction is uncertain.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")
    
from fastapi import Body

@router.put("/user/words/definitions/{id}", status_code=204)
async def update_definition(
    request: Request,
    id: int,
    definition: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_definition = get_definition_by_id(db, id)
        if not existing_definition:
            raise HTTPException(status_code=404, detail="Definition not found")
        
        # Get the word associated with the definition
        word = db.query(models.Words).filter(models.Words.id == existing_definition.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        update_definition_by_id(db, id, definition)

        db.commit()
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to update definition: " + str(e))
    
@router.put("/user/words/examples/{id}", status_code=204)
def update_example(
    request: Request,
    id: int,
    example_sentence: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_example = get_example_by_id(db, id)
        if not existing_example:
            raise HTTPException(status_code=404, detail="Example not found")

        # Get the word associated with the example
        word = db.query(models.Words).filter(models.Words.id == existing_example.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        update_example_by_id(db, example_id=id, new_example=example_sentence, word_id=existing_example.word_id)

        db.commit()
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
        # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail=f"Failed to update example: {e}")
    
@router.delete("/user/words/translations/{id}",status_code=204)
async def delete_translation(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        print("Deleting translation with id:", id, "for user:", clerk_id)
        was_deleted = delete_translation_by_id(db=db, clerk_id=clerk_id, translation_id=id)

        if not was_deleted:
            # This path is taken if the item wasn't found.
            raise HTTPException(status_code=404, detail="Translation not found or user does not have permission.")
        return None

    except HTTPException as http_exc:
        # If our own HTTPException is raised, just re-raise it.
        raise http_exc
    except Exception as e:
        # For any other unexpected errors, return a 500.
        # We avoid db.rollback() here as the state of the transaction is uncertain.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")

@router.put("/user/words/translations/{id}")
async def update_translation(
    request: Request,
    id: int,
    translation: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_translation = db.query(models.Translation).filter(models.Translation.id == id).first()
        if not existing_translation:
            raise HTTPException(status_code=404, detail="Translation not found")
        
        # Get the word associated with the translation
        word = db.query(models.Words).filter(models.Words.id == existing_translation.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        existing_translation.translation = translation
        db.commit()
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to update translation: " + str(e))
    
@router.delete("/user/words/tags/{id}",status_code=204)
async def delete_tag(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_tags_by_id(db=db, clerk_id=clerk_id, tag_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Tag not found or user does not have permission.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")

@router.put("/user/words/tags/{id}", status_code=204)
async def update_tag(
    request: Request,
    id: int,
    tag: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_tag = db.query(models.Tag).filter(models.Tag.id == id).first()
        if not existing_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        
        # Get the word associated with the tag
        word = db.query(models.Words).filter(models.Words.id == existing_tag.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        existing_tag.tag = tag
        db.commit()
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to update tag: " + str(e))
    
@router.delete("/user/words/synonyms/{id}",status_code=204)
async def delete_synonym(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_synonym_by_id(db=db, clerk_id=clerk_id, synonym_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Synonym not found or user does not have permission.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")
    
@router.put("/user/words/synonyms/{id}", status_code=204)
async def update_synonym(
    request: Request,
    id: int,
    synonym: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_synonym = db.query(models.Synonym).filter(models.Synonym.id == id).first()
        if not existing_synonym:
            raise HTTPException(status_code=404, detail="Synonym not found")
        
        # Get the word associated with the synonym
        word = db.query(models.Words).filter(models.Words.id == existing_synonym.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        existing_synonym.synonym = synonym
        db.commit()
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to update synonym: " + str(e))
    
@router.delete("/user/words/warnings/{id}",status_code=204)
async def delete_warning(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        was_deleted = delete_warning_by_id(db=db, clerk_id=clerk_id, warning_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Warning not found or user does not have permission.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")
    

@router.put("/user/words/warnings/{id}", status_code=204)
async def update_warning(
    request: Request,
    id: int,
    warning: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_warning = get_warning_by_id(db, id)
        if not existing_warning:
            raise HTTPException(status_code=404, detail="Warning not found")
        
        # Get the word associated with the warning
        word = db.query(models.Words).filter(models.Words.id == existing_warning.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        update_warning_by_id(db, id, warning, word.id)

        db.commit()
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to update warning: " + str(e))
    
@router.post("/user/words/synonyms", status_code=201)
async def add_synonym(request: Request, word_id: int = Body(..., embed=True), synonym: str = Body(..., embed=True), db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        # Verify that the word exists and belongs to the user
        word = db.query(models.Words).filter(models.Words.id == word_id, models.Words.added_by_user_id == clerk_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found or user does not have permission.")

        new_synonym = add_synonym(db, word_id, synonym)
        return {"synonym": new_synonym}

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
         # Log the error for debugging purposes
        raise HTTPException(status_code=500, detail="Failed to add synonym: " + str(e))