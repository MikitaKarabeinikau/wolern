from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserTagBase(BaseModel):
    """Base schema for user tags"""

    tag: str = Field(..., min_length=1, max_length=50, json_schema_extra={"example": "animals"})

    @field_validator("tag")
    @classmethod
    def validate_tag(cls, v: str) -> str:
        """Validate tag is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Tag cannot be empty or whitespace")
        return v.strip()


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserTagCreate(UserTagBase):
    """Schema for creating a new user tag"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserTagUpdate(BaseModel):
    """Schema for updating a user tag"""

    tag: Optional[str] = Field(
        None, min_length=1, max_length=50, json_schema_extra={"example": "nature"}
    )

    @field_validator("tag")
    @classmethod
    def validate_tag(cls, v: Optional[str]) -> Optional[str]:
        """Validate tag if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Tag cannot be empty or whitespace")
        return v.strip() if v else None


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserTagResponse(BaseModel):
    """Schema for user tag response"""

    id: int
    user_word_status_id: int
    tag: str

    model_config = ConfigDict(from_attributes=True)


class UserTagListResponse(BaseModel):
    """Schema for list of user tags"""

    success: bool = True
    count: int
    tags: list[UserTagResponse]
