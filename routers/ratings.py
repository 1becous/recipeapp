from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database, oauth2
from sqlalchemy import func

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/", response_model=schemas.RatingDisplay)
def create_rating(rating: schemas.RatingCreate,
                 db: Session = Depends(database.get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    # Check if rating is for a user or recipe
    if rating.rated_user_id and rating.recipe_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Cannot rate both user and recipe in one rating")
    
    if not rating.rated_user_id and not rating.recipe_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Must rate either a user or a recipe")

    # Create new rating
    new_rating = models.Rating(
        rating=rating.rating,
        comment=rating.comment,
        rater_id=current_user.id,
        rated_user_id=rating.rated_user_id,
        recipe_id=rating.recipe_id
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    # Update average rating
    if rating.rated_user_id:
        user = db.query(models.User).filter(models.User.id == rating.rated_user_id).first()
        avg_rating = db.query(func.avg(models.Rating.rating)).filter(
            models.Rating.rated_user_id == rating.rated_user_id
        ).scalar()
        user.average_rating = avg_rating or 0.0
    elif rating.recipe_id:
        recipe = db.query(models.Recipe).filter(models.Recipe.id == rating.recipe_id).first()
        avg_rating = db.query(func.avg(models.Rating.rating)).filter(
            models.Rating.recipe_id == rating.recipe_id
        ).scalar()
        recipe.average_rating = avg_rating or 0.0

    db.commit()
    return new_rating

@router.get("/user/{user_id}", response_model=List[schemas.RatingDisplay])
def get_user_ratings(user_id: int, db: Session = Depends(database.get_db)):
    ratings = db.query(models.Rating).filter(models.Rating.rated_user_id == user_id).all()
    return ratings

@router.get("/recipe/{recipe_id}", response_model=List[schemas.RatingDisplay])
def get_recipe_ratings(recipe_id: int, db: Session = Depends(database.get_db)):
    ratings = db.query(models.Rating).filter(models.Rating.recipe_id == recipe_id).all()
    return ratings

@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int,
                 db: Session = Depends(database.get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    
    if rating.rater_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="Not authorized to delete this rating")
    
    # Store the IDs before deleting
    rated_user_id = rating.rated_user_id
    recipe_id = rating.recipe_id
    
    db.delete(rating)
    db.commit()
    
    # Update average ratings
    if rated_user_id:
        user = db.query(models.User).filter(models.User.id == rated_user_id).first()
        avg_rating = db.query(func.avg(models.Rating.rating)).filter(
            models.Rating.rated_user_id == rated_user_id
        ).scalar()
        user.average_rating = avg_rating or 0.0
    elif recipe_id:
        recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
        avg_rating = db.query(func.avg(models.Rating.rating)).filter(
            models.Rating.recipe_id == recipe_id
        ).scalar()
        recipe.average_rating = avg_rating or 0.0
    
    db.commit()
    return None 