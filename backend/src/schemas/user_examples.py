from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from backend.src.config import Settings


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserExampleBase(BaseModel):
    """Base schema for user examples."""

    part_of_speech: Settings.PART_OF_SPEECH = Field(..., json_schema_extra={"example": "noun"})
    example: str = Field(
        ..., min_length=5, max_length=150, json_schema_extra={"example": "The cat sat on the mat."}
    )

    @field_validator("example")
    @classmethod
    def validate_example(cls, v: str) -> str:
        """Validate example is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Example cannot be empty or whitespace")
        return v.strip()


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserExampleCreate(UserExampleBase):
    """Schema for creating a user example."""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserExampleUpdate(BaseModel):
    """Schema for updating a user example."""

    part_of_speech: Optional[Settings.PART_OF_SPEECH] = Field(
        None, json_schema_extra={"example": "verb"}
    )
    example: Optional[str] = Field(
        None, min_length=5, max_length=150, json_schema_extra={"example": "She runs every morning."}
    )

    @field_validator("example")
    @classmethod
    def validate_example(cls, v: Optional[str]) -> Optional[str]:
        """Validate example if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Example cannot be empty or whitespace")
        return v.strip() if v else None


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserExampleResponse(BaseModel):
    """Schema for user example response."""

    id: int
    user_word_status_id: int
    part_of_speech: str
    example: str

    model_config = ConfigDict(from_attributes=True)


class UserExampleListResponse(BaseModel):
    """Schema for list of user examples response."""

    success: bool = True
    count: int
    examples: list[UserExampleResponse]
