from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    recipes = relationship("Recipe", back_populates="owner")
    comments = relationship("Comment", back_populates="user")
    saved_recipes = relationship("SavedRecipe", back_populates="user")
    

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe")
    saved_by_users = relationship("SavedRecipe", back_populates="recipe")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    user = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")

class SavedRecipe(Base):
    __tablename__ = "saved_recipes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    user = relationship("User", back_populates="saved_recipes")
    recipe = relationship("Recipe", back_populates="saved_by_users")
