from fastapi import APIRouter, Depends, HTTPException, Form
from models import loginUser
from sqlalchemy.orm import Session
from sqlalch_db import SessionContextManger
from utils import verify_pwds
from sqlamch_model import Users
from oauth2_1 import get_jwt_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from models import Token

def database_session():
    with SessionContextManger() as db:
        yield db


router = APIRouter()

@router.post("/login", response_model=Token)
def usersLogin(userCreds: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], session: Session = Depends(database_session)):
    get_user = session.query(Users).filter(Users.email == userCreds.username).first()
    if get_user == None:
        raise HTTPException(status_code=404, detail='Seems like your are not regestered with us')
    
    is_auth = verify_pwds(userCreds.password, get_user.password)
    if not is_auth:
        raise HTTPException(status_code=401, detail="You provided wrong credentials")
    
    token = get_jwt_token({"id" : get_user.id})
    ## logic for returning token
    return {'access_token' : token, 'token_type' : 'bearer'}


