from langchain_postgres import PGVector
from langchain_core.documents import Document
import os
from pathlib import Path
from ollama_embeddings import OllamaEmbeddings
import uuid

def list_files(path):
    files = list()
    names = os.listdir(path)
    for name in names:
        file = os.path.join(path,name)
        if os.path.isfile(file):
            files.append(file)
    return files


def split_text(text):
    chunks = list()
    chunk_id = str(uuid.uuid4())
    chunk = Document(
        page_content=text,
        metadata={
            "id":chunk_id,
            "source": file
        }
    )
    chunks.append(chunk)
    return chunks


def get_chunks(file):
    text = Path(file).read_text()
    if text:
        chunks = split_text(text)
        return chunks

    
if __name__=="__main__":
    
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

    files = list_files("data")
    print("files",files)

    for file in files:
        print("process",file)
        chunks = get_chunks(file)
        print(len(chunks)," chunks made")
        if len(chunks)>0:
            ids = [chunk.metadata["id"] for chunk in chunks]
            vector_store.add_documents(chunks, ids = ids)
            print("chunks added", len(chunks), ids)
            
