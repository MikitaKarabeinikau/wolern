from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class WarningBase(BaseModel):
    """Base schema for warning entities."""
    warning_message: str = Field(..., min_length=1, max_length=255, json_schema_extra={"example": "NO TRANSLATION AVAILABLE."})
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class WarningCreate(WarningBase):
    """Schema for creating a new warning entity."""
    word_id: int = Field(..., json_schema_extra={"example": 1})

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class WarningResponse(WarningBase):
    """Schema for warning entity responses."""
    id: int = Field(..., json_schema_extra={"example": 1})
    word_id: int = Field(..., json_schema_extra={"example": 1})

    model_config = ConfigDict(from_attributes=True)