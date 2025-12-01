from pydantic import BaseModel, Field, field_validator , List,ConfigDict
from typing import Optional
from .multiple_choice_exercise import MultipleChoiceExerciseResponse
from datetime import datetime

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class ExerciseBase(BaseModel):
    '''Base schema for Exercise'''
    difficulty: str = Field(..., json_schema_extra={'example': 'Beginner'})
    part_of_speech: str = Field(..., json_schema_extra={'example': 'Noun'})
    question: str = Field(..., json_schema_extra={'example': 'What word means...'})
    explanation: str = Field(..., json_schema_extra={'example': 'This word is used to...'})
    hints: List[str] = Field(..., json_schema_extra={'example': ['Hint 1', 'Hint 2']})
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
    word_id:int = Field(..., json_schema_extra={"example": 1})

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class ExerciseResponse(ExerciseBase):
    '''Schema for Exercise response'''
    id: int
    word_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ============================================================================
# DETAILED RESPONSE WITH MULTIPLE CHOICE
# ============================================================================
class ExerciseDetailResponse(ExerciseResponse):
    '''Schema for Exercise with multiple choice details'''
    multiple_choice: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)