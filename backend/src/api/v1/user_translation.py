from fastapi import APIRouter, Depends, HTTPException, status
import logging
from sqlalchemy.orm import Session
from backend.src.database.database import get_db
from services import user_content_service as crud_service
from backend.src.schemas import user_translations as user_trans_schemas
from backend.src.api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-translations", tags=["User Translations"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_translation(
    translation_data: user_trans_schemas.UserTranslationCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new user translation entry in the database.

    - **user_word_status_id**: The word status to attach translation to
    - **language**: The language of the translation
    - **translation**: The translated text

    Returns:
        - 201: User translation created successfully
        - 403: Forbidden - User doesn't own the word status
        - 400: Bad Request - Invalid data
    """
    try:
        created_translation = crud_service.create_user_translation_secure(
            db=db,
            user_word_status_id=translation_data.user_word_status_id,
            user_id=user["id"],
            language=translation_data.language,
            translation=translation_data.translation,
        )

        logger.info(f"User {user['id']} created translation {created_translation.id}")

        return {
            "success": True,
            "message": "User translation created successfully",
            "translation": user_trans_schemas.UserTranslationResponse.model_validate(
                created_translation
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user translation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user translation",
        )


@router.get("/{translation_id}")
async def get_user_translation(
    translation_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve a user translation by its ID with ownership verification.

    - **translation_id**: The ID of the user translation to retrieve

    Returns:
        - 200: User translation retrieved successfully
        - 403: Forbidden - User doesn't own the translation
        - 404: Not Found - Translation does not exist
    """
    try:
        translation = crud_service.get_user_translation_secure(
            db=db, translation_id=translation_id, user_id=user["id"]
        )

        return {
            "success": True,
            "translation": user_trans_schemas.UserTranslationResponse.model_validate(
                translation
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user translation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user translation",
        )


@router.get("/word-status/{user_word_status_id}")
async def list_user_translations_by_word_status(
    user_word_status_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    List all user translations for a specific user word status with ownership verification.

    - **user_word_status_id**: The ID of the user word status to list translations for

    Returns:
        - 200: List of user translations retrieved successfully
        - 403: Forbidden - User doesn't own the word status
    """
    try:
        translations = crud_service.list_user_translations_by_word_status_secure(
            db=db, user_word_status_id=user_word_status_id, user_id=user["id"]
        )

        return {
            "success": True,
            "count": len(translations),
            "translations": [
                user_trans_schemas.UserTranslationResponse.model_validate(t).model_dump()
                for t in translations
            ],
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing user translations: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list user translations",
        )


@router.put("/{translation_id}")
async def update_user_translation(
    translation_id: int,
    translation_data: user_trans_schemas.UserTranslationUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a user translation by its ID with ownership verification.

    - **translation_id**: The ID of the user translation to update
    - **language**: The new language of the translation (optional)
    - **translation**: The new translated text (optional)

    Returns:
        - 200: User translation updated successfully
        - 403: Forbidden - User doesn't own the translation
        - 404: Not Found - Translation does not exist
        - 400: Bad Request - Invalid data
    """
    try:
        updated_translation = crud_service.update_user_translation_secure(
            db=db,
            translation_id=translation_id,
            user_id=user["id"],
            language=translation_data.language,
            translation=translation_data.translation,
        )

        logger.info(f"User {user['id']} updated translation {translation_id}")

        return {
            "success": True,
            "message": "User translation updated successfully",
            "translation": user_trans_schemas.UserTranslationResponse.model_validate(
                updated_translation
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user translation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user translation",
        )


@router.delete("/{translation_id}")
async def delete_user_translation(
    translation_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Delete a user translation by its ID with ownership verification.

    - **translation_id**: The ID of the user translation to delete

    Returns:
        - 200: User translation deleted successfully
        - 403: Forbidden - User doesn't own the translation
        - 404: Not Found - Translation does not exist
    """
    try:
        crud_service.delete_user_translation_secure(
            db=db, translation_id=translation_id, user_id=user["id"]
        )

        logger.info(f"User {user['id']} deleted translation {translation_id}")

        return {"success": True, "message": "User translation deleted successfully"}

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting user translation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user translation",
        )
