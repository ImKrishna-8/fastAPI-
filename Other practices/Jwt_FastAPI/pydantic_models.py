from pydantic import BaseModel
from typing import Optional

class userRequest(BaseModel):
    username:str
    password:str

class gameRequest(BaseModel):
    name:str
    company:Optional[str]

class gameResponse(gameRequest):
    id:int