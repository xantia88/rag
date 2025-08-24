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

|Name|Description|Technology|
|-|-|-|
|rag-api|access points|python|
|rag-db|database with embeddings|pgvector|
|rag-functions|various operations|python, bash|
|rag-models|embeddings models|ollama|
|rag-debug|debug containers within docker network|linux|

4. Start services

```
docker compose up -d
```

5. Install embeddings model into container where ollama is installed

```
docker exec -ti rag-models ollama pull nomic-embed-text
```

7. Use special container to debug interaction between containers within the network

```
docker compose --profile debug up -d
docker exec -ti rag-debug sh
```

8. Stop services

```
docker compose down --remove-orphans
```

9. Execute specific function via one-off container

```
docker compose run functions python /app/scripts/vectorize.py
docker compose run functions python /app/scripts/test.py
```


