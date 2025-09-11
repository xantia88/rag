import os
from app.ollama_embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
                    "id":doc.id,
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
        normalized_text = self._normalize_text(text)
        chunks = self._split_text(normalized_text, source)
        if len(chunks)>0:
            custom_ids = [str(uuid.uuid4()) for i in range(len(chunks))]
            vector_store = self._get_collection(collection_name)
            vector_store.add_documents(chunks, ids = custom_ids)
        return len(chunks)

    
    def delete_collection(self, collection_name):
        vector_store = self._get_collection(collection_name)
        vector_store.delete_collection()


    def _normalize_text(self, text):
        normalized = " ".join(text.lower().strip().split())
        return normalized
        
    def _split_text(self, text, source):

        documents = list()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20
        )

        chunks = text_splitter.split_text(text)
        for i,chunk in enumerate(chunks):
            document = Document(
                page_content=chunk,
                metadata={
                    "part": i,
                    "source":source
                }
            )
            documents.append(document)
        
        return documents


