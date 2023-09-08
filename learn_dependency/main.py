from fastapi import Depends, FastAPI
from typing import Annotated
import classes_dep

app = FastAPI()

def common_parameters(q:str | None = None, skip: int = 0, limit: int = 1000):
    return {"q" : q, "skip" : skip, "limit" : limit}


@app.get("/items/")
def read_items(common: Annotated[dict, Depends(common_parameters)]):
    return common

app.include_router(classes_dep.router)

"""
The items passed through the dependency is passed as a url parameter, using &.
In postman, donot pass through the body, instead use params

example url: localhost:8000/class_items?q="select 1"&skip=3001
"""