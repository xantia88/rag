
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

1. Get answer from LLM model

via http

```
curl http://localhost:8080/generate/items \
-X POST \
-H 'Content-type: application/json' \
-d '{"text":"your question here"}'
```

or command line

```
$ cli/generate.sh
```

2. Retreieve text documents without generating answer

via http

```
curl http://localhost:8080/retrieve/items \
-X POST \
-H 'Content-type: application/json' \
-d '{"text":"your question here"}'
```

or command line

```
$ cli/retrieve.sh
```

3. Add source to vector store (file will be downloaded via http stream from *storage/download* endpoint to emulate access to object storage)

via http

```
curl http://localhost:8080/update/items \
-X POST \
-H 'Content-type: application/json' \
-d '{
   "path":"path/to/document1.txt",
   "metadata": {
               "parameter1": "value1"
               }
   }'
```

or command line

```
$ cli/add.sh
```

4. Delete collection

via http

```
curl http://localhost:8080/delete/items -X DELETE
```

or command line

```
$ cli/delete.sh
```
