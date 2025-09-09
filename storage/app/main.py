from fastapi import FastAPI
from pathlib import Path

app = FastAPI()

@app.get("/file/{filename}")
def get_file(filename):
    path = f"/app/data/{filename}"
    text = Path(path).read_text()
    return text
    
