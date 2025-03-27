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
