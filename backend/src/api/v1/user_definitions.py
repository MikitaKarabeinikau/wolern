from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.database.database import get_db
from backend.src.services import user_content_serice as crud_service
from backend.src.schemas import user_definitions as user_def_schemas
from backend.src.api.dependencies import get_current_user
import logging 

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-definitions", tags=["User Definitions"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user_definition(
    definition_data: user_def_schemas.UserDefinitionCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a user definition with ownership verification.
    
    - **user_word_status_id**: The word status to attach definition to
    - **part_of_speech**: Part of speech (noun, verb, adjective, etc.)
    - **definition**: The definition text
    
    Returns:
        - 201: User definition created successfully
        - 403: Forbidden - User doesn't own the word status
        - 409: Conflict - Definition already exists
    """
    try:
        created_definition = crud_service.create_user_definition_secure(
            db=db,
            user_word_status_id=definition_data.user_word_status_id,
            user_id=user["id"],
            part_of_speech=definition_data.part_of_speech.value,
            definition=definition_data.definition
        )
        
        logger.info(f"User {user['id']} created definition {created_definition.id}")
        
        return {
            "success": True,
            "message": "User definition created successfully",
            "definition": user_def_schemas.UserDefinitionResponse.model_validate(
                created_definition
            ).model_dump()
        }
        
    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating user definition: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user definition"
        )


@router.get("/{definition_id}")
async def get_user_definition(
    definition_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a user definition by ID with ownership verification.
    
    Returns:
        - 200: User definition retrieved successfully
        - 404: Not Found - Definition doesn't exist
        - 403: Forbidden - User doesn't own the definition
    """
    try:
        definition = crud_service.get_user_definition_secure(
            db=db,
            definition_id=definition_id,
            user_id=user["id"]
        )
        
        if not definition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Definition {definition_id} not found"
            )
        
        return {
            "success": True,
            "definition": user_def_schemas.UserDefinitionResponse.model_validate(
                definition
            ).model_dump()
        }
        
    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user definition: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user definition"
        )


@router.put("/{definition_id}")
async def update_user_definition(
    definition_id: int,
    definition_data: user_def_schemas.UserDefinitionUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a user definition by ID with ownership verification.
    
    Returns:
        - 200: User definition updated successfully
        - 404: Not Found - Definition doesn't exist
        - 403: Forbidden - User doesn't own the definition
    """
    try:
        updated_definition = crud_service.update_user_definition_secure(
            db=db,
            definition_id=definition_id,
            user_id=user["id"],
            part_of_speech=definition_data.part_of_speech.value if definition_data.part_of_speech else None,
            definition=definition_data.definition
        )
        
        if not updated_definition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Definition {definition_id} not found"
            )
        
        logger.info(f"User {user['id']} updated definition {definition_id}")
        
        return {
            "success": True,
            "message": "User definition updated successfully",
            "definition": user_def_schemas.UserDefinitionResponse.model_validate(
                updated_definition
            ).model_dump()
        }
        
    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user definition: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user definition"
        )


@router.delete("/{definition_id}")
async def delete_user_definition(
    definition_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user definition by ID with ownership verification.
    
    Returns:
        - 200: User definition deleted successfully
        - 404: Not Found - Definition doesn't exist
        - 403: Forbidden - User doesn't own the definition
    """
    try:
        success = crud_service.delete_user_definition_secure(
            db=db,
            definition_id=definition_id,
            user_id=user["id"]
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Definition {definition_id} not found"
            )
        
        logger.info(f"User {user['id']} deleted definition {definition_id}")
        
        return {
            "success": True,
            "message": "User definition deleted successfully"
        }
        
    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user definition: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user definition"
        )


@router.get("/word-status/{user_word_status_id}")
async def get_definitions_for_word_status(
    user_word_status_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all user definitions for a specific word status with ownership verification.
    
    Returns:
        - 200: List of user definitions retrieved successfully
        - 403: Forbidden - User doesn't own the word status
    """
    try:
        definitions = crud_service.get_definitions_for_word_status_secure(
            db=db,
            user_word_status_id=user_word_status_id,
            user_id=user["id"]
        )
        
        return {
            "success": True,
            "count": len(definitions),
            "definitions": [
                user_def_schemas.UserDefinitionResponse.model_validate(defn).model_dump()
                for defn in definitions
            ]
        }
        
    except crud_service.OwnershipVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error retrieving definitions for word status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve definitions"
        )