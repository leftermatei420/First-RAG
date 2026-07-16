from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()
results = client.semantic_search("How do I reset my password?")

for r in results:
    print(r["similarity"], r["document_id"], r["chunk_index"])
    print(r["content"][:100])
    print("---")