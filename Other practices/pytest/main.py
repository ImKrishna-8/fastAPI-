from fastapi import FastAPI,Depends,HTTPException
import models 
from database import engine,sessionLocal
from sqlalchemy.orm import Session
from auth import get_current_user,role_check
from models import User,Game
from pydantic_models import GameRequest
import auth

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally: 
        db.close()


@app.get('/users')
def all_users(db:Session=Depends(get_db),user:dict=Depends(role_check('admin'))):
    if user:
        return db.query(User).all()

@app.post('/games',status_code=201)
def add_game(game:GameRequest,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        new_game = Game(id=game.id,name=game.name,size=game.size)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return new_game 
    else:
        raise HTTPException(status_code=401,detail="game not added")
    

@app.get('/games',status_code=200)
def get_all_games(db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    if user:
        return db.query(Game).all() 
