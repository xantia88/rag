1. Clone this repo

git clone ....

2. Create docker network

docker create rag_net

3. Build containers

docker compose --build --no-cache

4. Start containers

docker compose up

5. Install nomic-embed-text model

docker exec -ti rag-models ollama pull nomic-embed-text

