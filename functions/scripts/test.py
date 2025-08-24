import ollama
import os

if __name__=="__main__":
    
    host = os.getenv("MODELS_HOST", default="localhost")
    port = os.getenv("MODELS_PORT", default="11434")
    print("host",host,"port",port)

    client = ollama.Client(host=f"http://{host}:{port}")
    embeddings = client.embeddings(model='nomic-embed-text', prompt='this is test')
    print(len(embeddings.embedding))
