from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database, oauth2

router = APIRouter(prefix="/saved-recipes", tags=["saved-recipes"])

@router.post("/{recipe_id}", response_model=schemas.RecipeDisplay)
def save_recipe(recipe_id: int,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # Check if recipe exists
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    # Check if recipe is already saved
    existing_save = db.query(models.SavedRecipe).filter(
        models.SavedRecipe.user_id == current_user.id,
        models.SavedRecipe.recipe_id == recipe_id
    ).first()
    
    if existing_save:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Recipe already saved")
    
    # Create new saved recipe
    new_saved_recipe = models.SavedRecipe(
        user_id=current_user.id,
        recipe_id=recipe_id
    )
    db.add(new_saved_recipe)
    db.commit()
    
    return recipe

@router.get("/", response_model=List[schemas.RecipeDisplay])
def get_saved_recipes(db: Session = Depends(database.get_db),
                     current_user: models.User = Depends(oauth2.get_current_user)):
    saved_recipes = db.query(models.Recipe).join(
        models.SavedRecipe,
        models.SavedRecipe.recipe_id == models.Recipe.id
    ).filter(
        models.SavedRecipe.user_id == current_user.id
    ).all()
    return saved_recipes

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_saved_recipe(recipe_id: int,
                       db: Session = Depends(database.get_db),
                       current_user: models.User = Depends(oauth2.get_current_user)):
    saved_recipe = db.query(models.SavedRecipe).filter(
        models.SavedRecipe.user_id == current_user.id,
        models.SavedRecipe.recipe_id == recipe_id
    ).first()
    
    if not saved_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="Saved recipe not found")
    
    db.delete(saved_recipe)
    db.commit()
    return None 