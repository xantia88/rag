0. Ensure you have docker installed

1. Clone this repo

git clone ....

2. Create docker network

docker create rag_net

3. Build containers

docker compose build --no-cache

|Name|Description|Technology|
|-|-|-|
|rag-api|access points|python|
|rag-db|database with embeddings|pgvector|
|rag-functions|various operations|python, bash|
|rag-models|embeddings models|ollama|
|rag-debug|debug containers within docker network|linux|

4. Start containers

docker compose up -d

5. Install embeddings model

docker exec -ti rag-models ollama pull nomic-embed-text

7. Debug interaction between containers

docker compose --profile debug up

docker exec -ti rag-dev sh

8. Stop

docker compose down --remove-orphans

9. Run specific function (e.g. load data)

docker run --network=rag_net rag-functions python /app/scripts/load.py
