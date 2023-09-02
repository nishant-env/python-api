from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalch_db import SessionContextManger
from models import UserCreate, UserReturn
from sqlamch_model import Users
import bcrypt

router = APIRouter(prefix='/users')

def database_session():
    with SessionContextManger() as db:
        yield db


@router.post('/', response_model=UserReturn, status_code=201)
def insertpost(users: UserCreate, session: Session = Depends(database_session)):
    user_add = Users(**users.dict())
    salt = bcrypt.gensalt()
    user_add.password=bcrypt.hashpw(user_add.password.encode('utf-8'), salt)
    session.add(user_add)
    session.commit()
    session.refresh(user_add)
    return user_add


@router.get('/{id}', response_model=UserReturn)
def getUser(id: int,session: Session = Depends(database_session)):
    user_ret = session.query(Users).filter(Users.id == id).first()
    if user_ret == None:
        raise HTTPException(status_code=404, detail=f"user with the id {id} doesn't exist")
    
    return user_ret