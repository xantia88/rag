from fastapi import FastAPI
from app.rag import Rag
import requests

app = FastAPI()
rag = Rag()

@app.get("/")
def similarity_search():
    response = rag.find("moscow")
    return response


@app.get("/add/{filename}")
def add_file(filename):
    url = f"http://storage:8000/file/{filename}"
    print("request",url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        text = response.text
        rag.add(filename,text)
        return text
    else:
        return f"Failed to download the file. Status code: {response.status_code}"
        

@app.get("/delete")
def delete_collection(name:str):
    rag.delete_collection(name)
    return "ok"
