from jose import jwt, JWTError
from datetime import datetime, timedelta
from models import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status



SECRET_KEY = '5905c36e7ea5f8437b333e8a87940c24c440d76af40826e8493489cabc7dd393'
ALGO= 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
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