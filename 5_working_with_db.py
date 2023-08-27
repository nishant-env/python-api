from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from fastapi.params import Optional, Body
from random import randint
import psycopg2
import time
import pandas as pd
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(database='fastapi', host='localhost', port='9876', user='postgres', password='Root@123')
        cur = conn.cursor(cursor_factory= RealDictCursor)
        break
    except Exception as e:
        print(e)
        time.sleep(2)


app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


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
    # try:
        cur.execute('select * from posts where id = %s' , str(id))
        res = cur.fetchall()
        if len(res) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")
    # except Exception as e:
    #     print(e)
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
        return {"data" : res}



@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def new_post(post_inp: PostModel):
    try:
        post_dict = post_inp.dict()
        cur.execute("""insert into posts(title,content,published) values (%s,%s,%s) returning *""", (post_dict["title"], post_dict["content"], post_dict["published"]))
        post_ret = cur.fetchone()
        conn.commit()
    except Exception as e:
        print(e)
    return post_ret


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deletion_sql = f"delete from posts where id = {id} returning *"
    cur.execute(deletion_sql)
    del_ret = cur.fetchone()
    conn.commit()
    if del_ret == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/updateposts/{id}")
def update_post(id: int, update_post: PostModel):
    cur.execute("update posts set title = %s, content = %s, published = %s where id = %s returning *", (update_post.title, update_post.content, update_post.published, id))
    conn.commit()
    updated_post = cur.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data with id {id} was not found")

    return updated_post
