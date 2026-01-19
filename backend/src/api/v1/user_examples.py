from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.database.database import get_db
from services import user_content_service as crud_service
from backend.src.schemas import user_examples as user_example_schema
from backend.src.api.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-examples", tags=["User Examples"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_example(
    example_data: user_example_schema.UserExampleCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a user example with ownership verification.

    - **user_word_status_id**: The word status to attach example to
    - **part_of_speech**: Part of speech (noun, verb, adjective, etc.)
    - **example**: The example text

    Returns:
        - 201: User example created successfully
        - 403: Forbidden - User doesn't own the word status
        - 400: Bad Request - Invalid data
    """
    try:
        created_example = crud_service.create_user_example_secure(
            db=db,
            user_word_status_id=example_data.user_word_status_id,
            user_id=user["id"],
            part_of_speech=example_data.part_of_speech.value,
            example=example_data.example,
        )

        logger.info(f"User {user['id']} created example {created_example.id}")

        return {
            "success": True,
            "message": "User example created successfully",
            "example": user_example_schema.UserExampleResponse.model_validate(
                created_example
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user example: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user example",
        )


@router.get("/{example_id}")
async def get_user_example(
    example_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get a user example by ID with ownership verification.

    Returns:
        - 200: User example retrieved successfully
        - 403: Forbidden - User doesn't own the example
        - 404: Not Found - Example does not exist
    """
    try:
        user_example = crud_service.get_user_example_secure(
            db=db, example_id=example_id, user_id=user["id"]
        )

        return {
            "success": True,
            "example": user_example_schema.UserExampleResponse.model_validate(
                user_example
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user example: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user example",
        )


@router.get("/word-status/{user_word_status_id}")
async def get_user_examples_by_word_status(
    user_word_status_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get all user examples for a specific user word status with ownership verification.

    Returns:
        - 200: User examples retrieved successfully
        - 403: Forbidden - User doesn't own the word status
    """
    try:
        examples = crud_service.get_user_examples_by_word_status_secure(
            db=db, user_word_status_id=user_word_status_id, user_id=user["id"]
        )

        return {
            "success": True,
            "count": len(examples),
            "examples": [
                user_example_schema.UserExampleResponse.model_validate(ex).model_dump()
                for ex in examples
            ],
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving user examples: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user examples",
        )


@router.put("/{example_id}")
async def update_user_example(
    example_id: int,
    example_data: user_example_schema.UserExampleUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a user example with ownership verification.

    Returns:
        - 200: User example updated successfully
        - 403: Forbidden - User doesn't own the example
        - 404: Not Found - Example does not exist
    """
    try:
        updated_example = crud_service.update_user_example_secure(
            db=db,
            example_id=example_id,
            user_id=user["id"],
            part_of_speech=(
                example_data.part_of_speech.value if example_data.part_of_speech else None
            ),
            example=example_data.example,
        )

        logger.info(f"User {user['id']} updated example {example_id}")

        return {
            "success": True,
            "message": "User example updated successfully",
            "example": user_example_schema.UserExampleResponse.model_validate(
                updated_example
            ).model_dump(),
        }

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user example: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user example",
        )


@router.delete("/{example_id}")
async def delete_user_example(
    example_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Delete a user example by ID with ownership verification.

    Returns:
        - 200: User example deleted successfully
        - 403: Forbidden - User doesn't own the example
        - 404: Not Found - Example does not exist
    """
    try:
        crud_service.delete_user_example_secure(db=db, example_id=example_id, user_id=user["id"])

        logger.info(f"User {user['id']} deleted example {example_id}")

        return {"success": True, "message": "User example deleted successfully"}

    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except crud_service.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting user example: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user example",
        )
