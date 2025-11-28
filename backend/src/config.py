import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic for validation and type safety.
    """
    
    # ============================================================================
    # APPLICATION
    # ============================================================================
    APP_NAME: str = "Wolern API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # ============================================================================
    # API
    # ============================================================================
    API_V1_PREFIX: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # ============================================================================
    # DATABASE
    # ============================================================================
    # PostgreSQL connection
    DATABASE_URL: str
    
    # Connection pool settings
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_PRE_PING: bool = True
    DB_ECHO: bool = False  # Set to True to see SQL queries in logs
    
    # ============================================================================
    # CLERK AUTHENTICATION
    # ============================================================================
    
    # ============================================================================
    # CORS
    # ============================================================================
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5172",
        "http://localhost:8000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    
    # ============================================================================
    # SECURITY
    # ============================================================================
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ============================================================================
    # LOGGING
    # ============================================================================
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ============================================================================
    # RATE LIMITING
    # ============================================================================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # ============================================================================
    # QUOTA SYSTEM
    # ============================================================================
    DEFAULT_USER_QUOTA: int = 10
    QUOTA_RESET_HOURS: int = 24
    ADMIN_QUOTA: int = 1000
    
    # ============================================================================
    # EXERCISE SETTINGS
    # ============================================================================
    MAX_EXERCISES_PER_WORD: int = 10
    EXERCISE_DIFFICULTY_LEVELS: list[str] = ["Beginner", "Intermediate", "Advanced"]
    
    # ============================================================================
    # WORD SETTINGS
    # ============================================================================
    MAX_WORDS_PER_VOCABULARY: int = 1000
    SUPPORTED_LANGUAGES: list[str] = ["english", "russian", "polish"]
    WORD_LEARNING_STAGE: Dict[int,str] = {0:'UNKNOWN',1:'LEARNING',2:'GOOD',3:'EXCELLENT',4:'KNOWN'}
    CORRECT_STREAK_THRESHOLD: int = 5
        
    # ============================================================================
    # VOCABULARY SETTINGS
    # ===========================================================================
    MAX_VOCABULARIES_PER_USER: int = 25
    DEFAULT_VOCABULARIES: list[str] = ["NEW_WORDS", "LEARNING", "KNOWN"]
    

        
    # ============================================================================
    # ROLES AND PERMISSIONS
    # ============================================================================
    VALID_USER_ROLES: list[str] = ["user", "admin", "teacher", "student"]
    ALLOWED_SUBSCRIPTION_TYPES: list[str] = ["free", "premium", "enterprise"]
    
    # ============================================================================
    # VALIDATIONS
    # ============================================================================
    ALLOWED_EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com"]
    
    # ============================================================================
    # REDIS
    # ============================================================================
    REDIS_URL: Optional[str] = None
    REDIS_CACHE_ENABLED: bool = False
    REDIS_CACHE_TTL: int = 300  # seconds
    
    # ============================================================================
    # EXTERNAL APIs 
    # ============================================================================

    # ============================================================================
    # COMPUTED PROPERTIES
    # ============================================================================
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL."""
        return self.DATABASE_URL
    
    @property
    def database_url_async(self) -> str:
        """Get asynchronous database URL (if using async SQLAlchemy)."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Use @lru_cache to avoid reading .env file multiple times.
    """
    return Settings()


# Singleton instance
settings = get_settings()