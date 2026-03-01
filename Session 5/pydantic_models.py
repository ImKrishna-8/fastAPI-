from pydantic import BaseModel

class CreateUser(BaseModel):
    username:str
    password:str

class CreateBook(BaseModel):
    title:str
    author:str
    price:int

class BookResponse(CreateBook):
    id:int