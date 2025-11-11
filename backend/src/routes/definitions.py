from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Definition, Words
from backend.src.database.definitions import add_definition, get_all_definitions_for_user_from_db, delete_definition_by_id, update_definition_by_id, get_definition_by_id
from backend.schemas import DefinitionResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/user/words/definitions/{word_id}", status_code=201)
async def create_definitions(
    request: Request,
    word_id: int,
    definition: str = Body(..., embed=True),
    part_of_speech: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        word = db.query(Words).filter(Words.id == word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        add_definition(db, word_id, part_of_speech, definition)
        logger.info(f"Definitions added for word ID '{word_id}' by user '{clerk_id}'.")
        return {"message": "Definitions created successfully."}

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create definitions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create definitions: " + str(e))

@router.get("/user/words/definitions/all", response_model=DefinitionResponse)
async def get_all_definitions_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        all_definitions = get_all_definitions_for_user_from_db(db, clerk_id)
        logger.info(f"Retrieved all definitions for user '{clerk_id}'.")
        return {"definitions": all_definitions}
    
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    
    except Exception as e:
        logger.error(f"Failed to retrieve definitions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve definitions: " + str(e))


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
        
        word = db.query(Words).filter(Words.id == existing_definition.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        updated_definition = update_definition_by_id(db, id, definition)
        logger.info(f"Definition with ID '{id}' updated by user '{clerk_id}'.")
        return  updated_definition

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update definition: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update definition: " + str(e))
    

@router.delete("/user/words/definitions/{id}",status_code=204)
async def delete_definition(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_definition = get_definition_by_id(db, id)
        if not existing_definition:
            raise HTTPException(status_code=404, detail="Definition not found")
        
        word = db.query(Words).filter(Words.id == existing_definition.word_id).first()

        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        was_deleted = delete_definition_by_id(db=db, clerk_id=clerk_id, definition_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Definition not found or user does not have permission.")
        logger.info(f"Definition with ID '{id}' deleted by user '{clerk_id}'.")
        return was_deleted

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete definition: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")