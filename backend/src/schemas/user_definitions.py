from pydantic import BaseModel, Field, field_validator
from backend.src.config import settings

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserDefinitionBase(BaseModel):
    part_of_speech: str = Field(..., example="noun")
    definition: str = Field(..., example="A small domesticated carnivorous mammal.")

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserDefinitionCreate(UserDefinitionBase):
    user_word_status_id: int = Field(..., example=1)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserDefinitionResponse(BaseModel):
    id: int
    user_word_status_id: int
    part_of_speech: str
    definition: str

    class Config:
        from_attributes = True