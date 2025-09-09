import os
from app.ollama_embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
import uuid


class Rag:
    
    def __init__(self):

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

        self.vector_store = PGVector(
            embeddings=embeddings,
            collection_name=db_collection,
            connection=connection,
            use_jsonb=True,
        )

        
    def find(self, str):

        response = list()

        try:

            results = self.vector_store.similarity_search(
                #str, k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
                str, k=10
            )

            for doc in results:
                response.append(doc)
        except Exception as e:
            print("exception",e)
            response.append(e)

        return response

    
    def add(self, source, text):
        print("add to rag",source)
        chunks = self.split_text(text, source)
        print(len(chunks)," chunks made")
        if len(chunks)>0:
            ids = [chunk.metadata["id"] for chunk in chunks]
            self.vector_store.add_documents(chunks, ids = ids)
            print("chunks added", len(chunks), ids)
        return [{"x":123}]

    
    def delete_collection(self, name):
        self.vector_store.delete_collection()
        print("collection deleted",name)
        return "ok"

    
    def split_text(self, text, source):
        chunks = list()
        chunk_id = str(uuid.uuid4())
        chunk = Document(
            page_content=text,
            metadata={
                "id":chunk_id,
                "source": source
            }
        )
        chunks.append(chunk)
        return chunks


