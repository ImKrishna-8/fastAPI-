from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.routing import APIRouter
from pydantic_models import CreateUser
from database import sessionLocal
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from models import User
from datetime import datetime,timedelta
from jose import JWTError,jwt


SECRET_KEY='1qaz2wsx3edc4rfv5tgb6yhn7ujm8iklop90'
ALGORITHM = 'HS256'
oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
pwd_context = CryptContext(schemes=['bcrypt_sha256'],deprecated='auto')


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_db():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
def create_user(user:CreateUser,db:Session=Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400,detail='User already exist')
    db_user = User(
        username = user.username,
        password = pwd_context.hash(user.password)
    )
    if not db_user:
        raise HTTPException(status_code=400,detail='error while creating user')
    db.add(db_user)
    db.commit()
    return {'status':'success' , 'msg':'user created Successfully'}

@router.post('/token')
def generate_token(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = authenticate_user(form.username,form.password,db)

    if not user:
        raise HTTPException(status_code=400,detail='wrong cresendiciels')
    
    token = token_create(user.username,user.id,user.role,timedelta(minutes=10)) # type: ignore

    return {'access_token': token, 'token_type':'Bearer'}



def authenticate_user(username:str,password:str,db:Session):
    db_user = db.query(User).filter(User.username == username).first()

    if not db_user:
        raise HTTPException(status_code=404,detail='user not found')
    
    if not pwd_context.verify(password,db_user.password): # type: ignore
        raise HTTPException(status_code=401,detail='Wrong Password')
    
    return db_user

def token_create(username:str,id:int,role:str,expire:timedelta):
    to_encode = {'sub':username,'userid':id,'role':role}
    to_encode.update({'exp':datetime.utcnow()+expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def get_current_user(token:str=Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return {'username':payload.get('sub') , 'userid':payload.get('userid'),'role':payload.get('role')}

    except JWTError:
        return {"error while getting current user"} 