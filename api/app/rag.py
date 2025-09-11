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

        self.embeddings = OllamaEmbeddings(
            api_url=f"http://{host}:{port}",
            model_name=model
        )

        db_user = os.getenv("DB_USER", default="admin")
        db_password = os.getenv("DB_PASSWORD", default="admin")
        db_host = os.getenv("DB_HOST", default="localhost")
        db_port = os.getenv("DB_PORT", default="5432")
        db_name = os.getenv("DB_NAME", default="postgres")

        self.connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 


    def _get_collection(self, collection_name):
        vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=collection_name,
            connection=self.connection,
            use_jsonb=True,
        )
        return vector_store
    
        
    def retrieve(self, collection_name, str):
        response = list()
        try:
            vector_store = self._get_collection(collection_name)
            results = vector_store.similarity_search_with_score(
                #str, k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
                str, k=10
            )
            for doc,score in results:
                document = {
                    "score": score,
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                response.append(document)
        except Exception as e:
            print("exception",e)
            response.append(e)
        return response

    
    def update(self, collection_name, source, text):
        chunks = self._split_text(text, source)
        if len(chunks)>0:
            ids = [chunk.metadata["id"] for chunk in chunks]
            vector_store = self._get_collection(collection_name)
            vector_store.add_documents(chunks, ids = ids)
            print("chunks added", len(chunks), ids)
        return len(chunks)

    
    def delete_collection(self, collection_name):
        vector_store = self._get_collection(collection_name)
        vector_store.delete_collection()

        
    def _split_text(self, text, source):
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


