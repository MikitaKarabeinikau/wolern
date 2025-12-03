from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.database.database import get_db
from backend.src.services import user_content_serice as crud_service
from backend.src.schemas import user_synonyms as user_syn_schemas
from backend.src.api.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-synonyms", tags=["User Synonyms"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_synonym(
    synonym_data: user_syn_schemas.UserSynonymCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a user synonym with ownership verification.

    - **user_word_status_id**: The word status to attach synonym to
    - **synonym**: The synonym text

    Returns:
        - 201: User synonym created successfully
        - 403: Forbidden - User doesn't own the word status
        - 400: Bad Request - Invalid data
    """
    try:
        created_synonym = crud_service.create_user_synonym_secure(
            db=db,
            user_word_status_id=synonym_data.user_word_status_id,
            user_id=user["id"],
            synonym=synonym_data.synonym,
        )

        logger.info(f"User {user['id']} created synonym {created_synonym.id}")

        return {
            "success": True,
            "message": "User synonym created successfully",
            "synonym": user_syn_schemas.UserSynonymResponse.model_validate(
                created_synonym
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user synonym: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user synonym",
        )


@router.get("/{synonym_id}")
async def get_user_synonym(
    synonym_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve a user synonym by ID with ownership verification.

    Returns:
        - 200: User synonym retrieved successfully
        - 403: Forbidden - User doesn't own the synonym
        - 404: Not Found - Synonym does not exist
    """
    try:
        user_synonym = crud_service.get_user_synonym_secure(
            db=db, synonym_id=synonym_id, user_id=user["id"]
        )

        return {
            "success": True,
            "synonym": user_syn_schemas.UserSynonymResponse.model_validate(
                user_synonym
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user synonym: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user synonym",
        )


@router.get("/word-status/{user_word_status_id}")
async def list_user_synonyms_by_word_status(
    user_word_status_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    List all user synonyms for a given user word status with ownership verification.

    Returns:
        - 200: List of user synonyms retrieved successfully
        - 403: Forbidden - User doesn't own the word status
    """
    try:
        synonyms = crud_service.list_user_synonyms_by_word_status_secure(
            db=db, user_word_status_id=user_word_status_id, user_id=user["id"]
        )

        return {
            "success": True,
            "count": len(synonyms),
            "synonyms": [
                user_syn_schemas.UserSynonymResponse.model_validate(syn).model_dump()
                for syn in synonyms
            ],
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing user synonyms: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list user synonyms"
        )


@router.put("/{synonym_id}")
async def update_user_synonym(
    synonym_id: int,
    synonym_data: user_syn_schemas.UserSynonymUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a user synonym with ownership verification.

    Returns:
        - 200: User synonym updated successfully
        - 403: Forbidden - User doesn't own the synonym
        - 404: Not Found - Synonym does not exist
        - 400: Bad Request - Invalid data
    """
    try:
        updated_synonym = crud_service.update_user_synonym_secure(
            db=db, synonym_id=synonym_id, user_id=user["id"], synonym=synonym_data.synonym
        )

        logger.info(f"User {user['id']} updated synonym {synonym_id}")

        return {
            "success": True,
            "message": "User synonym updated successfully",
            "synonym": user_syn_schemas.UserSynonymResponse.model_validate(
                updated_synonym
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user synonym: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user synonym",
        )


@router.delete("/{synonym_id}")
async def delete_user_synonym(
    synonym_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Delete a user synonym by ID with ownership verification.

    Returns:
        - 200: User synonym deleted successfully
        - 404: Not Found - Synonym doesn't exist
        - 403: Forbidden - User doesn't own the synonym
    """
    try:
        crud_service.delete_user_synonym_secure(db=db, synonym_id=synonym_id, user_id=user["id"])

        logger.info(f"User {user['id']} deleted synonym {synonym_id}")

        return {"success": True, "message": "User synonym deleted successfully"}

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting user synonym: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user synonym",
        )
