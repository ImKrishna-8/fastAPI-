from sqlmodel import Field,SQLModel,Relationship
from typing import List,Optional


class UserCreate(SQLModel):
    username:str
    password:str

class User(UserCreate, table=True):
    __tablename__ = "user" # type: ignore

    id:Optional[int]=Field(primary_key=True)
    recipes : List["Recipe"] = Relationship(back_populates='owner')

class RecipeCreate(SQLModel):
    title: str
    description: str

class Recipe(RecipeCreate,table=True):
    __tablename__ = 'recipes' # type: ignore

    id:Optional[int]=Field(primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="recipes")
