from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy import select
from database import *
from models import *
import asyncio

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class userRequest(BaseModel):
    name:str
    age:int

class UserResponse(BaseModel):
    id:int
    name:str
    age:int

async def get_session():
    async with async_session() as session: # type: ignore
        yield session # type: ignore
 
 
@app.post('/')
async def post_data(uuser:userRequest,db:AsyncSession=Depends(get_session)):
    user = User(
        name=uuser.name,
        age=uuser.age
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return "success"

@app.get('/')
async def get_user(db:AsyncSession=Depends(get_session)):
    result = await db.execute(select(User))
    return result.scalars().all()