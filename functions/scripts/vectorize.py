from langchain_postgres import PGVector
from langchain_core.documents import Document
import os
from ollama_embeddings import OllamaEmbeddings

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

    docs = [
        Document(
            page_content="there are cats in the pond",
            metadata={"id": 1, "location": "pond", "topic": "animals"},
        ),
        Document(
            page_content="ducks are also found in the pond",
            metadata={"id": 2, "location": "pond", "topic": "animals"},
        )
    ]

    ids = [doc.metadata["id"] for doc in docs]
    vector_store.add_documents(docs, ids = ids)
    print("document added", len(docs), ids)
