from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import database, models, schemas, oauth2

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=schemas.UserProfile)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_pwd = pwd_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    token = oauth2.create_access_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}
