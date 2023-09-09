from sqlalchemy.orm import Session
from sqlamch_model import Posts
from typing import List
from models import *
from sqlamch_model import engine1
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalch_db import SessionContextManger
from oauth2_1 import get_user_det


router = APIRouter(prefix='/posts', tags=["posts"])

def database_session():
    with SessionContextManger() as db:
        yield db




@router.get("/", response_model=List[PostReturn])
def getallposts(session1: Session = Depends(database_session), user: TokenData = Depends(get_user_det),
                limit: int = 10, skip: int = 0, search : Optional[str] = ""):
    post = session1.query(Posts).filter(Posts.title.contains(search)).limit(limit).offset(skip).all()
    if len(post) == 0:
        raise HTTPException(status_code=404, detail="No post found in database")
    return post

@router.get("/myposts", response_model=List[PostReturn])
def getallposts(session1: Session = Depends(database_session), user: TokenData = Depends(get_user_det)):
    post = session1.query(Posts).filter(Posts.owner_id == user.id).all()
    if len(post) == 0:
        raise HTTPException(status_code=404, detail="No post found in database")
    return post


@router.get("/{id}", response_model=PostReturn)
def getpostfiltered(id: int, session1: Session = Depends(database_session), user: TokenData = Depends(get_user_det)):
    post = session1.query(Posts).filter(Posts.id == id).first()
    if post == None:
        raise HTTPException(status_code=404, detail=f"No post with id {id} found in database")
    return post




@router.post("/", status_code=201, response_model=PostReturn)
def insertpost(post: PostCreate, session: Session = Depends(database_session), user: TokenData = Depends(get_user_det)):
    post_insert = Posts(**post.dict())
    post_insert.owner_id = user.id
    session.add(post_insert)
    session.commit()
    session.refresh(post_insert)
    if post_insert == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    print(user.id)
    return post_insert


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session1: Session = Depends(database_session), user: TokenData = Depends(get_user_det)):
    post = session1.query(Posts).filter(Posts.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"No post with id = {id} found in database")
    
    if post.first().owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this operation")

    post.delete()
    
    session1.commit()



@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=PostReturn)
def update_post(post_updated: PostCreate, id: int, session1: Session = Depends(database_session), user: TokenData = Depends(get_user_det)):
    post = session1.query(Posts).filter(Posts.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"No post with id = {id} found in database")
    
    if post.first().owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this operation")

    post.update(post_updated.dict())
    session1.commit()
    return post.first()