from fastapi import FastAPI,Depends,HTTPException
import auth
import models
from database import engine,sessionLocal
from sqlalchemy.orm import Session
from auth import get_current_user,role_check

app = FastAPI()

app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    with sessionLocal() as session:
        yield session

@app.get('/')
def get_user(user:dict=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401)
    print("herree")
    return user

@app.get('/admin')
def admin_dashboard(user:dict=Depends(role_check('admin'))):
    if user:
        return "hi admin"

@app.get('/user')
def user_dashboard(user:dict=Depends(role_check('user'))):
    if user:
        return "hi user"