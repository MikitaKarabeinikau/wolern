from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserExerciseProgressBase(BaseModel):
    '''Base schema for user exercise progress'''
    correct: int = Field(default=0, ge=0, example=5)
    wrong: int = Field(default=0, ge=0, example=2)

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserExerciseProgressCreate(BaseModel):
    '''Schema for creating user exercise progress'''
    user_exercise_id: int = Field(..., example=1)
    correct: int = Field(default=0, ge=0, example=0)
    wrong: int = Field(default=0, ge=0, example=0)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserExerciseProgressUpdate(BaseModel):
    '''Schema for updating user exercise progress'''
    correct: Optional[int] = Field(None, ge=0, example=5)
    wrong: Optional[int] = Field(None, ge=0, example=2)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserExerciseProgressResponse(UserExerciseProgressBase):
    '''Schema for user exercise progress response'''
    id: int
    user_exercise_id: int
    last_attempted: datetime

    class Config:
        from_attributes = True

# ============================================================================
# STATISTICS SCHEMA
# ============================================================================
class UserExerciseStatsResponse(BaseModel):
    '''Schema for exercise statistics'''
    user_exercise_id: int
    correct: int
    wrong: int
    last_attempted: datetime
    
    class Config:
        from_attributes = True