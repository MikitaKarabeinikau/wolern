from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.prompts.exercise_prompt import generate_vocabulary_exercise
from backend.src.database.exercise import (
    get_exercise_quota,
    create_exercise_quota,
    reset_quota_if_needed,
    create_exercise,
    get_user_exercises,
    get_user_exercise_from_base,
    create_multiple_choice_exercise,
    get_random_word_for_exercise
)


from backend.utils import authenticate_and_get_user_details
from backend.src.database.database import get_database
import json
from datetime import datetime
import logging
from backend.schemas import ExerciseRequest

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/generate-exercise/{word_id}")
async def generate_exercise(
    word_id: int,
    request: ExerciseRequest,
    request_obj: Request,
    db: Session = Depends(get_database)
):
    try:
        user_details = authenticate_and_get_user_details(request_obj)
        if not user_details:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_clerk_id = user_details['user_id']
        quota = get_exercise_quota(db, user_clerk_id)
        if not quota:
            quota = create_exercise_quota(db, user_clerk_id)
        quota = reset_quota_if_needed(db, quota)

        if quota.exercises_remaining <= 0:
            raise HTTPException(status_code=429, detail="Exercise generation quota exceeded for today.")


        exercise_data = generate_vocabulary_exercise(
            target_word=request.word,
            difficulty=request.difficulty
        )
        print(f'\n\n\nGenerated Exercise Data: {exercise_data}\n\n\n')

        exercise = exercise_data['exercise']
        multiple_choice = exercise_data['multiple_choice']
        
        # Save the generated exercise to a JSON file for record-keeping
        
        target_dir = Path(__file__).parent.parent.parent / 'data' / 'generated'
        target_dir.mkdir(parents=True, exist_ok=True)

        json_filename = target_dir / f'exercise_{user_clerk_id}_{word_id}_{int(datetime.utcnow().timestamp())}.json'


        try:
            with open(json_filename, 'w') as json_file:
                json.dump(exercise_data, json_file, indent=4)
            logger.info(f"Generated exercise saved to {json_filename}")
        except Exception as e:
            logger.error(f"Failed to save generated exercise to file: {e}")
        
        new_exercise = create_exercise(
            db,
            created_by=user_clerk_id, 
            word_id=word_id,
            difficulty=request.difficulty,
            question=exercise['question'],
            hints=json.dumps(exercise['hints']), 
            explanation=exercise['explanation'],
            part_of_speech=exercise['part_of_speech']
        )
        exercise_id = new_exercise.id 

        new_multiple_choice = create_multiple_choice_exercise(
            db,
            exercise_id=exercise_id,
            options=json.dumps(multiple_choice['options']),
            correct_answer=multiple_choice['correct_answer']
        )


        quota.exercises_remaining -= 1
        db.commit()
        db.refresh(quota)

        return {
            "exercise": {
                "id": new_exercise.id,
                "word_id": new_exercise.word_id,
                "difficulty": request.difficulty,
                "question": new_exercise.question,
                "hints": json.loads(new_exercise.hints),
                "explanation": new_exercise.explanation,
                "part_of_speech": new_exercise.part_of_speech,
                "timestamp": new_exercise.timestamp.isoformat(),
                "multiple_choice": {
                    "options": json.loads(new_multiple_choice.options),
                    "correct_answer": new_multiple_choice.correct_answer
                }
            },
            "quota": {
                "exercises_remaining": quota.exercises_remaining,
                "last_reset_date": quota.last_reset_date
            }
        }

    except Exception as e:
        logger.error(f"Error generating exercise: {e}")
        raise HTTPException(status_code=400, detail="Bad Request")


@router.get("/exercise/exercises-history/")
async def get_exercises_history(
    request: Request,
    db: Session = Depends(get_database)
):
    user_details = authenticate_and_get_user_details(request=request)
    if not user_details:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_clerk_id = user_details['user_id']
    exercises = get_user_exercises(db, user_clerk_id)
    return {"exercises": exercises}


@router.get("/quota")
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

@router.get("/word/random")
async def get_random_word(
    request: Request,
    db: Session = Depends(get_database)
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        if not user_details:
            raise HTTPException(status_code=401, detail="Unauthorized")

        clerk_id = user_details['user_id']
        
        # Fetch a random word for the user
        word = get_random_word_for_exercise(db, clerk_id)
        
        if not word:
            raise HTTPException(status_code=404, detail="No words found for the user")

        return {
            "id": word.id,
            "word": word.word
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch random word: {str(e)}")

