from fastapi import FastAPI
from langchain_postgres import PGVector
import os
from app.ollama_embeddings import OllamaEmbeddings

app = FastAPI()

@app.get("/")
def read_root():
    
    host = os.getenv("MODELS_HOST", default="localhost")
    port = os.getenv("MODELS_PORT", default="11434")
    model = os.getenv("MODEL_NAME", default="nomic-embed-text")

    embeddings = OllamaEmbeddings(
        api_url=f"http://{host}:{port}",
        model_name=model
    )

    db_user = os.getenv("DB_USER", default="admin")
    db_password = os.getenv("DB_PASSWORD", default="admin")
    db_host = os.getenv("DB_HOST", default="localhost")
    db_port = os.getenv("DB_PORT", default="5432")
    db_name = os.getenv("DB_NAME", default="postgres")
    db_collection = os.getenv("DB_COLLECTION", default="items")

    connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=db_collection,
        connection=connection,
        use_jsonb=True,
    )
    
    results = vector_store.similarity_search(
        "kitty", k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
    )

    response = list()
    for doc in results:
        response.append(doc)
    return response
    
    #return {"message": "Hello from FastAPI"}
 
