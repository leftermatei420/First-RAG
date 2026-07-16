import os
import json

from config import EMBEDDINGS_FILE
from document_chunker import chunk_documents
from embeddings_client import EmbeddingsClient


def generate_embeddings():
    if os.path.exists(EMBEDDINGS_FILE):
        return

    all_chunks = chunk_documents()
    client = EmbeddingsClient()
    for chunk in all_chunks:
        chunk["embedding"] = client.get_embedding(chunk["content"])
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f)
    

if __name__ == "__main__":
    generate_embeddings()
    print("done")