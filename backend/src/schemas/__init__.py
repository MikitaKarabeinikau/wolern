"""
Pydantic schemas for request/response validation.
Centralized exports for all schema modules.
"""

# ============================================================================
# USER SCHEMAS
# ============================================================================
from .user import (
    UserBase,
    UserCreate,
    UserUpdateUsername,
    UserUpdateNativeLanguage,
    UserUpdatePreferredLanguage,
    UserUpdateRole,
    UserResponse,
    UserPublic,
    UserWithQuota,
)

# ============================================================================
# WORD SCHEMAS
# ============================================================================
from .word import (
    WordBase,
    WordCreate,
    WordResponse,
    WordPublic,
    WordWithFullData,
)

# ============================================================================
# VOCABULARY SCHEMAS
# ============================================================================
from .vocabulary import (
    VocabularyBase,
    VocabularyCreate,
    VocabularyUpdateName,
    VocabularyResponse,
)

# ============================================================================
# DEFINITION SCHEMAS
# ============================================================================
from .definitions import (
    DefinitionBase,
    DefinitionCreate,
    DefinitionResponse,
)

# ============================================================================
# EXAMPLE SCHEMAS
# ============================================================================
from .examples import (
    ExampleBase,
    ExampleCreate,
    ExampleResponse,
)

# ============================================================================
# TRANSLATION SCHEMAS
# ============================================================================
from .translations import (
    TranslationBase,
    TranslationCreate,
    TranslationResponse,
)

# ============================================================================
# SYNONYM SCHEMAS
# ============================================================================
from .synonyms import (
    SynonymBase,
    SynonymCreate,
    SynonymResponse,
)

# ============================================================================
# TAG SCHEMAS
# ============================================================================
from .tags import (
    TagBase,
    TagCreate,
    TagResponse,
)

# ============================================================================
# WARNING SCHEMAS
# ============================================================================
from .warnings import (
    WarningBase,
    WarningCreate,
    WarningResponse,
)

# ============================================================================
# PUBLIC API
# ============================================================================
__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdateUsername",
    "UserUpdateNativeLanguage",
    "UserUpdatePreferredLanguage",
    "UserUpdateRole",
    "UserResponse",
    "UserPublic",
    "UserWithQuota",
    
    # Word schemas
    "WordBase",
    "WordCreate",
    "WordResponse",
    "WordPublic",
    "WordWithFullData",
    
    # Vocabulary schemas
    "VocabularyBase",
    "VocabularyCreate",
    "VocabularyUpdateName",
    "VocabularyResponse",
    
    # Definition schemas
    "DefinitionBase",
    "DefinitionCreate",
    "DefinitionResponse",
    
    # Example schemas
    "ExampleBase",
    "ExampleCreate",
    "ExampleResponse",
    
    # Translation schemas
    "TranslationBase",
    "TranslationCreate",
    "TranslationResponse",
    
    # Synonym schemas
    "SynonymBase",
    "SynonymCreate",
    "SynonymResponse",
    
    # Tag schemas
    "TagBase",
    "TagCreate",
    "TagResponse",
    
    # Warning schemas
    "WarningBase",
    "WarningCreate",
    "WarningResponse",
]