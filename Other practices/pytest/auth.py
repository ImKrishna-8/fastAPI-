from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.routing import APIRouter
from pydantic_models import UserRequest
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from database import sessionLocal
from models import User
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

SECRECT_KEY = '1q2w3e4r5t6y7u8i9o0p'
ALGORITHM = 'HS256'

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/')
def create_user(user:UserRequest,db:Session = Depends(get_db)):
    db_user = User(
        id=user.id,
        username = user.username,
        password = pwd_context.hash(user.password)
    )

    if not db_user:
        raise HTTPException(status_code=401,detail="something wrong in details")
    
    db.add(db_user)
    db.commit()
    return {'msg':'User created Successfully'}

@router.post('/token')
def get_token(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user = authenticate_user(form.username,form.password,db)    

    if not user:
        raise HTTPException(status_code=404,detail='Something Wrong either Username Or Password')

    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=10)) # type: ignore

    return {
        'access_token':token,
        'token_type':'bearer'
    }

def authenticate_user(username:str,password:str,db:Session):
    db_user = db.query(User).filter(User.username == username).first()

    if not db_user:
        return None

    if not pwd_context.verify(password,db_user.password): # type: ignore
        return None

    return db_user

def create_access_token(username:str,userid:int,role:str,expire:timedelta):
    to_encode={
        'sub':username,
        'userid':userid,
        'role':role
    }
    to_encode.update({'exp':datetime.now(timezone.utc)+expire})
    return jwt.encode(to_encode,SECRECT_KEY,algorithm=ALGORITHM)

def get_current_user(token:str=Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token,SECRECT_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        userid=payload.get('userid')
        role = payload.get('role')

        if not username:
            raise HTTPException(status_code=404,detail="error in getting user")
        
        return {
            'username':username,
            'userid':userid,
            'role':role
        }

    except JWTError:
        raise JWTError
    
def role_check(role:str):
    def check(user:dict=Depends(get_current_user)):

        if role != user['role']:
            raise HTTPException(status_code=404,detail='not a admin')
        return user
    
    return check
