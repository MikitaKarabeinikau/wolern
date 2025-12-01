from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class ExampleBase(BaseModel):
    """Base schema for example entities."""
    part_of_speech : str = Field(..., min_length=5, max_length=50, json_schema_extra={"example": "Noun"})
    example: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "Sample Example"})


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class ExampleCreate(ExampleBase):
    """Schema for creating a new example entity."""
    word_id: int = Field(..., json_schema_extra={"example": 1})

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class ExampleResponse(ExampleBase):
    """Schema for responding with example entity data."""
    id: int = Field(..., json_schema_extra={"example": 1})
    word_id: int = Field(..., json_schema_extra={"example": 1})
    
    
    model_config = ConfigDict(from_attributes=True)