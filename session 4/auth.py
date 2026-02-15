from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import APIRouter 
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session

from pydantic_models import createUser,Token
import models
from database import sessionLocal 
from jose import jwt 
from datetime import timedelta,datetime
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "1q2w3e4r5t6y7u8i9o0p"
ALGORITHM = 'HS256'


pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    try:
        with sessionLocal() as session:
            yield session
    except:
        raise HTTPException(status_code=404)
    finally:
        session.close()
        

@router.post('/')
def create_user(user:createUser, db:Session=Depends(get_db)):
    db_user = models.User(
        username = user.username,
        password= pwd_context.hash(user.password)
    )

    db.add(db_user)
    db.commit()
    return "User created"

@router.post('/token',response_model=Token)
def get_token(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    
    user = authenticate_user(form.username,form.password,db)

    if not user:
        raise HTTPException(status_code=404,detail="User Authentication Failed")
    
    token = create_access_token(user.username,user.id,timedelta(minutes=10))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username:str,password:str,db:Session):
    user = db.query(models.User).filter(models.User.username==username).first()
    
    if not user:
        return None 
    
    if pwd_context.verify(password,user.password):
        return user
    
    return None

def create_access_token(username,userid,expiretime):
    to_encode = {'sub':username,"id":userid}
    to_encode.update({'exp':datetime.utcnow()+expiretime})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def get_current_user(token:str=Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')

        if not username:
            raise HTTPException(status_code=401)
        
        return {'username':username,"id":user_id}

    except:
        raise HTTPException(status_code=401)