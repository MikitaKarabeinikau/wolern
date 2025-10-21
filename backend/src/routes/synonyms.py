from fastapi import APIRouter, Depends, HTTPException, Request, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Synonym, Words
from backend.src.database.synonyms import add_synonym, get_all_synonyms_for_user_from_db, delete_synonym_by_id, update_synonym_by_id, get_synonym_by_id
from backend.schemas import SynonymResponse  

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/user/words/synonyms", status_code=201)
async def add_synonym_route(request: Request, word_id: int = Body(..., embed=True), synonym: str = Body(..., embed=True), db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        # Verify that the word exists and belongs to the user
        word = db.query(Words).filter(Words.id == word_id, Words.added_by_user_id == clerk_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found or user does not have permission.")

        new_synonym = add_synonym(db, word_id, synonym)
        logger.info(f"Synonym '{synonym}' added for word_id '{word_id}' by user '{clerk_id}'.")
        return {"synonym": new_synonym}

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc 
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add synonym: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to add synonym: " + str(e))

@router.get("/user/words/synonyms/all", response_model=SynonymResponse)
async def get_all_synonyms_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        all_synonyms = get_all_synonyms_for_user_from_db(db, clerk_id)
        logger.info(f"Retrieved all synonyms for user '{clerk_id}'.")
        return {"synonyms": all_synonyms}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  
    except Exception as e:
        logger.error(f"Failed to retrieve synonyms: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve synonyms: " + str(e))

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

        existing_synonym = get_synonym_by_id(db, id)
        if not existing_synonym:
            raise HTTPException(status_code=404, detail="Synonym not found")

        word = db.query(Words).filter(Words.id == existing_synonym.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        update_synonym_by_id(db, id, synonym, word.id)
        db.commit()
        logger.info(f"Synonym with ID '{id}' updated by user '{clerk_id}'.")
        return None  

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update synonym: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update synonym: " + str(e))
    

@router.delete("/user/words/synonyms/{id}",status_code=204)
async def delete_synonym(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_synonym = get_synonym_by_id(db, id)
        if not existing_synonym:
            raise HTTPException(status_code=404, detail="Synonym not found")

        word = db.query(Words).filter(Words.id == existing_synonym.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        was_deleted = delete_synonym_by_id(db=db, clerk_id=clerk_id, synonym_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Synonym not found or user does not have permission.")
        logger.info(f"Synonym with ID '{id}' deleted by user '{clerk_id}'.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete synonym: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")