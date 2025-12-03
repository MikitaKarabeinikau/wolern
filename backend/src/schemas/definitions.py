from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================


class DefinitionBase(BaseModel):
    """Base schema for definition entities."""

    definition: str = Field(
        ...,
        min_length=1,
        max_length=500,
        json_schema_extra={"example": "A statement of the exact meaning of a word."},
    )
    part_of_speech: str = Field(
        ..., min_length=3, max_length=50, json_schema_extra={"example": "noun"}
    )


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class DefinitionCreate(DefinitionBase):
    """Schema for creating a new definition."""

    word_id: int = Field(..., json_schema_extra={"example": 1})


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class DefinitionResponse(BaseModel):
    """Schema for definition response."""

    id: int
    word_id: int
    definition: str
    part_of_speech: str

    model_config = ConfigDict(from_attributes=True)
