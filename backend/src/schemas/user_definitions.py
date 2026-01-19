from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from backend.src.config import Settings


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserDefinitionBase(BaseModel):
    """Base user definition schema."""

    part_of_speech: Settings.PART_OF_SPEECH = Field(..., json_schema_extra={"example": "noun"})
    definition: str = Field(
        ...,
        min_length=1,
        max_length=150,
        json_schema_extra={"example": "A small domesticated carnivorous mammal."},
    )

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, v: str) -> str:
        """Validate definition is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Definition cannot be empty or whitespace")
        return v.strip()


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserDefinitionCreate(UserDefinitionBase):
    """Schema for creating a user definition."""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserDefinitionUpdate(BaseModel):
    """Schema for updating a user definition."""

    part_of_speech: Optional[Settings.PART_OF_SPEECH] = Field(
        None, json_schema_extra={"example": "verb"}
    )
    definition: Optional[str] = Field(
        None, min_length=1, max_length=500, json_schema_extra={"example": "An updated definition"}
    )

    @field_validator("definition")
    @classmethod
    def validate_definition(cls, v: Optional[str]) -> Optional[str]:
        """Validate definition if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Definition cannot be empty or whitespace")
        return v.strip() if v else None


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserDefinitionResponse(BaseModel):
    """Schema for user definition response."""

    id: int
    user_word_status_id: int
    part_of_speech: str
    definition: str

    model_config = ConfigDict(from_attributes=True)


class UserDefinitionListResponse(BaseModel):
    """Schema for list of user definitions."""

    success: bool = True
    count: int
    definitions: list[UserDefinitionResponse]
