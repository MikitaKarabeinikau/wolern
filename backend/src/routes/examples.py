from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Words, Example
from backend.src.database.examples import add_example, get_all_examples_for_user_from_db,update_example_by_id, get_example_by_id, delete_example_by_id
from backend.schemas import ExampleResponse
import backend.src.database.models as models
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/user/words/examples/all", response_model=ExampleResponse)
async def get_all_examples_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        
        # This function now returns raw Example objects from the DB
        all_examples = get_all_examples_for_user_from_db(db, clerk_id)
        logger.info(f"Retrieved all examples for user '{clerk_id}'.")
        # FastAPI will use the response_model to correctly format this
        return {"examples": all_examples}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        logger.error(f"Failed to retrieve examples: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve examples: " + str(e))


@router.put("/user/words/examples/{id}", status_code=204)
async def update_example(
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
        word = db.query(Words).filter(Words.id == existing_example.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        update_example_by_id(db, example_id=id, new_example=example_sentence, word_id=existing_example.word_id)
        logger.info(f"Example with ID '{id}' updated by user '{clerk_id}'.")
        return None  # 204 No Content should not return a body

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update example: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update example: {e}")
    
@router.delete("/user/words/examples/{id}",status_code=204)
async def delete_example(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_example = get_example_by_id(db, id)
        if not existing_example:
            raise HTTPException(status_code=404, detail="Example not found")
        
        # Get the word associated with the example
        word = db.query(Words).filter(Words.id == existing_example.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        was_deleted = delete_example_by_id(db=db, clerk_id=clerk_id, example_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Example not found or user does not have permission.")
        logger.info(f"Example with ID '{id}' deleted by user '{clerk_id}'.")
        return None
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete example: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")