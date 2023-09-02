from fastapi import FastAPI, Depends, HTTPException, status
from sqlalch_db import SessionContextManger, engine1
from sqlamch_model import Base
from routers import posts, users

app = FastAPI()

@app.get('/')
def homepage():
    return {"data" : "This is homepage"}

app.include_router(posts.router)
app.include_router(users.router)