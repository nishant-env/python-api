from jose import jwt, JWTError
from datetime import datetime, timedelta
from models import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from config import settings


SECRET_KEY = settings.secret_key
ALGO= settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth_schema = OAuth2PasswordBearer('login')

def get_jwt_token(data: dict):
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire_time
    tok = jwt.encode(claims=data, key=SECRET_KEY,algorithm=ALGO)
    return tok 


def verify_jwt_token(token:str, authexception):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGO])
        id: str = payload.get('id')
        if id is None:
            raise authexception
        token_data = TokenData(id=id)

    except JWTError:
        raise authexception
    return token_data

def get_user_det(token: str = Depends(oauth_schema)):
    authexception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Something is wrong with your token",
                        headers={"WWW-authenticate" : "bearer"})
    return verify_jwt_token(token, authexception)