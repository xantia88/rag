import ollama
import psycopg
import json

OLLAMA_URL = "http://ollama:11434"
MODEL = "nomic-embed-text"
DB_URI = "postgres://admin:admin@db:5432/kbase"

def get_embeddings(client:ollama.Client, text:str) -> list:
    response = client.embeddings(
        model = MODEL,
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

    conn = psycopg.connect(DB_URI)
    cur = conn.cursor()
 
    client = ollama.Client(host=OLLAMA_URL)

    chunks = get_chunks()
    for chunk in chunks:
        vect = get_embeddings(client, chunk)
        save_embeddings(cur, chunk, vect)
        print(chunk,"inserted")
    
    conn.commit()
    cur.close()
    conn.close()
