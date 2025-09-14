from langchain_core.embeddings import Embeddings
from ollama import Client

class OllamaEmbeddings(Embeddings):

    
    def __init__(self, api_url: str, model_name: str):
        self.model_name = model_name
        self.client = Client(host=api_url)

        
    def embed_query(self, text:str) -> list[float]:
        response = self.client.embeddings(model=self.model_name, prompt=text)
        return response.embedding

    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = list()
        for text in texts:
            embedding = self.embed_query(text)
            embeddings.append(embedding)
        return embeddings


class OllamaGenerator:

    
    def __init__(self, api_url: str, model_name: str):
        self.model_name = model_name
        self.client = Client(host=api_url)

    
    def generate(self, text: str) -> str:
        response = self.client.generate(model=self.model_name, prompt=text)
        text = response['response']
        return text
        
