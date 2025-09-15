
# Setup

1. Clone this repo

```
git clone https://github.com/xantia88/rag.git
```

2. Build containers

```
docker compose build --no-cache
```

|Service name|Description|Technology|
|-|-|-|
|api|service endpoints|python, fastapi|
|db|data storage|postgres, pgvector|
|ollama|embeddings models|ollama|
|storage|data storage|python, fastapi, local fs|

3. Start services

```
docker compose up -d
```

4. Install embeddings and generation models 

```
docker exec -ti rag-models ollama pull nomic-embed-text
docker exec -ti rag-models ollama pull qwen3:4b
```

5. Stop services

```
docker compose down --remove-orphans
```

# Operations

Assume *items* is a collection name.

1. Retreieve data

```
curl http://localhost:8080/retrieve/items \
-X POST \
-H 'Content-type: application/json' \
-d '{"text":"your question here"}'
```

2. Add file to vector store (file will be downloaded via http stream from *storage/download* endpoint to emulate access to object storage)

```
curl http://localhost:8080/update/items \
-X POST \
-H 'Content-type: application/json' \
-d '{"path":"path/to/document1.txt"}'
```

3. Delete collection

```
curl http://localhost:8080/delete/items -X DELETE
```
