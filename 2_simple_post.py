from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.post("/")
def postData(payload: dict = Body(...)):
	return {"data" : f"title: {payload['title']}, content: {payload['content']}"}