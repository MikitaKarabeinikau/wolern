from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.database.database import get_db
from services import user_content_service as crud_service
from backend.src.schemas import user_tags as user_tags_schemas
from backend.src.api.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-tags", tags=["User Tags"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_tag(
    tag_data: user_tags_schemas.UserTagCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a user tag with ownership verification.

    - **user_word_status_id**: The word status to attach tag to
    - **tag**: The tag text

    Returns:
        - 201: User tag created successfully
        - 403: Forbidden - User doesn't own the word status
        - 400: Bad Request - Invalid data
    """
    try:
        created_tag = crud_service.create_user_tag_secure(
            db=db,
            user_word_status_id=tag_data.user_word_status_id,
            user_id=user["id"],
            tag=tag_data.tag,
        )

        logger.info(f"User {user['id']} created tag {created_tag.id}")

        return {
            "success": True,
            "message": "User tag created successfully",
            "tag": user_tags_schemas.UserTagResponse.model_validate(created_tag).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user tag: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user tag"
        )


@router.get("/{tag_id}")
async def get_user_tag(
    tag_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve a user tag by ID with ownership verification.

    - **tag_id**: The ID of the user tag to retrieve

    Returns:
        - 200: User tag retrieved successfully
        - 403: Forbidden - User doesn't own the tag
        - 404: Not Found - Tag does not exist
    """
    try:
        tag = crud_service.get_user_tag_secure(db=db, tag_id=tag_id, user_id=user["id"])

        return {
            "success": True,
            "tag": user_tags_schemas.UserTagResponse.model_validate(tag).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user tag: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve user tag"
        )


@router.get("/word-status/{user_word_status_id}")
async def get_user_tags_by_word_status(
    user_word_status_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve all user tags for a given user word status with ownership verification.

    - **user_word_status_id**: The word status to get tags for

    Returns:
        - 200: User tags retrieved successfully
        - 403: Forbidden - User doesn't own the word status
    """
    try:
        tags = crud_service.list_user_tags_by_word_status_secure(
            db=db, user_word_status_id=user_word_status_id, user_id=user["id"]
        )

        return {
            "success": True,
            "count": len(tags),
            "tags": [
                user_tags_schemas.UserTagResponse.model_validate(tag).model_dump() for tag in tags
            ],
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user tags: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve user tags"
        )


@router.put("/{tag_id}")
async def update_user_tag(
    tag_id: int,
    tag_data: user_tags_schemas.UserTagUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a user tag by ID with ownership verification.

    - **tag_id**: The ID of the user tag to update
    - **tag**: The new tag text (optional)

    Returns:
        - 200: User tag updated successfully
        - 403: Forbidden - User doesn't own the tag
        - 404: Not Found - Tag does not exist
        - 400: Bad Request - Invalid data
    """
    try:
        updated_tag = crud_service.update_user_tag_secure(
            db=db, tag_id=tag_id, user_id=user["id"], tag=tag_data.tag
        )

        logger.info(f"User {user['id']} updated tag {updated_tag.id}")

        return {
            "success": True,
            "message": "User tag updated successfully",
            "tag": user_tags_schemas.UserTagResponse.model_validate(updated_tag).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user tag: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user tag"
        )


@router.delete("/{tag_id}")
async def delete_user_tag(
    tag_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Delete a user tag by ID with ownership verification.

    - **tag_id**: The ID of the user tag to delete

    Returns:
        - 200: User tag deleted successfully
        - 403: Forbidden - User doesn't own the tag
        - 404: Not Found - Tag does not exist
    """
    try:
        crud_service.delete_user_tag_secure(db=db, tag_id=tag_id, user_id=user["id"])

        logger.info(f"User {user['id']} deleted tag {tag_id}")

        return {"success": True, "message": "User tag deleted successfully"}

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting user tag: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user tag"
        )
