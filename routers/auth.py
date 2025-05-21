from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models import User
from schemas import UserLogin, UserProfile, UserCreate
from oauth2 import create_access_token

router = APIRouter(tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserProfile)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# auth.py
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    token = create_access_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}
