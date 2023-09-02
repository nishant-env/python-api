from sqlalchemy.orm import Session
from sqlamch_model import Posts
from typing import List
from models import *
from sqlamch_model import engine1
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalch_db import SessionContextManger


router = APIRouter()

def database_session():
    with SessionContextManger() as db:
        yield db




@router.get("/posts", response_model=List[PostReturn])
def getallposts(session1: Session = Depends(database_session)):
    post = session1.query(Posts).all()
    if len(post) == 0:
        raise HTTPException(status_code=404, detail="No post found in database")
    return post


@router.get("/posts/{id}", response_model=PostReturn)
def getpostfiltered(id: int, session1: Session = Depends(database_session)):
    post = session1.query(Posts).filter(Posts.id == id).first()
    if post == None:
        raise HTTPException(status_code=404, detail="No post found in database")
    return post




@router.post("/posts", status_code=201, response_model=PostReturn)
def insertpost(post: PostCreate, session: Session = Depends(database_session)):
    post_insert = Posts(**post.dict())
    session.add(post_insert)
    session.commit()
    session.refresh(post_insert)
    if post_insert == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_insert


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session1: Session = Depends(database_session)):
    post = session1.query(Posts).filter(Posts.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"No post with id = {id} found in database")
    
    post.delete()
    
    session1.commit()



@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=PostReturn)
def update_post(post_updated: PostCreate, id: int, session1: Session = Depends(database_session)):
    post = session1.query(Posts).filter(Posts.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"No post with id = {id} found in database")
    
    post.update(post_updated.dict())
    session1.commit()
    return post.first()