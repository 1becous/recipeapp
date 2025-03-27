from fastapi import APIRouter, Depends
import schemas, models, oauth2

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserProfile)
def get_user_profile(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user
