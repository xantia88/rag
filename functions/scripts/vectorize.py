from langchain_postgres import PGVector
from langchain_core.documents import Document
import os
from pathlib import Path
from ollama_embeddings import OllamaEmbeddings
import psycopg

def get_documents(path):
    documents = list()
    names = os.listdir(path)
    for name in names:
        file = os.path.join(path,name)
        if os.path.isfile(file):
            text = Path(file).read_text()
            if text and len(text)>0:
                document = Document(
                    page_content=text,
                    metadata={"id":len(documents), "source": file}
                )
                documents.append(document)
    return documents

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

    # clean database
    # ------------------------
    connection2 = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
    conn = psycopg.connect(connection2)
    cur = conn.cursor()
    cur.execute("delete from langchain_pg_collection where name=%s", (db_collection,))
    conn.commit()
    cur.close()
    conn.close()
    # -----------------------

    connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=db_collection,
        connection=connection,
        use_jsonb=True,
    )
    
    docs = get_documents("data")
    print(docs)

    ids = [doc.metadata["id"] for doc in docs]
    vector_store.add_documents(docs, ids = ids)
    print("document added", len(docs), ids)
