from fastapi import FastAPI
from app.rag import Rag
import requests

app = FastAPI()
rag = Rag()

@app.get("/retrieve/{name}")
def retrieve(name):
    response = rag.retrieve(name, "rain london")
    return response


@app.get("/update/{name}/{filename}")
def update(name, filename):
    url = f"http://storage:8000/file/{filename}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        text = response.text
        rag.update(name, filename, text)
        return text
    else:
        return f"Failed to download the file. Status code: {response.status_code}"

    
@app.get("/delete/{name}")
def delete(name):
    rag.delete_collection(name)
    return f"collection {name} deleted"
