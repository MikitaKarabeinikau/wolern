from fastapi import APIRouter, Depends, HTTPException, Request, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.src.database import get_database
from backend.utils import authenticate_and_get_user_details
from backend.src.database.models import Tag, Words
from backend.src.database.tags import get_all_tags_for_user_from_db, delete_tag_by_id, update_tag_by_id, get_tag_by_id
from backend.schemas import TagResponse  

router = APIRouter()

@router.get("/user/words/tags/all", response_model=TagResponse)
async def get_all_tags_for_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]
        all_tags = get_all_tags_for_user_from_db(db, clerk_id)
        
        return {"tags": all_tags}
    except HTTPException as http_exc:
        raise HTTPException(status_code=http_exc.status_code,detail=http_exc.detail)  
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve tags: " + str(e))


@router.put("/user/words/tags/{id}", status_code=204)
async def update_tag(
    request: Request,
    id: int,
    tag: str = Body(..., embed=True),
    db: Session = Depends(get_database),
):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_tag = get_tag_by_id(db, id)
        if not existing_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        
        word = db.query(Words).filter(Words.id == existing_tag.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        update_tag_by_id(db, id, tag, word.id)
        db.commit()
        return None  

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc  
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update tag: " + str(e))
    

@router.delete("/user/words/tags/{id}",status_code=204)
async def delete_tag(request: Request, id: int, db: Session = Depends(get_database)):
    try:
        user_details = authenticate_and_get_user_details(request=request)
        clerk_id = user_details["user_id"]

        existing_tag = get_tag_by_id(db, id)
        if not existing_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        
        word = db.query(Words).filter(Words.id == existing_tag.word_id).first()
        if not word or word.added_by_user_id != clerk_id:
            raise HTTPException(status_code=403, detail="User does not have permission.")

        was_deleted = delete_tag_by_id(db=db, clerk_id=clerk_id, tag_id=id)

        if not was_deleted:
            raise HTTPException(status_code=404, detail="Tag not found or user does not have permission.")
        return None

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred after the transaction: {e}")