## the client can send whatever data they want
## the data isn't getting validated
## we ultimately want to force the client to send the data in a schema that we expect
# schemas in api refers the structure and datatype api accepts

# we use a library called pydantic, it parses the input json and validates the data against the pydantic defined variable types


from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional



#lets define the schema for api input data (title and content)

class Post(BaseModel):
    title: str      # non optional field
    content: str
    published: bool = True  # optional field with True as default
    rating: Optional[int] = None  # we can also define optional fields like this

app = FastAPI()

@app.post('/createposts')
def create_post(post_inp: Post):
    ## the input pydantic model can also be converted into dictionary
    print(post_inp.dict())
    return {"post_title" : f"{post_inp.title}", "content" : f"{post_inp.content}"}

