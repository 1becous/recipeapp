from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database, oauth2

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=schemas.RecipeDisplay)
def create_recipe(recipe: schemas.RecipeCreate,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(oauth2.get_current_user)):
    new_recipe = models.Recipe(**recipe.dict(), owner_id=current_user.id)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

@router.get("/", response_model=List[schemas.RecipeDisplay])
def get_recipes(db: Session = Depends(database.get_db)):
    recipes = db.query(models.Recipe).all()
    return recipes

@router.get("/{recipe_id}", response_model=schemas.RecipeDisplay)
def get_recipe(recipe_id: int, db: Session = Depends(database.get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe
