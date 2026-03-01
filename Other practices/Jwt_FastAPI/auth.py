from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.routing import APIRouter
from passlib.context import CryptContext
from database import sessionLocal
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from models import User
from pydantic_models import userRequest
from datetime import timedelta,datetime
from jose import jwt
from jose import JWTError
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "1q2w3e4r5t6y7u8i9o0p"
ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    with sessionLocal() as session:
        yield session

@router.post('/')
def create_user(user:userRequest,db:Session=Depends(get_db)):
    db_user = User(username=user.username,password=pwd_context.hash(user.password))

    try: 
        db.add(db_user)
        db.commit()
    except:
        print("Creatation failed")


@router.post('/token')
def create_token(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = authenticate_user(form.username,form.password,db)
    if not user:
        raise HTTPException(status_code=401)
    
    token = generate_token(user.username,user.id,user.role,timedelta(minutes=10))
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def authenticate_user(username:str,password:str,db:Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return None
    if not pwd_context.verify(password,user.password):
        return None
    return user

def generate_token(username,userid,role,expire):
    to_encode = {'sub':username,'userid':userid,'role':role}
    to_encode.update({'exp':datetime.utcnow()+expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:str=Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('userid') 
        role = payload.get('role')

        if not username:
            raise HTTPException(status_code=401)
        
        return {'username':username,"id":user_id,'role':role}

    except:
        raise HTTPException(status_code=401)
    
def role_check(role:str):

    def check(user:dict=Depends(get_current_user)):
        if user['role'] != role:
            raise HTTPException(status_code=403,detail='Not a admin')
        return user
    
    return check
        

