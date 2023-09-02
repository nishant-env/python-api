from fastapi import APIRouter, Depends, HTTPException
from models import loginUser
from sqlalchemy.orm import Session
from sqlalch_db import SessionContextManger
from utils import verify_pwds
from sqlamch_model import Users

def database_session():
    with SessionContextManger() as db:
        yield db


router = APIRouter()

@router.post("/login")
def usersLogin(userCreds: loginUser, session: Session = Depends(database_session)):
    get_user = session.query(Users).filter(Users.email == userCreds.email).first()
    if get_user == None:
        raise HTTPException(status_code=404, detail='Seems like your are not regestered with us')
    
    is_auth = verify_pwds(userCreds.password, get_user.password)
    if not is_auth:
        raise HTTPException(status_code=401, detail="You provided wrong credentials")
    
    ### logic for returning token
    return {"Successful authentication"}