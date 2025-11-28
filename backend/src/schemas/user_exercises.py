from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from .user_exercise_progress import UserExerciseProgressResponse

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserExerciseBase(BaseModel):
    '''Base schema for user exercises'''
    user_id: int = Field(..., example=1)
    exercise_id: int = Field(..., example=1)
    word_id: int = Field(..., example=1)

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserExerciseCreate(UserExerciseBase):
    '''Schema for assigning an exercise to a user'''
    pass

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserExerciseResponse(UserExerciseBase):
    '''Schema for user exercise response'''
    id: int
    user_id: int
    exercise_id: int
    word_id: int
    
    class Config:
        from_attributes = True

# ============================================================================
# DETAILED RESPONSE
# ============================================================================
class UserExerciseDetailResponse(UserExerciseResponse):
    '''Schema for detailed user exercise'''
    user_exercise_progress: UserExerciseProgressResponse
    
    class Config:
        from_attributes = True