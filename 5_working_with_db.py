from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from fastapi.params import Optional, Body
from random import randint
import psycopg2
import time

while True:
    try:
        conn = psycopg2.connect(database='fastapi', host='localhost', port='9876', user='postgres', password='Root@123')
        cur = conn.cursor()
        res = cur.execute('select * from posts')
        print(res)
        break
    except Exception as e:
        print(e)
        time.sleep(2)


app = FastAPI()
database = [{"id": 1, "title" : "Post 1", "content": "Content 1"}, {"id": 2, "title" : "Post 2", "content": "Content 2"}]

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
    return database

@app.get('/posts/{id}')
def single_post(id: int):
    try:
        value_to_return = database[id-1]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return value_to_return



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post_inp: PostModel):
    post_dict = post_inp.dict()
    id = randint(3,100000)
    post_dict["id"] = id
    database.append(post_dict)
    print(post_dict)
    return post_dict


def get_index(id):
    for dict_id, data in enumerate(database):
        if data["id"] == id:
            return dict_id

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        dict_index = get_index(id)
        database.pop(dict_index)
    except TypeError:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data with id {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, update_post: PostModel):
    try:
        dict_index = get_index(id)
        database[dict_index] = update_post.dict()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data with id {id} was not found")
    return database[dict_index]
