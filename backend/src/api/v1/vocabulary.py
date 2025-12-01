from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  
from backend.src.api.dependencies import get_current_user
from backend.src.database.database import get_db
from backend.src.database.crud import vocabulary as vocab_crud 
from backend.src.schemas import vocabulary as vocab_schemas
import logging 

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vocabularies", tags=["Vocabularies"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_vocabulary(
    vocabulary_data: vocab_schemas.VocabularyCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new vocabulary list for the authenticated user.
    
    - **name**: Name of the vocabulary (e.g., "Work", "Travel", "Business")
    
    Returns:
        - 201: Vocabulary created successfully
        - 409: Vocabulary with same name already exists
        - 400: Maximum vocabularies limit reached
    """
    try:
        # Check if vocabulary with same name exists
        existing = vocab_crud.get_vocabulary_by_name(db, user["id"], vocabulary_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vocabulary '{vocabulary_data.name}' already exists"
            )
        
        # Create vocabulary (user_id from token, not request)
        vocabulary = vocab_crud.create_vocabulary(
            db=db, 
            user_id=user["id"],  # ✅ From authenticated user
            name=vocabulary_data.name
        )
        logger.info(f"Vocabulary '{vocabulary_data.name}' created for user {user['id']}")
        
        return {
            "success": True,
            "message": f"Vocabulary '{vocabulary.name}' created successfully",
            "vocabulary": vocab_schemas.VocabularyResponse.model_validate(vocabulary).model_dump()
        }
        
    except HTTPException:
        raise
        
    except ValueError as e:
        # Max vocabularies reached
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except Exception as e:
        logger.error(f"Error creating vocabulary: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create vocabulary"
        )


@router.get("") 
async def get_user_vocabularies(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all vocabulary lists for the authenticated user.
    
    Returns:
        - 200: List of vocabularies with word counts
    """
    try:
        vocabularies = vocab_crud.get_vocabularies_by_user(db=db, user_id=user["id"])
        logger.info(f"Retrieved {len(vocabularies)} vocabularies for user {user['id']}")
        
        return {
            "success": True,
            "count": len(vocabularies),
            "vocabularies": [
                {
                    **vocab_schemas.VocabularyResponse.model_validate(vocab).model_dump(),
                    "created_at": vocab.created_at.isoformat() if vocab.created_at else None,
                    "word_count": len(vocab.words) if hasattr(vocab, 'words') else 0
                }
                for vocab in vocabularies
            ]
        }
        
    except Exception as e:
        logger.error(f"Error retrieving vocabularies for user {user['id']}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vocabularies"
        )


@router.get("/{vocabulary_id}")
async def get_vocabulary_by_id(
    vocabulary_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific vocabulary by ID.
    
    Returns:
        - 200: Vocabulary details
        - 404: Vocabulary not found
    """
    try:
        vocabulary = vocab_crud.get_vocabulary_by_vocabulary_id(
            db=db, 
            user_id=user["id"], 
            vocabulary_id=vocabulary_id
        )
        
        if not vocabulary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vocabulary with ID {vocabulary_id} not found"
            )
        
        logger.info(f"Retrieved vocabulary {vocabulary_id} for user {user['id']}")
        
        return {
            "success": True,
            "vocabulary": {
                **vocab_schemas.VocabularyResponse.model_validate(vocabulary).model_dump(),
                "created_at": vocabulary.created_at.isoformat() if vocabulary.created_at else None,
                "word_count": len(vocabulary.words) if hasattr(vocabulary, 'words') else 0
            }
        }
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error retrieving vocabulary {vocabulary_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vocabulary"
        )


@router.put("/{vocabulary_id}")
async def update_vocabulary_name(
    vocabulary_id: int,
    vocabulary_data: vocab_schemas.VocabularyUpdateName,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a vocabulary's name.
    
    Returns:
        - 200: Vocabulary updated successfully
        - 404: Vocabulary not found
        - 403: User doesn't own vocabulary
    """
    try:
        vocabulary = vocab_crud.update_vocabulary_name(
            db=db,
            user_id=user["id"],
            vocabulary_id=vocabulary_id,
            new_name=vocabulary_data.name
        )
        
        if not vocabulary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vocabulary with ID {vocabulary_id} not found"
            )
        
        logger.info(f"Updated vocabulary {vocabulary_id} to '{vocabulary_data.name}' for user {user['id']}")
        
        return {
            "success": True,
            "message": f"Vocabulary renamed to '{vocabulary_data.name}'",
            "vocabulary": vocab_schemas.VocabularyResponse.model_validate(vocabulary).model_dump()
        }
        
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error updating vocabulary {vocabulary_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update vocabulary"
        )


@router.delete("/{vocabulary_id}")
async def delete_vocabulary_by_id(
    vocabulary_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a vocabulary by ID.
    
    This will also delete all associated words and customizations (cascade).
    
    Returns:
        - 200: Vocabulary deleted successfully
        - 404: Vocabulary not found
        - 403: User doesn't own vocabulary
    """
    try:
        # Check if vocabulary exists first
        vocabulary = vocab_crud.get_vocabulary_by_vocabulary_id(
            db=db,
            user_id=user["id"],
            vocabulary_id=vocabulary_id
        )
        
        if not vocabulary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vocabulary with ID {vocabulary_id} not found"
            )
        
        # Delete vocabulary
        success = vocab_crud.delete_vocabulary_by_id(
            db=db,
            user_id=user["id"],
            vocabulary_id=vocabulary_id
        )
        
        if success:
            logger.info(f"Deleted vocabulary {vocabulary_id} for user {user['id']}")
            return {
                "success": True,
                "message": f"Vocabulary '{vocabulary.name}' deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete vocabulary"
            )
        
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error deleting vocabulary {vocabulary_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete vocabulary"
        )


@router.delete("/by-name/{vocabulary_name}")
async def delete_vocabulary_by_name(
    vocabulary_name: str,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a vocabulary by name.
    
    Alternative endpoint to delete by name instead of ID.
    This will also delete all associated words and customizations (cascade).
    
    Returns:
        - 200: Vocabulary deleted successfully
        - 404: Vocabulary not found
    """
    try:
        # Check if vocabulary exists first
        vocabulary = vocab_crud.get_vocabulary_by_name(
            db=db,
            user_id=user["id"],
            vocabulary_name=vocabulary_name
        )
        
        if not vocabulary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vocabulary '{vocabulary_name}' not found"
            )
        
        # Delete vocabulary
        success = vocab_crud.delete_vocabulary_by_name(
            db=db, 
            user_id=user["id"],
            vocabulary_name=vocabulary_name
        )
        
        if success:
            logger.info(f"Deleted vocabulary '{vocabulary_name}' for user {user['id']}")
            return {
                "success": True,
                "message": f"Vocabulary '{vocabulary_name}' deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete vocabulary"
            )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error deleting vocabulary '{vocabulary_name}': {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete vocabulary"
        )