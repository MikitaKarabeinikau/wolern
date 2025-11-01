from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.src.database import (
    get_exercise_quota,
    create_exercise_quota,
    reset_quota_if_needed,
    create_exercise,
    create_exercise_base,
    get_user_exercises,
    get_user_exercise_from_base
)

from backend.schemas import FillInTheBlankExercise, MultipleChoiceExercise


from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import get_db
import json
from datetime import datetime
import logging
from backend.schemas import ExerciseRequest

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/generate-exercise/")
async def generate_exercise(
    request: ExerciseRequest,
    db: Session = Depends(get_db)
):
    try
        user_details = await authenticate_and_get_user_details(request)
        if not user_details:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_clerk_id = user_details['clerk_id']
        quota = get_exercise_quota(db, user_clerk_id)
        if not quota:
            quota = create_exercise_quota(db, user_clerk_id)
        quota = reset_quota_if_needed(db, quota)

        if quota.exercises_remaining <= 0:
            raise HTTPException(status_code=429, detail="Exercise generation quota exceeded for today.")

        exercise_data = None
        
        #TODO: Call AI generator here to get exercise_data
        
        quota.exercises_remaining -= 1
        db.commit()
        db.refresh(quota)
        
        return exercise_data
        
    except Exception as e:
        logger.error(f"Error generating exercise: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")
        
    
@router.get("/exercises-history/")
async def get_exercises_history(
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = await authenticate_and_get_user_details(request)
    if not user_details:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_clerk_id = user_details['clerk_id']
    exercises = get_user_exercises(db, user_clerk_id)
    return {"exercises": exercises}


@router.get("/quota")
async def get_exercise_quota_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint to get the current exercise generation quota for a user.
    """
    user_details = await authenticate_and_get_user_details(request)
    if not user_details:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_clerk_id = user_details['clerk_id']
    quota = get_exercise_quota(db, user_clerk_id)
    if not quota:
        return {"user_id": user_clerk_id, "exercises_remaining": 0, "last_reset_date": datetime.utcnow()}
    quota = reset_quota_if_needed(db, quota)

    return quota

