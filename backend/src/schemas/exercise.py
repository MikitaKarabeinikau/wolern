from pydantic import BaseModel, Field, field_validator , List
from typing import Optional
from .multiple_choice_exercise import MultipleChoiceExerciseResponse
from datetime import datetime

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class ExerciseBase(BaseModel):
    '''Base schema for Exercise'''
    difficulty: str = Field(..., example='Beginner')
    part_of_speech: str = Field(..., example='Noun')
    question: str = Field(..., example='What word means...')
    explanation: str = Field(..., example='This word is used to...')
    hints: List[str] = Field(..., example=['Hint 1', 'Hint 2'])

    @field_validator('difficulty')
    def validate_difficulty(cls, value):
        if value not in ['Beginner', 'Intermediate', 'Advanced']:
            raise ValueError('Difficulty must be one of Beginner, Intermediate, or Advanced')
        return value

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class ExerciseCreate(ExerciseBase):
    '''Schema for creating an Exercise'''
    word_id:int = Field(..., example=1)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class ExerciseResponse(ExerciseBase):
    '''Schema for Exercise response'''
    id: int
    word_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# DETAILED RESPONSE WITH MULTIPLE CHOICE
# ============================================================================
class ExerciseDetailResponse(ExerciseResponse):
    '''Schema for Exercise with multiple choice details'''
    multiple_choice: Optional[dict] = None
    
    class Config:
        from_attributes = True