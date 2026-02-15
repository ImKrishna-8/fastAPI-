from pydantic import BaseModel
from typing import Optional
class bookResponse(BaseModel):
    id:int
    title:str
    author:str
    price:int

class bookRequest(BaseModel):
    title:str
    author:Optional[str] = None
    price:int

class createUser(BaseModel):
    username:str
    password:str 

class Token(BaseModel):
    access_token:str
    token_type:str
