from fastapi import FastAPI


app = FastAPI()

@app.get("/data/{file_path:path}")
def get_file(file_path: str):
    return {"file_path" : file_path}
