from sqlmodel import SQLModel,Field
from typing import Optional
from database import engine

class BookCreate(SQLModel):
    title:str = Field(max_length=30)
    author:Optional[str]=Field()
    price:int

class Book(BookCreate,table=True):
    id:int=Field(primary_key=True)


SQLModel.metadata.create_all(engine)
