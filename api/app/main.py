from fastapi import FastAPI
from app.rag import Rag

app = FastAPI()

@app.get("/")
def read_root():
    rag = Rag()
    response = rag.find("moscow")
    return response

@app.post("/add")
def read_root():
    return None
