from fastapi import FastAPI,Depends,HTTPException
from jose import jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

SECRET_KEY = "im_krishna"
ALGORITHM="HS256"

def createToken(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=10)
    to_encode.update({"expire":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

Oauth_schema = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(token:str=Depends(Oauth_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            return HTTPException(status_code=401,detail="something wrong")
        return username
    except:
        return HTTPException(status_code=401)