from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime



class UserReturn(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True
    

class PostModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostModel):
    pass


class PostReturn(PostModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserReturn
    
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class loginUser(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int