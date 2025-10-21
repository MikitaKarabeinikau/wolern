from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.src.database.database import get_database
from backend.src.database.models import Users
from backend.utils import authenticate_and_get_user_details
from backend.src.database.words import get_user_vocabularies
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/user/vocabularies")
async def get_vocabularies(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request = request)
        user_id = user_details["user_id"]

        vocabularies = get_user_vocabularies(db, user_id=user_id)
        logger.info(f"Vocabularies fetched for user {user_id}: {vocabularies}")
        return {"vocabularies": vocabularies}
    except Exception as e:
        logger.error(f"Error fetching vocabularies: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/")
async def get_users(db: Session = Depends(get_database)):
    try:
        users = db.query(Users).all()
        return {"users": users}
    except Exception as e:
        logger.error(f"Error fetching users: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

