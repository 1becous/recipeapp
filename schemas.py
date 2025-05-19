from pydantic import BaseModel, EmailStr
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserProfile(UserBase):
    id: int
    class Config:
        from_attributes = True

# Recipe Schemas
class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    cooking_time: int
    difficulty: int

class RecipeCreate(RecipeBase):
    pass

class RecipeDisplay(RecipeBase):
    id: int
    owner: UserProfile
    class Config:
        from_attributes = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    recipe_id: int

class CommentDisplay(CommentBase):
    id: int
    user: UserProfile
    class Config:
        from_attributes = True

# schemas.py
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RatingBase(BaseModel):
    rating: float
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    rated_user_id: Optional[int] = None
    recipe_id: Optional[int] = None

class RatingDisplay(RatingBase):
    id: int
    rater_id: int
    rated_user_id: Optional[int]
    recipe_id: Optional[int]

    class Config:
        orm_mode = True

class UserDisplay(BaseModel):
    id: int
    name: str
    email: str
    average_rating: float

    class Config:
        orm_mode = True

class RecipeDisplay(BaseModel):
    id: int
    title: str
    ingredients: str
    instructions: str
    cooking_time: int
    difficulty: int
    average_rating: float
    owner_id: int

    class Config:
        orm_mode = True
