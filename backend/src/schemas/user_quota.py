from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from backend.src.config import settings

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserQuotaBase(BaseModel):
    '''Base schema for user quota'''
    subscription_type: Optional[Literal["free", "premium", "enterprise"]] = Field(
        default="free", 
        example="free"
    )
    quota_remaining: int = Field(..., ge=0, example=100)

    @field_validator('subscription_type')
    @classmethod
    def validate_subscription_type(cls, value):
        if value and value not in settings.ALLOWED_SUBSCRIPTION_TYPES:
            raise ValueError(f"Subscription type must be one of {settings.ALLOWED_SUBSCRIPTION_TYPES}")
        return value

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserQuotaCreate(BaseModel):
    '''Schema for creating user quota'''
    user_id: int = Field(..., example=1)
    subscription_type: Optional[Literal["free", "premium", "enterprise"]] = Field(
        default="free", 
        example="free"
    )
    quota_remaining: int = Field(..., ge=0, example=100)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserQuotaUpdate(BaseModel):
    '''Schema for updating user quota'''
    subscription_type: Optional[Literal["free", "premium", "enterprise"]] = Field(
        None, 
        example="premium"
    )
    quota_remaining: Optional[int] = Field(None, ge=0, example=50)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserQuotaResponse(UserQuotaBase):
    '''Schema for user quota response'''
    id: int
    user_id: int
    last_reset: datetime

    class Config:
        from_attributes = True

# ============================================================================
# QUOTA STATUS SCHEMA
# ============================================================================
class UserQuotaStatusResponse(BaseModel):
    '''Schema for checking quota status'''
    user_id: int
    subscription_type: str
    quota_remaining: int
    last_reset: datetime
    
    class Config:
        from_attributes = True