import ollama

if __name__=="__main__":
    client = ollama.Client(host='http://ollama:11434')
    embeddings = client.embeddings(model='nomic-embed-text', prompt='this is test')
    print(embeddings)
