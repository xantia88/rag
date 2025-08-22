from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

def get_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")

connection = "postgresql+psycopg://admin:admin@db:5432/kbase" 
collection_name = "items"

vector_store = PGVector(
    embeddings=get_embeddings(),
    collection_name=collection_name,
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
vector_store.add_documents(docs, ids)

results = vector_store.similarity_search(
    "kitty", k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
)

for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")

