from pydantic import BaseModel, Field

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class WarningBase(BaseModel):
    """Base schema for warning entities."""
    warning_message: str = Field(..., min_length=1, max_length=255, example="NO TRANSLATION AVAILABLE.")
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class WarningCreate(WarningBase):
    """Schema for creating a new warning entity."""
    word_id: int = Field(..., example=1)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class WarningResponse(WarningBase):
    """Schema for warning entity responses."""
    id: int = Field(..., example=1)
    word_id: int = Field(..., example=1)

    class Config:
        from_attributes = True