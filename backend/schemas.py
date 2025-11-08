from pydantic import BaseModel, Field
from typing import List, Optional,Literal

class WebhookPayload(BaseModel):
    data: dict
    object: str
    type: str


class UserCreateRequest(BaseModel):
    clerk_user_id: str
    username: str = None
    email: str

class AddWordRequest(BaseModel):
    word: str
    

class Translation(BaseModel):
    id: int
    word_id: int
    language: Optional[str] = None
    

    translated_word: str = Field(alias='translation')

    class Config:
        from_attributes = True
        populate_by_name = True 


class TranslationResponse(BaseModel):
    translations: List[Translation]


class Synonym(BaseModel):
    id: int
    word_id: int
    synonym: str

    class Config:
        from_attributes = True

class SynonymResponse(BaseModel):
    synonyms: List[Synonym]

class Definition(BaseModel):
    id: int
    word_id: int
    part_of_speech: Optional[str] = None
    definition: str

    class Config:
        from_attributes = True

class DefinitionResponse(BaseModel):
    definitions: List[Definition]

class Example(BaseModel):
    id: int
    word_id: int
    part_of_speech: Optional[str] = None
    example_sentence: str = Field(alias='example_sentence')

    class Config:
        from_attributes = True
        populate_by_name = True

class ExampleResponse(BaseModel):
    examples: List[Example]

class Tag(BaseModel):
    id: int
    word_id: int
    tag: str

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    tags: List[Tag]

class Warning(BaseModel):
    id: int
    word_id: int
    warning_message: str = Field(alias='warning')

    class Config:
        from_attributes = True 
        populate_by_name = True
         
class WarningResponse(BaseModel):
    warnings: List[Warning]
    
    

class Exercise(BaseModel):
    """A data model for a vocabulary exercise."""

    exercise_id: str = Field(description="A unique ID for the exercise (e.g., VOCAB_FIB_001).")
    word: str = Field(description="The word the user is meant to learn/be tested on.")
    difficulty: Literal["Beginner", "Intermediate", "Advanced"] = Field(description="The difficulty level of the exercise.")
    part_of_speech: str = Field(description="The part of speech of the word (e.g., 'noun', 'adjective').")
    question: str = Field(description="The sentence with a blank where the target word should go.")
    explanation: str = Field(description="A brief explanation of the correct answer.")
    hints: Optional[List[str]] = Field(default=None, description="Optional hints to help the user answer the question.")
    created_by: str = Field(description="The clerk user ID of the user who created the exercise.")
    
class MultipleChoiceExercise(BaseModel):
    """A data model for a multiple-choice vocabulary exercise."""
    id: int = Field(description="Database ID for the exercise.")
    exercise_id: str = Field(description="A unique ID for the exercise (e.g., VOCAB_MC_001). Reference the exercise ID for tracking progress.")
    options: str = Field(description="A JSON string representing a list of 4 answer options (strings).")
    correct_answer: int = Field(description="The correct answer from the options provided.")
    
class ExerciseRequest(BaseModel):
    word: str
    difficulty: Literal["Beginner", "Intermediate", "Advanced"]
    
    class Config:
        from_attributes = True
        json_schema_extra = {"example": {
            "word": "ubiquitous",
            "difficulty": "Intermediate"
        }}