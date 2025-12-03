from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserSynonymBase(BaseModel):
    """Base schema for user synonyms"""

    synonym: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "quick"})

    @field_validator("synonym")
    @classmethod
    def validate_synonym(cls, v: str) -> str:
        """Validate synonym is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Synonym cannot be empty or whitespace")
        return v.strip()


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserSynonymCreate(UserSynonymBase):
    """Schema for creating user synonym"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserSynonymUpdate(BaseModel):
    """Schema for updating user synonym"""

    synonym: Optional[str] = Field(
        None, min_length=1, max_length=100, json_schema_extra={"example": "rapid"}
    )

    @field_validator("synonym")
    @classmethod
    def validate_synonym(cls, v: Optional[str]) -> Optional[str]:
        """Validate synonym if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Synonym cannot be empty or whitespace")
        return v.strip() if v else None


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserSynonymResponse(BaseModel):
    """Schema for user synonym response"""

    id: int
    user_word_status_id: int
    synonym: str

    model_config = ConfigDict(from_attributes=True)


class UserSynonymListResponse(BaseModel):
    """Schema for list of user synonyms"""

    success: bool = True
    count: int
    synonyms: list[UserSynonymResponse]
