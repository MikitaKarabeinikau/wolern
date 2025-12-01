"""
CRUD operations for all models.
Provides centralized access to database operations.
"""

# ============================================================================
# USER CRUD OPERATIONS
# ============================================================================
from .users import (
    create_user,
    get_all_users,
    get_user_by_username,
    get_user_role,
    get_user_by_id,
    get_user_id_by_clerk_id,
    get_user_by_clerk_id,
    update_username,
    update_native_language,
    update_preferred_language,
    delete_user,
)

# ============================================================================
# VOCABULARY CRUD OPERATIONS
# ============================================================================
from .vocabulary import (
    create_vocabulary,
    get_number_of_vocabularies_by_user,
    update_vocabulary_name,
)

# ============================================================================
# WORDS CRUD OPERATIONS
# ============================================================================
from .words import (
    add_word,
    get_all_words_from_db,
    get_word_id_by_word,
    get_word_by_id,
    get_words_count,
    get_words_by_language,
    get_word_audio_url,
    get_word_frequency,
)

# ============================================================================
# PUBLIC API
# ============================================================================
__all__ = [
    # User operations
    "create_user",
    "get_all_users",
    "get_user_by_username",
    "get_user_role",
    "get_user_by_id",
    "get_user_id_by_clerk_id",
    "get_user_by_clerk_id",
    "update_username",
    "update_native_language",
    "update_preferred_language",
    "delete_user",
    
    # Vocabulary operations
    "create_vocabulary",
    "get_vocabulary_by_user",
    "get_number_of_vocabularies_by_user",
    "update_vocabulary_name",
    "delete_vocabulary",
    
    # Words operations
    "add_word",
    "get_all_words_from_db",
    "get_word_id_by_word",
    "get_word_by_id",
    "get_words_count",
    "get_words_by_language",
    "get_word_audio_url",
    "get_word_frequency",
]