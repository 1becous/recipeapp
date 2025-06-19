from fastapi import APIRouter, Depends
from schemas import UserProfile
from models import User
from oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserProfile)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
