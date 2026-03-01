from pydantic import BaseModel


class UserRequest(BaseModel):
    id:int
    username:str
    password:str

class GameRequest(BaseModel):
    id:int
    name:str
    size:int 