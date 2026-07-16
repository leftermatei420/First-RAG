from config import CHUNK_SIZE
from conversation_context import load_registry, load_file
import os

def split_text(text, chunk_size):
    sections = []
    for x in range(0, len(text), chunk_size):
        chunk = text[x : x + chunk_size]
        sections.append(chunk)
    return sections

def chunk_documents():
    all_chunks = []
    for folder in ["facts", "procedures"]:
        docs = load_registry(folder)
        for doc in docs:
            if not doc["always_load"]:
                path = os.path.join("knowledge", folder, doc["id"] + ".md")
                content = load_file(path)
                chunks = split_text(content, CHUNK_SIZE)
                for i, chunk in enumerate(chunks):
                    all_chunks.append({"document_id": doc["id"], "chunk_index": i, "content": chunk})
    return all_chunks

if __name__ == "__main__":
    result = chunk_documents()
    print(len(result), "chunks")
    print(result[0])