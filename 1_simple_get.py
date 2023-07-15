from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def simple_get():
	return {"body" : "Hello world"}