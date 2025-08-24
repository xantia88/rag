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
|api|access points|python, fastapi|
|db|data storage|postgres, vector|
|functions|various operations|python, bash|
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

9. Execute specific function via one-off container

```
docker compose run --rm functions python /app/scripts/vectorize.py
docker compose run --rm functions python /app/scripts/test.py
```


