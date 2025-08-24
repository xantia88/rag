from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
import ollama
import os

class OllamaEmbeddings(Embeddings):

    def __init__(self, api_url: str, model_name: str):
        self.api_url = api_url
        self.model_name = model_name

    def embed_query(self, text:str) -> list[float]:
        client = ollama.Client(host=self.api_url)
        response = client.embeddings(model=self.model_name, prompt=text)
        return response.embedding

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = list()
        for text in texts:
            embedding = self.embed_query(text)
            embeddings.append(embedding)
        return embeddings

if __name__=="__main__":
    
    host = os.getenv("MODELS_HOST", default="localhost")
    port = os.getenv("MODELS_PORT", default="11434")
    model = os.getenv("MODEL_NAME", default="nomic-embed-text")

    db_user = os.getenv("DB_USER", default="admin")
    db_password = os.getenv("DB_PASSWORD", default="admin")
    db_host = os.getenv("DB_HOST", default="localhost")
    db_port = os.getenv("DB_PORT", default="5432")
    db_name = os.getenv("DB_NAME", default="postgres")
    db_collection = os.getenv("DB_COLLECTION", default="items")

    embeddings = OllamaEmbeddings(
        api_url=f"http://{host}:{port}",
        model_name=model
    )

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

    results = vector_store.similarity_search(
        "kitty", k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
    )

    for doc in results:
        print(f"* {doc.page_content} [{doc.metadata}]")

