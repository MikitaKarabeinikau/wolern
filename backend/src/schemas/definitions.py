from pydantic import BaseModel, Field

# ============================================================================
# BASE SCHEMAS
# ============================================================================

class DefinitionBase(BaseModel):
    """Base schema for definition entities."""
    definition: str = Field(..., min_length=1, max_length=500, example="A statement of the exact meaning of a word.")
    part_of_speech: str = Field(..., min_length=3, max_length=50, example="noun")

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class DefinitionCreate(DefinitionBase):
    """Schema for creating a new definition."""
    word_id: int = Field(..., example=1)


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class DefinitionResponse(BaseModel):
    """Schema for definition response."""
    id: int
    word_id: int
    definition: str
    part_of_speech: str

    class Config:
        from_attributes = True