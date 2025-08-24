from langchain_core.embeddings import Embeddings
from ollama import Client

class OllamaEmbeddings(Embeddings):

    def __init__(self, api_url: str, model_name: str):
        self.api_url = api_url
        self.model_name = model_name

    def embed_query(self, text:str) -> list[float]:
        client = Client(host=self.api_url)
        response = client.embeddings(model=self.model_name, prompt=text)
        return response.embedding

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = list()
        for text in texts:
            embedding = self.embed_query(text)
            embeddings.append(embedding)
        return embeddings
