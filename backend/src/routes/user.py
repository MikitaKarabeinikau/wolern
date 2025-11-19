from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.src.database.models import Users
from backend.utils import authenticate_and_get_user_details
from backend.src.database.words import get_user_vocabularies, get_words_and_vocabularies
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/user/vocabularies")
async def get_vocabularies(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        user_id = user_details["user_id"]

        vocabularies = get_user_vocabularies(db, user_id=user_id)
        logger.info(f"\nVocabularies fetched for user {user_id}: {vocabularies}\n")
        return {"vocabularies": vocabularies}
    except Exception as e:
        logger.error(f"Error fetching vocabularies: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/user/words/vocabularies")
async def get_all_words_and_vocabularies(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        logger.debug(f"Fetching words and vocabularies for clerk_id: {clerk_id}")
        words_and_vocabularies = get_words_and_vocabularies(db, clerk_id)
        logger.info(f"Retrieved all words and vocabularies for user '{clerk_id}': {len(words_and_vocabularies)} records.")
        return {"words_and_vocabularies": words_and_vocabularies if words_and_vocabularies else []}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code, detail=http_exc.detail)
    except Exception as e:
        logger.error(f"Failed to retrieve words and vocabularies: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve words and vocabularies: " + str(e))


@router.get("/users/")
async def get_users(db: Session = Depends(get_database)):
    try:
        users = db.query(Users).all()
        return {"users": users}
    except Exception as e:
        logger.error(f"Error fetching users: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

