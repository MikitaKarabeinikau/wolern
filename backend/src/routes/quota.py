from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.utils import authenticate_and_get_user_details
from backend.src.database.database import get_database
import json
from datetime import datetime
import logging
from backend.schemas import ExerciseRequest

from backend.src.database.database import get_database
from backend.src.database.quota import (
    get_exercise_quota,
    create_exercise_quota,
    reset_quota_if_needed
)  

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@router.get("/")
async def get_exercise_quota_endpoint(
    request: Request,
    db: Session = Depends(get_database)
):
    """
    Endpoint to get the current exercise generation quota for a user.
    """
    user_details = authenticate_and_get_user_details(request=request)
    if not user_details:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_clerk_id = user_details['user_id']
    quota = get_exercise_quota(db, user_clerk_id)
    if not quota:
        return {"user_id": user_clerk_id, "exercises_remaining": 0, "last_reset_date": datetime.utcnow()}
    quota = reset_quota_if_needed(db, quota)

    return quota