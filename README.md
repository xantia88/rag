
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

4. Install embeddings model into container where ollama is installed

```
docker exec -ti rag-models ollama pull nomic-embed-text
```

5. Use special container to debug network

```
docker compose --profile debug up -d
docker exec -ti rag-debug sh
```

6. Stop services

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
http://localhost:8080/update/items/document1.txt
```

3. Delete collection

```
http://localhost:8080/delete/items
```
