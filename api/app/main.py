from fastapi import FastAPI
from app.rag import Rag
from app.query import Query
from app.source import Source
import requests

app = FastAPI()
rag = Rag()

@app.post("/generate/{name}")
def retrieve(name, query: Query):
    response = rag.generate(name, query)
    return response


@app.post("/retrieve/{name}")
def retrieve(name, query: Query):
    response = rag.retrieve(name, query)
    return response


@app.post("/update/{name}")
def update(name, source: Source):
    url = f"http://storage:8000/file/{source.path}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        text = response.text
        rag.update(name, source, text)
        return text
    else:
        return f"Failed to download the file. Status code: {response.status_code}"

    
@app.delete("/delete/{name}")
def delete(name):
    rag.delete_collection(name)
    return f"collection {name} deleted"
