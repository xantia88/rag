import ollama
import psycopg
import json
import os

def get_embeddings(client:ollama.Client, model:str, text:str) -> list:
    response = client.embeddings(
        model = model,
        prompt = text
    )
    return response.get("embedding")

def get_chunks() -> list:
    chunks = list()
    for i in range(10):
        chunks.append(f"this is chunk {i}")
    return chunks

def save_embeddings(cur, chunk: str, vect: list):
    cur.execute(
        """
        INSERT INTO items (name, item_data, embedding)
        VALUES (%s, %s, %s)
        """,
        (chunk, json.dumps(chunk), vect),
    )

if __name__=="__main__":

    host = os.getenv("MODELS_HOST", default="localhost")
    port = os.getenv("MODELS_PORT", default="11434")
    model = os.getenv("MODEL_NAME", default="nomic-embed-text")

    db_user = os.getenv("DB_USER", default="admin")
    db_password = os.getenv("DB_PASSWORD", default="admin")
    db_host = os.getenv("DB_HOST", default="localhost")
    db_port = os.getenv("DB_PORT", default="5432")
    db_name = os.getenv("DB_NAME", default="postgres")
    
    url = f"http://{host}:{port}"
    db_uri = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    conn = psycopg.connect(db_uri)
    cur = conn.cursor()
 
    client = ollama.Client(host=url)

    chunks = get_chunks()
    for chunk in chunks:
        vect = get_embeddings(client, model, chunk)
        save_embeddings(cur, chunk, vect)
        print(chunk,"inserted")
    
    conn.commit()
    cur.close()
    conn.close()
