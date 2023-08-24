from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from fastapi.params import Optional, Body
from random import randint
import psycopg2
import time
import pandas as pd

while True:
    try:
        conn = psycopg2.connect(database='fastapi', host='localhost', port='9876', user='postgres', password='Root@123')
        cur = conn.cursor()
        break
    except Exception as e:
        print(e)
        time.sleep(2)


app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False
    rating: Optional[float] = None


@app.get('/')
def home():
    return {"data": "This is homepage"}

@app.get('/posts')
def all_posts():
    try:
        cur.execute('select * from posts')
        res = cur.fetchall()
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return res    

@app.get('/posts/{id}')
def single_post(id: int):
    try:
        cur.execute('select * from posts where id = %s' , str(id) )
        res= cur.fetchall()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return res



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post_inp: PostModel):
    try:
        post_dict = post_inp.dict()
        cur.execute("""insert into posts(title,content,published) values (%s,%s,%s) returning *""", (post_dict["title"], post_dict["content"], post_dict["published"])) 
        post_ret = cur.fetchone()
        conn.commit()
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    return post_ret


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        deletion_sql = f"delete from posts where id = {id}"
        cur.execute(deletion_sql)
        conn.commit()
    except TypeError:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data with id {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @app.put("/posts/{id}")
# def update_post(id: int, update_post: PostModel):
#     try:
#         dict_index = get_index(id)
#         database[dict_index] = update_post.dict()
#     except:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data with id {id} was not found")
#     return database[dict_index]
