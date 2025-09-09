0. Ensure you have docker installed

1. Clone this repo

```
git clone https://github.com/xantia88/rag.git
```

2. Create docker network

```
docker create rag_net
```

3. Build containers

```
docker compose build --no-cache
```

|Service name|Description|Technology|
|-|-|-|
|api|service endpoints|python, fastapi|
|db|data storage|postgres, pgvector|
|ollama|embeddings models|ollama|
|deb|network debug|linux,iputils|

4. Start services

```
docker compose up -d
```

5. Install embeddings model into container where ollama is installed

```
docker exec -ti rag-models ollama pull nomic-embed-text
```

7. Use special container to debug network

```
docker compose --profile debug up -d
docker exec -ti rag-debug sh
```

8. Stop services

```
docker compose down --remove-orphans
```

9. Similarity search in vector store

```
http://localhost:8080/
```

10. Add file to vector store. File will be downloaded via http stream from *storage/download* endpoint to emulate access to object storage.

```
http://localhost:8080/add/document1.txt
```

