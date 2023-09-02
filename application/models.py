from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostModel):
    pass


class PostReturn(PostModel):
    
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True
    