from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from backend.src.api.dependencies import get_current_user
import backend.src.database.crud.words as words_crud
from backend.src.database.database import get_db
from backend.src.core import Word
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/words", tags=["Words"])

@router.post("/{word}", status_code=status.HTTP_201_CREATED)
async def add_word():
    pass
