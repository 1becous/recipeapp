from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import schemas, models, database, oauth2


router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=schemas.CommentDisplay)
def create_comment(comment: schemas.CommentCreate,
                   db: Session = Depends(database.get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == comment.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    new_comment = models.Comment(content=comment.content, recipe_id=comment.recipe_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/recipe/{recipe_id}", response_model=List[schemas.CommentDisplay])
def get_comments(recipe_id: int, db: Session = Depends(database.get_db)):
    comments = (
      db.query(models.Comment)
        .options(joinedload(models.Comment.user))
        .filter(models.Comment.recipe_id == recipe_id)
        .all()
    )
    return comments