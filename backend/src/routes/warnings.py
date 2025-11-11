from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Words, Warning
from backend.src.database.warnings import create_warning, get_all_warnings_for_user_from_db, delete_warning_by_id, update_warning_by_id, get_warning_by_id
from backend.schemas import WarningResponse  # Assuming you create a schemas.py file
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/user/words/warnings/", status_code=201)
async def create_word_warning(
    request: Request,
    word_id: int = Body(..., embed=True),
    warning: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        word = db.query(Words).filter(Words.id == word_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")
        if word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission to add a warning to this word.")

        create_warning(db, word_id, warning)
        logger.info(f"Warning created for word ID '{word_id}' by user '{clerk_id}'.")
        return {"message": "Warning created successfully."}

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create warning: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create warning: " + str(e))

@router.get("/user/words/warnings/all", response_model=WarningResponse)
async def get_all_warnings_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        all_warnings = get_all_warnings_for_user_from_db(db, clerk_id)
        logger.info(f"Retrieved all warnings for user '{clerk_id}'.")
        return {"warnings": all_warnings}
    
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)
    except Exception as e:
        logger.error(f"Failed to retrieve warnings: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve warnings: " + str(e))

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
        
        word = db.query(Words).filter(Words.id == existing_warning.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        updated_warning = update_warning_by_id(db, id, warning, word.id)
        logger.info(f"Warning with ID '{id}' updated by user '{clerk_id}'.")
        return updated_warning

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update warning: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update warning: " + str(e))
    

@router.delete("/user/words/warnings/{id}",status_code=204)
async def delete_warning(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_warning = get_warning_by_id(db, id)
        if not existing_warning:
            raise HTTPException(status_code=404, detail="Warning not found")
        
      
        word = db.query(Words).filter(Words.id == existing_warning.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        was_deleted = delete_warning_by_id(db=db, clerk_id=clerk_id, warning_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Warning not found or user does not have permission.")
        logger.info(f"Warning with ID '{id}' deleted by user '{clerk_id}'.")
        return was_deleted

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete warning: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")