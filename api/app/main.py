from fastapi import FastAPI
from app.rag import Rag
import requests

app = FastAPI()
rag = Rag()

@app.get("/{name}")
def similarity_search(name):
    response = rag.find(name, "moscow")
    return response


@app.get("/add/{name}/{filename}")
def add_file(name, filename):
    url = f"http://storage:8000/file/{filename}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        text = response.text
        rag.add(name, filename, text)
        return text
    else:
        return f"Failed to download the file. Status code: {response.status_code}"
        

@app.get("/delete/{name}")
def delete_collection(name):
    rag.delete_collection(name)
    return "ok"
